"""Allow running tumblr_backup as a module with `python -m tumblr_backup`."""
import sys

from tumblr_backup.main import main

if __name__ == '__main__':
    sys.argv[0] = 'tumblr-backup'
    sys.exit(main())
