"""
This module defines doctor service class:
"""
from sqlalchemy.orm import Query

from clinic_app.models import Doctor, User
from clinic_app.service.base_service import BaseService


# pylint: disable=arguments-differ, no-member
class DoctorService(BaseService):
    """Service class for querying Doctor model"""
    model = Doctor
    order_by = (model.full_name,)

    @classmethod
    def _filter_by(cls, *, search_name: str = None, no_user: bool = False) -> Query:
        """
        Return query ordered and filtered.

        :param search_name: filter doctors with full name like this one
        :param no_user: filter doctors with no associated user accounts
        """
        query = cls._order()
        if search_name is not None:
            query = query.filter(cls.model.full_name.like(f'%{search_name}%'))
        if no_user:
            query = query.filter(~User.query.filter_by(doctor_id=Doctor.id).exists())
        return query
