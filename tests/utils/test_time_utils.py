from utils.time_utils import unix_to_utc_datetime


def test_unix_to_utc_datetime():
    dt = unix_to_utc_datetime(0)
    assert dt.year == 1970
