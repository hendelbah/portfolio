# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring
from flask import url_for

from tests.base_test_case import BaseTestCase


class TestApi(BaseTestCase):
    endpoints_1 = ('api.users', 'api.doctors', 'api.patients', 'api.appointments')
    endpoints_2 = ('api.user', 'api.doctor', 'api.patient', 'api.appointment')

    def test_unauthorized_request(self):
        response = self.client.get(url_for('api.users'))
        self.assertStatus(response, 401)
        self.assertEqual(response.json['message'], "Credentials not present in request")
        response = self.client.get(url_for('api.users'), headers={'api-key': 'zxc'})
        self.assertStatus(response, 401)
        self.assertEqual(response.json['message'], "Credentials not valid")

    def test_head(self):
        response = self.client.head(url_for('api.users', per_page=5), headers=self.api_auth)
        self.assertStatus(response, 204)
        response = self.client.head(url_for('api.users', search_email='zxc'), headers=self.api_auth)
        self.assert404(response)
        response = self.client.head(url_for('api.user', uuid='1'), headers=self.api_auth)
        self.assertStatus(response, 204)
        response = self.client.head(url_for('api.user', uuid='qaz'), headers=self.api_auth)
        self.assert404(response)

    def test_all_get_200(self):
        for endpoint in self.endpoints_1:
            with self.subTest(endpoint):
                response = self.client.get(url_for(endpoint, per_page=5), headers=self.api_auth)
                self.assert200(response)
                self.assertEqual(len(response.json['items']), 5)
        for endpoint in self.endpoints_2:
            with self.subTest(endpoint):
                response = self.client.get(url_for(endpoint, uuid='1'), headers=self.api_auth)
                self.assert200(response)

    def test_get_by_id(self):
        properties = (
            ('email', 'doctor_001@spam.ua'),
            ('full_name', 'Аблялимова Альбина Шевкетовна'),
            ('phone_number', '380000000006'),
            ('time', '11:00:00'),
            ('time', '12:00:00')
        )
        for endpoint, prop in zip(self.endpoints_2, properties):
            with self.subTest(endpoint):
                response = self.client.get(url_for(endpoint, uuid='2'), headers=self.api_auth)
                self.assert200(response)
                self.assertEqual(response.json['uuid'], '2')
                self.assertEqual(response.json[prop[0]], prop[1])

    def test_post_and_delete(self):
        data = (
            {'email': 'Somebody once', 'password_hash': 'told me', 'is_admin': True},
            {'full_name': 'the world', 'speciality': 'is gonna', 'info': 'roll me',
             'experience_years': 100},
            {'phone_number': '88005553535', 'full_name': 'Slave Ass 300', 'birthday': '2012-12-12'},
            {'patient_uuid': '4', 'doctor_uuid': '5', 'date': '2013-10-10', 'time': '10:00:01',
             'conclusion': 'will die soon', 'prescription': 'submit', 'bill': 5000},
        )
        uuids = []
        for endpoint, item in zip(self.endpoints_1, data):
            with self.subTest(endpoint + ':POST'):
                response = self.client.post(url_for(endpoint), json=item, headers=self.api_auth)
                self.assertStatus(response, 201)
                uuids.append(response.json['uuid'])
        for endpoint, uuid in zip(self.endpoints_2, uuids):
            with self.subTest(endpoint + ':DELETE'):
                response = self.client.delete(url_for(endpoint, uuid=uuid), headers=self.api_auth)
                self.assertStatus(response, 204)

    def test_put(self):
        data = (
            {'password_hash': 'cocos_olia_jojoba', 'email': 'cocojambo'},
            {'full_name': 'Артем Петрович', 'experience_years': 1488},
            {'full_name': 'McDonalds ltd', 'birthday': '1940-05-15'},
            {'date': '2025-01-01', 'time': '07:00:00', 'conclusion': 'very well'},
        )
        for endpoint, item in zip(self.endpoints_2, data):
            with self.subTest(endpoint):
                response = self.client.put(url_for(endpoint, uuid='10'), json=item,
                                           headers=self.api_auth)
                self.assertStatus(response, 200)

    def test_get_filtered_404(self):
        filters = (
            {'search_email': 'zxc'},
            {'search_name': 'cocojambo'},
            {'search_name': 'amogus'},
            {'doctor_uuid': 'poppa'}
        )
        for endpoint, data in zip(self.endpoints_1, filters):
            with self.subTest(endpoint):
                response = self.client.get(url_for(endpoint, **data), headers=self.api_auth)
                self.assert404(response)

    def test_wrong_get_put_delete(self):
        for endpoint in self.endpoints_2:
            with self.subTest(endpoint):
                response = self.client.get(url_for(endpoint, uuid='fgh'), headers=self.api_auth)
                self.assert404(response)
                response = self.client.put(url_for(endpoint, uuid='q1q1q1'), json={},
                                           headers=self.api_auth)
                self.assert404(response)
                response = self.client.delete(url_for(endpoint, uuid='3zxc'), headers=self.api_auth)
                self.assert404(response)

    def test_post_wrong_data(self):
        cases = (
            ({'email': 'doctor_001@spam.ua', 'is_admin': False, 'password_hash': 'asd'},
             ['IntegrityError']),
            ({'full_name': 'the   world', 'speciality': 'is gonna'},
             ['experience_years', 'full_name', 'info']),
            ({'full_name': 'A', 'birthday': '20123-10-10'},
             ['birthday', 'full_name', 'phone_number']),
            ({'id': 365, 'patient_uuid': '4', 'date': '013-10-10', 'prescription': 'a', 'bill': 5},
             ['date', 'doctor_uuid', 'id', 'time']),
        )
        for endpoint, case in zip(self.endpoints_1, cases):
            with self.subTest(endpoint):
                response = self.client.post(url_for(endpoint), json=case[0], headers=self.api_auth)
                self.assertStatus(response, 422)
                errors = response.json['errors']
                keys = sorted(list(errors))
                self.assertEqual(keys, case[1])

    def test_put_wrong_data(self):
        cases = (
            ({'doctor_uuid': 'Somebody', 'email': 'once', 'password_hash': 'told me'},
             ['ValueError']),
            ({'fu': 'the world', 'spe': 'is gonna', 'info': 'roll me'},
             ['fu', 'spe']),
            ({'phone_number': '380000000003', 'full_name': 'palmolive gel'},
             ['IntegrityError']),
            ({'doctor_uuid': '1', 'date': '013-10-10', 'time': '75:00:00', 'aoa': 'oao'},
             ['aoa', 'date', 'time']),
        )
        for endpoint, case in zip(self.endpoints_2, cases):
            with self.subTest(endpoint):
                response = self.client.put(url_for(endpoint, uuid='3'), json=case[0],
                                           headers=self.api_auth)
                self.assertStatus(response, 422)
                errors = response.json['errors']
                keys = sorted(list(errors))
                self.assertEqual(keys, case[1])

    def test_get_statistics(self):
        response = self.client.get(url_for('api.statistics', doctor_uuid=1), headers=self.api_auth)
        self.assert200(response)
        self.assertEqual(response.json, {'count': 12, 'income': 105})
