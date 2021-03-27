import json
import uuid
from test_app.models import Asset
from django.contrib.gis.geos import Point

from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        super().__init__(json.dumps(data), content_type='application/json', *args, **kwargs)

def jsonify_asset(asset):
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
    results = Asset.objects.filter().values()
    assets = [jsonify_asset(item) for item in results]

    reply = {
        'type': 'FeatureCollection',
        'features': assets,
    }

    return JsonResponse(data=reply, status=200)


def get_asset(request, asset_id):
    results = Asset.objects.filter(asset_id=asset_id).values()

    if not results:
        return JsonResponse(data={
            'message': f'No asset was found with the given id',
            'asset_id': asset_id,
        }, status=404)

    jsonReply = jsonify_asset(results[0])

    return JsonResponse(data=jsonReply, status=200)


###
# Doing no validation yet. Needs to be done before going to prod.
# Assuming correct input from user.
###
def add_assets(request):
    bodyString = request.body.decode('utf-8')
    body = json.loads(bodyString)

    asset_type = body['type']
    asset_id = body['properties']['asset_id']
    asset_id = str(uuid.uuid4())
    geo_type = body['geometry']['type']
    geo_coord = Point(tuple(body['geometry']['coordinates']))

    created = Asset.objects.create(geography=geo_coord, asset_id=asset_id)

    return get_asset(request, asset_id)


def get_or_add_assets(request):
    if request.method == 'POST':
        return add_assets(request)
    else:
        return get_assets(request)
