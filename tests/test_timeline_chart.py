"""Tests for timeline chart rendering functions."""

from datetime import date

from orgstats.core import _map_value_to_bar, render_timeline_chart


def test_map_value_to_bar_zero_max() -> None:
    """Test bar mapping when max value is zero."""
    assert _map_value_to_bar(0, 0) == " "
    assert _map_value_to_bar(5, 0) == " "


def test_map_value_to_bar_zero_value() -> None:
    """Test bar mapping when value is zero."""
    assert _map_value_to_bar(0, 100) == " "


def test_map_value_to_bar_100_percent() -> None:
    """Test bar mapping at 100%."""
    assert _map_value_to_bar(100, 100) == "█"
    assert _map_value_to_bar(10, 10) == "█"


def test_map_value_to_bar_thresholds() -> None:
    """Test bar character mapping at various percentage thresholds."""
    assert _map_value_to_bar(1, 100) == "▁"
    assert _map_value_to_bar(24, 100) == "▁"
    assert _map_value_to_bar(25, 100) == "▂"
    assert _map_value_to_bar(37, 100) == "▂"
    assert _map_value_to_bar(38, 100) == "▃"
    assert _map_value_to_bar(49, 100) == "▃"
    assert _map_value_to_bar(50, 100) == "▄"
    assert _map_value_to_bar(62, 100) == "▄"
    assert _map_value_to_bar(63, 100) == "▅"
    assert _map_value_to_bar(74, 100) == "▅"
    assert _map_value_to_bar(75, 100) == "▆"
    assert _map_value_to_bar(87, 100) == "▆"
    assert _map_value_to_bar(88, 100) == "▇"
    assert _map_value_to_bar(99, 100) == "▇"


def test_render_chart_all_zeros() -> None:
    """Test rendering chart with no activity."""
    timeline = {
        date(2023, 10, 22): 0,
        date(2023, 10, 23): 0,
        date(2023, 10, 24): 0,
    }
    chart_line, start_date, end_date = render_timeline_chart(
        timeline, date(2023, 10, 22), date(2023, 10, 24), 3
    )
    assert chart_line == "|   | 0"
    assert start_date == "2023-10-22"
    assert end_date == "2023-10-24"


def test_render_chart_all_equal() -> None:
    """Test rendering chart with equal activity on all days."""
    timeline = {
        date(2023, 10, 22): 5,
        date(2023, 10, 23): 5,
        date(2023, 10, 24): 5,
    }
    chart_line, start_date, end_date = render_timeline_chart(
        timeline, date(2023, 10, 22), date(2023, 10, 24), 3
    )
    assert chart_line == "|███| 5"
    assert start_date == "2023-10-22"
    assert end_date == "2023-10-24"


def test_render_chart_single_peak() -> None:
    """Test rendering chart with one bucket at 100%."""
    timeline = {
        date(2023, 10, 22): 1,
        date(2023, 10, 23): 10,
        date(2023, 10, 24): 1,
    }
    chart_line, start_date, end_date = render_timeline_chart(
        timeline, date(2023, 10, 22), date(2023, 10, 24), 3
    )
    assert "█" in chart_line
    assert "| 10" in chart_line


def test_render_chart_format() -> None:
    """Test chart format structure."""
    timeline = {date(2023, 10, 22): 5}
    chart_line, start_date, end_date = render_timeline_chart(
        timeline, date(2023, 10, 22), date(2023, 10, 22), 5
    )
    assert chart_line.startswith("|")
    assert chart_line.endswith("| 5")
    assert start_date == "2023-10-22"
    assert end_date == "2023-10-22"


def test_render_chart_width() -> None:
    """Test that chart width matches num_buckets."""
    timeline = {
        date(2023, 10, 22) + __import__("datetime").timedelta(days=i): i for i in range(100)
    }
    chart_line, _, _ = render_timeline_chart(
        timeline,
        date(2023, 10, 22),
        date(2023, 10, 22) + __import__("datetime").timedelta(days=99),
        50,
    )
    bars = chart_line.split("|")[1]
    assert len(bars) == 50


def test_render_chart_date_strings() -> None:
    """Test date formatting in output."""
    timeline = {date(2023, 1, 5): 1, date(2023, 12, 25): 1}
    chart_line, start_date, end_date = render_timeline_chart(
        timeline, date(2023, 1, 5), date(2023, 12, 25), 20
    )
    assert start_date == "2023-01-05"
    assert end_date == "2023-12-25"


def test_render_chart_with_gaps() -> None:
    """Test rendering chart with sparse activity."""
    timeline = {
        date(2023, 10, 22): 1,
        date(2023, 10, 26): 4,
    }
    chart_line, start_date, end_date = render_timeline_chart(
        timeline, date(2023, 10, 22), date(2023, 10, 26), 5
    )
    assert "|" in chart_line
    assert start_date == "2023-10-22"
    assert end_date == "2023-10-26"
    assert "| 4" in chart_line or "| 1" in chart_line


def test_render_chart_single_day() -> None:
    """Test rendering chart for a single day."""
    timeline = {date(2023, 10, 22): 7}
    chart_line, start_date, end_date = render_timeline_chart(
        timeline, date(2023, 10, 22), date(2023, 10, 22), 20
    )
    assert start_date == end_date
    assert "| 7" in chart_line


def test_render_chart_handles_missing_data() -> None:
    """Test rendering chart when timeline is missing some dates."""
    timeline = {
        date(2023, 10, 22): 5,
        date(2023, 10, 25): 3,
    }
    chart_line, start_date, end_date = render_timeline_chart(
        timeline, date(2023, 10, 22), date(2023, 10, 26), 5
    )
    assert start_date == "2023-10-22"
    assert end_date == "2023-10-26"
    assert "|" in chart_line


def test_render_chart_max_value_displayed() -> None:
    """Test that max value is correctly displayed in chart."""
    timeline = {
        date(2023, 10, 22): 10,
        date(2023, 10, 23): 20,
        date(2023, 10, 24): 30,
    }
    chart_line, _, _ = render_timeline_chart(timeline, date(2023, 10, 22), date(2023, 10, 24), 3)
    assert chart_line.endswith("| 30")
