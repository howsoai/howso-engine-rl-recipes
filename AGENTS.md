# Repository Guidelines

## Project Structure & Module Organization
Core reinforcement-learning examples live in `howso_engine_rl_recipes/`, grouped by scenario (`cart_pole/`, `wafer_thin_mint/`) with shared utilities in `common/` and entry points in `__main__.py`. End-to-end tests reside in `tests/`, mirroring module names via `test_*.py`. Configuration bundles for engine variants live in `config/`, and helper scripts (for example `bin/build.sh`) support local setup. Keep data artifacts out of the repository; store transient outputs under a gitignored scratch directory when needed.

## Environment Setup
Use Python 3.10–3.13. Create a virtual environment, then install dependencies with `pip install -e .[dev]` or run `bin/build.sh install_deps 3.12` to pull the matching `requirements-3.12-dev.txt`. When running interactively, launch recipes via `python -m howso_engine_rl_recipes --help` to enumerate scenario options.

## Build, Test, and Development Commands
- `pip install -e .[dev]`: installs the package plus lint/test tooling for iterative development.
- `pytest`: executes the entire regression suite defined in `tests/`.
- `pytest -n auto`: shuffles the suite across available cores with `pytest-xdist` when diagnosing performance issues.
- `python -m howso_engine_rl_recipes cartpole` (or `wtm`): exercises an example end-to-end for manual smoke checks.

## Coding Style & Naming Conventions
Follow standard Python style with 4-space indentation and descriptive snake_case names. Formatting is enforced via YAPF (119-column limit) and import hygiene via isort (Google profile). Run `yapf -ri howso_engine_rl_recipes tests` and `isort .` before committing. Lint new code with `flake8` and include docstrings for public functions describing the scenario role or agent behaviour.

## Testing Guidelines
Use `pytest` fixtures in `tests/conftest.py` to share environment setup; name new files `test_<module>.py` and prefer Given/When/Then comments when scenarios get complex. Keep tests deterministic and fast—mock external services and limit gym rollouts to the minimum timesteps that surface regressions. Add regression tests alongside new modules (e.g., `tests/test_cart_pole.py` for cart-pole changes). If you modify recipe interfaces, add smoke tests that run the module via `python -m ...` to validate CLI wiring.

## Commit & Pull Request Guidelines
Commit messages typically begin with a numeric ticket (`24082: Remove support for Python 3.9`) followed by a concise summary; mirror that style and reference the related issue when possible. Squash trivial fixups locally. PRs should describe scenario impacts, list testing commands executed, and link to any Howso internal or GitHub issues. Include screenshots or CLI transcripts when behaviour changes are user-visible, and confirm CLA eligibility before requesting review.
