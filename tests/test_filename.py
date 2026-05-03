import os

from tumblr_backup.filename import resolve_tumblr_basename, sanitize_filename


class TestResolveTumblrBasename:
    """resolve_tumblr_basename() contract: given a provisional basename, the final
    URL, and response headers, return the basename we should save the file as."""

    def test_non_tumblr_host_passthrough(self):
        # Off-domain URLs get no header-driven rewrite, even when headers would
        # otherwise apply. Scoping the rewrite to tumblr's CDN avoids stomping
        # on other providers (e.g. embedded soundcloud art).
        out = resolve_tumblr_basename(
            'original.pnj',
            'https://example.com/original.pnj',
            {'Content-Type': 'image/jpeg', 'Content-Disposition': 'attachment; filename="foo.png"'},
        )
        assert out == 'original.pnj'

    def test_content_type_fallback_when_cd_absent(self):
        out = resolve_tumblr_basename(
            'tumblr_abc.pnj',
            'https://64.media.tumblr.com/tumblr_abc.pnj',
            {'Content-Type': 'image/png'},
        )
        assert out == 'tumblr_abc.png'

    def test_cd_without_extension_falls_through_to_ct(self):
        # CD filename without an extension is useless for extension inference;
        # don't strip the provisional basename's suffix on its basis.
        out = resolve_tumblr_basename(
            'tumblr_abc.pnj',
            'https://64.media.tumblr.com/tumblr_abc.pnj',
            {'Content-Type': 'image/jpeg', 'Content-Disposition': 'attachment; filename="thing"'},
        )
        assert out == 'tumblr_abc.jpg'

    def test_unknown_content_type_preserves_basename(self):
        # Conservative fallback: if we can't map the mime to an extension and
        # CD didn't help, don't invent one.
        out = resolve_tumblr_basename(
            'tumblr_abc.pnj',
            'https://64.media.tumblr.com/tumblr_abc.pnj',
            {'Content-Type': 'image/x-exotic'},
        )
        assert out == 'tumblr_abc.pnj'

    def test_pnj_to_jpg(self):
        # The common tumblr-CDN case: .pnj in the URL is a JPEG on the wire,
        # and we want it saved as .jpg so downstream tools recognize it.
        out = resolve_tumblr_basename(
            'tumblr_abc.pnj',
            'https://64.media.tumblr.com/tumblr_abc.pnj',
            {'Content-Type': 'image/jpeg'},
        )
        assert out == 'tumblr_abc.jpg'

    def test_gifv_to_gif(self):
        out = resolve_tumblr_basename(
            'tumblr_abc.gifv',
            'https://64.media.tumblr.com/tumblr_abc.gifv',
            {'Content-Type': 'image/gif'},
        )
        assert out == 'tumblr_abc.gif'


class TestSanitizeFilename:
    """sanitize_filename() contract: unconditionally strip path separators;
    additionally strip Windows-reserved characters on Windows. The separator
    stripping is unconditional because / and \\ are never valid in a basename
    on any OS."""

    def test_strips_path_separators_everywhere(self):
        assert sanitize_filename('a/b\\c.jpg') == 'abc.jpg'

    def test_windows_strips_reserved_chars(self, monkeypatch):
        monkeypatch.setattr(os, 'name', 'nt')
        assert sanitize_filename('a:b<c>d"e|f*g?h.jpg') == 'abcdefgh.jpg'
