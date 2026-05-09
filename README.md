# zensical-shadcn

A [shadcn](https://ui.shadcn.com/)-styled theme for [Zensical](https://zensical.org/), the modern static site generator from the Material for MkDocs team.

Ported from [`asiffer/mkdocs-shadcn`](https://github.com/asiffer/mkdocs-shadcn).

## Install

```bash
uv add zensical-shadcn
```

## Use

In `zensical.toml`:

```toml
[theme]
name = "shadcn"
```

Or `mkdocs.yml`:

```yaml
theme:
  name: shadcn
```

## Develop

```bash
just sync         # uv sync
just build-css    # bun run build
just test         # uvx karva test
just serve        # uv run zensical serve pages/
just lint         # uvx prek run -a
```

## License

MIT. See [LICENSE](LICENSE). Original work © Alban Siffer (mkdocs-shadcn).
