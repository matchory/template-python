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
editable mode. `pre-commit install` wires git hooks that re-run ruff and the style-wiring check
against the files you changed, on every commit. The hooks and CI overlap but are not identical:
pre-commit does not run `uv run pytest`, and CI does not invoke pre-commit itself. The hooks also
bring their own ruff — `matchory-coding-style`'s pre-commit environment resolves `ruff>=0.14.0`
independently, at hook-install time, from whatever `ruff` version `uv.lock` pins for the project
venv. If pre-commit reformats a file that CI then reports as unformatted, or the other way around,
that version skew is the first thing to check.

## Commands

```bash
uv run pytest                                   # run the test suite
uv run ruff check .                             # lint
uv run ruff format .                            # format
uv run matchory-coding-style verify --strict    # confirm the style wiring itself is intact
```

`matchory-coding-style verify --strict` checks that `.matchory/`, `.editorconfig`, and
`pyproject.toml`'s `[tool.ruff]` all agree with the currently installed `matchory-coding-style`,
whichever preset `.matchory/ruff.toml` selects. It does not inspect `.pre-commit-config.yaml`, and
on its own it does not prove this repository is on `strict` rather than `base` — a repository
synced to `base` passes it too. CI asserts the `strict` selector separately, with
`matchory-coding-style sync --check --preset strict`, alongside `verify --strict`, lint, format,
and tests, on every push and pull request.

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

## Make it yours

A fresh clone builds a package named `matchory-template-python`, importing as `matchory_template`.
Renaming it touches four places:

1. `name` in `pyproject.toml`
2. `[tool.hatch.build.targets.wheel].packages` in `pyproject.toml` — the build breaks the moment
   this still points at a directory that no longer exists
3. the directory `src/matchory_template/`
4. the import in `tests/test_greeting.py`

Once all four agree, a plain `uv sync` rebuilds and reinstalls the package under the new name —
uv treats the renamed project as a different requirement from the one already installed, so it
uninstalls the old one and installs the new one in the same run. No forced reinstall is needed.

## Keeping the dependency and the pre-commit hook in sync

`pyproject.toml` pins `matchory-coding-style` with a floating lower bound
(`matchory-coding-style>=0.1.2`), while `.pre-commit-config.yaml` pins the hook to a fixed
`rev: v0.1.2`. These agree today, but nothing keeps them in sync automatically, and Dependabot will
actively pull them apart: it has no pre-commit ecosystem configured here, so it bumps the
`uv.lock` dependency without ever touching `rev:`.

The good news is that the resulting drift announces itself. `verify` compares `.matchory/` against
whatever `matchory-coding-style` is currently installed, so once a newer version changes the
presets, CI's "Style wiring" job fails on the Dependabot pull request itself, before it can merge
silently. The fix is:

```bash
uv run matchory-coding-style sync --preset strict
```

Commit the result, and bump `.pre-commit-config.yaml`'s `rev:` to match the new version.
