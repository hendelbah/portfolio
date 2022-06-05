"""
Useful tools for keeping views DRY.
"""
from secrets import choice
from string import ascii_letters, digits

from flask import redirect, url_for, flash
from flask import request
from flask_wtf import FlaskForm


def get_pagination_args(default_per_page: int = 20) -> tuple[int, int]:
    """
    Return pagination GET parameters: page, per_page(as a tuple)

    :param default_per_page: default value for per_page (default page is 1 anyway)
    :return: page, per_page
    """
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=default_per_page, type=int)
    return page, per_page


def parse_filters(kwargs_list: list[dict], form: FlaskForm) -> dict:
    """
    Parse GET parameters(filters for get request), using list of kwargs args.get() function.
    Kwargs have to contain at least 'key' key.
    Put retrieved values into dict with corresponding keys,
    and patch form fields(with name == kwargs['key']) with these values.

    :param kwargs_list: list of dicts, each dict is used as kwargs for args.get()
    :param form: flask-WTForm to patch with filters data
    :return: filters dict
    """
    filters = {}
    for kwargs in kwargs_list:
        arg = request.args.get(**kwargs)
        filters[kwargs['key']] = arg
        field = getattr(form, kwargs['key'])
        field.data = arg
    return filters


def extract_filters(keys, form) -> dict:
    """
    Extract field data from given form(basically serialize) into dict, using given keys.
    :param keys: field names and keys in resulting dict
    :param form: flask-WTForm to extract
    :return: dict of filters
    """
    filters = {}
    for key in keys:
        field = getattr(form, key)
        filters[key] = field.data
    return filters


def random_password(length=15) -> str:
    """
    Return random password with given length, generated from ascii letters and digits

    :param int length: password length
    """
    alphabet = ascii_letters + digits
    return ''.join(choice(alphabet) for _ in range(length))


def process_form_submit(form, service, uuid, name, **kwargs):
    """
    Process form submission at item endpoints of admin blueprint.
    Save form data to database, flash corresponding messages and return
    redirect response with status code as tuple.

    :param form: submitted and validated form
    :param service: service for db operations
    :param uuid: uuid of resource, 'new' for create operation
    :param name: name of item
    :param kwargs: additional fields that are absent in form and should be submitted to database.
    :return: redirect response
    """
    data = form.data
    data.pop('submit')
    if data.get('csrf_token'):
        data.pop('csrf_token')
    data.update(kwargs)
    if uuid == 'new':
        result, code = service.create(data)
        if code == 201:
            flash(f'{name.capitalize()} created successfully', 'success')
    else:
        result, code = service.update(uuid, data)
        if code == 200:
            flash(f'{name.capitalize()} updated successfully', 'success')
    if code not in (200, 201):
        errors = result.get('errors') and ' ,'.join(
            f'{key}: {value}' for key, value in result['errors'].items())
        flash(f'{errors}', 'error')
        if uuid == 'new':
            return redirect(url_for(f'.{name}s')), code
    return redirect(url_for(f'.{name}', uuid=result.uuid)), code
