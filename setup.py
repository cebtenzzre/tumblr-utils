"""Setuptools shim: rewrites relative markdown links in README.md to absolute
GitHub URLs so they work on PyPI."""

import re
from pathlib import Path

from setuptools import setup

REPO_URL = 'https://github.com/cebtenzzre/tumblr-utils/blob/master'

long_description = Path('README.md').read_text()
long_description = re.sub(
    r'(\[[^\]]+\]\()(?!https?://|#|mailto:)([^)]+\))',
    rf'\1{REPO_URL}/\2',
    long_description,
)

setup(long_description=long_description, long_description_content_type='text/markdown')
