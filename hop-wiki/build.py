#!/usr/bin/env python3
"""Builds the House of Pips player wiki for the Slapcraft Games site (/hop/wiki).

Inputs, all in this repository:
  * hop-wiki/catalogue.json: the perks, supplies, skills, modes, achievements
    and numbers from the game, as a snapshot,
  * hop-wiki/content/: the hand-written Markdown pages and catalogue notes,
  * public/hop/wiki-data/img/: every picture, including screenshots.

Output: one JSON file per page plus manifest.json in public/hop/wiki-data/,
which the Angular wiki renders. The pages are first built as a plain HTML site
in hop-wiki/.build/site/ (gitignored) so every link and picture can be
checked, and a Steam Community guide draft is written to hop-wiki/.build/steam/.

The build fails when a catalogue entry has no notes, when notes name an entry
the catalogue no longer has, when an image or internal link does not resolve,
or when player-facing text leaks internal or spoiler material.

Standard library only. Usage from the site root:
  python hop-wiki/build.py   (or: npm run wiki)
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import posixpath
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

WIKI = Path(__file__).resolve().parent
ROOT = WIKI.parent
CONTENT = WIKI / "content"
DATA = ROOT / "public" / "hop" / "wiki-data"
PICTURES = DATA / "img"
BUILD = WIKI / ".build"
DEFAULT_CATALOGUE = WIKI / "catalogue.json"
DEFAULT_OUT = BUILD / "site"
DEFAULT_STEAM_OUT = BUILD / "steam"
SITE_NAME = "House of Pips Wiki"
# The Slapcraft Games site serves the wiki at this route and its data at
# WEBSITE_ASSETS, resolved against the site's <base href>.
WEBSITE_ROUTE = "/hop/wiki"
WEBSITE_ASSETS = "hop/wiki-data/"

# Navigation sections, in order. Pages name their section in front matter.
SECTIONS = [
    "Start here",
    "Playing",
    "Perks and items",
    "Progression",
    "Modes and rivals",
    "Online",
    "Options",
    "Help",
    "Spoilers",
]

RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary", "malus"]

# Player-facing text must never carry implementation detail, how rivals are
# made harder (a trade secret) or anything about telemetry and anti-cheat.
# Checked on every generated page's visible text.
FORBIDDEN = [
    (re.compile(r"\bsrc/|\.lua\b|\btests/|\btools/", re.I), "a source path"),
    (re.compile(r"\bADR-?\d", re.I), "an ADR reference"),
    (re.compile(r"telemetry|anti-?cheat|sentry|dsn\b", re.I), "telemetry or anti-cheat detail"),
    (re.compile(r"\bTODO\b|\bFIXME\b"), "an editing marker"),
]
# Phrases that must never reach the public pages are kept only as hashes, so
# this file (in a public repository) does not spell them out. Text is checked
# in runs of one to three words. Spoiler phrases are allowed only on the
# spoiler page; rival logic phrases are never allowed.
SPOILER_HASHES = frozenset({"a5e7c002443743c5", "091dc8ec0db4ff81", "b41c15d2d93b3e02", "484b26967f28bfff", "c5b73c391b9d029f", "a5d1537eb749e54c", "167e463e4bb01391"})
RIVAL_LOGIC_HASHES = frozenset({"1a989ea86150171c", "06d7b1665a504b39", "bcbb0eeac8d6a424", "2b52f28766a3e15c", "ce9a8bb4500d8a25", "e1517be14d06cdb7", "ce18d968699ef0d9", "de4eb10ce8b37e53", "eea3c9b17324aed7", "8ce3b0f272e6d877", "71a2630b890ffe62", "2d13a68bbd45b502", "8b4ad2ac0441c7ae", "3531daf0f027d564", "5d86a07c73e51189"})
SPOILER_PAGE = "spoilers"
# Pages and catalogue entries that must stay off the public repository (the
# spoiler page and anything it needs) live in this gitignored folder.
PRIVATE = WIKI / "private"


def phrase_hashes(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    found = set()
    for size in (1, 2, 3):
        for start in range(len(words) - size + 1):
            found.add(hashlib.sha256(" ".join(words[start : start + size]).encode("utf-8")).hexdigest()[:16])
    return found


class BuildError(Exception):
    pass


def fail(message: str) -> None:
    raise BuildError(message)


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def slugify(text: str) -> str:
    slug = re.sub(r"<[^>]+>", "", text)
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    return slug or "section"


def plain(markup: str) -> str:
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", markup, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------


def read_front_matter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end < 0:
            fail(f"{path.name}: front matter is not closed")
        for line in text[4:end].splitlines():
            if not line.strip():
                continue
            key, separator, value = line.partition(":")
            if not separator:
                fail(f"{path.name}: bad front matter line {line!r}")
            meta[key.strip()] = value.strip()
        text = text[end + 5 :]
    return meta, text


def read_notes(path: Path, ids: list[str], label: str) -> dict[str, str]:
    """Reads `## <id>` sections; every catalogue id must appear exactly once."""
    if not path.exists():
        fail(f"missing {label} notes: {path}")
    notes: dict[str, str] = {}
    current = None
    buffer: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^## ([a-z0-9_]+)\s*$", line)
        if match:
            if current:
                notes[current] = "\n".join(buffer).strip()
            current = match.group(1)
            if current in notes:
                fail(f"{label} notes: {current} appears twice")
            buffer = []
        elif current:
            buffer.append(line)
    if current:
        notes[current] = "\n".join(buffer).strip()
    known = set(ids)
    missing = [entry for entry in ids if entry not in notes]
    extra = sorted(set(notes) - known)
    if missing:
        fail(f"{label} notes are missing for: {', '.join(missing)}")
    if extra:
        fail(f"{label} notes name entries the game does not have: {', '.join(extra)}")
    empty = [entry for entry in ids if not notes[entry]]
    if empty:
        fail(f"{label} notes are empty for: {', '.join(empty)}")
    return notes


def read_screenshots(path: Path) -> dict[str, dict]:
    shots: dict[str, dict] = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        columns = line.split("\t")
        if len(columns) != 2:
            fail(f"screenshots.tsv line {number}: expected a key and a caption separated by a tab")
        key, caption = columns
        if key in shots:
            fail(f"screenshots.tsv: {key} appears twice")
        shots[key] = {"key": key, "caption": caption}
    return shots


# --------------------------------------------------------------------------
# Markdown subset
# --------------------------------------------------------------------------

LIST_RE = re.compile(r"^(\s*)([-*]|\d+[.)])\s+(.*)$")
TABLE_RULE_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
BLOCK_MACRO_RE = re.compile(r"^\{\{([a-z-]+)(?::([^}]*))?\}\}$")


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def term_split(lead: str):
    """Split "**Term**: explanation" into its term and explanation.

    The term must open with bold text, keep its bold markers balanced and stay
    short, so an ordinary sentence with a colon is never taken for a term.
    """
    if not lead.startswith("**"):
        return None
    index = lead.find(": ")
    if index < 0:
        return None
    term = lead[:index]
    if term.count("**") % 2 or len(term) > 64 or "." in term.replace("**", ""):
        return None
    return term, lead[index + 2 :]


class Renderer:
    """Converts the wiki's Markdown subset into HTML for one page."""

    def __init__(self, site: "Site", page_slug: str, root: str):
        self.site = site
        self.page = page_slug
        self.root = root
        self.used_ids: set[str] = set()
        self.toc: list[tuple[str, str]] = []

    # Inline ---------------------------------------------------------------

    def inline(self, text: str) -> str:
        parts = re.split(r"(`[^`]+`)", text)
        out = []
        for part in parts:
            if len(part) >= 2 and part.startswith("`") and part.endswith("`"):
                out.append("<code>" + esc(part[1:-1]) + "</code>")
            else:
                out.append(self._inline_text(part))
        return "".join(out)

    def _inline_text(self, text: str) -> str:
        held: list[str] = []

        def hold(markup: str) -> str:
            held.append(markup)
            return f"\x00{len(held) - 1}\x00"

        text = html.escape(text, quote=False)
        text = re.sub(r"\{\{([a-z-]+):([^}]*)\}\}", lambda m: hold(self.site.inline_macro(m.group(1), m.group(2), self)), text)
        text = re.sub(r"\{\{([a-z-]+)\}\}", lambda m: hold(self.site.inline_macro(m.group(1), "", self)), text)
        text = re.sub(
            r"!\[([^\]]*)\]\(([^)\s]+)\)",
            lambda m: hold(f'<img src="{esc(self.site.link(m.group(2), self))}" alt="{esc(html.unescape(m.group(1)))}" class="inline-img">'),
            text,
        )
        text = re.sub(
            r"\[([^\]]+)\]\(([^)\s]+)\)",
            lambda m: hold(f'<a href="{esc(self.site.link(m.group(2), self))}">{self._emphasis(m.group(1))}</a>'),
            text,
        )
        text = self._emphasis(text)
        return re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], text)

    @staticmethod
    def _emphasis(text: str) -> str:
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)

    # Blocks ---------------------------------------------------------------

    def heading_id(self, text: str) -> str:
        base = slugify(text)
        candidate, number = base, 2
        while candidate in self.used_ids:
            candidate, number = f"{base}-{number}", number + 1
        self.used_ids.add(candidate)
        return candidate

    def blocks(self, source) -> str:
        lines = source.splitlines() if isinstance(source, str) else list(source)
        out: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not stripped:
                i += 1
                continue
            if stripped.startswith("```"):
                j = i + 1
                body = []
                while j < len(lines) and not lines[j].strip().startswith("```"):
                    body.append(lines[j])
                    j += 1
                out.append("<pre><code>" + esc("\n".join(body)) + "</code></pre>")
                i = j + 1
                continue
            if stripped.startswith(":::") and len(stripped) > 3:
                kind, _, title = stripped[3:].partition(" ")
                depth, j, body = 1, i + 1, []
                while j < len(lines):
                    inner = lines[j].strip()
                    if inner.startswith(":::") and len(inner) > 3:
                        depth += 1
                    elif inner == ":::":
                        depth -= 1
                        if depth == 0:
                            break
                    body.append(lines[j])
                    j += 1
                if depth:
                    fail(f"{self.page}: unclosed ::: block")
                out.append(self.container(kind, title.strip(), body))
                i = j + 1
                continue
            heading = re.match(r"^(#{1,4})\s+(.*)$", line)
            if heading:
                level = len(heading.group(1))
                inner = self.inline(heading.group(2).strip())
                anchor = self.heading_id(plain(inner))
                if level == 2:
                    self.toc.append((anchor, plain(inner)))
                link = f' <a class="anchor" href="#{anchor}" aria-label="Link to this section">#</a>' if level > 1 else ""
                out.append(f'<h{level} id="{anchor}">{inner}{link}</h{level}>')
                i += 1
                continue
            if re.match(r"^-{3,}$", stripped):
                out.append("<hr>")
                i += 1
                continue
            macro = BLOCK_MACRO_RE.match(stripped)
            if macro:
                out.append(self.site.block_macro(macro.group(1), macro.group(2) or "", self))
                i += 1
                continue
            if stripped.startswith("|") and i + 1 < len(lines) and TABLE_RULE_RE.match(lines[i + 1]):
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|"):
                    j += 1
                out.append(self.table(lines[i], lines[i + 2 : j]))
                i = j
                continue
            if stripped.startswith(">"):
                j, body = i, []
                while j < len(lines) and lines[j].strip().startswith(">"):
                    body.append(re.sub(r"^\s*> ?", "", lines[j]))
                    j += 1
                out.append("<blockquote>" + self.blocks(body) + "</blockquote>")
                i = j
                continue
            if LIST_RE.match(line):
                markup, i = self.list_block(lines, i)
                out.append(markup)
                continue
            j, body = i, []
            while j < len(lines):
                current = lines[j]
                text = current.strip()
                if not text or (j > i and (re.match(r"^(#{1,4})\s", current) or LIST_RE.match(current) or text.startswith(("```", ":::", ">", "|")) or BLOCK_MACRO_RE.match(text))):
                    break
                body.append(text)
                j += 1
            out.append("<p>" + self.inline(" ".join(body)) + "</p>")
            i = j
        return "\n".join(out)

    def container(self, kind: str, title: str, body: list[str]) -> str:
        inner = self.blocks(body)
        if kind == "spoiler":
            return f'<details class="spoiler"><summary>{self.inline(title or "Spoiler")}</summary>{inner}</details>'
        if kind in ("note", "tip", "warning", "example"):
            label = title or {"note": "Note", "tip": "Tip", "warning": "Heads up", "example": "Worked example"}[kind]
            return f'<aside class="callout callout-{kind}"><p class="callout-title">{self.inline(label)}</p>{inner}</aside>'
        fail(f"{self.page}: unknown ::: block {kind}")
        return ""

    def table(self, header: str, rows: list[str]) -> str:
        def cells(line: str) -> list[str]:
            line = line.strip()
            if line.startswith("|"):
                line = line[1:]
            if line.endswith("|"):
                line = line[:-1]
            return [cell.strip() for cell in line.split("|")]

        head = "".join(f"<th>{self.inline(cell)}</th>" for cell in cells(header))
        body = "".join("<tr>" + "".join(f"<td>{self.inline(cell)}</td>" for cell in cells(row)) + "</tr>" for row in rows)
        return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

    def list_block(self, lines: list[str], i: int) -> tuple[str, int]:
        first = LIST_RE.match(lines[i])
        base = indent_of(lines[i])
        ordered = first.group(2)[0].isdigit()
        items: list[list[str]] = []
        content_indent = base + len(first.group(2)) + 1
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and items and (indent_of(lines[j]) > base or (LIST_RE.match(lines[j]) and indent_of(lines[j]) == base)):
                    i = j
                    continue
                break
            match = LIST_RE.match(line)
            current = indent_of(line)
            if match and current == base and (match.group(2)[0].isdigit()) == ordered:
                items.append([match.group(3)])
                content_indent = base + len(match.group(2)) + 1
                i += 1
                continue
            if current > base and items:
                items[-1].append(line[min(current, content_indent) :])
                i += 1
                continue
            break
        leads = []
        for body in items:
            lead = [body[0]]
            rest_start = 1
            while rest_start < len(body) and not LIST_RE.match(body[rest_start]) and body[rest_start].strip():
                lead.append(body[rest_start].strip())
                rest_start += 1
            leads.append((" ".join(lead), rest_start))
        terms = [term_split(lead) for lead, _ in leads]
        as_terms = not ordered and len(items) >= 3 and all(terms)
        rendered = []
        for body, (lead, rest_start), term in zip(items, leads, terms):
            if as_terms:
                markup = f'<span class="term">{self.inline(term[0])}</span> {self.inline(term[1])}'
            else:
                markup = self.inline(lead)
            if rest_start < len(body):
                markup += self.blocks(body[rest_start:])
            rendered.append(f"<li>{markup}</li>")
        tag = "ol" if ordered else "ul"
        opening = '<ul class="terms">' if as_terms else f"<{tag}>"
        return opening + "".join(rendered) + f"</{tag}>", i


