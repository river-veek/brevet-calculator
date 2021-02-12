import nose
import arrow
from acp_times import open_time, close_time


def test_open():
    start1 = arrow.get('2020-01-01T00:00:00+00:00')
    open1 = arrow.get('2020-01-01T01:46:00+00:00')
    open2 = arrow.get('2020-01-01T05:53:00+00:00')
    open3 = arrow.get('2020-01-01T10:34:00+00:00')
    open4 = arrow.get('2020-01-01T17:08:00+00:00')
    open5 = arrow.get('2020-01-01T05:53:00+00:00')
    open6 = arrow.get('2020-01-02T05:31:00+00:00')
    assert open_time(0, 200, start1) == start1
    assert open_time(60, 200, start1) == open1
    assert open_time(200, 200, start1) == open2
    assert open_time(350, 400, start1) == open3
    assert open_time(550, 600, start1) == open4
    assert open_time(240, 200, start1) == open5
    assert open_time(900, 1000, start1) == open6

def test_close():
    start1 = arrow.get('2020-01-01T00:00:00+00:00')
    end1 = arrow.get('2020-01-01T04:00:00+00:00')
    end2 = arrow.get('2020-01-01T08:00:00+00:00')
    end3 = arrow.get('2020-01-01T11:40:00+00:00')
    end4 = arrow.get('2020-01-02T16:00:00+00:00')
    end5 = arrow.get('2020-01-03T17:23:00+00:00')
    end6 = arrow.get('2020-01-01T13:30:00+00:00')
    assert close_time(60, 200, start1) == end1
    assert close_time(120, 200, start1) == end2
    assert close_time(175, 200, start1) == end3
    assert close_time(600, 600, start1) == end4
    assert close_time(890, 1000, start1) == end5
    assert close_time(200, 200, start1) == end6
    assert close_time(241, 200, start1) == -1  # may have to deal with this is HTML
    


# workaround instead of dealing with Docker (python3 test_acp_times.py)
# test_open()
# test_close()
