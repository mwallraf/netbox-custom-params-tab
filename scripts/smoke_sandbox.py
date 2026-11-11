"""Live CSRF/session and native v2 API authentication checks, without secret output."""
import html.parser
import http.cookiejar
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

import sandbox


class SmokeFailure(RuntimeError):
    pass


class ScriptSources(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.sources.append(dict(attrs).get('src', ''))


class LoginForm(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.token = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'input' and attrs.get('name') == 'csrfmiddlewaretoken':
            self.token = attrs.get('value')


class LocalRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(self, base):
        self.origin = urllib.parse.urlsplit(base)[:2]

    def redirect_request(self, request, fp, code, message, headers, newurl):
        if urllib.parse.urlsplit(newurl)[:2] != self.origin:
            raise SmokeFailure('unexpected nonlocal redirect')
        return super().redirect_request(request, fp, code, message, headers, newurl)


def client(base):
    cookies = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), LocalRedirects(base),
                                      urllib.request.HTTPCookieProcessor(cookies)), cookies


def fetch(opener, url, *, data=None, headers=None):
    request = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with opener.open(request, timeout=15) as response:
            return response.status, response.geturl(), response.read(2_000_000).decode('utf-8')
    except urllib.error.HTTPError as error:
        return error.code, error.geturl(), ''
    except (OSError, urllib.error.URLError, TimeoutError):
        raise SmokeFailure('bounded HTTP request failed (request details redacted)') from None


def is_authenticated_page(result, base):
    status, url, body = result
    return (status == 200 and url == base + '/users/users/'
            and 'name="password"' not in body)


def login(opener, base, username, password):
    status, _, page = fetch(opener, base + '/login/')
    form = LoginForm()
    form.feed(page)
    if status != 200 or not form.token:
        raise SmokeFailure('login form or CSRF token missing')
    encoded = urllib.parse.urlencode({'username': username, 'password': password,
                                     'csrfmiddlewaretoken': form.token,
                                     'next': '/users/users/'}).encode()
    result = fetch(opener, base + '/login/', data=encoded,
                   headers={'Referer': base + '/login/', 'Content-Type': 'application/x-www-form-urlencoded'})
    return is_authenticated_page(result, base)


def assert_api_identity(result, expected):
    status, _, body = result
    if status != 200:
        raise SmokeFailure('native API authentication failed')
    try:
        data = json.loads(body)
        users = data['results']
        if data['count'] != 1 or len(users) != 1 or users[0]['username'] != expected:
            raise ValueError()
    except (ValueError, KeyError, TypeError):
        raise SmokeFailure('native API identity evidence missing') from None


def check_profile_assets(opener, base):
    status, _, body = fetch(opener, base + '/plugins/custom-field-profiles/add/')
    scripts = ScriptSources()
    scripts.feed(body)
    expected_path = '/static/netbox_custom_field_profiles/profile_fields.js'
    sources = [src for src in scripts.sources if src.split('?', 1)[0] == expected_path]
    if status != 200 or not sources:
        raise SmokeFailure('profile editor or ordering script reference missing')
    status, _, script = fetch(opener, base + sources[0])
    expected = (sandbox.ROOT / 'netbox_custom_field_profiles/static/'
                'netbox_custom_field_profiles/profile_fields.js').read_text()
    if status != 200 or script != expected:
        raise SmokeFailure('profile ordering JavaScript missing or stale; rebuild the sandbox image')
    print('PROFILE_ASSETS_HTTP_OK editor references current served selection/order script')


def smoke():
    values = sandbox.ensure_env()
    sandbox.runtime()
    base = 'http://127.0.0.1:' + values['NETBOX_PORT']
    anonymous, _ = client(base)
    if is_authenticated_page(fetch(anonymous, base + '/users/users/'), base):
        raise SmokeFailure('anonymous account access accepted')
    wrong, _ = client(base)
    if login(wrong, base, values['SUPERUSER_NAME'], 'intentionally-invalid-sandbox-password'):
        raise SmokeFailure('wrong password accepted')
    if is_authenticated_page(fetch(wrong, base + '/users/users/'), base):
        raise SmokeFailure('failed login created an authenticated session')
    authenticated, cookies = client(base)
    if not login(authenticated, base, values['SUPERUSER_NAME'], values['SUPERUSER_PASSWORD']):
        raise SmokeFailure('real CSRF login failed')
    if not any(cookie.name == 'sessionid' for cookie in cookies):
        raise SmokeFailure('authenticated session cookie missing')
    if not is_authenticated_page(fetch(authenticated, base + '/users/users/'), base):
        raise SmokeFailure('authenticated follow-up failed')
    endpoint = base + '/api/users/users/?username=' + urllib.parse.quote(values['SUPERUSER_NAME'])
    header = 'Bearer nbt_' + values['SUPERUSER_API_KEY'] + '.' + values['SUPERUSER_API_TOKEN']
    assert_api_identity(fetch(anonymous, endpoint, headers={'Authorization': header}), values['SUPERUSER_NAME'])
    bad_status, _, _ = fetch(anonymous, endpoint, headers={'Authorization': 'Bearer nbt_' + 'x' * 12 + '.' + 'x' * 40})
    if bad_status not in (401, 403):
        raise SmokeFailure('invalid API token was not rejected')
    check_profile_assets(authenticated, base)
    print('BASELINE_SMOKE_OK runtime/schema/registration/admin-session/native-token/negative-controls')


if __name__ == '__main__':
    try:
        smoke()
    except (SmokeFailure, ValueError, RuntimeError, OSError) as error:
        print('SMOKE_FAILED: ' + sandbox.redact(str(error)), file=sys.stderr)
        sys.exit(1)