# --------------------------------------------------------------------------
# Site
# --------------------------------------------------------------------------


class Site:
    def __init__(self, data: dict, export: Path, captures: Path, out: Path, steam_out: Path):
        self.data = data
        self.export = export
        self.captures = captures
        self.out = out
        self.steam_out = steam_out
        self.perks = data["perks"]
        self.supplies = data["supplies"]
        self.skills = data["skills"]
        self.perk_by_id = {perk["id"]: perk for perk in self.perks}
        self.supply_by_id = {item["id"]: item for item in self.supplies}
        self.skill_by_id = {skill["id"]: skill for skill in self.skills}
        self.mode_by_id = {mode["id"]: mode for mode in data["modes"]}
        self.rarity_by_id = {rarity["id"]: rarity for rarity in data["rarities"]}
        self.branch_by_id = {branch["id"]: branch for branch in data["skillBranches"]}
        self.pages: dict[str, dict] = {}
        self.shots = read_screenshots(CONTENT / "screenshots.tsv")
        self.used_shots: set[str] = set()
        self.search: list[dict] = []
        self.written: list[Path] = []
        self.version = data["game"]["version"]
        maluses = sum(1 for perk in self.perks if perk["rarity"] == "malus")
        data["counts"] = {
            "perks": len(self.perks),
            "positivePerks": len(self.perks) - maluses,
            "maluses": maluses,
            "legendaryPerks": sum(1 for perk in self.perks if perk["rarity"] == "legendary"),
            "supplies": len(self.supplies),
            "skills": len(self.skills),
            "achievements": len(data["achievements"]) + data["hiddenAchievementCount"],
        }

    # Links and macros -------------------------------------------------------

    def link(self, target: str, renderer: Renderer) -> str:
        if re.match(r"^[a-z]+://", target) or target.startswith(("mailto:", "#")):
            return target
        if target.startswith("shot:"):
            return renderer.root + "img/screens/" + self.screenshot(target[5:])["key"] + ".png"
        path, _, anchor = target.partition("#")
        if path.endswith(".md"):
            slug = Path(path).stem
            if slug not in self.pages and slug not in ("perks", "supplies", "skills", "index"):
                fail(f"{renderer.page}: link to unknown page {target}")
            path = slug + ".html"
        return renderer.root + path + (("#" + anchor) if anchor else "")

    def screenshot(self, key: str) -> dict:
        if key not in self.shots:
            fail(f"unknown screenshot key {key}; add it to hop-wiki/content/screenshots.tsv")
        self.used_shots.add(key)
        return self.shots[key]

    def lookup(self, path: str):
        value = self.data
        for part in path.split("."):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                fail(f"unknown data path {path}")
        return value

    def perk_ref(self, perk_id: str, renderer: Renderer) -> str:
        perk = self.perk_by_id.get(perk_id) or fail(f"{renderer.page}: unknown perk {perk_id}")
        label = perk["rarityLabel"] if perk["rarity"] == "malus" else perk["rarityLabel"] + " perk"
        return (
            f'<a class="ref rarity-{perk["rarity"]}" href="{renderer.root}perks/{perk_id}.html" title="{esc(label)}">'
            f'<img src="{renderer.root}img/{perk["icon"]}" alt="" class="ref-icon">{esc(perk["name"])}</a>'
        )

    def supply_ref(self, item_id: str, renderer: Renderer) -> str:
        item = self.supply_by_id.get(item_id) or fail(f"{renderer.page}: unknown supply {item_id}")
        return (
            f'<a class="ref rarity-{item["rarity"]}" href="{renderer.root}supplies.html#{item_id}" title="{esc(item["rarityLabel"])} supply">'
            f'<img src="{renderer.root}img/{item["icon"]}" alt="" class="ref-icon">{esc(item["name"])}</a>'
        )

    def skill_ref(self, skill_id: str, renderer: Renderer) -> str:
        skill = self.skill_by_id.get(skill_id) or fail(f"{renderer.page}: unknown skill {skill_id}")
        return (
            f'<a class="ref ref-skill" href="{renderer.root}skills.html#{skill_id}" title="Skill tree: {esc(skill["branchName"])}">'
            f'<img src="{renderer.root}img/{skill["icon"]}" alt="" class="ref-icon">{esc(skill["name"])}</a>'
        )

    def inline_macro(self, name: str, argument: str, renderer: Renderer) -> str:
        if name == "perk":
            return self.perk_ref(argument, renderer)
        if name == "supply":
            return self.supply_ref(argument, renderer)
        if name == "skill":
            return self.skill_ref(argument, renderer)
        if name == "mode":
            mode = self.mode_by_id.get(argument) or fail(f"{renderer.page}: unknown mode {argument}")
            if mode.get("private") and renderer.page != SPOILER_PAGE:
                fail(f"{renderer.page}: spoiler mode {argument} outside the spoiler page")
            return f'<strong class="mode-name">{esc(mode["name"])}</strong>'
        if name == "n":
            value = self.lookup(argument)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return f"{value:,}" if abs(value) >= 10000 else str(value)
            return esc(value)
        if name == "page":
            page = self.pages.get(argument) or fail(f"{renderer.page}: link to unknown page {argument}")
            if page.get("hidden"):
                fail(f"{renderer.page}: link to hidden page {argument}")
            return f'<a href="{renderer.root}{argument}.html">{esc(page["title"])}</a>'
        if name == "version":
            return esc(self.version)
        if name == "rarity":
            rarity = self.rarity_by_id.get(argument) or fail(f"{renderer.page}: unknown rarity {argument}")
            return f'<span class="pill rarity-{argument}">{esc(rarity["label"])}</span>'
        if name == "branch":
            branch = self.branch_by_id.get(argument) or fail(f"{renderer.page}: unknown skill tab {argument}")
            return f'<strong class="branch-name">{esc(branch["name"])}</strong>'
        fail(f"{renderer.page}: unknown inline macro {name}")
        return ""

    def figure(self, key: str, renderer: Renderer, wide: bool = True) -> str:
        shot = self.screenshot(key)
        source = f"{renderer.root}img/screens/{key}.png"
        caption = renderer.inline(shot["caption"])
        return (
            f'<figure class="shot"><a href="{source}"><img src="{source}" alt="{esc(plain(caption))}" loading="lazy" width="1920" height="1080"></a>'
            f"<figcaption>{caption}</figcaption></figure>"
        )

    def block_macro(self, name: str, argument: str, renderer: Renderer) -> str:
        data = self.data
        if name == "shot":
            return self.figure(argument, renderer)
        if name == "modes-table":
            rows = []
            for mode in data["modes"]:
                if mode.get("private"):
                    continue
                unlock = "; ".join(esc(task) for task in mode["unlock"]) or "Available from the start"
                rows.append(
                    f'<tr id="mode-{esc(mode["id"])}"><th scope="row">{esc(mode["name"])}</th><td>{mode["targetScore"]}</td>'
                    f'<td>{mode["handSize"]}</td><td>{esc(mode["description"])}</td><td>{unlock}</td></tr>'
                )
            return (
                '<div class="table-wrap"><table><thead><tr><th>Mode</th><th>Target</th><th>Bones per hand</th><th>In the game</th>'
                "<th>How to unlock</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
            )
        if name == "spoiler-modes":
            if renderer.page != SPOILER_PAGE:
                fail(f"{renderer.page}: spoiler modes may only appear on the spoiler page")
            items = []
            for mode in data["modes"]:
                if mode.get("spoiler"):
                    unlock = "; ".join(esc(task) for task in mode["unlock"])
                    items.append(f'<li><strong>{esc(mode["name"])}</strong> &mdash; {esc(mode["description"])} <em>Unlock:</em> {unlock}.</li>')
            return "<ul>" + "".join(items) + "</ul>"
        if name == "custom-modifiers":
            rows = "".join(f'<tr><th scope="row">{esc(m["name"])}</th><td>{esc(m["description"])}</td></tr>' for m in data["customModifiers"])
            return f'<div class="table-wrap"><table><thead><tr><th>Modifier</th><th>Effect</th></tr></thead><tbody>{rows}</tbody></table></div>'
        if name == "rival-levels":
            rows = "".join(f'<tr><th scope="row">{esc(level["name"])}</th><td>{esc(level["description"])}</td></tr>' for level in data["rivalLevels"])
            return f'<div class="table-wrap"><table><thead><tr><th>Skill level</th><th>In the game</th></tr></thead><tbody>{rows}</tbody></table></div>'
        if name == "rival-styles":
            rows = "".join(f'<tr><th scope="row">{esc(style["name"])}</th><td>{esc(style["description"])}</td></tr>' for style in data["rivalStyles"])
            return f'<div class="table-wrap"><table><thead><tr><th>Style</th><th>Table plan</th></tr></thead><tbody>{rows}</tbody></table></div>'
        if name == "bone-boxes":
            cards = []
            for box in data["boneBoxes"]:
                odds = ", ".join(f'{esc(row["rarityLabel"])} {row["percent"]}%' for row in box["odds"])
                guarantee = f' The first supply is always {esc(box["guaranteedMinimum"])} or better.' if box.get("guaranteedMinimum") else ""
                cards.append(
                    f'<div class="mini-card rarity-{box["rarity"]}"><img src="{renderer.root}img/{box["icon"]}" alt="" class="mini-icon">'
                    f'<div><strong>{esc(box["name"])}</strong><br><span class="muted">{box["price"]} Bone Bucks &middot; '
                    f'{box["rewardCount"]} supplies inside &middot; hold up to {box["maxOwned"]}<br>Odds per supply: {odds}.{guarantee}</span></div></div>'
                )
            return '<div class="mini-grid">' + "".join(cards) + "</div>"
        if name == "achievements":
            cards = []
            for entry in data["achievements"]:
                cards.append(
                    f'<div class="mini-card"><img src="{renderer.root}img/{entry["icon"]}" alt="" class="mini-icon">'
                    f'<div><strong>{esc(entry["name"])}</strong><br><span class="muted">{esc(entry["description"])}</span></div></div>'
                )
            hidden = data["hiddenAchievementCount"]
            note = f'<p class="muted">Plus {hidden} hidden achievements. This wiki does not list them; finding them is part of the fun.</p>' if hidden else ""
            return '<div class="mini-grid">' + "".join(cards) + "</div>" + note
        if name == "legendary-trials":
            rows = []
            for perk in self.perks:
                if perk.get("trials"):
                    trials = "".join(f"<li>{esc(task)}</li>" for task in perk["trials"])
                    rows.append(f"<tr><th scope=\"row\">{self.perk_ref(perk['id'], renderer)}</th><td><ul class=\"compact\">{trials}</ul></td></tr>")
            return f'<div class="table-wrap"><table><thead><tr><th>Legendary perk</th><th>Career trials</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
        if name == "perk-prices":
            prices = data["economy"]["perkPrices"]
            rows = "".join(
                f'<tr><th scope="row"><span class="pill rarity-{rarity}">{esc(self.rarity_by_id[rarity]["label"])}</span></th><td>{prices[rarity]:,}</td></tr>'
                for rarity in RARITY_ORDER
                if rarity in prices
            )
            return f'<div class="table-wrap"><table><thead><tr><th>Rarity</th><th>Bone Bucks to unlock</th></tr></thead><tbody>{rows}</tbody></table></div>'
        if name == "skill-branches":
            cards = []
            for branch in data["skillBranches"]:
                count = sum(1 for skill in self.skills if skill["branch"] == branch["id"])
                cards.append(
                    f'<div class="mini-card"><img src="{renderer.root}img/{branch["icon"]}" alt="" class="mini-icon">'
                    f'<div><strong>{esc(branch["name"])}</strong><br><span class="muted">{count} skills &middot; '
                    f'<a href="{renderer.root}skills.html#tab-{branch["id"]}">see the tab</a></span></div></div>'
                )
            return '<div class="mini-grid">' + "".join(cards) + "</div>"
        if name == "rarity-legend":
            pills = "".join(f'<span class="pill rarity-{r["id"]}">{esc(r["label"])}</span> ' for r in data["rarities"])
            return f'<p class="legend">{pills}</p>'
        fail(f"{renderer.page}: unknown block macro {name}")
        return ""

    # Page shell -------------------------------------------------------------

    def nav(self, current: str, root: str) -> str:
        groups = []
        for section in SECTIONS:
            entries = sorted((page for page in self.pages.values() if page["section"] == section and not page.get("hidden")), key=lambda page: (page["order"], page["title"]))
            if not entries:
                continue
            links = "".join(
                f'<li><a href="{root}{page["slug"]}.html"{" aria-current=\"page\"" if page["slug"] == current else ""}>{esc(page["title"])}</a></li>'
                for page in entries
            )
            groups.append(f'<p class="nav-heading">{esc(section)}</p><ul>{links}</ul>')
        return "".join(groups)

    def shell(self, title: str, body: str, current: str, root: str, description: str, toc=None) -> str:
        toc_html = ""
        if toc and len(toc) >= 3:
            items = "".join(f'<li><a href="#{anchor}">{esc(text)}</a></li>' for anchor, text in toc)
            toc_html = f'<nav class="toc" aria-label="On this page"><p class="nav-heading">On this page</p><ul>{items}</ul></nav>'
        full_title = SITE_NAME if current == "index" else f"{title} - {SITE_NAME}"
        return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="color-scheme" content="dark">
