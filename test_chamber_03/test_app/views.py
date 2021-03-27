import json
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        super().__init__(json.dumps(data), content_type='application/json', *args, **kwargs)


def get_assets(request):
    return JsonResponse(data={
        'message': 'Unimplemented get_assets view.'
    }, status=400)


def add_assets(request):
    return JsonResponse(data={
        'message': 'Unimplemented add_assets view.'
    }, status=400)


def get_or_add_assets(request):
    if request.method == 'POST':
        return add_assets(request)
    else:
        return get_assets(request)
