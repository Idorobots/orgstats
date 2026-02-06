# orgstats

Analyze Emacs Org-mode archive files to extract task statistics and tag/word frequencies.

## Installation

```bash
python -m venv dev
source dev/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py <org-file> [<org-file> ...]
```

Example:
```bash
python src/main.py examples/ARCHIVE_small
```

Output:
```
Processing examples/ARCHIVE_small...

Total tasks:  33
Done tasks:  33

Top tags:
 [('projectmanagement', 10), ('debugging', 8), ('jira', 6), ...]

Top words in headline:
 [('ejabberd', 8), ('prepare', 4), ('session', 3), ...]

Top words in body:
 [...]
```

## Testing

```bash
pytest                                     # Run all tests
pytest tests/test_normalize.py             # Run single file
pytest --cov=src --cov-report=term-missing # With coverage
```

## Project Structure

- `src/core.py` - Core analysis logic
- `src/cli.py` - CLI interface
- `src/main.py` - Entry point
- `tests/` - Test suite (78 tests, 97% coverage)