<link rel="icon" type="image/png" href="{root}img/site/favicon.png">
</head>
<body data-root="{root}">
<a class="skip" href="#content">Skip to content</a>
<header class="topbar">
  <a class="brand" href="{root}index.html"><img src="{root}img/site/logo.png" alt="" width="40" height="40"><span>House of Pips <small>Wiki</small></span></a>
  <div class="search" role="search">
    <label class="visually-hidden" for="search-box">Search the wiki</label>
    <input id="search-box" type="search" placeholder="Search perks, rules, modes..." autocomplete="off" spellcheck="false">
    <ol id="search-results" class="search-results" hidden></ol>
  </div>
  <button class="nav-toggle" type="button" aria-controls="sidebar" aria-expanded="false">Menu</button>
</header>
<div class="layout">
  <nav id="sidebar" class="sidebar" aria-label="Wiki pages">{self.nav(current, root)}</nav>
  <main id="content" class="content">
{body}
  </main>
  {toc_html}
</div>
<footer class="footer">
  <p>Player guide for House of Pips {esc(self.version)}, built from the game's own catalogues. House of Pips is made by Slapcraft Games.</p>
</footer>
</body>
</html>
"""

    def write(self, relative: str, markup: str) -> None:
        path = self.out / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markup, encoding="utf-8", newline="\n")
        self.written.append(path)

    def index_entry(self, title: str, url: str, section: str, text: str, kind: str = "page") -> None:
        self.search.append({"t": title, "u": url, "s": section, "k": kind, "x": text[:600]})

    # Catalogue pages ----------------------------------------------------------

    def charges_text(self, perk: dict) -> str | None:
        charges = perk.get("charges")
        if not charges:
            return None
        if charges["scope"] == "draft":
            text = "Once per draft for each copy you hold." if charges["perCopy"] else "Once per draft, shared by all copies."
        elif charges["perCopy"]:
            text = "One use per hand for each copy you hold. Uses refill at the start of every hand."
        else:
            text = "One use per hand no matter how many copies you hold."
        if charges.get("cooldownHands"):
            hands = charges["cooldownHands"]
            text += f" After you use it, it rests for the next {hands} hand{'s' if hands != 1 else ''}."
        return text

    def unlock_text(self, perk: dict) -> str:
        rarity = perk["rarity"]
        if rarity == "malus":
            return "Never bought. A Malus card is dealt into every standard draft."
        if perk.get("starter"):
            return "Unlocked from the start of every career."
        price = perk.get("unlockPrice")
        if perk.get("trials"):
            trials = "; ".join(perk["trials"])
            return f"Complete its three career trials ({trials}), then unlock it for {price:,} Bone Bucks."
        index = RARITY_ORDER.index(rarity)
        if index == 0:
            return f"Unlock it in the Perks compendium for {price:,} Bone Bucks."
        previous = self.rarity_by_id[RARITY_ORDER[index - 1]]["label"]
        requirement = self.data["economy"]["rarityUnlockRequirement"]
        return f"Unlock it in the Perks compendium for {price:,} Bone Bucks once you own {requirement} {previous} perks."

    def perk_pages(self, notes: dict[str, str]) -> None:
        by_rarity: dict[str, list[dict]] = {rarity: [] for rarity in RARITY_ORDER}
        for perk in self.perks:
            if perk["rarity"] not in by_rarity:
                fail(f"perk {perk['id']} has unknown rarity {perk['rarity']}")
            by_rarity[perk["rarity"]].append(perk)
        ordered = [perk for rarity in RARITY_ORDER for perk in by_rarity[rarity]]
        for index, perk in enumerate(ordered):
            renderer = Renderer(self, "perk-" + perk["id"], "../")
            how = renderer.blocks(notes[perk["id"]])
            rarity = self.rarity_by_id[perk["rarity"]]
            facts = [
                ("Rarity", f'<span class="pill rarity-{perk["rarity"]}">{esc(rarity["label"])}</span>'),
                ("Type", esc(perk["kind"])),
            ]
            if perk["scoringPlayOnly"]:
                facts.append(("Needs a scoring play", "Yes. It only fires when the open-end total is a positive multiple of 5."))
            charges = self.charges_text(perk)
            if charges:
                facts.append(("Uses", esc(charges)))
            facts.append(("How to get it", esc(self.unlock_text(perk))))
            fact_rows = "".join(f'<tr><th scope="row">{label}</th><td>{value}</td></tr>' for label, value in facts)
            previous = ordered[index - 1] if index > 0 else None
            following = ordered[index + 1] if index + 1 < len(ordered) else None
            pager = '<nav class="pager" aria-label="Neighbouring perks">'
            pager += f'<a href="{previous["id"]}.html">&larr; {esc(previous["name"])}</a>' if previous else "<span></span>"
            pager += f'<a href="{following["id"]}.html">{esc(following["name"])} &rarr;</a>' if following else "<span></span>"
            pager += "</nav>"
            label = rarity["label"] if perk["rarity"] == "malus" else rarity["label"] + " perk"
            body = f"""<p class="crumbs"><a href="../perks.html">Perks</a> &rsaquo; <a href="../perks.html#{perk['rarity']}">{esc(rarity['label'])}</a></p>
