# Matchory Python Project Template

A starting point for Matchory Python projects: [uv](https://docs.astral.sh/uv/) for dependency
management, [hatchling](https://hatch.pypa.io/) as the build backend, [ruff](https://docs.astral.sh/ruff/)
for linting and formatting, and [pytest](https://docs.pytest.org/) for tests. Ruff is wired to the
shared [`matchory/coding-style`](https://github.com/matchory/coding-style) presets.

## Getting started

```bash
uv sync
uvx pre-commit install
```

`uv sync` installs the project and its dev dependencies into `.venv` and builds the package in
editable mode. `pre-commit install` wires the git hooks that run the same checks CI runs, against
only the files you changed.

## Commands

```bash
uv run pytest                                   # run the test suite
uv run ruff check .                             # lint
uv run ruff format .                            # format
uv run matchory-coding-style verify --strict    # confirm the style wiring itself is intact
```

`matchory-coding-style verify --strict` is the acceptance test for this template: if it exits 0,
the ruff configuration, `.editorconfig`, and pre-commit hook are all correctly wired to the
`strict` preset. CI runs it on every push and pull request, alongside lint, format, and tests.

This project uses the `strict` preset rather than `base`. `base` exists to let an established
codebase adopt the shared style gradually; a repository freshly created from this template has no
legacy code to migrate, so it starts at the target configuration instead of ramping up to it.

## Why `.matchory/` is committed

Ruff's `extend` setting in `pyproject.toml` points at `.matchory/ruff.toml` by filesystem path.
`extend` cannot reach inside an installed package, and the path to a package installed in
`.venv`'s site-packages embeds the Python version and does not survive a recreated virtualenv. The
`matchory-coding-style` package is therefore a transport for these files, not a place ruff reads
them from directly.

`.matchory/` is **generated — never hand-edited**. Refresh it with:

```bash
uv run matchory-coding-style sync --preset strict
```

Both `.matchory/ruff/base.toml` and `.matchory/ruff/strict.toml` are committed, even though this
project only extends `strict.toml`, because `strict.toml` itself extends `base.toml` by relative
path.

The same command also refreshes `.editorconfig`. It is one of the files `matchory-coding-style
verify` checks, so if your editor or another tool rewrites it, `sync --preset strict` is how you
put it back.

## Adding your first module

`uv sync` builds the package from whatever is in `src/matchory_template/` at the time it runs. If
you run `uv sync` before adding real code, then add a module and run a plain `uv sync` again, uv
may treat the package as unchanged and skip rebuilding it, leaving you with a stale editable
install and `ModuleNotFoundError` even though the file exists on disk. Force a rebuild with:

```bash
uv sync --reinstall-package matchory-template-python
```

## Keeping the dependency and the pre-commit hook in sync

`pyproject.toml` pins `matchory-coding-style` with a floating lower bound
(`matchory-coding-style>=0.1.2`), while `.pre-commit-config.yaml` pins the hook to a fixed
`rev: v0.1.2`. These agree today, but nothing keeps them in sync automatically. If you bump one
without the other, the CLI installed via `uv sync` can run a different `sync` than the version the
pinned pre-commit hook checks against with `--check`, and the two can start disagreeing about
whether the repository is in sync. Bump both together.
