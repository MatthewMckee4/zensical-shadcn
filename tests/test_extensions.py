"""Snapshot tests for shadcn markdown extensions.

Each test renders a short markdown snippet and snapshots the HTML output.
Run `uvx karva test --snapshot-update` to (re)generate inline snapshots.
"""

from __future__ import annotations

import karva
import markdown


def _render(text: str, *extensions: object) -> str:
    return markdown.Markdown(extensions=list(extensions)).convert(text)


def test_autonumber_label() -> None:
    from shadcn.extensions.autonumber import AutoNumberExtension

    html = _render("Caption {#fig:diagram}", AutoNumberExtension())
    karva.assert_snapshot(
        html,
        inline='<p>Caption <span id="fig:diagram" class="autonumber fig">Figure 1</span></p>',
    )


def test_autonumber_reference() -> None:
    from shadcn.extensions.autonumber import AutoNumberExtension

    src = "Title {#fig:a}\n\nSee @fig:a for details."
    karva.assert_snapshot(
        _render(src, AutoNumberExtension()),
        inline="""\
        <p>Title <span id="fig:a" class="autonumber fig">Figure 1</span></p>
        <p>See <a href="#fig:a" class="autonumber fig">figure 1</a> for details.</p>
        """,
    )


def test_autonumber_capitalized_reference() -> None:
    from shadcn.extensions.autonumber import AutoNumberExtension

    src = "{#tbl:t}\n\n@Tbl:t shows results."
    karva.assert_snapshot(
        _render(src, AutoNumberExtension()),
        inline="""\
        <p><span id="tbl:t" class="autonumber tbl">Table 1</span></p>
        <p><a href="#tbl:t" class="autonumber tbl">Table 1</a> shows results.</p>
        """,
    )


def test_autonumber_unknown_reference_left_intact() -> None:
    from shadcn.extensions.autonumber import AutoNumberExtension

    karva.assert_snapshot(
        _render("@fig:nope", AutoNumberExtension()), inline="<p>@fig:nope</p>"
    )


def test_autonumber_increments_per_prefix() -> None:
    from shadcn.extensions.autonumber import AutoNumberExtension

    src = "{#fig:a}\n\n{#fig:b}\n\n{#tbl:c}"
    karva.assert_snapshot(
        _render(src, AutoNumberExtension()),
        inline="""\
        <p><span id="fig:a" class="autonumber fig">Figure 1</span></p>
        <p><span id="fig:b" class="autonumber fig">Figure 2</span></p>
        <p><span id="tbl:c" class="autonumber tbl">Table 1</span></p>
        """,
    )


def test_iconify_emits_client_side_span() -> None:
    from shadcn.extensions.iconify import IconifyExtension

    karva.assert_snapshot(
        _render("+mdi:home+", IconifyExtension()),
        inline='<p><span class="iconify" data-icon="mdi:home"></span></p>',
    )


def test_iconify_with_height_param() -> None:
    from shadcn.extensions.iconify import IconifyExtension

    karva.assert_snapshot(
        _render("+mdi:home;height=24px+", IconifyExtension()),
        inline='<p><span class="iconify" data-icon="mdi:home" data-height="24px"></span></p>',
    )


def test_codexec_extension_loads() -> None:
    from shadcn.extensions.codexec import CodexecBlockExtension

    md = markdown.Markdown(extensions=[CodexecBlockExtension()])
    karva.assert_snapshot(md.convert("hello"), inline="<p>hello</p>")


def test_hover_card_extension_loads() -> None:
    from shadcn.extensions.hover_card import HoverCardBlockExtension

    md = markdown.Markdown(extensions=[HoverCardBlockExtension()])
    karva.assert_snapshot(md.convert("hello"), inline="<p>hello</p>")
