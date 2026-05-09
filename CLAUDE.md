# CLAUDE.md

Project conventions for Claude Code in this repository.

## What this is

A shadcn-styled theme package for [Zensical](https://zensical.org/). Pure Python, ported from `asiffer/mkdocs-shadcn`.

## Layout

- `shadcn/` — installable Python package (theme code, templates, assets).
- `tailwind/` — Tailwind v4 source. Compiled to `shadcn/css/base.css` via `bun run build`.
- `pages/` — demo site, doubles as the test fixture.
- `tests/` — karva tests (`uvx karva test`). Not pytest.

## Conventions

- Test runner is **karva**, not pytest. `conftest.py` and fixtures work; pytest plugins like `pytest-playwright` do not.
- Templates use **MiniJinja** (Zensical's Rust-based engine), not Jinja2. Avoid `{% do %}`, custom Jinja2 filters.
- The committed `shadcn/css/base.css` must equal a clean `bun run build`. CI verifies.
- Theme entry-point group is `mkdocs.themes` (Zensical reads it intentionally).
- No general plugin hook system in Zensical — express features as `markdown.Extension` subclasses.

## Common tasks

```bash
just sync          # uv sync --all-extras --dev
just build-css     # rebuild base.css
just test          # uvx karva test
just lint          # uvx prek run -a
just serve         # local preview
```
