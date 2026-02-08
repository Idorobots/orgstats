"""Tests for the compute_frequencies() function."""

from orgstats.core import Frequency, compute_frequencies


def test_compute_frequencies_empty_items():
    """Test with empty set creates no entries."""
    items = set()
    frequencies = {}

    compute_frequencies(items, frequencies, 1, "regular")

    assert frequencies == {}


def test_compute_frequencies_single_item():
    """Test single item creates Frequency with correct counts."""
    items = {"python"}
    frequencies = {}

    compute_frequencies(items, frequencies, 1, "regular")

    assert "python" in frequencies
    assert frequencies["python"].total == 1
    assert frequencies["python"].regular == 1
    assert frequencies["python"].simple == 0
    assert frequencies["python"].hard == 0


def test_compute_frequencies_multiple_items():
    """Test multiple items all get incremented."""
    items = {"python", "testing", "debugging"}
    frequencies = {}

    compute_frequencies(items, frequencies, 1, "regular")

    assert len(frequencies) == 3
    assert "python" in frequencies
    assert "testing" in frequencies
    assert "debugging" in frequencies
    assert frequencies["python"].total == 1
    assert frequencies["testing"].total == 1
    assert frequencies["debugging"].total == 1


def test_compute_frequencies_simple_difficulty():
    """Test that simple difficulty increments simple field."""
    items = {"python"}
    frequencies = {}

    compute_frequencies(items, frequencies, 1, "simple")

    assert frequencies["python"].total == 1
    assert frequencies["python"].simple == 1
    assert frequencies["python"].regular == 0
    assert frequencies["python"].hard == 0


def test_compute_frequencies_regular_difficulty():
    """Test that regular difficulty increments regular field."""
    items = {"python"}
    frequencies = {}

    compute_frequencies(items, frequencies, 1, "regular")

    assert frequencies["python"].total == 1
    assert frequencies["python"].simple == 0
    assert frequencies["python"].regular == 1
    assert frequencies["python"].hard == 0


def test_compute_frequencies_hard_difficulty():
    """Test that hard difficulty increments hard field."""
    items = {"python"}
    frequencies = {}

    compute_frequencies(items, frequencies, 1, "hard")

    assert frequencies["python"].total == 1
    assert frequencies["python"].simple == 0
    assert frequencies["python"].regular == 0
    assert frequencies["python"].hard == 1


def test_compute_frequencies_count_one():
    """Test with count of 1."""
    items = {"python"}
    frequencies = {}

    compute_frequencies(items, frequencies, 1, "regular")

    assert frequencies["python"].total == 1
    assert frequencies["python"].regular == 1


def test_compute_frequencies_count_multiple():
    """Test with count > 1 for repeated tasks."""
    items = {"python"}
    frequencies = {}

    compute_frequencies(items, frequencies, 5, "regular")

    assert frequencies["python"].total == 5
    assert frequencies["python"].regular == 5


def test_compute_frequencies_accumulates():
    """Test multiple calls accumulate correctly."""
    items1 = {"python"}
    items2 = {"python", "testing"}
    frequencies = {}

    compute_frequencies(items1, frequencies, 1, "regular")
    compute_frequencies(items2, frequencies, 2, "simple")

    assert frequencies["python"].total == 3
    assert frequencies["python"].regular == 1
    assert frequencies["python"].simple == 2
    assert frequencies["testing"].total == 2
    assert frequencies["testing"].simple == 2


def test_compute_frequencies_existing_entry():
    """Test updating existing Frequency object."""
    items = {"python"}
    frequencies = {"python": Frequency(total=5, simple=2, regular=3, hard=0)}

    compute_frequencies(items, frequencies, 3, "hard")

    assert frequencies["python"].total == 8
    assert frequencies["python"].simple == 2
    assert frequencies["python"].regular == 3
    assert frequencies["python"].hard == 3


def test_compute_frequencies_mutates_dict():
    """Test that function modifies dict in-place."""
    items = {"python"}
    frequencies = {}

    result = compute_frequencies(items, frequencies, 1, "regular")

    assert result is None
    assert "python" in frequencies


def test_compute_frequencies_with_normalized_tags():
    """Test with normalized tag sets."""
    items = {"python", "testing", "devops"}
    frequencies = {}

    compute_frequencies(items, frequencies, 2, "simple")

    assert len(frequencies) == 3
    assert frequencies["python"].total == 2
    assert frequencies["python"].simple == 2
    assert frequencies["testing"].total == 2
    assert frequencies["testing"].simple == 2
    assert frequencies["devops"].total == 2
    assert frequencies["devops"].simple == 2
