import logging
import os
import pytz
from datetime import datetime
from typing import Dict, List

def get_timezone(timezone_str: str) -> str:
    return pytz.timezone(timezone_str).zone

def get_utc_now() -> datetime:
    return datetime.now(pytz.utc)

def get_timestamp(date_time: datetime) -> int:
    return int(date_time.timestamp())

def get_date_range(start: datetime, end: datetime) -> List[datetime]:
    date_range = []
    while start <= end:
        date_range.append(start)
        start += datetime.timedelta(days=1)
    return date_range

def get_config_value(config: Dict, key: str) -> str:
    return config.get(key, os.environ.get(key))

def setup_logging(config: Dict) -> None:
    log_level = config.get('log_level', 'INFO')
    logging.basicConfig(level=getattr(logging, log_level.upper()), format='%(asctime)s - %(levelname)s - %(message)s')