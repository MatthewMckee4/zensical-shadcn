"""Iconify markdown extension.

Inline syntax: ``+provider:name+`` or ``+provider:name;height=24px+``.
Emits a ``<span class="iconify" data-icon="..." data-height="...">`` that
the iconify client library renders into an SVG at runtime.
"""

from __future__ import annotations

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

ICONIFY_TAG_RE = (
    r"[+]([a-z0-9\-]+:[a-z0-9\-]+)(?:[;][a-z]+[=][0-9a-zA-Z.#%]+)*[+]"
)


class IconifyInlinePattern(InlineProcessor):
    def handleMatch(self, m, data):  # noqa: ARG002
        icon_id = m.group(1)
        raw_query = m.group(0).replace(icon_id, "").strip("+").strip(";")
        params: dict[str, str] = {}
        if raw_query:
            params = dict(k.split("=") for k in raw_query.split(";"))

        attrs = ['class="iconify"', f'data-icon="{icon_id}"']
        for k, v in params.items():
            attrs.append(f'data-{k}="{v}"')
        html = f"<span {' '.join(attrs)}></span>"
        placeholder = self.md.htmlStash.store(html)
        return placeholder, m.start(0), m.end(0)


class IconifyExtension(Extension):
    def extendMarkdown(self, md):
        pattern = IconifyInlinePattern(ICONIFY_TAG_RE, md)
        md.inlinePatterns.register(pattern, "iconify", 175)


def makeExtension(**kwargs):
    return IconifyExtension(**kwargs)
