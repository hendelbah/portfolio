from flask_restful import Resource, Api, reqparse
from flask import Blueprint, abort, Response
from report_app.db import Driver, DoesNotExist, connection
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import json

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
parser = reqparse.RequestParser()
parser.add_argument('format', default='json', choices=['json', 'xml'])


def make_formatted_response(data, custom_root='root'):
    """
    Makes response with data formatted accordingly to `format` value, JSON or XML\n
    :param data: data to serialize for making response
    :param str custom_root: specify a custom root element (XML)
    :return: Response object
    """
    args = parser.parse_args()
    if args['format'] == 'xml':
        raw_xml = dicttoxml(data, custom_root=custom_root, attr_type=False)
        data = parseString(raw_xml).toprettyxml()
    else:  # args['format'] == 'json'
        data = json.dumps(data, indent=2)
    return Response(data, 200, mimetype='application/' + args['format'])


class Report(Resource):
    @staticmethod
    def get(driver_id=None):
        if driver_id is None:
            with connection():
                query = Driver.select(*Driver.FIELDS).order_by(Driver.lap_time.asc()).dicts()
                return make_formatted_response(list(query), 'report')
        else:
            try:
                with connection():
                    query = Driver.select(*Driver.FIELDS).where(Driver.code == driver_id).dicts()
                    return make_formatted_response(query.get(), 'driver')
            except DoesNotExist:
                return abort(404, 'Driver is not found')


class Drivers(Resource):
    @staticmethod
    def get():
        with connection():
            query = Driver.select(Driver.full_name, Driver.code).order_by(Driver.lap_time.asc()).dicts()
            return make_formatted_response(list(query), 'drivers')


api.add_resource(Drivers, '/drivers/')
api.add_resource(Report, '/report/')
api.add_resource(Report, '/report/<string:driver_id>', endpoint='driver_report')
