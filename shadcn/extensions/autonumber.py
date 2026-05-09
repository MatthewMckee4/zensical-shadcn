"""Autonumber markdown extension.

Within a single document, replaces label syntax `{#prefix:id}` with a
numbered span and references `@prefix:id` (or `@Prefix:id`) with a
same-page anchor link. Supports `fig`, `tbl`, `eq` by default; configurable
via the `prefixes` option.

Limitations vs. the upstream MkDocs plugin: numbering is per-document, not
site-wide, and references can only target labels in the same document.
"""

from __future__ import annotations

import re
from xml.etree import ElementTree as etree

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor

DEFAULT_PREFIXES: dict[str, str] = {
    "fig": "Figure",
    "tbl": "Table",
    "eq": "Equation",
}


class _LabelPreprocessor(Preprocessor):
    def __init__(self, md: Markdown, prefixes: dict[str, str]) -> None:
        super().__init__(md)
        self.prefixes = prefixes
        self.pattern = re.compile(
            r"\{#(" + "|".join(map(re.escape, prefixes)) + r"):"
            r"([a-zA-Z0-9._-]+)\}"
        )
        self.registry: dict[str, tuple[str, int]] = {}

    def run(self, lines: list[str]) -> list[str]:
        counters: dict[str, int] = {p: 0 for p in self.prefixes}
        out: list[str] = []
        for line in lines:

            def repl(match: re.Match[str]) -> str:
                prefix = match.group(1)
                id_ = match.group(2)
                counters[prefix] += 1
                number = counters[prefix]
                anchor = f"{prefix}:{id_}"
                self.registry[id_] = (prefix, number)
                label = self.prefixes[prefix]
                return (
                    f'<span id="{anchor}" class="autonumber {prefix}">'
                    f"{label} {number}</span>"
                )

            out.append(self.pattern.sub(repl, line))
        return out


class _ReferenceTreeprocessor(Treeprocessor):
    def __init__(
        self,
        md: Markdown,
        prefixes: dict[str, str],
        label_proc: _LabelPreprocessor,
    ) -> None:
        super().__init__(md)
        upper_lower = list(prefixes) + [p.capitalize() for p in prefixes]
        self.pattern = re.compile(
            r"@("
            + "|".join(map(re.escape, upper_lower))
            + r"):([a-zA-Z0-9._-]+)"
        )
        self.prefixes = prefixes
        self.label_proc = label_proc

    def run(self, root: etree.Element) -> etree.Element | None:
        for el in root.iter():
            for attr in ("text", "tail"):
                value = getattr(el, attr)
                if not value or "@" not in value:
                    continue
                new_value = self._rewrite(value)
                if new_value != value:
                    setattr(el, attr, new_value)
        return None

    def _rewrite(self, text: str) -> str:
        def repl(match: re.Match[str]) -> str:
            raw_prefix = match.group(1)
            id_ = match.group(2)
            prefix = raw_prefix.lower()
            entry = self.label_proc.registry.get(id_)
            if entry is None or entry[0] != prefix:
                return match.group(0)
            label = self.prefixes[prefix]
            display = (
                label.capitalize()
                if raw_prefix[0].isupper()
                else label.lower()
            )
            anchor = f"{prefix}:{id_}"
            html = (
                f'<a href="#{anchor}" class="autonumber {prefix}">'
                f"{display} {entry[1]}</a>"
            )
            return self.md.htmlStash.store(html)

        return self.pattern.sub(repl, text)


class AutoNumberExtension(Extension):
    def __init__(self, **kwargs: object) -> None:
        self.config = {
            "prefixes": [
                dict(DEFAULT_PREFIXES),
                "Mapping of label prefix to display name.",
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        prefixes = dict(DEFAULT_PREFIXES)
        prefixes.update(self.getConfig("prefixes") or {})
        label_proc = _LabelPreprocessor(md, prefixes)
        md.preprocessors.register(label_proc, "shadcn_autonumber_label", 30)
        md.treeprocessors.register(
            _ReferenceTreeprocessor(md, prefixes, label_proc),
            "shadcn_autonumber_ref",
            5,
        )


def makeExtension(**kwargs: object) -> AutoNumberExtension:
    return AutoNumberExtension(**kwargs)
