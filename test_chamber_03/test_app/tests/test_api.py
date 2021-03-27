import json
from test_app.tests import JsonClientTestCase


class ApiTestCase(JsonClientTestCase):
    def test_add_a_single_asset(self):
        response = self.client.post('/assets',
                                    data=json.dumps(self.assets['features'][0]),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.get('/assets/wgs_montpellier')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['properties']['asset_id'], 'wgs_montpellier')

    def test_adds_assets(self):
        response = self.client.post('/assets',
                                    data=json.dumps(self.assets),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response = self.client.get('/assets')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['features']), 5)

    def test_search(self):
        response = self.client.post('/assets',
                                    data=json.dumps(self.assets),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response = self.client.get('/assets/search',
                                   data={
                                       'lat': 43.6,
                                       'lng': 3.883
                                   })

        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data['features']), 3)
        self.assertEqual(round(json_data['features'][0]['properties']['distance']),
                         674.0)
