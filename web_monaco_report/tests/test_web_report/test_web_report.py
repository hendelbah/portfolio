import pytest
from web_report import create_app


@pytest.fixture
def client():
    app = create_app(True)
    with app.test_client() as client:
        return client


class TestRouts:
    index_strings = [
        b'<h1>Report of Monaco 2018 racing</h1>',
        b'<h2>Menu:</h2>',
        b'Drivers</a>'
    ]

    @pytest.mark.parametrize('string', index_strings)
    def test_index(self, client, string):
        rv = client.get('/')
        assert string in rv.data

    table_cases = [
        (b'<h1>Report of Monaco 2018 racing</h1>', 'a'),
        (b'<th>Driver</th>', 'a'),
        (b'<td>Sergey Sirotkin</td>', 'a'),
        (b'17.</td>', 'a'),
        (b'Return to index page</a>', 'a'),
        (b'<th>Car</th>', 'r'),
        (b'<td>FORCE INDIA MERCEDES</td>', 'r'),
        (b'0:55:12.706</td>', 'r'),
        (b'Show drivers list</a>', 'r'),
        (b'<th>Code</th>', 'd'),
        (b'SVM</a>', 'd'),
        (b'Return to report page</a>', 'd'),
    ]

    @pytest.mark.parametrize('string, is_in_table', table_cases)
    def test_report(self, client, string, is_in_table):
        rv = client.get('/report/')
        if is_in_table in ['a', 'r']:
            assert string in rv.data
        else:
            assert string not in rv.data

    @pytest.mark.parametrize('string, is_in_table', table_cases)
    def test_drivers(self, client, string, is_in_table):
        rv = client.get('/report/drivers/')
        if is_in_table in ['a', 'd']:
            assert string in rv.data
        else:
            assert string not in rv.data

    driver_strings = [
        b'<h1>Report of Monaco 2018 racing</h1>',
        b'<h2>Statistics about Pierre Gasly:</h2>',
        b'<th>Place:</th>',
        b'<td>1:01:12.941</td>',
        b'Return to drivers list</a>'
    ]

    @pytest.mark.parametrize('string', driver_strings)
    def test_driver(self, client, string):
        rv = client.get('/report/drivers/?driver_id=PGS')
        assert string in rv.data

    no_driver_strings = [
        b'<h1>Report of Monaco 2018 racing</h1>',
        b'<h2>Oops, there is no driver with code asd</h2>',
        b'Back to drivers</a>'
    ]

    @pytest.mark.parametrize('string', no_driver_strings)
    def test_no_such_driver(self, client, string):
        rv = client.get('/report/drivers/?driver_id=asd')
        assert string in rv.data
