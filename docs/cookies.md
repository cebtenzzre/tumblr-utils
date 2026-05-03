# Getting Cookies

Some features — like backing up [dashboard-only blogs](installation.md#dashboard-only-blogs),
downloading videos, and saving notes — require you to be logged in to Tumblr. tumblr-backup
uses a cookie file to access your Tumblr session.

There are two ways to get a cookie file:

## Option 1: Use `tb-login` (recommended)

`tb-login` is a command that comes with tumblr-backup. It logs in to Tumblr and saves
your cookies to a file.

Run it with the name of the file you want to save cookies to:

```console
tb-login cookies.txt
```

It will ask for your Tumblr email and password. Once you've logged in, use the cookie
file with `--cookiefile`:

```console
tumblr-backup --cookiefile cookies.txt blog-name
```

If your cookies expire (you'll see login-related errors), just run `tb-login cookies.txt`
again to refresh them.

!!! note
    Authentication via `Continue with Google` or `Continue with Apple` is not supported.\
    Continue with [Option 2](#option-2-export-cookies-from-your-browser) to still get the correct cookies.

## Option 2: Export cookies from your browser

If you'd rather not enter your password in the terminal, you can export cookies from a
browser where you're already logged in to Tumblr.

1. Install a cookies.txt browser extension:
    - **Chrome:** [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
    - **Firefox:** [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)
2. Go to [tumblr.com](https://www.tumblr.com) and make sure you're logged in.
3. Click the extension icon and export/save the cookies to a file (e.g. `cookies.txt`).
4. Use the file with `--cookiefile`:

```console
tumblr-backup --cookiefile cookies.txt blog-name
```

!!! note
    Browser cookies expire over time. If your backup starts failing with login errors,
    export a fresh cookie file from your browser.
