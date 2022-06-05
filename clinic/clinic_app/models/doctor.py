"""
This module implements instance of doctor in database
"""
from datetime import datetime
from uuid import uuid4

from clinic_app import db


class Doctor(db.Model):
    """
    Doctor object stands for representation of data row in `doctor` table.
    There is information about doctors that work in this clinic
    """
    __tablename__ = 'doctor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), nullable=False, unique=True, index=True)
    full_name = db.Column(db.String(127), nullable=False)
    speciality = db.Column(db.String(255), nullable=False)
    info = db.Column(db.String(1023), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow,
                              onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='doctor', uselist=False, lazy='joined')

    def __init__(self, full_name: str, speciality: str, info: str, experience_years: int):
        """
        :param full_name: doctor's full name
        :param speciality: doctor's speciality
        :param info: some information about doctor to display on site
        :param experience_years: years of doctor's work experience
        """
        self.full_name = full_name
        self.speciality = speciality
        self.info = info
        self.experience_years = experience_years
        self.uuid = str(uuid4())

    def __repr__(self):
        keys = ('id', 'full_name')
        values = (f"{key}={getattr(self, key)!r}" for key in keys)
        return f'<Doctor({", ".join(values)})>'
