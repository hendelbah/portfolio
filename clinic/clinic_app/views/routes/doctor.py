"""
Doctor panel routes
"""
from datetime import date, datetime

from flask import Blueprint, render_template, abort, redirect, url_for, request, g
from flask_login import current_user, login_required

from clinic_app.service import AppointmentService
from clinic_app.views.forms import FilterAppointments, FillAppointment
from clinic_app.views.utils import get_pagination_args, parse_filters, \
    extract_filters, process_form_submit

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor-panel')


# pylint: disable=assigning-non-slot
@doctor_bp.before_request
@login_required
def doctors_only():
    """
    Checks if user is logged in and has doctor privileges
    before all requests for this blueprint.
    """
    if current_user.doctor is None:
        return abort(403)
    name = current_user.doctor.full_name
    g.unfilled = AppointmentService.get_count(filled=False, upcoming=False, doctor_name=name)
    g.booked = AppointmentService.get_count(upcoming=True, doctor_name=name)
    return None


# pylint: disable=missing-function-docstring
@doctor_bp.route('/')
def index():
    return render_template('doctor_panel/index.html')


@doctor_bp.route('/appointments/booked', methods=['GET', 'POST'], endpoint='booked_apps',
                 defaults={'case': 1})
@doctor_bp.route('/appointments/unfilled', methods=['GET', 'POST'], endpoint='unfilled_apps',
                 defaults={'case': 2})
@doctor_bp.route('/appointments/archived', methods=['GET', 'POST'], endpoint='archived_apps',
                 defaults={'case': 3})
def appointments(case: int):
    form = FilterAppointments()
    if form.validate_on_submit():
        filters = extract_filters(['patient_name', 'date'], form)
        return redirect(url_for(request.endpoint, **filters))
    kwargs_list = [{'key': 'patient_name'},
                   {'key': 'date', 'type': date.fromisoformat}]
    filters = parse_filters(kwargs_list, form)
    filters['doctor_name'] = current_user.doctor.full_name
    if case == 1:
        filters['upcoming'] = True
    elif case == 2:
        filters['filled'] = False
        filters['upcoming'] = False
    else:
        filters['filled'] = True
        filters['upcoming'] = False
    pages = get_pagination_args()
    data = AppointmentService.get_pagination(*pages, **filters)
    income = AppointmentService.get_income(**filters)
    return render_template('doctor_panel/appointments.html', data=data, form=form,
                           active_menu_item=case, income=income)


@doctor_bp.route('/appointments/<uuid>', methods=['GET', 'POST'], endpoint='appointment')
def appointment_view(uuid):
    form = FillAppointment()
    if form.validate_on_submit():
        response, _ = process_form_submit(form, AppointmentService, uuid, 'appointment')
        return response
    appointment = AppointmentService.get(uuid)
    if appointment is None:
        abort(404)
    if appointment.doctor.full_name != current_user.doctor.full_name:
        abort(403)
    form = FillAppointment(obj=appointment)
    app_datetime = datetime.combine(appointment.date, appointment.time)
    readonly = app_datetime >= datetime.now() or appointment.bill is not None
    return render_template(
        'doctor_panel/appointment.html', item=appointment, form=form, readonly=readonly)
