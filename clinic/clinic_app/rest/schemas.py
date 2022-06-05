"""
This module contains all marshmallow schemas for serialization/deserialization of db models,
and some useful functions.

Here are defined The following classes:

- `DoctorSchema`, doctor serialization/deserialization schema
- `PatientSchema`
- `BookedAppointmentSchema`
- `AppointmentSchema`

Functions:

- `paginate_schema`: dynamically defines schema for serialization of flask-SQLAlchemy pagination
"""

from flask_restful import abort
from marshmallow import ValidationError, validate

from clinic_app import ma
from clinic_app.models import User, Doctor, Patient, Appointment


class BaseSchema(ma.SQLAlchemyAutoSchema):
    """Custom base schema class"""

    def __init__(self, *args, **kwargs):
        self.opts.exclude += ('id', 'last_modified')
        self.opts.dump_only += ('uuid',)
        super().__init__(*args, **kwargs)

    # pylint: disable=inconsistent-return-statements
    def load_or_422(self, data, **kwargs):
        """
        Return loaded data. If validation error occurs throw 422 http error.

        :param data: data to validate
        :param kwargs: kwargs to Schema.load()
        :return: loaded_object
        """
        try:
            return self.load(data, **kwargs)
        except ValidationError as err:
            abort(422, errors=err.messages, message='Data is invalid')


# pylint: disable=no-member
class UserSchema(BaseSchema):
    """
    User serialization/deserialization schema
    """

    class Meta:
        """
        User schema metadata
        """
        model = User

    doctor = ma.Nested('DoctorSchema', exclude=['user'], dump_only=True)
    doctor_uuid = ma.String(allow_none=True, load_only=True)


class DoctorSchema(BaseSchema):
    """
    Doctor serialization/deserialization schema
    """

    class Meta:
        """
        Doctor schema metadata
        """
        model = Doctor

    full_name = ma.auto_field(validate=validate.Regexp(r'^\w{2,}( \w{2,}){1,2}$'))
    user = ma.Nested('UserSchema', exclude=['doctor'], dump_only=True)


class PatientSchema(BaseSchema):
    """
    Patient serialization/deserialization schema
    """

    class Meta:
        """
        Patient schema metadata
        """
        model = Patient

    full_name = ma.auto_field(validate=validate.Regexp(r'^\w{2,}( \w{2,}){1,2}$'))


class AppointmentSchema(BaseSchema):
    """
    Appointment serialization/deserialization schema
    """

    class Meta:
        """
        Appointment schema metadata
        """
        model = Appointment
        partial = ['conclusion', 'prescription', 'bill']

    doctor = ma.Nested('DoctorSchema', exclude=['user'], dump_only=True)
    patient = ma.Nested('PatientSchema', dump_only=True)
    doctor_uuid = ma.String(required=True, load_only=True)
    patient_uuid = ma.String(required=True, load_only=True)


# pylint: disable=no-member
def pagination_schema(items_schema: ma.Schema):
    """
    Return schema instance for serialization of flask-SQLAlchemy pagination
    with dynamically defined schema of nested field `items`.

    :param items_schema: schema for Pagination.items
    """

    class PaginationSchema(ma.Schema):
        """Schema for serialization of Pagination object"""

        class Meta:
            """
            Pagination schema metadata
            """
            additional = ('page', 'per_page', 'pages', 'total', 'has_prev', 'has_next')

        items = ma.Nested(items_schema, many=True)

    return PaginationSchema()
