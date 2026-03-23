# Installation Guide

## Basic Installation

1. Install the latest Python 3.
2. Run `pipx install tumblr-backup` from a command line.
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
5. The `dash` extra enables backing up [dashboard-only blogs](#dashboard-only-blogs).
6. The `all` extra includes all of the above features.

To install one or more extras, put them in square brackets after the package name in the
install command. Multiple extras may be separated by commas. Make sure to quote the command
properly, as square brackets have a special meaning in many environments when not quoted.

For example:

```console
pipx install 'tumblr-backup[video,bs4]'
```

[issue 132]: (https://github.com/bbolli/tumblr-utils/issues/132)

## Dashboard-only blogs

Some Tumblr blogs don't have a public page — they only post to the dashboard. To back
up these blogs, you need the `dash` extra:

```console
pip install "tumblr-backup[dash]"
```

(On Linux/Homebrew, replace `pip install` with `pipx install` or `uv tool install`.)

You will also need to provide a cookie file so tumblr-backup can access the dashboard.
See the `--cookiefile` option in the [Usage Guide](usage.md) for details.

### Getting an error about "Failed building wheel for quickjs"?

This is a known issue on **Python 3.13 and newer**. The `quickjs` package that
tumblr-backup normally uses doesn't support Python 3.13+ yet, and this error is
most common on **Windows** where the tools needed to build it from scratch aren't
usually installed.

You can use `mini-racer` instead — it works the same way and is easier to install.
tumblr-backup will automatically pick it up.

If you installed with **pip**:

```console
pip install mini-racer
```

If you installed with **pipx**:

```console
pipx inject tumblr-backup mini-racer
```

After that, try your backup command again — it should work now.

## Notes About py3exiv2

`py3exiv2` is not a pure Python package, and requires OS-specific dependencies. If you
would like to install the `exif` or `all` extras, you may need to install additional
dependencies for the install command to succeed.

For example, on macOS, these steps successfully install the `exif` extra (requires [Homebrew]):

```console
brew install boost-python3 exiv2
export CPATH=/opt/homebrew/include
export LIBRARY_PATH=/opt/homebrew/lib
pipx install 'tumblr-backup[exif]'
```

[Homebrew]: https://brew.sh/
