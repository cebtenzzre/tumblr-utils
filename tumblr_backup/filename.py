"""Filename sanitization + header-based basename resolution for Tumblr CDN media.

`sanitize_filename` strips characters disallowed in basenames.
`resolve_tumblr_basename` turns a provisional URL-derived filename into the
real filename using Content-Disposition / Content-Type response headers.
"""
import os
import re
from collections.abc import Mapping
from email.message import EmailMessage
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Final
from urllib.parse import urlparse

__all__ = [
    'resolve_tumblr_basename',
    'sanitize_filename',
]


def sanitize_filename(fname: str) -> str:
    """Remove path separators and (on Windows) other illegal filename characters."""
    fname = fname.replace('/', '').replace('\\', '')
    if os.name == 'nt':
        fname = re.sub(r'[:<>"|*?]', '', fname)
    return fname


_CONTENT_TYPE_TO_EXT: Final = MappingProxyType({
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'image/webp': '.webp',
    'image/bmp': '.bmp',
})


def _parse_cd_filename(header: str) -> str | None:
    """Extract the filename from a Content-Disposition header via stdlib
    EmailMessage (which handles RFC 5987/6266, both plain `filename="…"` and
    extended `filename*=UTF-8''…` forms). Returns None for missing, malformed,
    or filename-less headers."""
    msg = EmailMessage()
    msg['Content-Disposition'] = header
    return msg.get_filename()


def resolve_tumblr_basename(old_basename: str, final_url: str, headers: Mapping[str, str]) -> str:
    """Resolve the correct basename for Tumblr CDN media from response headers.

    Scoped to *.media.tumblr.com URLs; returns ``old_basename`` unchanged for
    any other host. Within that scope, prefers ``Content-Disposition``'s
    filename extension, falls back to a ``Content-Type`` lookup, and ultimately
    returns ``old_basename`` unchanged if neither yields a usable extension.
    The stem of ``old_basename`` is preserved; only the suffix changes.
    """
    parsed = urlparse(final_url)
    if not (parsed.hostname and parsed.hostname.endswith('.media.tumblr.com')):
        return old_basename

    name = PurePosixPath(old_basename)

    cd_filename = _parse_cd_filename(headers.get('Content-Disposition', ''))
    if cd_filename:
        cd_ext = PurePosixPath(cd_filename).suffix
        if cd_ext:
            return sanitize_filename(name.with_suffix(cd_ext).name)

    ct = headers.get('Content-Type', '')
    mime = ct.split(';', 1)[0].strip().lower()
    ct_ext = _CONTENT_TYPE_TO_EXT.get(mime)
    if ct_ext:
        return sanitize_filename(name.with_suffix(ct_ext).name)

    return old_basename
