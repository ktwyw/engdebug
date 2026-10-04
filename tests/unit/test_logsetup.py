import io
import json
import logging

from engdebug import logsetup


def test_json_formatter_emits_one_object_per_line():
    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.setFormatter(logsetup.JsonFormatter(run_id="day1"))
    log = logging.getLogger("engdebug.test_json")
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    try:
        log.info("loaded %d records", 3)
        try:
            raise ValueError("boom")
        except ValueError:
            log.exception("failed")
    finally:
        log.removeHandler(handler)
    lines = [json.loads(line) for line in buf.getvalue().strip().splitlines()]
    assert lines[0]["message"] == "loaded 3 records" and lines[0]["run_id"] == "day1" and lines[0]["level"] == "INFO"
    assert "ValueError: boom" in lines[1]["exception"]
