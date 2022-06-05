"""
This module contains classes representing all API resources.

- `UserListApi`: users collection API resource class
- `UserApi`: user API resource class
- `DoctorListApi`: doctors collection API resource class
- `DoctorApi`: doctor API resource class
- `PatientListApi`: patients collection API resource class
- `PatientApi`: patient API resource class
- `AppointmentListApi`: appointments collection API resource class
- `AppointmentApi`: appointment API resource class
- `StatisticsApi`: API resource class for statistics on appointments
"""

from datetime import date

from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from clinic_app.rest.base_resource import BaseResource, BaseListResource, validate_auth
from clinic_app.rest.schemas import UserSchema, DoctorSchema, PatientSchema, AppointmentSchema
from clinic_app.service import UserService, DoctorService, PatientService, AppointmentService


class UserApi(BaseResource):
    """User resource class"""
    service = UserService
    schema = UserSchema


class UserListApi(BaseListResource):
    """User list resource class"""
    service = UserService
    schema = UserSchema
    filters = RequestParser()
    filters.add_argument('search_email')


class DoctorApi(BaseResource):
    """Doctor resource class"""
    service = DoctorService
    schema = DoctorSchema


class DoctorListApi(BaseListResource):
    """Doctor list resource class"""
    service = DoctorService
    schema = DoctorSchema
    filters = RequestParser()
    filters.add_argument('search_name')
    filters.add_argument('no_user', type=bool, default=False)


class PatientApi(BaseResource):
    """Patient resource class"""
    service = PatientService
    schema = PatientSchema


class PatientListApi(BaseListResource):
    """Patient list resource class"""
    service = PatientService
    schema = PatientSchema
    filters = RequestParser()
    filters.add_argument('search_phone')
    filters.add_argument('search_name')


app_filters = RequestParser()
app_filters.add_argument('doctor_uuid')
app_filters.add_argument('patient_uuid')
app_filters.add_argument('doctor_name')
app_filters.add_argument('patient_name')
app_filters.add_argument('date_from', type=date.fromisoformat)
app_filters.add_argument('date_to', type=date.fromisoformat)


class AppointmentApi(BaseResource):
    """Appointment resource class"""
    service = AppointmentService
    schema = AppointmentSchema


class AppointmentListApi(BaseListResource):
    """Appointment list resource class"""
    service = AppointmentService
    schema = AppointmentSchema
    filters = app_filters


class StatisticsApi(Resource):
    """Appointment's statistics resource class"""
    service = AppointmentService
    schema = AppointmentSchema
    filters = app_filters

    @classmethod
    @validate_auth
    def get(cls):
        """Retrieve"""
        filters = cls.filters.parse_args()
        count = cls.service.get_count(**filters)
        income = cls.service.get_income(**filters)
        return {'count': count, 'income': income}, 200
