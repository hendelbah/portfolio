# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring
from clinic_app.rest.schemas import UserSchema, DoctorSchema, PatientSchema, AppointmentSchema
from tests.base_test_case import BaseTestCase

schemas = (UserSchema, DoctorSchema, PatientSchema, AppointmentSchema)


class TestSchemas(BaseTestCase):
    def test_validate(self):
        cases = (
            ['email', 'is_admin', 'password_hash'],
            ['experience_years', 'full_name', 'info', 'speciality'],
            ['birthday', 'full_name', 'phone_number'],
            ['date', 'doctor_uuid', 'patient_uuid', 'time'],
        )
        for case, schema in zip(cases, schemas):
            with self.subTest(schema.__name__):
                schema = schema()
                keys = sorted(list(schema.validate({})))
                self.assertEqual(keys, case)

    def test_dump(self):
        cases = (
            ['doctor', 'email', 'is_admin', 'password_hash', 'uuid'],
            ['experience_years', 'full_name', 'info', 'speciality', 'user', 'uuid'],
            ['birthday', 'full_name', 'phone_number', 'uuid'],
            ['bill', 'conclusion', 'date', 'doctor', 'patient', 'prescription', 'time', 'uuid'],
        )
        for case, schema, model in zip(cases, schemas, self.models):
            with self.subTest(schema.__name__):
                schema = schema()
                instance = model.query.get(1)
                keys = sorted(list(schema.dump(instance)))
                self.assertEqual(keys, case)
