# tumblr-backup

[![Discord](https://img.shields.io/discord/1444409963920228484?label=Discord&logo=discord&logoColor=FFFFFF)](https://discord.gg/UtzGeYBNvQ)

tumblr-backup is a Python tool that backs up your [Tumblr](http://tumblr.com) blog locally as HTML files, preserving all your posts, images, and media. It creates a beautiful, browsable archive of your blog that you can view offline.

This is a fork of bbolli's [tumblr-utils](https://github.com/bbolli/tumblr-utils), with added Python 3 compatibility, bug fixes, support for dashboard-only blogs, and many other enhancements.

## Quick Start

### Installation

1. Install with pip:

   ```bash
   pip install tumblr-backup
   ```

2. Create a Tumblr app at <https://www.tumblr.com/oauth/apps> to get an API key

3. Set your API key:

   ```bash
   tumblr-backup --set-api-key YOUR_API_KEY
   ```

### Backup a Blog

To backup a blog, simply run:

```bash
tumblr-backup blog-name
```

For example, to backup `staff.tumblr.com`:

```bash
tumblr-backup staff
```

This will create a `staff/` directory containing:

- An `index.html` file with links to all posts
- Monthly archive pages
- Individual post pages
- All images and media from the blog

### Incremental Backups

To update an existing backup with only new posts:

```bash
tumblr-backup -i blog-name
```

## Advanced Features

tumblr-backup supports many advanced features like:

- Backing up videos and audio files
- Saving post notes (likes/reblogs)
- Filtering posts by tag or type
- Dashboard-only blog support
- And much more!

See the [detailed documentation](docs/) for all options and features.

## Documentation

- **[Installation Guide](docs/installation.md)** - Detailed installation instructions including optional features
- **[Usage Guide](docs/usage.md)** - Complete list of options and command-line arguments
- **[Operation Guide](docs/operation.md)** - How tumblr-backup works under the hood

## Support & Community

Join our Discord community to:

- Get help and support
- Ask questions
- Request new features
- Get notified about new releases
- Share your feedback

**[Join the Discord server →](https://discord.gg/UtzGeYBNvQ)**

## Third-party Components

This project redistributes **npf2html** (MIT) from <https://github.com/nex3/npf2html> at commit `05d602a`.

- Upstream license: see `3rdparty/npf2html/LICENSE`.
- Source used to produce the bundled JS: `3rdparty/npf2html/` with build steps in `3rdparty/README.md`.

## Acknowledgments

- [bdoms](https://github.com/bdoms/tumblr_backup) for the initial implementation
- [WyohKnott](https://github.com/WyohKnott) for numerous bug reports and patches
- [Tumblr](https://www.tumblr.com) for their discontinued backup tool whose
  output was the inspiration for the styling applied in `tumblr_backup`.
- [Beat Bolli](https://github.com/bbolli/tumblr-utils)
