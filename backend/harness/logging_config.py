import json
import logging


logger = logging.getLogger("healthbrief")

logger.setLevel(logging.INFO)


if not logger.handlers:

    handler = logging.StreamHandler()

    logger.addHandler(handler)


def log_event(
    event: str,
    request_id: str,
    **fields
):
    

    log_data = {
        "event": event,
        "request_id": request_id,
        **fields
    }

    logger.info(
        json.dumps(
            log_data,
            ensure_ascii=False
        )
    )