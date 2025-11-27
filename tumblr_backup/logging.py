import sys
import threading
from enum import Enum
from functools import total_ordering
from typing import TextIO


@total_ordering
class LogLevel(Enum):
    INFO = 0
    WARN = 1
    ERROR = 2

    def __lt__(self, other: object) -> bool:
        if isinstance(other, LogLevel):
            return self.value < other.value
        return NotImplemented


class Logger:
    _quiet: bool
    _file: TextIO
    _lock: threading.Lock
    _backup_account: str | None
    _status_msg: str | None

    def __init__(self, quiet: bool = False, file: TextIO = sys.stdout) -> None:
        self._quiet = quiet
        self._file = file
        self._lock = threading.Lock()
        self._backup_account = None
        self._status_msg = None

    def log(self, level: LogLevel, msg: str, account: bool = False) -> None:
        if self._quiet and level < LogLevel.WARN:
            return
        with self._lock:
            for line in msg.splitlines(True):
                self._print(line, account)
            if self._status_msg:
                self._print(self._status_msg, account=True)
            sys.stdout.flush()

    def info(self, msg: str, account: bool = False) -> None:
        self.log(LogLevel.INFO, msg, account)

    def warn(self, msg: str, account: bool = False) -> None:
        self.log(LogLevel.WARN, msg, account)

    def error(self, msg: str, account: bool = False) -> None:
        self.log(LogLevel.ERROR, msg, account)

    def status(self, msg: str | None) -> None:
        self._status_msg = msg
        self.log(LogLevel.INFO, '')

    def set_quiet(self, quiet: bool) -> None:
        self._quiet = quiet

    def set_file(self, file: TextIO) -> None:
        self._file = file

    def set_backup_account(self, account: str | None) -> None:
        self._backup_account = account

    def _print(self, msg: str, account: bool = False) -> None:
        if account:  # Optional account prefix
            msg = '{}: {}'.format(self._backup_account, msg)

        # Separate terminator
        it = (i for i, c in enumerate(reversed(msg)) if c not in '\r\n')
        try:
            idx = len(msg) - next(it)
        except StopIteration:
            idx = 0
        msg, term = msg[:idx], msg[idx:]

        pad = ' ' * (80 - len(msg))  # Pad to 80 chars
        print(msg + pad + term, end='', file=self._file)


logger: Logger = Logger()
