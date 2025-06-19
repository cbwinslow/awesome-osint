from pathlib import Path
from datetime import datetime

API_LOG = Path('api_keys.log')


def log_api_key(service: str, api_key: str) -> None:
    timestamp = datetime.utcnow().isoformat()
    with API_LOG.open('a') as f:
        f.write(f"{timestamp} {service}: {api_key}\n")
