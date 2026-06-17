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
        "search_shortcut_registered": 'document.addEventListener("keydown", searchShortcutHandler)'
        in (SITE / "js" / "callbacks.js").read_text(),
        "search_titles_sanitized": "title.textContent = searchTitle(item)"
        in (SITE / "js" / "callbacks.js").read_text(),
        "copy_button_supports_pygments_highlight": "div.codehilite, div.highlight"
        in (SITE / "js" / "copy-button.js").read_text(),
        "material_shell_removed": all(
            marker not in html
            for marker in ("md-header", "md-tabs", "md-sidebar", "md-content")
        ),
        "shadcn_header_rendered": 'class="sh-header"' in html,
        "shadcn_sidebar_rendered": 'class="sh-sidebar"' in html,
        "shadcn_toc_rendered": 'class="sh-toc"' in html,
    }
    karva.assert_json_snapshot(
        markers,
        inline="""\
        {
          "base_css_linked": true,
          "copy_button_supports_pygments_highlight": true,
          "geist_css_linked": true,
          "iconify_script_linked": true,
          "material_shell_removed": true,
          "search_shortcut_registered": true,
          "search_titles_sanitized": true,
          "shadcn_header_rendered": true,
          "shadcn_sidebar_rendered": true,
          "shadcn_toc_rendered": true
        }
        """,
    )
