"""
Package contains modules defining SQLAlchemy models

Modules:

- `doctor.py`: defines model representing doctors
- `patient.py`: defines model representing doctors
- `user.py`: defines model representing users
- `appointment.py`: defines model representing appointments
"""
from clinic_app.models.appointment import Appointment
from clinic_app.models.doctor import Doctor
from clinic_app.models.patient import Patient
from clinic_app.models.user import User

__all__ = ['Doctor', 'Appointment', 'Patient', 'User']
