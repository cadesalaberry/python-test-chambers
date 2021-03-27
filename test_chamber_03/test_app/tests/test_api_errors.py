import json

from test_app.tests import JsonClientTestCase


class ApiErrorsTestCase(JsonClientTestCase):
    def test_search_parameters(self):
        response = self.client.get('/assets/search')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/assets/search',
                                   data={
                                       'lat': 'not_a_float',
                                       'lng': 3.883
                                   })
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/assets/search',
                                   data={
                                       'lng': 'not_a_float',
                                       'lat': 43.6
                                   })
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/assets/search',
                                   data={
                                       'lat': 43.6
                                   })
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/assets/search',
                                   data={
                                       'lng': 3.883
                                   })
        self.assertEqual(response.status_code, 400)

    def test_get_asset_by_id(self):
        response = self.client.get('/assets/an_id')
        self.assertEqual(response.status_code, 404)

    def test_import_invalid_geometry(self):
        response = self.client.post('/assets', data=json.dumps({
            'type': 'Feature',
            'properties': {
                'asset_id': 'my_asset_id'
            },
            'geometry': {
                'shit': 'geom'
            }
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_import_invalid_type(self):
        response = self.client.post('/assets', data=json.dumps({
            'type': 'Rorschach',
            'properties': {
                'asset_id': 'my_asset_id'
            },
            'geometry': {
                'shit': 'geom'
            }
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_missing_properties(self):
        response = self.client.post('/assets', data=json.dumps({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    3.880721926689148,
                    43.61530638830013
                ]
            }
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_missing_geometry(self):
        response = self.client.post('/assets', data=json.dumps({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    3.880721926689148,
                    43.61530638830013
                ]
            }
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