<article class="entry rarity-{perk['rarity']}" id="perk-{perk['id']}">
<header class="entry-head">
<img class="entry-icon" src="../img/{perk['icon']}" alt="" width="96" height="96">
<div><h1>{esc(perk['name'])}</h1><p class="entry-sub">{esc(label)} &middot; {esc(perk['kind'])}</p></div>
</header>
<div class="entry-body">
<div class="entry-main">
<blockquote class="card-text"><p>{esc(perk['description'])}</p><footer>In-game card text</footer></blockquote>
<h2 id="how-it-works">How it works</h2>
{how}
<h2 id="at-a-glance">At a glance</h2>
<div class="table-wrap"><table class="facts"><tbody>{fact_rows}</tbody></table></div>
</div>
<figure class="entry-card"><a href="../img/{perk['card']}"><img src="../img/{perk['card']}" alt="The {esc(perk['name'])} card as drawn in the game" width="468" height="498" loading="lazy"></a><figcaption>The card as it appears in a draft.</figcaption></figure>
</div>
</article>
{pager}"""
            self.write(
                f"perks/{perk['id']}.html",
                self.shell(perk["name"], body, "perks", "../", f"{perk['name']} ({label}) in House of Pips: {perk['description']}"),
            )
            self.index_entry(perk["name"], f"perks/{perk['id']}.html", label, perk["description"] + " " + plain(how), "perk")

        renderer = Renderer(self, "perks", "")
        intro = renderer.blocks((CONTENT / "catalogue" / "perks-intro.md").read_text(encoding="utf-8"))
        kinds = sorted({perk["kind"] for perk in self.perks})
        filters = '<div class="filters" data-filter-root="perk-list"><span class="filter-label">Rarity</span>'
        filters += '<button type="button" class="chip" data-filter="rarity" data-value="" aria-pressed="true">All</button>'
        for rarity in RARITY_ORDER:
            filters += f'<button type="button" class="chip rarity-{rarity}" data-filter="rarity" data-value="{rarity}" aria-pressed="false">{esc(self.rarity_by_id[rarity]["label"])}</button>'
        filters += '<span class="filter-label">Type</span><select data-filter="kind" aria-label="Filter by type"><option value="">Any type</option>'
        filters += "".join(f'<option value="{esc(kind)}">{esc(kind)}</option>' for kind in kinds)
        filters += '</select><input type="search" data-filter="text" placeholder="Filter by name or text" aria-label="Filter perks by text"></div>'
        groups = []
        for rarity in RARITY_ORDER:
            label = self.rarity_by_id[rarity]["label"]
            cards = []
            for perk in by_rarity[rarity]:
                cards.append(
                    f'<li class="perk-tile rarity-{rarity}" data-rarity="{rarity}" data-kind="{esc(perk["kind"])}" data-id="{perk["id"]}" '
                    f'data-text="{esc((perk["name"] + " " + perk["description"]).lower())}">'
                    f'<a href="perks/{perk["id"]}.html"><img src="img/{perk["icon"]}" alt="" width="64" height="64" loading="lazy">'
                    f'<span class="tile-name">{esc(perk["name"])}</span><span class="tile-kind">{esc(perk["kind"])}</span>'
                    f'<span class="tile-text">{esc(perk["description"])}</span></a></li>'
                )
            heading = f"{label} ({len(by_rarity[rarity])})" if rarity == "malus" else f"{label} perks ({len(by_rarity[rarity])})"
            groups.append(f'<section class="perk-group" data-group="{rarity}"><h2 id="{rarity}">{esc(heading)}</h2><ul class="perk-grid">{"".join(cards)}</ul></section>')
        body = f'<h1>Perks</h1>\n{intro}\n{filters}\n<div id="perk-list">{"".join(groups)}</div><p class="muted" id="perk-empty" hidden>No perk matches those filters.</p>'
        self.write("perks.html", self.shell("Perks", body, "perks", "", "Every perk and malus in House of Pips with icons, rarities and exact rules."))
        self.index_entry("Perks", "perks.html", "Perks and items", plain(intro))

    def supplies_page(self, notes: dict[str, str]) -> None:
        renderer = Renderer(self, "supplies", "")
        intro = renderer.blocks((CONTENT / "catalogue" / "supplies-intro.md").read_text(encoding="utf-8"))
        entries = []
        for item in self.supplies:
            how = renderer.blocks(notes[item["id"]])
            price = f'{item["price"]:,} Bone Bucks in the Supply Shop' if item["purchasable"] else "Not sold in the shop: found in Bone Boxes and on the Slap Track"
            duration = f'<tr><th scope="row">Lasts</th><td>{item["matches"]} match{"es" if item["matches"] != 1 else ""}</td></tr>' if item.get("matches") else ""
            entries.append(
                f"""<article class="entry rarity-{item['rarity']}" id="{item['id']}">
