from flask import Blueprint, render_template, request, g
from report_app.db import Driver, DoesNotExist, connection

bp = Blueprint('routes', __name__)


def select_all(*fields):
    """Query helper"""
    order = Driver.lap_time.desc() if g.order == 'desc' else Driver.lap_time.asc()
    return Driver.select(*fields).order_by(order).dicts()


@bp.before_request
def before_request():
    g.order = request.args.get('order')
    g.order_dict = {'order': None, 'reversed_order': 'desc'} if g.order != 'desc' else \
        {'order': 'desc', 'reversed_order': None}


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route("/report/")
def report():
    with connection():
        query = select_all(Driver.rank, Driver.full_name, Driver.car, Driver.lap_time)
        return render_template("report.html", drivers=query, **g.order_dict)


@bp.route("/report/drivers/")
def drivers():
    driver_id = request.args.get('driver_id')
    if driver_id is None:
        with connection():
            query = select_all(Driver.rank, Driver.full_name, Driver.code)
            return render_template("drivers.html", drivers=query, **g.order_dict)
    else:
        try:
            with connection():
                query = Driver.select(*Driver.FIELDS).where(Driver.code == driver_id).dicts()
                return render_template("driver.html", driver=query.get(), **g.order_dict)
        except DoesNotExist:
            return render_template("no_such_driver.html", code=driver_id, **g.order_dict)
