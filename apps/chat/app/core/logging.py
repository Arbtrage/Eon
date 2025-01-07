import logging
from typing import Any
import json
from datetime import datetime


class CustomJSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if hasattr(record, "props"):
            log_record.update(record.props)
        return json.dumps(log_record)


def setup_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    json_handler = logging.StreamHandler()
    json_handler.setFormatter(CustomJSONFormatter())
    logger.addHandler(json_handler)
