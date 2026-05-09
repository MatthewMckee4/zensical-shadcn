# https://just.systems

default:
    @just --list

# Build CSS via Tailwind v4
build-css:
    bun run build

# Watch CSS during development
watch-css:
    bun run dev

# Run the test suite via karva
test *args:
    uvx karva test {{args}}

# Run all pre-commit hooks
lint:
    uvx prek run -a

# Build the wheel + sdist
build:
    uv build

# Serve the demo site
serve:
    uv run zensical serve pages/

# Install dev environment
sync:
    uv sync --all-extras --dev
