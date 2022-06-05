"""
This module contains proxy descriptors for setting some model's foreign key using uuid field
"""

from clinic_app import db
from clinic_app.models.doctor import Doctor
from clinic_app.models.patient import Patient


class DoctorUUID:
    """
    Proxy descriptor for setting doctor_id foreign key using doctor's uuid
    """

    def __set__(self, obj, value: str):
        """
        Set instance's doctor_id attribute to id of doctor with given uuid.
        Also update doctor relationship.
        If value is None - set doctor_id to None

        :raise ValueError: if doctor is not found
        """
        if value is None:
            obj.doctor = None
            obj.doctor_id = None
        else:
            with db.session.no_autoflush as session:
                doctor = session.query(Doctor).filter_by(uuid=value).first()
            if doctor is None:
                raise ValueError('Invalid doctor_uuid')
            obj.doctor = doctor
            obj.doctor_id = doctor.id

    def __get__(self, obj, obj_type=None):
        """
        Return uuid of doctor from relationship, None if doctor is None
        """
        if obj.doctor is None:
            return None
        return obj.doctor.uuid


class PatientUUID:
    """
    Proxy descriptor for setting patient_id foreign key using patient's uuid
    """

    def __set__(self, obj, value: str):
        """
        Set instance's patient_id attribute to id of patient with given uuid.
        Also update patient relationship.
        If value is None - set patient_id to None

        :raise ValueError: if patient is not found
        """
        if value is None:
            obj.patient = None
            obj.patient_id = None
        else:
            with db.session.no_autoflush as session:
                patient = session.query(Patient).filter_by(uuid=value).first()
            if patient is None:
                raise ValueError('Invalid patient_uuid')
            obj.patient = patient
            obj.patient_id = patient.id

    def __get__(self, obj, obj_type=None):
        """
        Return uuid of patient from relationship, None if patient is None
        """
        if obj.patient is None:
            return None
        return obj.patient.uuid
