import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'scripts'))
import legacy_tests
import sandbox


class LegacyReportTests(unittest.TestCase):
    def test_outcomes_do_not_turn_failure_green(self):
        cases = [(0, '4 passed', 'passed'), (0, '', 'unverified-zero-exit'),
                 (1, '2 failed, 3 passed', 'test-failures'),
                 (1, 'No module named pytest', 'runner-unavailable'),
                 (2, 'ERROR collecting tests/test_models.py', 'collection-error'),
                 (1, 'ERROR at setup of TestDevice', 'setup-error'),
                 (5, 'no tests ran', 'no-tests-collected')]
        for code, text, expected in cases:
            self.assertEqual(legacy_tests.classify(code, text), expected)

    def test_counts_are_actual_reported_counts(self):
        self.assertEqual(legacy_tests.counts('3 failed, 12 passed, 1 error'), {'failed': 3, 'passed': 12, 'error': 1})

    def test_generated_values_redacted(self):
        with mock.patch.object(sandbox.Path, 'exists', return_value=True), mock.patch.object(sandbox.Path, 'read_text', return_value='SUPERUSER_PASSWORD=topsecret\n'):
            self.assertEqual(sandbox.redact('password topsecret hidden'), 'password [REDACTED] hidden')


if __name__ == '__main__':
    unittest.main()
