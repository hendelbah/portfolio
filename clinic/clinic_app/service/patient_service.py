"""
This module defines patient service class:
"""
from sqlalchemy.orm import Query

from clinic_app.models import Patient
from clinic_app.service.base_service import BaseService


# pylint: disable=arguments-differ
class PatientService(BaseService):
    """Service class for querying Patient model"""
    model = Patient
    order_by = (model.full_name,)

    @classmethod
    def _filter_by(cls, *, search_phone: str = None, search_name: str = None) -> Query:
        """
        Return query ordered and filtered.

        :param search_phone: filter patients with phone number like this one
        :param search_name: filter patients with full name like this one
        """
        query = cls._order()
        if search_phone is not None:
            query = query.filter(cls.model.phone_number.like(f'%{search_phone}%'))
        if search_name is not None:
            query = query.filter(cls.model.full_name.like(f'%{search_name}%'))
        return query
