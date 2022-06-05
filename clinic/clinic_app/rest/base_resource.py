"""
This module contains base resource classes with common routines.

Classes:

- `BaseResource` base resource class, defines routines for single item resources
- `BaseListResource` base resource class, defines routines for collection resources

Functions:

- `validate_auth`: wrapper for validation api authentication.
"""
from functools import wraps

from flask import request, current_app
from flask_restful import Resource, reqparse, abort
from werkzeug.http import http_date

from clinic_app import ma
from clinic_app.rest.schemas import pagination_schema
from clinic_app.service import BaseService


def validate_auth(func):
    """
    Wraps request handler function, throws 401 http error
    if valid api-key isn't provided in headers

    :param func: function with request context
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'api-key' not in request.headers:
            return abort(401, message="Credentials not present in request")
        if request.headers['api-key'] != current_app.config['API_KEY']:
            return abort(401, message="Credentials not valid")
        return func(*args, **kwargs)

    return wrapper


# pylint: disable=missing-function-docstring
class BaseResource(Resource):
    """Base Resource class with common routines for inheritance"""

    service: BaseService
    schema: ma.Schema

    @classmethod
    @validate_auth
    def head(cls, uuid):
        modified = cls.service.get_modified(uuid)
        if modified is None:
            return abort(404)
        return {}, 204, {'Last-Modified': http_date(modified)}

    @classmethod
    @validate_auth
    def get(cls, uuid):
        schema = cls.schema()
        instance = cls.service.get(uuid)
        if instance is None:
            return abort(404)
        modified = http_date(instance.last_modified)
        return schema.dump(instance), 200, {'Last-Modified': modified}

    @classmethod
    @validate_auth
    def put(cls, uuid):
        schema = cls.schema(partial=True)
        data = schema.load_or_422(request.json)
        data, code = cls.service.update(uuid, data)
        if code >= 400:
            return abort(code, **data)
        return schema.dump(data), code

    @classmethod
    @validate_auth
    def delete(cls, uuid):
        if cls.service.delete(uuid):
            return {}, 204
        return abort(404)


class BaseListResource(Resource):
    """Base Resource class with common routines for inheritance"""

    service: BaseService
    schema: ma.Schema
    filters: reqparse.RequestParser
    pages = reqparse.RequestParser()
    pages.add_argument('page', type=int, default=1)
    pages.add_argument('per_page', type=int, default=20)

    @classmethod
    @validate_auth
    def head(cls):
        filters = cls.filters.parse_args()
        pages = cls.pages.parse_args()
        modified = cls.service.get_pagination_modified(**pages, **filters)
        if modified is None:
            return abort(404)
        return {}, 204, {'Last-Modified': http_date(modified)}

    @classmethod
    @validate_auth
    def get(cls):
        schema = cls.schema()
        filters = cls.filters.parse_args()
        pages = cls.pages.parse_args()
        pagination = cls.service.get_pagination(**pages, **filters)
        if not pagination.items:
            return abort(404)
        modified = http_date(max(map(lambda i: i.last_modified, pagination.items)))
        p_schema = pagination_schema(schema)
        return p_schema.dump(pagination), 200, {'Last-Modified': modified}

    @classmethod
    @validate_auth
    def post(cls):
        schema = cls.schema()
        data = schema.load_or_422(request.json)
        data, code = cls.service.create(data)
        if code >= 400:
            return abort(code, **data)
        return schema.dump(data), code
