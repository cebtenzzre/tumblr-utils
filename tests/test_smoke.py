"""Smoke test: the package and its two biggest modules import cleanly."""


def test_import_package() -> None:
    import tumblr_backup  # noqa: F401


def test_import_main() -> None:
    import tumblr_backup.main  # noqa: F401


def test_import_wget() -> None:
    import tumblr_backup.wget  # noqa: F401
