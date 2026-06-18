# CI/CD & Workflows

PyChase ships with three ready-to-use **GitHub Actions workflows** in `.github/workflows/` to automate duplicate code detection in your CI/CD pipeline.

## Workflow Overview

| Workflow | File | Trigger | Purpose |
|---|---|---|---|
| **CI** | `ci.yml` | Push / PR to `master` | Tests PyChase against the full demo suite on Python 3.10–3.13 |
| **Publish** | `publish.yml` | GitHub Release published | Builds and uploads PyChase to PyPI |
| **Quality** | `quality.yml` | Push / PR to `master` | Self-analysis: runs PyChase on its own source code and generates a quality report |

---

## CI Workflow

The CI workflow runs on every push and pull request to `master`. It:

1. Checks out the repository
2. Sets up Python (3.10, 3.11, 3.12, 3.13 in parallel)
3. Runs the full demo test suite at two thresholds
4. Validates JSON, CSV, and HTML output formats
5. Verifies zero false positives on the `13_unique_code.py` file
6. Runs PyChase on its own source (`pychase/` directory)

```yaml
name: CI
on:
  push: { branches: [master] }
  pull_request: { branches: [master] }
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "${{ matrix.python-version }}" }
      - run: python -m pychase --threshold 0.55 --min-lines 2 --min-nodes 10 demo/
      - run: python -m pychase --threshold 0.7 demo/
      - run: python -m pychase --json --threshold 0.5 demo/ | python -m json.tool
      - run: python -m pychase --format html --output report.html demo/
      - run: python -m pychase --threshold 0.7 pychase/
```

---

## Publish Workflow

Triggered when you create a **GitHub Release**. It:

1. Builds the package with `python -m build`
2. Publishes to **PyPI** using trusted publishing (`pypa/gh-action-pypi-publish`)

To use, create a release on GitHub and the package will automatically appear on PyPI.

```yaml
name: Publish to PyPI
on:
  release: { types: [published] }
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions: { id-token: write }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python -m pip install build twine
      - run: python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

---

## Quality Workflow

Runs PyChase **on its own code** to detect any duplicate code within the project itself. This serves as both a dogfooding test and a quality gate.

1. Runs `pychase --threshold 0.7 pychase/` and outputs to the job summary
2. Generates an interactive HTML quality report
3. Uploads the report as a build artifact

```yaml
name: Scorecard
on:
  push: { branches: [master] }
  pull_request: { branches: [master] }
jobs:
  analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python -m pychase --threshold 0.7 pychase/
      - run: python -m pychase --format html --output quality-report.html .
      - uses: actions/upload-artifact@v4
        with: { name: quality-report, path: quality-report.html }
```

---

## Using PyChase in Your Own CI

You don't need these workflows — PyChase is a standalone CLI tool. Add it to any CI pipeline:

```yaml
# GitHub Actions
- run: pip install pychase
- run: pychase --json --threshold 0.85 ./src | tee results.json
- run: pychase --format html --output duplicates.html ./src

# GitLab CI
script:
  - pip install pychase
  - pychase --json --threshold 0.85 ./src > results.json
  - pychase --format html --output duplicates.html ./src
```

---

## Badges

Show your CI status in the README:

```markdown
![CI](https://github.com/Mayne-X/PyChase/actions/workflows/ci.yml/badge.svg)
![Quality](https://github.com/Mayne-X/PyChase/actions/workflows/quality.yml/badge.svg)
```
