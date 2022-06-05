"""
This module implements appointment model for 'appointment' table in database
"""
from datetime import date as date_, time as time_, datetime
from uuid import uuid4

from clinic_app import db
from clinic_app.models.descriptors import DoctorUUID, PatientUUID


class Appointment(db.Model):
    """
    Appointment object stands for representation of data row in `appointment` table.
    """
    __tablename__ = 'appointment'
    __table_args__ = (
        db.UniqueConstraint('doctor_id', 'date', 'time'),
        db.UniqueConstraint('patient_id', 'date', 'time'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), nullable=False, unique=True, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id', ondelete='CASCADE'),
                          nullable=False, index=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'),
                           nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=False)
    conclusion = db.Column(db.String(511))
    prescription = db.Column(db.String(511))
    bill = db.Column(db.Integer)
    last_modified = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow,
                              onupdate=datetime.utcnow)

    doctor = db.relationship('Doctor')
    patient = db.relationship('Patient')
    doctor_uuid = DoctorUUID()
    patient_uuid = PatientUUID()

    def __init__(self, doctor_uuid: str, patient_uuid: str, date: date_, time: time_,
                 conclusion: str = None, prescription: str = None, bill: str = None):
        """
        :param doctor_uuid: uuid of involved doctor
        :param patient_uuid: uuid of involved patient
        :param date: date of appointment
        :param time: time of appointment
        :param conclusion: doctor's conclusion
        :param prescription: prescription for the patient
        :param bill: overall cost of doctor's services
        """
        self.doctor_uuid = doctor_uuid
        self.patient_uuid = patient_uuid
        self.date = date
        self.time = time
        self.conclusion = conclusion
        self.prescription = prescription
        self.bill = bill
        self.uuid = str(uuid4())

    def __repr__(self):
        keys = ('id', 'patient_id', 'doctor_id', 'date', 'time')
        values = (f"{key}={getattr(self, key)!r}" for key in keys)
        return f'<Appointment({", ".join(values)})>'
