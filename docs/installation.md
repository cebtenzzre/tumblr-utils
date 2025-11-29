# Installation Guide

## Basic Installation

1. Install the latest Python 3.
2. Run `pip install tumblr-backup` from a command line.
3. Create an "app" at <https://www.tumblr.com/oauth/apps>. Follow the instructions
   there; most values entered don't matter.
4. Run `tumblr-backup --set-api-key API_KEY`, where API\_KEY is the OAuth Consumer
   Token from the app created in the previous step.
5. Run `tumblr-backup blog-name` as often as you like manually or from a cron
   job.

## Optional Extras

There are several optional extras that enable additional features:

1. The `video` extra enables the `--save-video` and `--save-video-tumblr` options, which
   download videos using yt-dlp. If you need HTTP cookies to download, use an appropriate
   browser plugin to extract the cookie(s) into a file and use option `--cookiefile=file`.
   See [issue 132].
2. The `exif` extra enables the `--exif` option, which adds post tags to the EXIF metadata
   of JPEG files. This pulls in the `py3exiv2` module which may have additional
   prerequites depending on your platform. See the below section on installing py3exiv2.
3. The `bs4` extra enables the `--save-notes` option, which saves the list of accounts
   that reblogged or liked a public post.
4. The `jq` extra enables the `--filter` option to filter the downloaded posts with arbitrary
   rules based on their metadata.
5. The `dashboard` extra enables backing up dashboard-only blogs by installing `quickjs` for
   fast NPF (Neue Post Format) rendering. This is required for dashboard-only blogs. It pulls in `quickjs` by default.
   `miniracer` is also supported, in case the `quickjs` package is not available - but it must be installed manually to
   use it as a fallback (`pip install mini-racer`).
6. The `all` extra includes all of the above features.

To install one or more extras, put them in square brackets after the package name in the
pip command. Multiple extras may be separated by commas. Make sure to quote the command
properly, as square brackets have a special meaning in many environments when not quoted.

For example:

```console
pip install 'tumblr-backup[video,bs4]'
```

[issue 132]: (https://github.com/bbolli/tumblr-utils/issues/132)

## Notes About py3exiv2

`py3exiv2` is not a pure Python package, and requires OS-specific dependencies. If you
would like to install the `exif` or `all` extras, you may need to install additional
dependencies for the `pip install` command to succeed.

For example, on macOS, these steps successfully install the `exif` extra (requires [Homebrew]):

```console
brew install boost-python3 exiv2
export CPATH=/opt/homebrew/include
export LIBRARY_PATH=/opt/homebrew/lib
pip install 'tumblr-backup[exif]'
```

[Homebrew]: https://brew.sh/
