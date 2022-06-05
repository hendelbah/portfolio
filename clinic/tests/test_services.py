# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring
from datetime import date, datetime, timedelta
from unittest.mock import patch

from flask_sqlalchemy import Pagination
from sqlalchemy.orm import Query

from clinic_app.service import UserService, DoctorService, PatientService, AppointmentService
from tests.base_test_case import BaseTestCase

services = (UserService, DoctorService, PatientService, AppointmentService)


# pylint: disable=protected-access, no-member
class TestAllServices(BaseTestCase):

    def test_filter_by(self):
        for service in services:
            with self.subTest(service.__name__):
                self.assertIsInstance(service._filter_by(), Query)

    def test_get_pagination(self):
        today = date.today()
        # noinspection SpellCheckingInspection
        cases = (
            ([{'search_email': 'doctor_00'}, 9],
             ),
            ([{'search_name': 'Геннад'}, 1],
             [{'no_user': True}, 0],
             ),
            ([{'search_phone': '380000000012'}, 1],
             [{'search_name': 'giga'}, 0],
             ),
            ([{'doctor_uuid': '2'}, 12],
             [{'patient_uuid': '4'}, 2],
             [{'doctor_name': 'тарас'}, 0],
             [{'patient_name': 'oao'}, 0],
             [{'date': today}, 1],
             [{'date_from': today}, 81],
             [{'date_to': today}, 120],
             [{'filled': True}, 100],
             [{'filled': False}, 100],
             [{'upcoming': True}, 81],
             [{'upcoming': False}, 119],
             ),
        )
        for service, bundle in zip(services, cases):
            for kwargs, total in bundle:
                with self.subTest(f'{service.__name__}:{list(kwargs.keys())[0]}'):
                    with patch.object(self.db.func, 'timestamp', self.db.func.datetime):
                        pagination = service.get_pagination(**kwargs)
                        modified = service.get_pagination_modified(**kwargs)
                    self.assertIsInstance(pagination, Pagination)
                    if 'upcoming' in kwargs:
                        self.assertAlmostEqual(pagination.total, total, delta=1)
                    else:
                        self.assertEqual(pagination.total, total)
                    self.assertEqual(pagination.filters, kwargs)
                    if total:
                        self.assertIsInstance(modified, datetime)
                    else:
                        self.assertIsNone(modified)
        self.assertEqual(pagination.page, 1)
        self.assertEqual(pagination.per_page, 20)
        pagination = PatientService.get_pagination(page=5, per_page=5)
        self.assertEqual(len(pagination.items), 5)
        self.assertEqual(pagination.page, 5)

    def test_get(self):
        for service, model in zip(services, self.models):
            with self.subTest(service.__name__):
                instance = service.get('5')
                self.assertIsInstance(instance, model)
                self.assertEqual(instance.uuid, '5')
                self.assertTrue(repr(instance).startswith(f'<{model.__name__}('))

    def test_appointment_get_count(self):
        kwargs = {'date_from': date.today() - timedelta(days=80),
                  'date_to': date.today() + timedelta(days=60)}
        count = AppointmentService.get_count(**kwargs)
        self.assertEqual(count, 140)

    def test_appointment_get_income(self):
        kwargs = {'date_from': date.today() - timedelta(days=70),
                  'date_to': date.today() - timedelta(days=30)}
        count = AppointmentService.get_income(**kwargs)
        self.assertEqual(count, 6150)

    def test_user_get_by_email(self):
        user = UserService.get_by_email('root')
        self.assertIsNotNone(user)
        user = UserService.get_by_email('zxcv')
        self.assertIsNone(user)
