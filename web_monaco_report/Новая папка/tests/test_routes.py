from tests.fixtures import *


class TestRoutes:
    cases = [
        ('routes.index', {}, []),
        ('routes.report', {}, []),
        ('routes.drivers', {}, []),
        ('routes.drivers', {'driver_id': 'PGS'}, []),
        ('routes.drivers', {'driver_id': 'asd'}, [b'there is no driver']),
    ]

    @pytest.mark.parametrize('endpoint, kwargs, strings', cases)
    def test_endpoint(self, get_app_response, endpoint, kwargs, strings):
        response = get_app_response('GET', endpoint, **kwargs)
        assert response.status_code == 200
        strings.append(b'Report of Monaco 2018 racing')
        for string in strings:
            assert string in response.data
