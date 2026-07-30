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

## Adding a module

If `uv sync` ran before a module existed under `src/matchory_template/`, adding the module and
running a plain `uv sync` again can leave a stale editable install. Force a rebuild with:

```bash
uv sync --reinstall-package matchory-template-python
```
