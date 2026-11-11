import pathlib
import sys
import unittest
from unittest import mock
import urllib.error

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'scripts'))
import smoke_sandbox as smoke


class SmokeTests(unittest.TestCase):
    def test_profile_editor_missing_or_stale_script_fails(self):
        page = '<script src="/static/netbox_custom_field_profiles/profile_fields.js?v=2"></script>'
        for asset in ((404, '', ''), (200, '', '// stale script')):
            with self.subTest(asset=asset), mock.patch.object(smoke, 'fetch', side_effect=[(200, '', page), asset]):
                with self.assertRaisesRegex(smoke.SmokeFailure, 'JavaScript missing or stale'):
                    smoke.check_profile_assets(None, 'http://localhost')

    def test_profile_editor_without_script_reference_fails(self):
        with mock.patch.object(smoke, 'fetch', return_value=(200, '', '<form></form>')):
            with self.assertRaisesRegex(smoke.SmokeFailure, 'script reference missing'):
                smoke.check_profile_assets(None, 'http://localhost')

    def test_csrf_parses_reordered_escaped_attributes(self):
        form = smoke.LoginForm()
        form.feed('<input value="abc&amp;def" type="hidden" name="csrfmiddlewaretoken">')
        self.assertEqual(form.token, 'abc&def')

    def test_login_get_is_not_authenticated_evidence(self):
        self.assertFalse(smoke.is_authenticated_page((200, 'http://localhost/login/', 'Login'), 'http://localhost'))
        self.assertFalse(smoke.is_authenticated_page((200, 'http://localhost/users/users/', '<input name="password">'), 'http://localhost'))

    def test_missing_csrf_fails_before_post(self):
        with mock.patch.object(smoke, 'fetch', return_value=(200, '/login/', 'Login')) as fetch:
            with self.assertRaises(smoke.SmokeFailure):
                smoke.login(None, 'http://localhost', 'admin', 'secret')
            self.assertEqual(fetch.call_count, 1)

    def test_api_requires_exact_user(self):
        for result in [(403, '', ''), (200, '', '{}'), (200, '', '{"count":1,"results":[{"username":"wrong"}]}')]:
            with self.assertRaises(smoke.SmokeFailure):
                smoke.assert_api_identity(result, 'admin')
        smoke.assert_api_identity((200, '', '{"count":1,"results":[{"username":"admin"}]}'), 'admin')

    def test_timeout_is_bounded_and_redacted(self):
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.URLError('sensitive contents')
        with self.assertRaisesRegex(smoke.SmokeFailure, 'redacted') as caught:
            smoke.fetch(opener, 'http://localhost')
        self.assertNotIn('sensitive', str(caught.exception))
        self.assertEqual(opener.open.call_args.kwargs['timeout'], 15)

    def test_redirects_cannot_leave_local_origin(self):
        redirect = smoke.LocalRedirects('http://127.0.0.1:18047')
        with self.assertRaises(smoke.SmokeFailure):
            redirect.redirect_request(None, None, 302, '', {}, 'https://example.com/')

    def test_runtime_failure_blocks_authentication(self):
        with mock.patch.object(smoke.sandbox, 'ensure_env', return_value={}), mock.patch.object(smoke.sandbox, 'runtime', side_effect=RuntimeError('schema drift')), mock.patch.object(smoke, 'client') as client:
            with self.assertRaisesRegex(RuntimeError, 'schema drift'):
                smoke.smoke()
            client.assert_not_called()

    def test_accepted_wrong_password_fails_smoke(self):
        values = {'NETBOX_PORT': '18047', 'SUPERUSER_NAME': 'admin'}
        with mock.patch.object(smoke.sandbox, 'ensure_env', return_value=values), mock.patch.object(smoke.sandbox, 'runtime'), mock.patch.object(smoke, 'client', return_value=(None, [])), mock.patch.object(smoke, 'fetch', return_value=(200, 'http://127.0.0.1:18047/login/', 'login')), mock.patch.object(smoke, 'login', return_value=True):
            with self.assertRaisesRegex(smoke.SmokeFailure, 'wrong password accepted'):
                smoke.smoke()

    def test_rejected_password_does_not_prove_positive_login(self):
        values = {'NETBOX_PORT': '18047', 'SUPERUSER_NAME': 'admin', 'SUPERUSER_PASSWORD': 'secret'}
        with mock.patch.object(smoke.sandbox, 'ensure_env', return_value=values), mock.patch.object(smoke.sandbox, 'runtime'), mock.patch.object(smoke, 'client', return_value=(None, [])), mock.patch.object(smoke, 'fetch', return_value=(200, 'http://127.0.0.1:18047/login/', 'login')), mock.patch.object(smoke, 'login', return_value=False):
            with self.assertRaisesRegex(smoke.SmokeFailure, 'real CSRF login failed'):
                smoke.smoke()


if __name__ == '__main__':
    unittest.main()
