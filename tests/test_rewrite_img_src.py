import pytest
from bs4 import BeautifulSoup

from tumblr_backup.main import _rewrite_img_src
from tumblr_backup.util import BS_PARSER


def _attrs(tag_html: str) -> dict[str, str]:
    """Parse a tag and return its attributes as a dict (order-independent compare)."""
    img = BeautifulSoup(tag_html, BS_PARSER).img
    assert img is not None
    return dict(img.attrs)


def test_rewrites_src():
    out = _rewrite_img_src('<img src="remote.jpg">', 'local.jpg')
    assert _attrs(out) == {'src': 'local.jpg'}


def test_strips_srcset():
    out = _rewrite_img_src(
        '<img src="remote.jpg" srcset="s1.jpg 1x, s2.jpg 2x">',
        'local.jpg',
    )
    assert _attrs(out) == {'src': 'local.jpg'}


def test_strips_sizes_paired_with_srcset():
    # Real-world shape from tumblr's output (see #14)
    tumblr_like = (
        '<img src="remote.jpg" data-orig-height="867" data-orig-width="794" '
        'srcset="s1.jpg 75w, s2.jpg 100w" sizes="(max-width: 794px) 100vw, 794px">'
    )
    out = _rewrite_img_src(tumblr_like, 'local.jpg')
    assert _attrs(out) == {
        'src': 'local.jpg',
        'data-orig-height': '867',
        'data-orig-width': '794',
    }


def test_strips_orphan_sizes():
    # Defensive: `sizes` without `srcset` is meaningless per spec
    out = _rewrite_img_src('<img src="a" sizes="100vw">', 'local.jpg')
    assert _attrs(out) == {'src': 'local.jpg'}


def test_rejects_non_img():
    with pytest.raises(ValueError, match='expected an <img> tag'):
        _rewrite_img_src('<div>not an img</div>', 'local.jpg')
