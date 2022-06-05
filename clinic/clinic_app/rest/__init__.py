"""
This package contains modules defining REST APIs for User, Doctor, Patient and Appointment
models. Respective API endpoints are initialized here and everything is linked to `api_bp`:

Modules:

- `base_resource.py`: defines base resource classes with common routines
- `resources`: defines all REST API resources
- `schemas.py`: contains Marshmallow schemas for serialization/deserialization of db models
"""
from flask import Blueprint
from flask_restful import Api

from clinic_app.rest.resources import \
    AppointmentApi, AppointmentListApi, StatisticsApi, UserApi, \
    UserListApi, DoctorApi, DoctorListApi, PatientApi, PatientListApi

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

api.add_resource(UserListApi, '/users', endpoint='users')
api.add_resource(UserApi, '/users/<uuid>', endpoint='user')
api.add_resource(DoctorListApi, '/doctors', endpoint='doctors')
api.add_resource(DoctorApi, '/doctors/<uuid>', endpoint='doctor')
api.add_resource(PatientListApi, '/patients', endpoint='patients')
api.add_resource(PatientApi, '/patients/<uuid>', endpoint='patient')
api.add_resource(AppointmentListApi, '/appointments', endpoint='appointments')
api.add_resource(AppointmentApi, '/appointments/<uuid>', endpoint='appointment')
api.add_resource(StatisticsApi, '/appointments/stats', endpoint='statistics')
