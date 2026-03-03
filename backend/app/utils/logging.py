import logging
import json
from typing import Any


def setup_structured_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure root logger to output one-line JSON logs to stdout."""
    handler = logging.StreamHandler()
    handler.setLevel(level)

    class JSONFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            # If message is already a dict/json-like string, try to preserve
            msg = record.getMessage()
            try:
                # If msg is JSON string, keep it
                json.loads(msg)
                message = msg
            except Exception:
                # build structured payload
                payload = {
                    "ts": self.formatTime(record, self.datefmt),
                    "level": record.levelname,
                    "logger": record.name,
                    "msg": msg,
                }
                # include extras if present
                for k, v in getattr(record, "extra", {}).items():
                    payload[k] = v
                message = json.dumps(payload, ensure_ascii=False)
            return message

    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    # remove existing handlers
    for h in list(root.handlers):
        root.removeHandler(h)
    root.addHandler(handler)
    root.setLevel(level)
    return root


def js(logger: logging.Logger, level: int = logging.INFO, **kwargs: Any) -> None:
    """Log a JSON object with the provided kwargs at the given level."""
    try:
        payload = {k: (v if not isinstance(v, str) else v) for k, v in kwargs.items()}
        logger.log(level, json.dumps(payload, ensure_ascii=False))
    except Exception:
        logger.log(level, json.dumps({"msg": str(kwargs)}))
