"""
This module defines base service class with common routines for working with database.

Classes:

- `BaseService` defines common routines for service class
"""
import typing as t
from datetime import datetime
from functools import wraps

from flask_sqlalchemy import Pagination
from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy.orm import Query

from clinic_app import db
from clinic_app.models import User, Doctor, Patient, Appointment

MODEL = t.Union[User, Doctor, Patient, Appointment]


def _handle_errors(func):
    """
    Decorator for handling errors in service class methods. If error occurs return dict with error
    description and 422 code

    :param func: function to wrap, designed for BaseService methods `update` and `create`
    :return: tuple of error description and status code
    """

    @wraps(func)
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (DatabaseError, TypeError, ValueError) as error:
            if isinstance(error, IntegrityError):
                msg = 'Request data violates database constraints'
            elif isinstance(error, DatabaseError):
                msg = 'Error occurred when committing transaction'
            else:
                msg = 'Error occurred during processing request data'
            err_info = error.orig.args[-1] if isinstance(error, DatabaseError) else str(error)
            return {'message': msg, 'errors': {error.__class__.__name__: err_info}}, 422

    return handler


class BaseService:
    """Base abstract service class for querying database with common routines"""
    db = db
    model: db.Model
    order_by: tuple[db.Column]

    @classmethod
    def _filter_by(cls, **kwargs) -> Query:
        """Should return some query with filtering clause using given kwargs"""
        raise NotImplementedError

    @classmethod
    def _order(cls) -> Query:
        """Return model's base query with ORDER BY clause using order_by class argument"""
        return cls.model.query.order_by(*cls.order_by)

    @classmethod
    def get(cls, uuid: str) -> t.Optional[MODEL]:
        """
        Return model instance by uuid, None if not found

        :param uuid: model's uuid
        """
        return cls.model.query.filter_by(uuid=uuid).first()

    @classmethod
    def get_modified(cls, uuid: str) -> t.Optional[datetime]:
        """
        Return last modified datetime of db row with given uuid, None if not found

        :param uuid: model's uuid
        """
        return db.session.query(cls.model.last_modified).filter_by(uuid=uuid).scalar()

    @classmethod
    @_handle_errors
    def update(cls, uuid: str, data: dict) -> t.Tuple[t.Union[MODEL, dict], int]:
        """
        Update row with given uuid using data.
        Return tuple of data and suitable http status code.
        If success return updated model instance and code 200.
        If uuid is not found return {} and code 404.
        In case of db conflicts, wrapper returns dict with error info and code 422

        :param uuid: model's uuid.
        :param data: dict with fields to update.
        """
        instance = cls.get(uuid)
        if instance is None:
            return {'errors': {'uuid': 'Resource not found'}}, 404
        for key, value in data.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance, 200

    @classmethod
    @_handle_errors
    def create(cls, data: dict) -> t.Tuple[t.Union[MODEL, dict], int]:
        """
        Create new model instance and save it to db using data dict.
        Return tuple of data and suitable http status code.
        If success return new model instance and code 200.
        In case of wrong data or db conflicts, wrapper returns dict with error info and code 422.

        :param data: dict with for model initialization
        :return: saved model instance
        """
        instance = cls.model(**data)
        db.session.add(instance)
        db.session.commit()
        return instance, 201

    @classmethod
    def delete(cls, uuid: str) -> bool:
        """
        Delete record by uuid. Return True if Success else False.

        :param uuid: model's uuid.
        """
        res = cls.model.query.filter_by(uuid=uuid).delete()
        if res:
            db.session.commit()
        return bool(res)

    @classmethod
    def get_pagination(cls, page: int = 1, per_page: int = 20, **filters) -> t.Optional[Pagination]:
        """
        Return Pagination object, for model instances selected and filtered using kwargs.

        :param page: pagination page
        :param per_page: items per page for pagination
        :param filters: kwargs for filtering
        """
        pagination = cls._filter_by(**filters).paginate(page=page, per_page=per_page)
        pagination.filters = filters
        return pagination

    # pylint: disable=no-member
    @classmethod
    def get_pagination_modified(cls, page: int = 1, per_page: int = 20, **filters) -> \
            t.Optional[datetime]:
        """
        Return datetime of last modification of filtered collection.
        If there is no items in filtered collection return None.

        :param page: pagination page
        :param per_page: items per page for pagination
        :param filters: kwargs for filtering
        """
        offset = (page - 1) * per_page
        subquery = cls._filter_by(**filters).limit(per_page).offset(offset).subquery()
        aliased_model = db.aliased(cls.model, subquery)
        return db.session.query(db.func.max(aliased_model.last_modified)).scalar()
