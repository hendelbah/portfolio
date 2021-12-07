import pytest
from report_app.db import Driver, init_db, load_drivers_to_db, connection
from pathlib import PurePath
from report_app import create_app
from flask import url_for


@pytest.fixture(scope='class')
def database(tmp_path_factory):
    test_db_path = tmp_path_factory.getbasetemp().joinpath('test.sqlite')
    with connection(test_db_path) as db:
        db.create_tables([Driver])
        load_drivers_to_db(PurePath(__file__).parent / 'data', db)
    yield test_db_path
    test_db_path.unlink()


@pytest.fixture(scope='class')
def get_app_response(tmp_path_factory):
    app_db_path = tmp_path_factory.getbasetemp().joinpath('app.sqlite')
    app = create_app(True, app_db_path)
    with app.app_context():
        init_db()

    def request(method: str, endpoint: str, **values):
        with app.test_request_context():
            url = url_for(endpoint, **values)
        with app.test_client() as client:
            response = client.open(url, method=method)
            return response

    yield request
    app_db_path.unlink()
