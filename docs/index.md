# tumblr-backup

[![Discord](https://img.shields.io/discord/1444409963920228484?label=Discord&logo=discord&logoColor=FFFFFF)](https://discord.gg/UtzGeYBNvQ)

tumblr-backup is a Python tool that backs up your [Tumblr](http://tumblr.com) blog locally as HTML files, preserving all your posts, images, and media. It creates a beautiful, browsable archive of your blog that you can view offline.

This is a fork of bbolli's [tumblr-utils](https://github.com/bbolli/tumblr-utils), with added Python 3 compatibility, bug fixes, support for dashboard-only blogs, and many other enhancements.

## Quick Start

### Step 1: Install Python (if you don't have it)

**Windows and macOS:** Download and install Python from [python.org](https://www.python.org/downloads/). During installation on Windows, **check the box that says "Add Python to PATH"** — this is important!

**Linux:** Python is usually already installed. You can check by opening a terminal and typing `python3 --version`.

### Step 2: Install tumblr-backup

Open a terminal. Then run the install command for your system:

<details>
<summary><b>Windows or macOS</b> (if you installed Python from python.org)</summary>

```console
pip install tumblr-backup
```

> **Tip:** If `pip` isn't recognized, try `python -m pip install tumblr-backup` instead.

</details>

<details>
<summary><b>Linux or Homebrew</b></summary>

On Linux (and macOS with Homebrew Python), the recommended way to install command-line tools is `pipx`, which manages them in isolated environments:

**Ubuntu/Debian:**
```console
sudo apt install pipx
pipx install tumblr-backup
```

**Fedora:**
```console
sudo dnf install pipx
pipx install tumblr-backup
```

**macOS (Homebrew):**
```console
brew install pipx
pipx install tumblr-backup
```

**Other distros / alternative method:** If your package manager doesn't have pipx, you can use [uv](https://docs.astral.sh/uv/), a fast Python tool installer:
```console
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install tumblr-backup
```

</details>

### Step 3: Get a Tumblr API key

1. Go to <https://www.tumblr.com/oauth/apps> (log in if needed)
2. Click **Register application**
3. Fill in any values for the required fields (the specific values don't matter)
4. Copy the **OAuth Consumer Key** shown on the next page

### Step 4: Save your API key

```console
tumblr-backup --set-api-key YOUR_API_KEY
```

Replace `YOUR_API_KEY` with the key you copied.

### Step 5: Back up a blog

```console
tumblr-backup blog-name
```

For example, to back up `staff.tumblr.com`:

```console
tumblr-backup staff
```

This will create a `staff/` directory in your current folder containing an `index.html` file you can open in your browser to view the backup, along with monthly archive pages, individual post pages, and all images and media.

### Updating an existing backup

To add only new posts to an existing backup:

```console
tumblr-backup -i blog-name
```

## Optional extras

tumblr-backup has optional features you can enable by installing extras. Add them in square brackets after the package name:

```console
pip install "tumblr-backup[video]"
```

(On Linux/Homebrew, replace `pip install` with `pipx install` or `uv tool install` as above.)

| Extra   | What it does |
|---------|-------------|
| `video` | Save video files (uses yt-dlp) |
| `exif`  | Add post tags to image EXIF metadata |
| `jq`    | Filter posts with custom rules |
| `dash`  | Back up dashboard-only blogs |
| `all`   | All of the above |

See the [Installation Guide](installation.md) for detailed instructions on each extra, including platform-specific notes.

## Support & Community

If you get stuck, have questions, or want to request features, join the Discord:

<iframe src="https://discord.com/widget?id=1444409963920228484&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
