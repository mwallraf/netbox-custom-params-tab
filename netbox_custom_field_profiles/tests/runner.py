"""Native feature test isolation; never run profile tests on the live database."""
from django.db import connections
from django.test.runner import DiscoverRunner


class ProfileTestRunner(DiscoverRunner):
    def build_suite(self, *args, **kwargs):
        suite = super().build_suite(*args, **kwargs)
        if not suite.countTestCases():
            raise RuntimeError('PROFILE_TESTS_EMPTY: refusing a zero-test success')
        return suite

    def setup_databases(self, **kwargs):
        original_names = {alias: connections[alias].settings_dict['NAME'] for alias in connections}
        for alias in connections:
            db = connections[alias]
            if db.vendor != 'postgresql':
                raise RuntimeError('PROFILE_TESTS_DATABASE: native PostgreSQL required')
            if db.creation._get_test_db_name() == original_names[alias]:
                raise RuntimeError('PROFILE_TESTS_DATABASE: test database equals live database')
        result = super().setup_databases(**kwargs)
        for alias, live_name in original_names.items():
            if connections[alias].settings_dict['NAME'] == live_name:
                raise RuntimeError('PROFILE_TESTS_DATABASE: test database was not activated')
        print('PROFILE_TESTS_ISOLATED PostgreSQL test database differs from live database')
        return result
