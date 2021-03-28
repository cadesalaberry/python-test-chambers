import json
import uuid
from test_app.models import (
    Asset,
    FeatureSerializer,
    FeatureCollectionSerializer,
    SearchQuerySerializer,
    UnknownQuerySerializer,
)
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        super().__init__(json.dumps(data), content_type='application/json', *args, **kwargs)

def get_valid_body(request, ProvidedSerializer):
    body_string = request.body.decode('utf-8')

    try:
        unsafe_body = json.loads(body_string)
    except Exception:
        unsafe_body = {}

    return ProvidedSerializer(data=unsafe_body)

def assetify_json(asset):
    """
    Turns a json asset into a django model.
    """

    asset_type = asset['type']
    asset_id = asset['properties']['asset_id']
    # asset_id = str(uuid.uuid4()) # temporarily generate random ids to avoid conflicts
    geo_type = asset['geometry']['type']
    geo_coord = Point(tuple(asset['geometry']['coordinates']), srid=4326)

    return Asset(geography=geo_coord, asset_id=asset_id)

def jsonify_asset(asset):
    """
    Turns a django model into a readable JSON for the API.
    """
    json_representation = {
        'type': 'Feature',
        # 'type': asset.type,
        'properties': {
            'asset_id': asset['asset_id'],
        },
        'geometry': {
            'type': 'Point',
            # 'type': asset['geometry']['type'],
            'coordinates': [
                asset['geography'].x,
                asset['geography'].y,
            ]
        },
    }

    if 'distance' in asset:
        json_representation['properties']['distance'] = asset['distance'].m

    return json_representation


def get_assets(request):
    """
    Get all assets from the database.
    """

    results = Asset.objects.filter().values()
    assets = [jsonify_asset(item) for item in results]

    reply = {
        'type': 'FeatureCollection',
        'features': assets,
    }

    return JsonResponse(data=reply, status=200)


def get_asset(request, asset_id):
    """
    Get an asset by asset_id from the database.

    Returns a 404 if not found.
    """

    results = Asset.objects.filter(asset_id=asset_id).values()

    if not results:
        return JsonResponse(data={
            'message': f'No asset was found with the given id',
            'asset_id': asset_id,
        }, status=404)

    jsonReply = jsonify_asset(results[0])

    return JsonResponse(data=jsonReply, status=200)


def add_assets(request):
    """
    Add a single asset to the database.

    Note: Assuming correct input from user.
          Validation needs to be done before going to prod.
    """

    validator = get_valid_body(request, FeatureCollectionSerializer)

    if not validator.is_valid():
        return JsonResponse(data={ 'errors': validator.errors }, status=400)

    body = validator.validated_data
    features = body['features']

    created_items = Asset.objects.bulk_create([
        assetify_json(item) for item in features
    ])

    ids = set([item.asset_id for item in created_items])

    results = Asset.objects.filter(asset_id__in=ids).values()
    assets = [jsonify_asset(item) for item in results]

    reply = {
        'type': 'FeatureCollection',
        'features': assets,
    }

    return JsonResponse(data=reply, status=200)


def add_asset(request):
    """
    Add a single asset to the database.

    deprecated:: 2.3
    """

    validator = get_valid_body(request, FeatureSerializer)

    if not validator.is_valid():
        return JsonResponse(data={ 'errors': validator.errors }, status=400)

    body = validator.validated_data
    created = assetify_json(body)

    created.save()

    return get_asset(request, created.asset_id)


def search_asset(request):
    """
    Get the 3 closest assets from the coordinates specified in the query.
    """

    unsafe_query = {
        'lat': request.GET.get('lat'),
        'lng': request.GET.get('lng'),
    }

    validator = SearchQuerySerializer(data=unsafe_query)

    if not validator.is_valid():
        return JsonResponse(data={ 'errors': validator.errors }, status=400)

    query = validator.validated_data
    point = Point((query['lng'], query['lat']), srid=4326)

    results = Asset.objects.annotate(
        distance=Distance('geography', point)
    ).filter(
        # geography__distance_gte=(point, D(m=0))
    ).order_by(
        'distance'
    )[:3].values()

    assets = [jsonify_asset(item) for item in results]

    reply = {
        'type': 'FeatureCollection',
        'features': assets,
    }

    return JsonResponse(data=reply, status=200)



def get_or_add_assets(request):
    if request.method == 'POST':
        validator = get_valid_body(request, UnknownQuerySerializer)

        if not validator.is_valid():
            return JsonResponse(data={ 'errors': validator.errors }, status=400)
        if validator.validated_data['type'] == 'FeatureCollection':
            return add_assets(request)
        else:
            return add_asset(request)

    else:
        return get_assets(request)
