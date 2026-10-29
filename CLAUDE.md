# CLAUDE.md

- Done means every check in `.github/workflows/ci.yml` passes locally.
- `.matchory/` and `.editorconfig` are generated. Refresh them with
  `uv run matchory-coding-style sync --preset strict`. Always pass `--preset strict`: the default is
  `base`, and CI rejects it.
