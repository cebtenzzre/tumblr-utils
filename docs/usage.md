# Usage Guide

## Synopsis

```
tumblr-backup [options] blog-name ...
```

## Options

```
positional arguments:
  blogs

options:
  -h, --help            show this help message and exit
  -O OUTDIR, --outdir OUTDIR
                        set the output directory (default: blog-name)
  -D, --dirs            save each post in its own folder
  -q, --quiet           suppress progress messages
  -i, --incremental     incremental backup mode
  -l, --likes           save a blog's likes, not its posts
  -k, --skip-images     do not save images; link to Tumblr instead
  --save-video          save all video files
  --save-video-tumblr   save only Tumblr video files
  --save-audio          save audio files
  --save-notes          save a list of notes for each post
  --copy-notes          copy the notes list from a previous archive (inverse:
                        --no-copy-notes)
  --notes-limit COUNT   limit requested notes to COUNT, per-post
  --cookiefile COOKIEFILE
                        cookie file for youtube-dl, --save-notes, and dashboard-only blogs
  -j, --json            save the original JSON source
  -b, --blosxom         save the posts in blosxom format
  -r, --reverse-month   reverse the post order in the monthly archives
  -R, --reverse-index   reverse the index file order
  --tag-index           also create an archive per tag
  -a HOUR, --auto HOUR  do a full backup at HOUR hours, otherwise do an
                        incremental backup (useful for cron jobs)
  -n COUNT, --count COUNT
                        save only COUNT posts
  -s SKIP, --skip SKIP  skip the first SKIP posts
  -p PERIOD, --period PERIOD
                        limit the backup to PERIOD ('y', 'm', 'd',
                        YYYY[MM[DD]][Z], or START,END)
  -N COUNT, --posts-per-page COUNT
                        set the number of posts per monthly page, 0 for
                        unlimited
  -Q REQUEST, --request REQUEST
                        save posts matching the request
                        TYPE:TAG:TAG:…,TYPE:TAG:…,…. TYPE can be text, quote,
                        link, answer, video, audio, photo, chat or any; TAGs
                        can be omitted or a colon-separated list. Example: -Q
                        any:personal,quote,photo:me:self
  -t REQUEST, --tags REQUEST
                        save only posts tagged TAGS (comma-separated values;
                        case-insensitive)
  -T REQUEST, --type REQUEST
                        save only posts of type TYPE (comma-separated values
                        from text, quote, link, answer, video, audio, photo,
                        chat)
  -F FILTER, --filter FILTER
                        save posts matching a jq filter (needs jq module)
  --no-reblog           don't save reblogged posts
  --only-reblog         save only reblogged posts
  -I FMT, --image-names FMT
                        image filename format ('o'=original, 'i'=<post-id>,
                        'bi'=<blog-name>_<post-id>)
  -e KW, --exif KW      add EXIF keyword tags to each picture (comma-separated
                        values; '-' to remove all tags, '' to add no extra
                        tags)
  -S, --no-ssl-verify   ignore SSL verification errors
  --prev-archives DIRS  comma-separated list of directories (one per blog)
                        containing previous blog archives
  --no-post-clobber     Do not re-download existing posts
  --no-server-timestamps
                        don't set local timestamps from HTTP headers
  --hostdirs            Generate host-prefixed directories for media
  --user-agent USER_AGENT
                        User agent string to use with HTTP requests
  --skip-dns-check      Skip DNS checks for internet access
  --threads THREADS     number of threads to use for post retrieval
  --continue            Continue an incomplete first backup
  --ignore-diffopt      Force backup over an incomplete archive with different
                        options
  --no-get              Don't retrieve files not found in --prev-archives
  --reuse-json          Reuse the API responses saved with --json (implies
                        --copy-notes)
  --internet-archive    Fall back to the Internet Archive for Tumblr media 403
                        and 404 responses
  --media-list          Save post media URLs to media.json
  --id-file FILE        file containing a list of post IDs to save, one per
                        line
  --json-info           Just print some info for each blog, don't make a
                        backup
```

## Arguments

_blog-name_: The name of the blog to backup.

If your blog is under `.tumblr.com`, you can give just the first domain name
part; if your blog is under your own domain, give the whole domain name. You
can give more than one _blog-name_ to backup multiple blogs in one go.

The default blog name(s) can be changed by copying `settings.py.example` to
`settings.py` and adding the name(s) to the `DEFAULT_BLOGS` list.

## Environment variables

`LC_ALL`, `LC_TIME`, `LANG`: These variables, in decreasing importance,
determine the locale for month names and the date/time format.

## Exit code

The exit code is 0 if at least one post has been backed up, 1 if no post has
been backed up, 2 on invocation errors, 3 if the backup was interrupted, or 4
on HTTP errors.
