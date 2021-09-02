from flask import Blueprint, render_template, request, g
from web_report.racing_report import Report_cached as Report, SearchError
from pathlib import PurePath

report_data_path = PurePath(__file__).parent / 'static/report_data'
bp = Blueprint('routes', __name__)


@bp.before_request
def before_request():
    order = request.args.get('order')
    if order != 'desc':
        order = None
    g.order_dict = {'order': order, 'reversed_order': None if order else 'desc'}
    g.report = Report(report_data_path, not order)


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route("/report/")
def report():
    return render_template("report.html", drivers=g.report.drivers, **g.order_dict)


@bp.route("/report/drivers/")
def drivers():
    driver_code = request.args.get('driver_id')
    if driver_code is not None:
        try:
            driver = g.report.find_driver(driver_code, 'code')
            return render_template("driver.html", driver=driver, **g.order_dict)
        except SearchError:
            return render_template("no_such_driver.html", code=driver_code, **g.order_dict)
    else:
        return render_template("drivers.html", drivers=g.report.drivers, **g.order_dict)
