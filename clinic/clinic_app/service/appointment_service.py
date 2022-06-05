"""
This module defines appointment service class:
"""
from datetime import date as date_

from sqlalchemy.orm import Query

from clinic_app.models import Appointment, Doctor, Patient
from clinic_app.service.base_service import BaseService


# pylint: disable=arguments-differ, no-member
class AppointmentService(BaseService):
    """Service class for querying Appointment model"""
    model = Appointment
    order_by = (model.date.desc(), model.time.desc())

    @classmethod
    def _filter_by(cls, *, doctor_uuid: str = None, patient_uuid: str = None,
                   doctor_name: str = None, patient_name: str = None,
                   date: date_ = None, date_from: date_ = None, date_to: date_ = None,
                   filled: bool = None, upcoming: bool = None, _query=None) -> Query:
        """
        Return query ordered and filtered.

        :param doctor_uuid: filter appointments related to doctor with this uuid
        :param patient_uuid: filter appointments related to patients with this uuid
        :param doctor_name: filter appointments related to doctor with full name like this
        :param patient_name: filter appointments related to patient with full name like this
        :param date: filter appointments by date, overrides date_from and date_to
        :param date_from: filter appointments since given date
        :param date_to: filter appointments up to given date
        :param filled: filter appointments having defined bill field
        :param upcoming: filter appointments yet to happen
        :param _query: query to override standard one
        """
        query = cls._order() if _query is None else _query
        if doctor_uuid is not None:
            query = query.filter(Doctor.query
                                 .filter_by(uuid=doctor_uuid)
                                 .filter_by(id=cls.model.doctor_id).exists())
        if patient_uuid is not None:
            query = query.filter(Patient.query
                                 .filter_by(uuid=patient_uuid)
                                 .filter_by(id=cls.model.patient_id).exists())
        if doctor_name is not None:
            query = query.filter(Doctor.query
                                 .filter(Doctor.full_name.like(f'%{doctor_name}%'))
                                 .filter_by(id=cls.model.doctor_id).exists())
        if patient_name is not None:
            query = query.filter(Patient.query
                                 .filter(Patient.full_name.like(f'%{patient_name}%'))
                                 .filter_by(id=cls.model.patient_id).exists())
        if date is not None:
            query = query.filter_by(date=date)
        else:
            if date_from is not None:
                query = query.filter(cls.model.date >= date_from)
            if date_to is not None:
                query = query.filter(cls.model.date <= date_to)
        if filled is True:
            query = query.filter(cls.model.bill.is_not(None))
        if filled is False:
            query = query.filter_by(bill=None)
        f = cls.db.func
        if upcoming is True:
            query = query.filter(f.timestamp(cls.model.date, cls.model.time) >= f.now())
        if upcoming is False:
            query = query.filter(f.timestamp(cls.model.date, cls.model.time) < f.now())
        return query

    @classmethod
    def get_count(cls, **filters) -> int:
        """
        Return amount of appointments rows filtered using kwargs

        :param filters: kwargs for filtering function
        """
        query = cls.model.query
        return cls._filter_by(_query=query, **filters).count()

    @classmethod
    def get_income(cls, **filters) -> int:
        """
        Return sum of bills of appointments filtered using kwargs

        :param filters: kwargs for filtering function
        """
        query = cls.db.session.query(cls.db.func.sum(cls.model.bill))
        return int(cls._filter_by(_query=query, **filters).scalar() or 0)
