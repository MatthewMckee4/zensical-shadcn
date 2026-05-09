# Contributing

## Setup

```bash
uv sync --all-extras --dev
bun install
```

## Workflow

```bash
just build-css    # rebuild shadcn/css/base.css after editing tailwind/*.css
just test         # uvx karva test
just lint         # uvx prek run -a (formatters + linters + type-check)
just serve        # local preview against pages/
```

The committed `shadcn/css/base.css` must match a clean `bun run build` — CI fails otherwise. Always rebuild and commit the output when editing `tailwind/`.

## Releasing

The `Release` workflow is dispatched manually with the target version tag (e.g. `0.1.1`). It:

1. Runs `uv build` to produce wheel + sdist.
1. Publishes to PyPI via Trusted Publishing (OIDC, no token).
1. Creates a GitHub release with auto-generated notes.

PyPI side: register a pending publisher for `zensical-shadcn` with `workflow = release.yml` and `environment = pypi`.
