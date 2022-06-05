"""
This module defines user service class:
"""
import typing as t

from sqlalchemy.orm import Query

from clinic_app.models import User
from clinic_app.service.base_service import BaseService


# pylint: disable=arguments-differ
class UserService(BaseService):
    """Service class for querying User model"""
    model = User
    order_by = (model.id,)

    @classmethod
    def _filter_by(cls, *, search_email: str = None) -> Query:
        """
        Return query ordered and filtered.

        :param search_email: filter with email like this one
        """
        query = cls._order()
        if search_email is not None:
            query = query.filter(cls.model.email.like(f'%{search_email}%'))
        return query

    @classmethod
    def get_by_email(cls, email: str) -> t.Optional[User]:
        """
        Load user from db by email, return User instance if success, else return None

        :param email: user's email
        """
        return cls.model.query.filter_by(email=email).first()
