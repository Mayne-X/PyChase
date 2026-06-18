# Getting Started

## Installation

```bash
pip install pychase
```

Requires **Python 3.10+** with **zero external dependencies**.

Or install from source:

```bash
git clone https://github.com/Mayne-X/PyChase.git
cd PyChase
pip install .
```

## Quick Start

Scan the current directory for duplicate code:

```bash
pychase .
```

Scan specific files or directories:

```bash
pychase src/module_a.py src/module_b.py
pychase --threshold 0.85 ./src ./tests
```

Generate an interactive HTML report:

```bash
pychase --format html --output duplicates.html .
```

## First Run

```bash
$ pychase .
PyChase found 3 duplicate groups (5 pairs) across 42 units

DUPLICATE score=1.000
  src/utils.py:12-18 format_date
  src/helpers.py:8-14 format_time

DUPLICATE score=0.786
  src/models/user.py:34-42 User.validate
  src/models/order.py:28-36 Order.validate
```

## Next Steps

- Explore the [CLI Reference](CLI-Reference) for all options
- Set up [Configuration](Configuration) via pyproject.toml
- Understand [How It Works](How-It-Works) under the hood
- Run the [Demo Test Suite](Demo-Test-Suite) to see capabilities
