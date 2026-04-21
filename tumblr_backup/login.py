from __future__ import annotations

from pathlib import Path
import re
import sys
from getpass import getpass
from http.cookiejar import MozillaCookieJar

import requests


def get_api_token(session: requests.Session) -> str:
    """get Tumblr API token to be able to log in."""
    r = session.get('https://www.tumblr.com/login')
    if r.status_code != 200:
        fmt = '[fetch API token] Response has non-200 status: HTTP {} {}. Response content: "{}"'
        raise ValueError(fmt.format(r.status_code, r.reason, r.text))
    # https://stackoverflow.com/a/1732454
    match = re.search(r'"API_TOKEN":"([^"]+)"', r.text)
    if not match:
        raise ValueError('[fetch API token] Could not find API token in Tumblr response.')
    return match.group(1)


def tumblr_login(session: requests.Session, login: str, password: str) -> None:
    """Login and load those cookies into the Session."""
    api_token = get_api_token(session)

    headers = {
        'Authorization': 'Bearer {}'.format(api_token),
        'Origin': 'https://www.tumblr.com',
        'Referer': 'https://www.tumblr.com/login',
    }
    request_body = {
        'grant_type': 'password',
        'username': login,
        'password': password,
    }
    r = session.post('https://www.tumblr.com/api/v2/oauth2/token', headers=headers, json=request_body)
    if r.status_code != 200:
        # try to display the Tumblr-provided error, otherwise fallback on generic error print.
        try:
            respjson = r.json()
            err = respjson['error']
            err_desc = respjson['error_description']
            raise ValueError(f'[login] HTTP {r.status_code} {r.reason}: {err}. Reason: {err_desc}.')
        except (requests.JSONDecodeError, KeyError):
            fmt = '[login] Response has non-200 status: HTTP {} {}. Response content: "{}"'
            raise ValueError(fmt.format(r.status_code, r.reason, r.text))

    # We now have the necessary cookies loaded into our session.


def help():
    """ print help message """
    print(f'Usage: {Path(sys.argv[0]).name} [options] <cookiefile>\n'
          'positional arguments:\n'
          '    cookiefile: path to the file to save the login cookies in.\n'
          'options:\n'
          '    -h, --help: show this help message and exit\n')


def main():
    if '-h' in sys.argv[1:] or '--help' in sys.argv[1:]:
        help()
        return
    if len(sys.argv) == 1:
        print('Missing argument: cookiefile\n')
        help()
        return 1
    if len(sys.argv) > 2:
        print(f"Error: Expected 1 argument, got {len(sys.argv) - 1}.\n")
        help()
        return 1
    cookiefile, = sys.argv[1:]


    print('[login] Enter the credentials for your Tumblr account.')
    login = input('Email: ')
    password = getpass()
    # Note: email validation left up to Tumblr,
    # as it is not feasible to create a perfect RegEx for it (https://www.regular-expressions.info/email.html),
    # and in the end it only matters if Tumblr allows you to log in.
    if not login or not password:
        print("Missing email or password.")
        return 1

    # Create a requests session with cookies
    with requests.Session() as session:
        session.cookies = MozillaCookieJar(cookiefile)  # type: ignore[assignment]
        session.headers['User-Agent'] = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 '
            'Safari/537.36'
        )

        try:
            # Log into Tumblr
            tumblr_login(session, login, password)

            # Save the cookies to file
            try:
                session.cookies.save(ignore_discard=True)  # type: ignore[attr-defined]
            except OSError as e:
                print(f"Failed to save cookies to file.\nError: {e}")
                return 1
        except ValueError as e:  # only catch ValueError as those are expected. Don't print traceback.
            print(e)
            return 1

    print("[login] Login session cookies successfully saved to file.")
