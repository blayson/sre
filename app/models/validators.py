from datetime import datetime, timezone


def normalize(name: str) -> str:
    return ' '.join((word.capitalize()) for word in name.split(' '))


def not_empty(val: str) -> str:
    assert val != '', 'Empty strings are not allowed'
    return val


def set_ts_now(val: datetime) -> datetime:
    return val or datetime.now(timezone.utc)
