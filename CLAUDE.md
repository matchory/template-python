# CLAUDE.md

## Stack

- Python 3.13, managed with [uv](https://docs.astral.sh/uv/)
- [hatchling](https://hatch.pypa.io/) as the build backend
- [ruff](https://docs.astral.sh/ruff/) for linting and formatting, configured via the `strict`
  preset from [`matchory/coding-style`](https://github.com/matchory/coding-style)
- [pytest](https://docs.pytest.org/) for tests

## Commands

```bash
uv sync                                         # install dependencies
uv run pytest                                   # run the test suite
uv run ruff check .                             # lint
uv run ruff format .                            # format
uv run matchory-coding-style verify --strict    # verify the style wiring
```

`uv run matchory-coding-style verify --strict` is the acceptance test for this repository. It
must exit 0 before any change is considered done.

## Ruff configuration

Ruff's rules live in `matchory/coding-style`, not in this repository. `pyproject.toml` extends
`.matchory/ruff.toml`, which in turn extends the `strict` preset.

`.matchory/` and `.editorconfig` are **generated — never hand-edited**. Refresh both with:

```bash
uv run matchory-coding-style sync --preset strict
```

Do not edit files under `.matchory/` directly; edits are overwritten the next time `sync` runs.

## Renaming the package

Renaming `matchory-template-python` / `matchory_template` touches `pyproject.toml`'s `name` and
`[tool.hatch.build.targets.wheel].packages`, the `src/matchory_template/` directory, and the import
in `tests/test_greeting.py`. Once all four agree, a plain `uv sync` picks up the new name — no
forced reinstall is needed.

## `tests/__init__.py`

This file is empty on purpose. `strict` selects `INP` (implicit namespace packages), and `INP001`
fires on `tests/` unless it is a real package. `base.toml`'s `**/tests/**` per-file-ignores cover
only `S105`/`S106`/`S107`/`PLC0415`, not `INP001`, so the file has to exist. Don't delete it.

## Claude Code hook

`.claude/settings.json` runs `ruff format` on a Python file after every edit. The hook pipes its
input through `jq`; if `jq` is not installed, the pipeline no-ops instead of failing, so formatting
silently falls back to whatever runs at commit or CI time.
