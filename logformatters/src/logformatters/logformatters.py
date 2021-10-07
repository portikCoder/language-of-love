import logging
from datetime import datetime

import pytz as pytz
from tzlocal import get_localzone
from typing import Optional


class LogFormatterIsoStandard(logging.Formatter):
    # override the converter in logging.Formatter
    converter = datetime.fromtimestamp

    # override formatTime in logging.Formatter
    def formatTime(self, record, datefmt=None, timezone="UTC"):
        return self.converter(record.created, tz=pytz.timezone(timezone)).isoformat()


class LogFormatterCustom(logging.Formatter):
    # override the converter in logging.Formatter
    converter = datetime.fromtimestamp

    DEBUG_FMT = "%(asctime)s | %(filename)s:%(lineno)s | [%(levelname)s]:%(message)s"

    # override formatTime in logging.Formatter
    def __init__(self, fmt: Optional[str] = ...):
        super().__init__(fmt)

    def format(self, record: logging.LogRecord) -> str:
        original_fmt = self._fmt
        if record.levelno == logging.DEBUG:
            self._fmt = LogFormatterCustom.DEBUG_FMT
        original_style = self._style
        self._style = logging.PercentStyle(self._fmt)
        result_fmt = logging.Formatter.format(self, record)
        self._fmt = original_fmt
        self._style = original_style
        return result_fmt

    def formatTime(self, record, datefmt=None, timezone="UTC"):
        return datetime.fromtimestamp(record.created, get_localzone())
