"""
General routes
"""
from flask import Blueprint, render_template, redirect, url_for

from clinic_app.service import DoctorService
from clinic_app.views.utils import get_pagination_args

general_bp = Blueprint('general', __name__)


# pylint: disable=missing-function-docstring
@general_bp.route('/')
def index():
    return render_template('index.html')


@general_bp.route('/doctors')
def doctors():
    pages = get_pagination_args(8)
    pagination = DoctorService.get_pagination(*pages)
    if len(pagination.items) == 0 < pagination.total:
        return redirect(url_for('general.doctors'))
    return render_template('doctors.html', data=pagination)