<header class="entry-head"><img class="entry-icon" src="img/{item['icon']}" alt="" width="80" height="80">
<div><h2>{esc(item['name'])}</h2><p class="entry-sub"><span class="pill rarity-{item['rarity']}">{esc(item['rarityLabel'])}</span> {esc(item['category'])}</p></div></header>
<blockquote class="card-text"><p>{esc(item['description'])}</p><footer>In-game text &middot; {esc(item['timing'])}</footer></blockquote>
{how}
<div class="table-wrap"><table class="facts"><tbody>
<tr><th scope="row">Where to get it</th><td>{esc(price)}</td></tr>
<tr><th scope="row">Most you can hold</th><td>{item['maxOwned']}</td></tr>{duration}
</tbody></table></div>
</article>"""
            )
            self.index_entry(item["name"], f"supplies.html#{item['id']}", "Supply", item["description"] + " " + plain(how), "supply")
        body = f"<h1>Supplies</h1>\n{intro}\n" + "\n".join(entries)
        self.write("supplies.html", self.shell("Supplies", body, "supplies", "", "Every House of Pips supply: what it does, when to use it and where to get it.", renderer.toc))

    def skills_page(self, notes: dict[str, str]) -> None:
        renderer = Renderer(self, "skills", "")
        intro = renderer.blocks((CONTENT / "catalogue" / "skills-intro.md").read_text(encoding="utf-8"))
        sections = []
        toc = []
        for branch in self.data["skillBranches"]:
            entries = []
            for skill in self.skills:
                if skill["branch"] != branch["id"]:
                    continue
                how = renderer.blocks(notes[skill["id"]])
                requires = ", ".join(f'{esc(r["name"])} rank {r["rank"]}' for r in skill["requires"]) or "Nothing: it is a starting skill on this tab"
                entries.append(
                    f"""<article class="entry skill" id="{skill['id']}">
