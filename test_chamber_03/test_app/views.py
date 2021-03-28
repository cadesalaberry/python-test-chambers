import json
import uuid
from test_app.models import Asset
from django.contrib.gis.geos import Point

from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        super().__init__(json.dumps(data), content_type='application/json', *args, **kwargs)

def assetify_json(asset):
    """
    Turns a json asset into a django model.
    """

    asset_type = asset['type']
    asset_id = asset['properties']['asset_id']
    asset_id = str(uuid.uuid4()) # temporarily generate random ids to avoid conflicts
    geo_type = asset['geometry']['type']
    geo_coord = Point(tuple(asset['geometry']['coordinates']))

    return Asset(geography=geo_coord, asset_id=asset_id)

def jsonify_asset(asset):
    """
    Turns a django model into a readable JSON for the API.
    """
    return {
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

    body_string = request.body.decode('utf-8')
    body = json.loads(body_string)
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

    Note: Assuming correct input from user.
          Validation needs to be done before going to prod.

    deprecated:: 2.3
    """

    body_string = request.body.decode('utf-8')
    body = json.loads(body_string)

    created = assetify_json(body)

    created.save()

    return get_asset(request, created.asset_id)


def get_or_add_assets(request):
    if request.method == 'POST':
        return add_assets(request)
    else:
        return get_assets(request)
