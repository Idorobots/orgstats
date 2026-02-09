"""Tests for gamify_exp parsing."""

from orgstats.core import gamify_exp, parse_gamify_exp


class MockEmptyTimestamp:
    """Mock empty timestamp (mimics orgparse behavior when no timestamp)."""

    def __init__(self):
        self.start = None

    def __bool__(self):
        return False


class MockNode:
    """Mock node object for testing analyze()."""

    def __init__(  # noqa: PLR0913
        self,
        todo="TODO",
        tags=None,
        heading="",
        body="",
        repeated_tasks=None,
        properties=None,
        closed=None,
        scheduled=None,
        deadline=None,
    ):
        self.todo = todo
        self.tags = tags if tags is not None else []
        self.heading = heading
        self.body = body
        self.repeated_tasks = repeated_tasks if repeated_tasks is not None else []
        self.properties = properties if properties is not None else {}
        self.closed = closed if closed is not None else MockEmptyTimestamp()
        self.scheduled = scheduled if scheduled is not None else MockEmptyTimestamp()
        self.deadline = deadline if deadline is not None else MockEmptyTimestamp()


class MockRepeatedTask:
    """Mock repeated task for testing."""

    def __init__(self, after="TODO", start=None):
        self.after = after
        self.start = start


def test_parse_gamify_exp_integer():
    """Test parsing integer gamify_exp values."""
    assert parse_gamify_exp("5") == 5
    assert parse_gamify_exp("10") == 10
    assert parse_gamify_exp("20") == 20
    assert parse_gamify_exp("25") == 25
    assert parse_gamify_exp("100") == 100


def test_parse_gamify_exp_tuple_format():
    """Test parsing (X Y) tuple format."""
    assert parse_gamify_exp("(5 10)") == 5
    assert parse_gamify_exp("(25 30)") == 25
    assert parse_gamify_exp("(15 20)") == 15
    assert parse_gamify_exp("(100 200)") == 100


def test_parse_gamify_exp_tuple_with_whitespace():
    """Test parsing (X Y) format with various whitespace."""
    assert parse_gamify_exp("( 5 10 )") == 5
    assert parse_gamify_exp("(  15   20  )") == 15
    assert parse_gamify_exp("(25  30)") == 25


def test_parse_gamify_exp_none():
    """Test parsing None returns None."""
    assert parse_gamify_exp(None) is None


def test_parse_gamify_exp_empty_string():
    """Test parsing empty string returns None."""
    assert parse_gamify_exp("") is None
    assert parse_gamify_exp("   ") is None


def test_parse_gamify_exp_invalid_format():
    """Test parsing invalid formats returns None."""
    assert parse_gamify_exp("invalid") is None
    assert parse_gamify_exp("abc") is None
    assert parse_gamify_exp("not a number") is None


def test_parse_gamify_exp_invalid_tuple():
    """Test parsing invalid tuple format returns None."""
    assert parse_gamify_exp("(abc 10)") is None
    assert parse_gamify_exp("(abc def)") is None
    assert parse_gamify_exp("(10)") is None
    assert parse_gamify_exp("()") is None


def test_parse_gamify_exp_tuple_with_invalid_second():
    """Test that (X Y) format extracts X even if Y is invalid."""
    assert parse_gamify_exp("(10 abc)") == 10
    assert parse_gamify_exp("(15 invalid)") == 15


def test_parse_gamify_exp_with_extra_spaces():
    """Test parsing values with leading/trailing spaces."""
    assert parse_gamify_exp("  5  ") == 5
    assert parse_gamify_exp("  15  ") == 15


def test_gamify_exp_with_integer():
    """Test gamify_exp() extracts integer values."""
    node = MockNode(properties={"gamify_exp": "15"})
    assert gamify_exp(node) == 15


def test_gamify_exp_with_none():
    """Test gamify_exp() returns None when property missing."""
    node = MockNode(properties={})
    assert gamify_exp(node) is None


def test_gamify_exp_with_tuple():
    """Test gamify_exp() extracts from tuple format."""
    node = MockNode(properties={"gamify_exp": "(20 25)"})
    assert gamify_exp(node) == 20


def test_gamify_exp_with_invalid():
    """Test gamify_exp() returns None for invalid values."""
    node = MockNode(properties={"gamify_exp": "invalid"})
    assert gamify_exp(node) is None


def test_gamify_exp_with_empty_string():
    """Test gamify_exp() returns None for empty string."""
    node = MockNode(properties={"gamify_exp": ""})
    assert gamify_exp(node) is None


def test_gamify_exp_with_various_values():
    """Test gamify_exp() with various integer values."""
    assert gamify_exp(MockNode(properties={"gamify_exp": "5"})) == 5
    assert gamify_exp(MockNode(properties={"gamify_exp": "10"})) == 10
    assert gamify_exp(MockNode(properties={"gamify_exp": "20"})) == 20
    assert gamify_exp(MockNode(properties={"gamify_exp": "100"})) == 100


def test_gamify_exp_with_tuple_formats():
    """Test gamify_exp() with various tuple formats."""
    assert gamify_exp(MockNode(properties={"gamify_exp": "(5 10)"})) == 5
    assert gamify_exp(MockNode(properties={"gamify_exp": "(25 30)"})) == 25
    assert gamify_exp(MockNode(properties={"gamify_exp": "( 15 20 )"})) == 15
