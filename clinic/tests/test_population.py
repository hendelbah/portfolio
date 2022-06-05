# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring
from clinic_app.service.populate import clear_tables
from clinic_app.service.populate.__main__ import main
from tests.base_test_case import BaseTestCase


class TestPopulation(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_populate(self):
        main()
        counts = (18, 17, 100, 200)
        for model, count in zip(self.models, counts):
            with self.subTest(model.__name__):
                self.assertEqual(model.query.count(), count)

    def test_clear_tables(self):
        clear_tables()
        for model in self.models:
            with self.subTest(model.__name__):
                self.assertEqual(model.query.count(), 0)
