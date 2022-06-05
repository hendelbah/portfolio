"""
This module contains main populating functions
"""
from datetime import date, time, timedelta
from random import choice, randint

from werkzeug.security import generate_password_hash

from clinic_app import db
from clinic_app.models import Appointment, Doctor, Patient, User
from clinic_app.service.populate.population_data import (
    DOCTORS_SRC, NAMES_SRC, SURNAMES_SRC, PATRONYMICS_SRC, ROOT_PASSWORD, DOCTORS_PASSWORD)

root_pass_hash = generate_password_hash(ROOT_PASSWORD)
doctors_pass_hash = generate_password_hash(DOCTORS_PASSWORD)


def clear_tables():
    """
    Clear all tables.
    """
    Appointment.query.delete()
    Patient.query.delete()
    User.query.delete()
    Doctor.query.delete()
    db.session.commit()


# pylint: disable=no-member
def populate(patients_amount=100):
    """
    Populate database with sample data, using population_data and random_utils.

    :param patients_amount: amount of random patients to insert
    """
    users_doctors_src = [
        {'id': 1,
         'uuid': '1',
         'email': 'root',
         'password_hash': root_pass_hash,
         'is_admin': True}
    ]
    users_doctors_src.extend(
        {
            'id': user_id,
            'uuid': str(user_id),
            'doctor_id': doctor["id"],
            'email': f'doctor_{doctor["id"]:0>3}@spam.ua',
            'password_hash': doctors_pass_hash,  # hashing is too slow to do it for every user
            'is_admin': user_id == 2,
        }
        for user_id, doctor in enumerate(DOCTORS_SRC, 2)  # 1st user is root
    )
    patients_src = []
    appointments_1_src = []
    appointments_2_src = []
    for i in range(1, patients_amount + 1):
        sex = randint(0, 1)
        name = f'{choice(SURNAMES_SRC)} {choice(NAMES_SRC[sex])} {choice(PATRONYMICS_SRC[sex])}'
        patient = {
            'id': i,
            'uuid': str(i),
            'phone_number': f'380{i * 3:0>9}',
            'full_name': name,
            'birthday': date.fromordinal(717200 + i * 10)
        }
        doctor_id = int(i / patients_amount * (len(DOCTORS_SRC) - 1) + 1)
        appointment_1 = {
            'id': i,
            'uuid': str(i),
            'patient_id': i,
            'doctor_id': doctor_id,
            'date': date.today() + timedelta(days=i - 20),
            'time': time(hour=11),
        }
        appointment_2 = {
            'id': i + patients_amount,
            'uuid': str(i + patients_amount),
            'patient_id': i,
            'doctor_id': doctor_id,
            'date': date.today() - timedelta(days=20 + i),
            'time': time(hour=12),
            'conclusion': 'Diagnosis: common cold',
            'prescription': 'Panadol 500mg',
            'bill': i * 5,
        }
        patients_src.append(patient)
        appointments_1_src.append(appointment_1)
        appointments_2_src.append(appointment_2)

    db.session.bulk_insert_mappings(Doctor, DOCTORS_SRC)
    db.session.bulk_insert_mappings(User, users_doctors_src)
    db.session.bulk_insert_mappings(Patient, patients_src)
    db.session.bulk_insert_mappings(Appointment, appointments_1_src)
    db.session.bulk_insert_mappings(Appointment, appointments_2_src)
    db.session.commit()


def main():
    """main"""
    clear_tables()
    populate()


if __name__ == '__main__':
    main()
