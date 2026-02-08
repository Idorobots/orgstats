"""Tests for the compute_frequencies() function."""

from orgstats.core import Frequency, compute_frequencies


def test_compute_frequencies_empty_items():
    """Test with empty set creates no entries."""
    items = set()
    frequencies = {}

    compute_frequencies(items, frequencies, 1)

    assert frequencies == {}


def test_compute_frequencies_single_item():
    """Test single item creates Frequency with correct counts."""
    items = {"python"}
    frequencies = {}

    compute_frequencies(items, frequencies, 1)

    assert "python" in frequencies
    assert frequencies["python"].total == 1


def test_compute_frequencies_multiple_items():
    """Test multiple items all get incremented."""
    items = {"python", "testing", "debugging"}
    frequencies = {}

    compute_frequencies(items, frequencies, 1)

    assert len(frequencies) == 3
    assert "python" in frequencies
    assert "testing" in frequencies
    assert "debugging" in frequencies
    assert frequencies["python"].total == 1
    assert frequencies["testing"].total == 1
    assert frequencies["debugging"].total == 1


def test_compute_frequencies_count_one():
    """Test with count of 1."""
    items = {"python"}
    frequencies = {}

    compute_frequencies(items, frequencies, 1)

    assert frequencies["python"].total == 1


def test_compute_frequencies_count_multiple():
    """Test with count > 1 for repeated tasks."""
    items = {"python"}
    frequencies = {}

    compute_frequencies(items, frequencies, 5)

    assert frequencies["python"].total == 5


def test_compute_frequencies_accumulates():
    """Test multiple calls accumulate correctly."""
    items1 = {"python"}
    items2 = {"python", "testing"}
    frequencies = {}

    compute_frequencies(items1, frequencies, 1)
    compute_frequencies(items2, frequencies, 2)

    assert frequencies["python"].total == 3
    assert frequencies["testing"].total == 2


def test_compute_frequencies_existing_entry():
    """Test updating existing Frequency object."""
    items = {"python"}
    frequencies = {"python": Frequency(total=5)}

    compute_frequencies(items, frequencies, 3)

    assert frequencies["python"].total == 8


def test_compute_frequencies_mutates_dict():
    """Test that function modifies dict in-place."""
    items = {"python"}
    frequencies = {}

    result = compute_frequencies(items, frequencies, 1)

    assert result is None
    assert "python" in frequencies


def test_compute_frequencies_with_normalized_tags():
    """Test with normalized tag sets."""
    items = {"python", "testing", "devops"}
    frequencies = {}

    compute_frequencies(items, frequencies, 2)

    assert len(frequencies) == 3
    assert frequencies["python"].total == 2
    assert frequencies["testing"].total == 2
    assert frequencies["devops"].total == 2
