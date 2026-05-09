"""Snapshot tests for `zensical build`."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import karva

ROOT = Path(__file__).parent.parent
PAGES = ROOT / "pages"
SITE = PAGES / "site"


def _have_zensical() -> bool:
    return shutil.which("zensical") is not None


def test_zensical_build_runs() -> None:
    """Build the demo site and snapshot key markers from the index page.

    We don't snapshot the entire HTML because Zensical may emit version
    strings, build timestamps, or tweaks to its own partials. Instead,
    we sanity-check the parts that prove our theme and CSS are wired in.
    """
    if not _have_zensical():
        return

    if SITE.exists():
        shutil.rmtree(SITE)

    result = subprocess.run(
        ["zensical", "build", "-f", "zensical.toml"],
        capture_output=True,
        text=True,
        cwd=PAGES,
    )
    assert result.returncode == 0, (
        f"zensical build failed:\nSTDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    index = SITE / "index.html"
    assert index.exists(), "site/index.html not produced"
    html = index.read_text()

    markers = {
        "base_css_linked": "css/base.css" in html,
        "geist_css_linked": "css/geist.css" in html,
        "iconify_script_linked": "iconify.min.js" in html,
        "extends_material_base": "data-md-color-scheme" in html,
    }
    karva.assert_json_snapshot(
        markers,
        inline="""\
        {
          "base_css_linked": true,
          "extends_material_base": true,
          "geist_css_linked": true,
          "iconify_script_linked": true
        }
        """,
    )