<header class="entry-head"><img class="entry-icon" src="img/{skill['icon']}" alt="" width="72" height="72">
<div><h3>{esc(skill['name'])}</h3><p class="entry-sub">{esc(branch['name'])} &middot; up to rank {skill['maxRank']}</p></div></header>
<blockquote class="card-text"><p>{esc(skill['description'])}</p><footer>In-game text</footer></blockquote>
{how}
<p class="muted"><strong>Requires:</strong> {requires}.</p>
</article>"""
                )
                self.index_entry(skill["name"], f"skills.html#{skill['id']}", f"Skill · {branch['name']}", skill["description"] + " " + plain(how), "skill")
            anchor = f"tab-{branch['id']}"
            toc.append((anchor, branch["name"]))
            shot_key = f"skill-tree-{branch['id']}"
            shot = self.figure(shot_key, renderer) if shot_key in self.shots else ""
            sections.append(
                f'<section class="branch"><h2 id="{anchor}"><img src="img/{branch["icon"]}" alt="" width="40" height="40" class="branch-icon"> {esc(branch["name"])}</h2>{shot}{"".join(entries)}</section>'
            )
        body = f"<h1>Skill tree</h1>\n{intro}\n" + "\n".join(sections)
        self.write("skills.html", self.shell("Skill tree", body, "skills", "", "Every House of Pips skill on the Table Sense, Fortune and House Rules tabs.", toc))

    # Hand-written pages ---------------------------------------------------------

    def load_pages(self) -> list[tuple[dict, str]]:
        loaded = []
        private_pages = sorted((PRIVATE / "pages").glob("*.md")) if (PRIVATE / "pages").is_dir() else []
        for path in sorted((CONTENT / "pages").glob("*.md")) + private_pages:
            meta, text = read_front_matter(path)
            for key in ("title", "section", "order", "description"):
                if key not in meta:
                    fail(f"{path.name}: front matter needs {key}")
            slug = meta.get("slug", path.stem)
            if slug != path.stem:
                fail(f"{path.name}: slug must match the file name")
            if meta["section"] not in SECTIONS:
                fail(f"{path.name}: unknown section {meta['section']}")
            # `hidden: true` keeps a page's source and build checks but leaves it
            # out of the navigation, search and the website data.
            if meta.get("hidden", "false") not in ("true", "false"):
                fail(f"{path.name}: hidden must be true or false")
            page = {"slug": slug, "title": meta["title"], "section": meta["section"], "order": int(meta["order"]), "description": meta["description"], "hidden": meta.get("hidden") == "true"}
            if slug in self.pages:
                fail(f"page {slug} defined twice")
            self.pages[slug] = page
            loaded.append((page, text))
        for slug, title, order in (("perks", "Perks", 10), ("supplies", "Supplies", 20), ("skills", "Skill tree", 30)):
            if slug in self.pages:
                fail(f"pages/{slug}.md clashes with a generated page")
            self.pages[slug] = {"slug": slug, "title": title, "section": "Perks and items", "order": order, "description": ""}
        if "index" not in self.pages:
            fail("hop-wiki/content/pages/index.md is required")
        if SPOILER_PAGE in self.pages and not self.pages[SPOILER_PAGE].get("hidden"):
            fail("the spoiler page must stay hidden: it lives in hop-wiki/private/, which is never published")
        return loaded

    def render_pages(self, loaded: list[tuple[dict, str]]) -> None:
        for page, text in loaded:
            renderer = Renderer(self, page["slug"], "")
            body = renderer.blocks(text)
            if not re.search(r"<h1[ >]", body):
                body = f"<h1>{esc(page['title'])}</h1>\n" + body
            self.write(page["slug"] + ".html", self.shell(page["title"], body, page["slug"], "", page["description"], renderer.toc))
            # Search results quote page text, so the spoiler page is indexed by
            # its description only and never surfaces its contents.
            unspoiled = re.sub(r'<details class="spoiler">.*?</details>', " ", body, flags=re.S)
            text = page["description"] if page["slug"] == SPOILER_PAGE else plain(unspoiled)
            if not page.get("hidden"):
                self.index_entry(page["title"], page["slug"] + ".html", page["section"], text, "page")

    # Assets ---------------------------------------------------------------------

    def copy_assets(self) -> None:
        pictures = set()
        for perk in self.perks:
            pictures.update((perk["icon"], perk["card"]))
        for collection in (self.supplies, self.skills, self.data["skillBranches"], self.data["boneBoxes"], self.data["achievements"]):
            for entry in collection:
                pictures.add(entry["icon"])
        pictures.update(("site/logo.png", "site/favicon.png"))
        for relative in sorted(pictures):
            source = self.export / relative
            if not source.is_file():
                fail(f"missing picture {relative}; add it to public/hop/wiki-data/img/")
            target = self.out / "img" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        for key in sorted(self.used_shots):
            source = self.captures / f"{key}.png"
            if not source.is_file():
                fail(f"missing screenshot {key}.png; add it to public/hop/wiki-data/img/screens/")
            target = self.out / "img" / "screens" / f"{key}.png"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        unused = sorted(set(self.shots) - self.used_shots)
        if unused:
            fail(f"screenshots.tsv lists captures no page shows: {', '.join(unused)}")

    # Steam guide ------------------------------------------------------------------

    def bbcode_inline(self, text: str) -> str:
        text = re.sub(r"\{\{perk:([a-z0-9_]+)\}\}", lambda m: self.perk_by_id[m.group(1)]["name"], text)
        text = re.sub(r"\{\{supply:([a-z0-9_]+)\}\}", lambda m: self.supply_by_id[m.group(1)]["name"], text)
        text = re.sub(r"\{\{skill:([a-z0-9_]+)\}\}", lambda m: self.skill_by_id[m.group(1)]["name"], text)
        text = re.sub(r"\{\{page:([a-z0-9-]+)\}\}", lambda m: "the wiki's " + self.pages[m.group(1)]["title"] + " page", text)
        text = re.sub(r"\{\{n:([a-zA-Z0-9_.]+)\}\}", lambda m: str(self.lookup(m.group(1))), text)
        text = re.sub(r"\{\{rarity:([a-z]+)\}\}", lambda m: self.rarity_by_id[m.group(1)]["label"], text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"\*\*(.+?)\*\*", r"[b]\1[/b]", text)
        text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"[i]\1[/i]", text)
        if "{{" in text:
            fail(f"Steam guide: unconverted macro in {text!r}")
        return text.replace("`", "")

    def bbcode(self, markdown: str) -> str:
        """Converts perk notes to Steam guide BBCode. Wrapped lines are joined
        into paragraphs and list items first, so emphasis may span lines."""
        blocks: list[tuple[str, str]] = []
        for line in markdown.splitlines():
            text = line.strip()
            item = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.*)$", line)
            if not text:
                blocks.append(("blank", ""))
            elif text.startswith(":::"):
                kind, _, title = text[3:].partition(" ")
                blocks.append(("label", (title or "Worked example") if kind else ""))
            elif item:
                blocks.append(("item", item.group(1).strip()))
            elif blocks and blocks[-1][0] in ("item", "text"):
                blocks[-1] = (blocks[-1][0], blocks[-1][1] + " " + text)
            else:
                blocks.append(("text", text))
        lines: list[str] = []
        in_list = False
        for kind, text in blocks:
            if kind != "item" and in_list:
                lines.append("[/list]")
                in_list = False
            if kind == "item":
                if not in_list:
                    lines.append("[list]")
                    in_list = True
                lines.append("[*]" + self.bbcode_inline(text))
            elif kind == "label" and text:
                lines.append(f"[b]{self.bbcode_inline(text)}:[/b]")
            elif kind == "text":
                lines.append(self.bbcode_inline(text))
            elif kind == "blank" and lines and lines[-1] != "":
                lines.append("")
        if in_list:
            lines.append("[/list]")
        return "\n".join(lines).strip()

    def steam_guide(self, notes: dict[str, str]) -> None:
        self.steam_out.mkdir(parents=True, exist_ok=True)
        sections = []
        for rarity in RARITY_ORDER:
            label = self.rarity_by_id[rarity]["label"]
            parts = [f"[h1]{label}{'' if rarity == 'malus' else ' perks'}[/h1]"]
            for perk in self.perks:
                if perk["rarity"] != rarity:
                    continue
                parts.append(
                    f"[h2]{perk['name']}[/h2]\n[img]UPLOAD perks/{perk['id']}-icon.png[/img]\n[i]{perk['description']}[/i]\n\n{self.bbcode(notes[perk['id']])}"
                )
            sections.append("\n\n".join(parts))
        header = (
            "House of Pips perk guide (Steam Community Guide draft)\n"
            f"Generated for game version {self.version}. Each '=== SECTION ===' block is one guide section.\n"
            "Upload the icons from public/hop/wiki-data/img/perks/ in the guide editor, then replace each [img]UPLOAD ...[/img]\n"
            "placeholder with the image tag the editor gives you. Nothing here is uploaded automatically.\n"
        )
        text = header + "".join(f"\n=== SECTION: {RARITY_ORDER[i].title()} ===\n\n{section}\n" for i, section in enumerate(sections))
        (self.steam_out / "perks-guide.bbcode.txt").write_text(text, encoding="utf-8", newline="\n")

    # Verification -------------------------------------------------------------------

    def verify(self) -> dict:
        anchors: dict[Path, set[str]] = {}
        pages = sorted(path.resolve() for path in self.out.rglob("*.html"))
        for path in pages:
            anchors[path] = set(re.findall(r'\bid="([^"]+)"', path.read_text(encoding="utf-8")))
        problems = []
        for path in pages:
            markup = path.read_text(encoding="utf-8")
            where = path.relative_to(self.out).as_posix()
            for attribute, target in re.findall(r'\b(href|src)="([^"]+)"', markup):
                if re.match(r"^[a-z]+:", target):
                    # Outbound links are allowed for reading; nothing is ever loaded from another host.
                    if attribute == "src" or not target.startswith(("https://", "mailto:")):
                        problems.append(f"{where}: external {attribute} {target}")
                    continue
                file_part, _, anchor = target.partition("#")
                resolved = path if not file_part else (path.parent / unquote(file_part)).resolve()
                if resolved != self.out and self.out not in resolved.parents:
                    problems.append(f"{where}: link leaves the site: {target}")
                    continue
                if not resolved.exists():
                    problems.append(f"{where}: broken {attribute} {target}")
                    continue
                if anchor and resolved.suffix == ".html" and anchor not in anchors.get(resolved, set()):
                    problems.append(f"{where}: missing anchor #{anchor} in {file_part or path.name}")
            visible = plain(markup)
            for pattern, label in FORBIDDEN:
                found = pattern.search(visible)
                if found:
                    problems.append(f"{path.relative_to(self.out)}: player text contains {label}: {found.group(0)!r}")
            hashes = phrase_hashes(visible)
            if hashes & RIVAL_LOGIC_HASHES:
                problems.append(f"{path.relative_to(self.out)}: player text describes how Rival decides its moves")
            if (path.stem != SPOILER_PAGE or path.parent != self.out) and hashes & SPOILER_HASHES:
                problems.append(f"{path.relative_to(self.out)}: spoiler term outside the spoiler page")
        for entry in self.search:
            if phrase_hashes(entry["x"] + " " + entry["t"]) & (SPOILER_HASHES | RIVAL_LOGIC_HASHES):
                problems.append(f"search index: spoiler or rival logic term in {entry['u']}")
        if problems:
            fail("verification failed:\n  " + "\n  ".join(problems[:60]) + (f"\n  ... and {len(problems) - 60} more" if len(problems) > 60 else ""))

        # Each catalogue entry appears exactly once in its listing and once as an entry.
        perk_list = (self.out / "perks.html").read_text(encoding="utf-8")
        for perk in self.perks:
            count = perk_list.count(f'data-id="{perk["id"]}"')
            if count != 1:
                fail(f"perk {perk['id']} appears {count} times on the perk list")
            detail = self.out / "perks" / f"{perk['id']}.html"
            if not detail.exists() or detail.read_text(encoding="utf-8").count(f'id="perk-{perk["id"]}"') != 1:
                fail(f"perk {perk['id']} has no single detail entry")
        detail_pages = {path.stem for path in (self.out / "perks").glob("*.html")}
        if detail_pages != set(self.perk_by_id):
            fail(f"perk pages do not match the catalogue: {sorted(detail_pages ^ set(self.perk_by_id))}")
        for page, collection in (("supplies.html", self.supplies), ("skills.html", self.skills)):
            markup = (self.out / page).read_text(encoding="utf-8")
            for entry in collection:
                count = len(re.findall(rf'<article class="entry[^"]*" id="{re.escape(entry["id"])}"', markup))
                if count != 1:
                    fail(f"{entry['id']} appears {count} times on {page}")
            articles = len(re.findall(r'<article class="entry', markup))
            if articles != len(collection):
                fail(f"{page} has {articles} entries for {len(collection)} catalogue items")
        return {"pages": len(pages), "perks": len(self.perks), "supplies": len(self.supplies), "skills": len(self.skills), "screenshots": len(self.used_shots)}

    # Slapcraft Games website -------------------------------------------------------

    def website_bundle(self) -> dict:
        """Writes every built page as JSON for the Angular wiki at /hop/wiki.
        Page links become site routes and pictures resolve under
        hop/wiki-data/img/; every rewritten link must still resolve."""
        target = DATA
        if (target / "pages").exists():
            shutil.rmtree(target / "pages")
        (target / "pages").mkdir(parents=True)
        hidden = {slug for slug, page in self.pages.items() if page.get("hidden")}
        built = {path.relative_to(self.out).as_posix()[:-5]: path.read_text(encoding="utf-8") for path in sorted(self.out.rglob("*.html"))}
        built = {slug: markup for slug, markup in built.items() if slug not in hidden}
        anchors = {slug: set(re.findall(r'\bid="([^"]+)"', markup)) for slug, markup in built.items()}
        problems: list[str] = []

        def route(slug: str, anchor: str = "") -> str:
            return WEBSITE_ROUTE + ("" if slug == "index" else "/" + slug) + ("#" + anchor if anchor else "")

        def resolve(slug: str, reference: str) -> str:
            file_part, _, anchor = reference.partition("#")
            if not file_part:
                if anchor not in anchors[slug]:
                    problems.append(f"{slug}: missing anchor #{anchor}")
                return route(slug, anchor)
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(slug), unquote(file_part)))
            if resolved.endswith(".html"):
                page = resolved[:-5]
                if page not in built:
                    problems.append(f"{slug}: link to missing page {reference}")
                elif anchor and anchor not in anchors[page]:
                    problems.append(f"{slug}: missing anchor #{anchor} in {page}")
                return route(page, anchor)
            if not (target / resolved).is_file():
                problems.append(f"{slug}: missing file {reference}")
            return WEBSITE_ASSETS + resolved

        def rewrite(slug: str, markup: str) -> str:
            def replace(match: re.Match) -> str:
                reference = html.unescape(match.group(2))
                if re.match(r"^[a-z]+:", reference):
                    return match.group(0)
                return f'{match.group(1)}="{esc(resolve(slug, reference))}"'

            return re.sub(r'\b(href|src)="([^"]+)"', replace, markup)

        for slug, markup in built.items():
            body = re.search(r'<main id="content" class="content">\n(.*?)\n  </main>', markup, re.S)
            title = re.search(r"<title>(.*?)</title>", markup, re.S)
            description = re.search(r'<meta name="description" content="(.*?)">', markup)
            if not (body and title and description):
                fail(f"{slug}.html does not match the page shell; update website_bundle with the shell")
            toc_block = re.search(r'<nav class="toc"[^>]*>(.*?)</nav>', markup, re.S)
            toc = [{"id": anchor, "text": html.unescape(text)} for anchor, text in re.findall(r'<a href="#([^"]+)">(.*?)</a>', toc_block.group(1))] if toc_block else []
            page = {
                "route": route(slug),
                "title": html.unescape(title.group(1)),
                "description": html.unescape(description.group(1)),
                "html": rewrite(slug, body.group(1)),
                "toc": toc,
            }
            out = target / "pages" / f"{slug}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(page, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")
        if problems:
            fail("website bundle:\n  " + "\n  ".join(problems[:60]))
        nav = []
        for section in SECTIONS:
            entries = sorted((page for page in self.pages.values() if page["section"] == section and not page.get("hidden")), key=lambda page: (page["order"], page["title"]))
            if entries:
                nav.append({"section": section, "pages": [{"title": page["title"], "route": route(page["slug"])} for page in entries]})
        search = [dict(entry, u=resolve("index", entry["u"])) for entry in self.search]
        manifest = {"site": SITE_NAME, "version": self.version, "nav": nav, "search": search, "pages": sorted(route(slug) for slug in built)}
        (target / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")
        return {"pages": len(built), "target": target}

    # Build ----------------------------------------------------------------------------

    def build(self) -> dict:
        if self.out.exists():
            shutil.rmtree(self.out)
        self.out.mkdir(parents=True)
        perk_notes = read_notes(CONTENT / "catalogue" / "perks.md", [perk["id"] for perk in self.perks], "perk")
        supply_notes = read_notes(CONTENT / "catalogue" / "supplies.md", [item["id"] for item in self.supplies], "supply")
        skill_notes = read_notes(CONTENT / "catalogue" / "skills.md", [skill["id"] for skill in self.skills], "skill")
        loaded = self.load_pages()
        self.perk_pages(perk_notes)
        self.supplies_page(supply_notes)
        self.skills_page(skill_notes)
        self.render_pages(loaded)
        self.copy_assets()
        self.steam_guide(perk_notes)
        return self.verify()


def safe_output(path: Path) -> Path:
    """Build folders are deleted and rebuilt, so they must sit inside the
    gitignored hop-wiki/.build/ folder."""
    resolved = path.resolve()
    if BUILD.resolve() not in resolved.parents:
        fail(f"refusing to rebuild {resolved}: build output belongs under hop-wiki/.build/")
    return resolved


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build the House of Pips player wiki for /hop/wiki.")
    parser.add_argument("--catalogue", type=Path, default=DEFAULT_CATALOGUE, help="catalogue snapshot (default hop-wiki/catalogue.json)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="checked HTML build folder under hop-wiki/.build/")
    parser.add_argument("--steam-out", type=Path, default=DEFAULT_STEAM_OUT, help="Steam guide draft folder under hop-wiki/.build/")
    arguments = parser.parse_args(argv)
    try:
        if not arguments.catalogue.is_file():
            fail(f"missing catalogue snapshot {arguments.catalogue}")
        data = json.loads(arguments.catalogue.read_text(encoding="utf-8"))
        private = PRIVATE / "catalogue.json"
        if private.is_file():
            data["modes"] += [dict(mode, private=True) for mode in json.loads(private.read_text(encoding="utf-8")).get("modes", [])]
        out = safe_output(arguments.out)
        site = Site(data, PICTURES, PICTURES / "screens", out, safe_output(arguments.steam_out))
        summary = site.build()
        bundle = site.website_bundle()
    except BuildError as error:
        print(f"FAIL wiki build: {error}", file=sys.stderr)
        return 1
    print(
        "Built wiki: {pages} pages, {perks} perks, {supplies} supplies, {skills} skills, {screenshots} screenshots -> {out}".format(
            out=arguments.out, **summary
        )
    )
    print(f"Steam guide draft: {arguments.steam_out / 'perks-guide.bbcode.txt'}")
    print(f"Website wiki data: {bundle['pages']} pages -> {bundle['target']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
