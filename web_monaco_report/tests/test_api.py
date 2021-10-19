from tests.fixtures import *
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


class TestAPI:
    def test_report(self, get_app_response, database):
        with connection(database):
            query = Driver.select(*Driver.FIELDS).order_by(Driver.lap_time.asc()).dicts()
            report_obj = list(query)
        response_obj = get_app_response('GET', 'api.report', format='json').json
        assert response_obj == report_obj
        report_xml = parseString(dicttoxml(report_obj, custom_root='report', attr_type=False)).toprettyxml()
        response = get_app_response('GET', 'api.report', format='xml')
        assert response.data == bytes(report_xml, encoding='UTF-8')

    def test_report_driver(self, get_app_response, database):
        with connection(database):
            query = Driver.select(*Driver.FIELDS).where(Driver.code == 'SVF').dicts()
            driver_obj = query.get()
        response_obj = get_app_response('GET', 'api.driver_report', driver_id='SVF', format='json').json
        assert response_obj == driver_obj
        driver_xml = parseString(dicttoxml(driver_obj, custom_root='driver', attr_type=False)).toprettyxml()
        response = get_app_response('GET', 'api.driver_report', driver_id='SVF', format='xml')
        assert response.data == bytes(driver_xml, encoding='UTF-8')

    def test_drivers(self, get_app_response, database):
        with connection(database):
            query = Driver.select(Driver.full_name, Driver.code).order_by(Driver.lap_time.asc()).dicts()
            drivers_obj = list(query)
        response_obj = get_app_response('GET', 'api.drivers', format='json').json
        assert response_obj == drivers_obj
        drivers_xml = parseString(dicttoxml(drivers_obj, custom_root='drivers', attr_type=False)).toprettyxml()
        response = get_app_response('GET', 'api.drivers', format='xml')
        assert response.data == bytes(drivers_xml, encoding='UTF-8')

    def test_wrong_driver(self, get_app_response):
        report_obj = get_app_response('GET', 'api.driver_report', driver_id='aaa', format='json').json
        assert report_obj['message'] == 'Driver is not found'

    def test_wrong_format(self, get_app_response):
        report_obj = get_app_response('GET', 'api.report', format='jpeg').json
        assert report_obj['message']['format'] == 'jpeg is not a valid choice'
