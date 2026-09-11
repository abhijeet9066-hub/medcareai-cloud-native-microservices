import json
import logging
import os
import time
try:
    import redis
except ImportError:
    redis = None

logging.basicConfig(level=logging.INFO, format="%(message)s")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
STREAM = "medcareai.audit"
GROUP = "audit-workers"
CONSUMER = os.getenv("HOSTNAME", "audit-worker")


def main():
    if redis is None:
        raise RuntimeError("redis package required")
    client = redis.from_url(REDIS_URL)
    try:
        client.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
    except Exception:
        pass
    while True:
        messages = client.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=10, block=5000)
        for _, entries in messages:
            for message_id, fields in entries:
                payload = fields.get(b"payload", b"{}").decode()
                logging.info(json.dumps({"audit_message_id": message_id.decode(), "payload": json.loads(payload)}))
                client.xack(STREAM, GROUP, message_id)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
