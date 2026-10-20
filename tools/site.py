#!/usr/bin/env python3
"""Build the public reading site from verified renderings and pinned candidate XML.

Never execute code from candidate commits. Building is offline; --fetch-candidates
explicitly fetches validated commit pins from origin. No deployment or submission.
SPDX-License-Identifier: BSD-3-Clause
"""
from __future__ import annotations

import difflib
import html
from html.parser import HTMLParser
import importlib.metadata
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

import draft

ROOT = draft.ROOT
REPO = "https://github.com/MikhailSergeev369/draft-audit-task-requirements"
PUBLISHED = f"https://datatracker.ietf.org/doc/{draft.BASE}/00/"
CSS = """
:root { color-scheme: light dark; }
body { max-width: 72rem; margin: 2rem auto; padding: 0 1rem; font: 17px/1.6 system-ui, sans-serif; }
a { color: #165ec3; } @media (prefers-color-scheme: dark) { a { color: #9ac4ff; } }
h1 { line-height: 1.2; } h2 { margin-top: 2rem; }
nav { display: flex; flex-wrap: wrap; gap: 1rem; margin: 1rem 0; }
article, .notice { border: 1px solid #8886; border-radius: .5rem; padding: 1rem; margin: 1rem 0; }
code { overflow-wrap: anywhere; } .meta { font-size: .85rem; }
.removed { border-left: .3rem solid #b44343; background: #d3343415; }
.added { border-left: .3rem solid #24804a; background: #24804a15; }
.changed-text { white-space: pre-wrap; overflow-wrap: anywhere; }
"""


def page(title: str, body: str) -> str:
    footer = (f'<footer><p><a href="{REPO}/blob/main/CONTRIBUTING.md">Contributing and Note Well</a> · '
              f'<a href="{REPO}/blob/main/LICENSE.md">Document and tooling terms</a> · '
              f'<a href="{REPO}/blob/main/PUBLICATION-PROCESS.md">Publication process</a></p></footer>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{html.escape(title)}</title><style>{CSS}</style></head>'
            f'<body><main><h1>{html.escape(title)}</h1>{body}</main>{footer}</body></html>\n')


class ReadingText(HTMLParser):
    """Extract visible text blocks, excluding generated TOC and IETF boilerplate.

    External link targets are retained. Whitespace is normalized except in pre.
    This is a reading aid; source diff remains available for structural changes.
    """
    blocks = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "pre", "dt", "dd", "tr", "li", "caption", "figcaption"}
    void = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.skip = None
        self.active = None
        self.parts = []
        self.result = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag not in self.void:
            self.stack.append(tag)
        depth = len(self.stack)
        if self.skip is not None:
            return
        if (tag in {"head", "script", "style", "nav"}
                or attr.get("id", "").startswith(("section-toc", "section-boilerplate"))
                or "hidden" in attr
                or set(attr.get("class", "").split()) & {"pilcrow", "toplink", "ears"}):
            if tag not in self.void:
                self.skip = depth
            return
        if self.active is None and tag in self.blocks:
            self.active = (tag, depth)
            self.parts = []
        if self.active:
            if tag in self.blocks | {"br", "td", "th"} and self.active[0] != "pre":
                self.parts.append(" ")
            if tag == "a":
                self.links.append((depth, attr.get("href", ""), len(self.parts)))

    def handle_endtag(self, tag):
        depth = len(self.stack)
        if self.skip is not None:
            if depth == self.skip:
                self.skip = None
        elif self.active:
            if tag in self.blocks and self.active[1] != depth:
                self.parts.append(" ")
            if tag == "a" and self.links and self.links[-1][0] == depth:
                _, href, start = self.links.pop()
                if urlsplit(href).scheme in {"http", "https", "mailto"} and href != "".join(self.parts[start:]).strip():
                    self.parts.append(f" <{href}>")
            if self.active[1] == depth:
                text = "".join(self.parts)
                text = text.strip("\n") if self.active[0] == "pre" else " ".join(text.split())
                if text:
                    self.result.append(text)
                self.active = None
                self.links = []
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, text):
        if self.active and self.skip is None:
            self.parts.append(text)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.void:
            self.handle_endtag(tag)


def reading_blocks(rendered: str) -> list[str]:
    parser = ReadingText()
    parser.feed(rendered)
    parser.close()
    if not parser.result:
        raise ValueError("No readable content in rendered HTML")
    return parser.result


def text_diff(old: str, new: str, old_label: str, new_label: str) -> str:
    before, after = reading_blocks(old), reading_blocks(new)
    groups = list(difflib.SequenceMatcher(None, before, after, autojunk=False).get_grouped_opcodes(1))
    body = ('<nav><a href="index.html">Version overview</a><a href="draft.html">Read this version</a>'
            '<a href="source-diff.patch">XML source diff from -00</a></nav>'
            f'<p>From <strong>{html.escape(old_label)}</strong> to <strong>{html.escape(new_label)}</strong>.</p>'
            '<p>Comparison of document text from xml2rfc HTML. Generated contents, print headers/footers, IETF boilerplate, '
            'pilcrows and ordinary whitespace are excluded; external link targets are retained. '
            'Use the XML diff for markup, metadata and structural changes.</p>')
    if not groups:
        body += '<p>No reading-text changes in the compared content.</p>'
    for n, group in enumerate(groups, 1):
        body += f'<section><h2>Change {n}</h2>'
        for kind, i, j, k, l in group:
            if kind == "equal":
                body += ''.join(f'<p>{html.escape(x)}</p>' for x in before[i:j])
            else:
                if kind in {"delete", "replace"}:
                    body += '<article class="removed"><strong>Removed</strong>' + ''.join(
                        f'<p class="changed-text">{html.escape(x)}</p>' for x in before[i:j]) + '</article>'
                if kind in {"insert", "replace"}:
                    body += '<article class="added"><strong>Added</strong>' + ''.join(
                        f'<p class="changed-text">{html.escape(x)}</p>' for x in after[k:l]) + '</article>'
        body += '</section>'
    return page("Reading-text changes", body)


def candidates_config(path: Path) -> list[dict]:
    config = json.loads(path.read_text(encoding="utf-8"))
    if set(config) != {"candidates"} or not isinstance(config["candidates"], list):
        raise ValueError("Invalid candidate configuration")
    seen = set()
    for entry in config["candidates"]:
        if set(entry) != {"pr", "commit", "source_sha256", "title", "summary"}:
            raise ValueError("Invalid candidate fields")
        if type(entry["pr"]) is not int or entry["pr"] < 1:
            raise ValueError("Invalid or duplicate candidate PR")
        if (not isinstance(entry["commit"], str) or not isinstance(entry["source_sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{40}", entry["commit"])
                or not re.fullmatch(r"[0-9a-f]{64}", entry["source_sha256"])):
            raise ValueError("Candidate must pin a full commit and source digest")
        if (entry["pr"], entry["commit"]) in seen:
            raise ValueError("Duplicate candidate snapshot")
        if not all(isinstance(entry[k], str) and entry[k].strip() for k in ("title", "summary")):
            raise ValueError("Candidate requires a title and summary")
        seen.add((entry["pr"], entry["commit"]))
    return config["candidates"]


def render(data: bytes, directory: Path) -> dict[str, bytes]:
    draft.parse_source(data)
    directory.mkdir(parents=True, exist_ok=True)
    source = directory / "source.xml"
    source.write_bytes(data)
    formatter = shutil.which("xml2rfc")
    if formatter is None:
        raise RuntimeError("xml2rfc missing")
    result = {"xml": data}
    for ext, flag in (("html", "--html"), ("txt", "--text")):
        target = directory / ("draft." + ext)
        command = [formatter, str(source), flag, "--no-network", "--skip-config-files", "--out", str(target)]
        run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
        if run.returncode:
            raise RuntimeError(f"Candidate/baseline rendering failed: {run.stderr}")
        result[ext] = target.read_bytes()
    return result


def routes() -> str:
    return ('<h2>Where to start</h2><ul>'
            '<li>Architecture and Audit Store: <a href="draft.html#audit-architecture">§6.1</a> → '
            '<a href="draft.html#expected-evidence-across-administrative-domains">§4.2</a> → '
            '<a href="draft.html#collection-and-query-interfaces">§5.3</a>.</li>'
            '<li>Expected Records: <a href="draft.html#evidence-requirements-and-production-expectations">§3.2</a> → '
            '<a href="draft.html#expected-evidence-across-administrative-domains">§4.2</a> → '
            '<a href="draft.html#expected-record-declarations">§6.7</a>.</li>'
            '<li>First reading: <a href="draft.html#key-separations">Key Separations</a> and '
            '<a href="draft.html#illustrative-refund-evaluation">refund example</a>.</li></ul>')


def write_version(directory: Path, outputs: dict, baseline: dict, label: str, commit: str,
                  home: str, description: str = "", pr: int | None = None, current: dict | None = None) -> dict:
    directory.mkdir(parents=True)
    # Direct links to the formatted draft also retain the version status.
    banner = (f'<aside class="site-banner" aria-label="Version status" '
              'style="padding:1rem;margin:1rem;border:2px solid #52739b;background:#fff;color:#172739;font:16px/1.5 system-ui">'
              f'<strong>{html.escape(label)}</strong> — working material, not a new IETF publication. '
              f'Source commit: <code>{commit[:12]}</code>. '
              '<a href="index.html">Version details and discussion</a> · '
              f'<a href="{home}">All versions</a></aside>')
    decorated, count = re.subn(r'(<body\b[^>]*>)', lambda m: m[1] + banner, outputs["html"].decode(), count=1)
    if count != 1:
        raise ValueError("Missing HTML body for version banner")
    # The formatter's source filename differs from the public download name.
    decorated, source_links = re.subn(
        r'<link href="[^"]+" rel="alternate" type="application/rfc\+xml">',
        '<link href="draft.xml" rel="alternate" type="application/rfc+xml">', decorated)
    if source_links != 1:
        raise ValueError("Expected one RFCXML alternate link")
    served = dict(outputs, html=decorated.encode())
    for ext, data in served.items():
        (directory / f"draft.{ext}").write_bytes(data)
    # xml2rfc links this optional override sheet; keep that resource resolvable.
    (directory / "rfc-local.css").write_text(
        "/* No local overrides: use the embedded xml2rfc styles. */\n", encoding="utf-8")
    old_xml = baseline["xml"].decode()
    new_xml = outputs["xml"].decode()
    patch = ''.join(difflib.unified_diff(old_xml.splitlines(True), new_xml.splitlines(True),
                                       fromfile="published-00.xml", tofile="candidate.xml" if pr else "editor.xml"))
    (directory / "source-diff.patch").write_text(patch or "No XML source changes from published -00.\n", encoding="utf-8")
    (directory / "changes.html").write_text(text_diff(baseline["html"].decode(), outputs["html"].decode(),
                                                       "published -00 (locally rendered)", label), encoding="utf-8")
    extra = ""
    if current is not None:
        (directory / "changes-from-main.html").write_text(text_diff(current["html"].decode(), outputs["html"].decode(),
                                                                    "editor build shown on this site", label), encoding="utf-8")
        extra = '<a href="changes-from-main.html">Changes from this site’s editor build</a>'
    document = draft.parse_source(outputs["xml"]).get("docName")
    note = (f'Pinned review snapshot from <a href="{REPO}/pull/{pr}">PR #{pr}</a>. '
            'Not an adopted or published IETF revision. This page does not track the live PR state; '
            'follow the PR for newer revisions or disposition.' if pr else
            'Editor’s working copy. On the live site this is the successfully built main branch. '
            'A downloaded PR build is a preview of that PR’s checked revision.')
    body = (f'<nav><a href="{home}">All versions</a><a href="draft.html">Read HTML</a>'
            '<a href="changes.html">Changes from -00</a>' + extra +
            f'<a href="{REPO}/issues">Discuss</a></nav><p class="notice">{note}</p>'
            f'<p>{html.escape(description)}</p><p>Source document label: <code>{html.escape(document)}</code>.</p>'
            f'<p class="meta">Source commit: <a href="{REPO}/commit/{commit}"><code>{commit}</code></a><br>'
            f'XML SHA-256: <code>{draft.sha256(outputs["xml"])}</code></p>'
            '<p><a href="draft.txt">TXT</a> · <a href="draft.xml">XML</a> · '
            '<a href="source-diff.patch">XML diff</a> · <a href="manifest.json">Build identity</a> · '
            f'<a href="{PUBLISHED}">Published IETF -00</a></p>' + routes() +
            f'<p>Feedback: <a href="{REPO}/issues/new?template=feedback.md">open an issue</a> '
            'or email <a href="mailto:audit@ietf.org">audit@ietf.org</a>. '
            'Please identify this version and the section or paragraph.</p>')
    (directory / "index.html").write_text(page(label, body), encoding="utf-8")
    report = {"label": label, "source_commit": commit, "document": document,
              "source_sha256": draft.sha256(outputs["xml"]), "pr": pr,
              "formatter_version": importlib.metadata.version("xml2rfc"),
              "outputs": {f"draft.{ext}": draft.sha256(data) for ext, data in served.items()},
              "html_note": "xml2rfc rendering with an added version/navigation banner"}
    (directory / "manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag in {"a", "link"} and attrs.get("href"):
            self.links.append(attrs["href"])
        for name in ("src", "poster"):
            if attrs.get(name):
                self.links.append(attrs[name])


def check_links(directory: Path) -> None:
    pages = {}
    for file in directory.rglob("*.html"):
        parsed = LinkParser()
        parsed.feed(file.read_text(encoding="utf-8"))
        pages[file.resolve()] = parsed
    for file, parsed in pages.items():
        for href in parsed.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = (file.parent / unquote(url.path)).resolve() if url.path else file
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(directory.resolve()) or not target.is_file():
                raise ValueError(f"Broken local link: {file.name}: {href}")
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                raise ValueError(f"Broken local fragment: {file.name}: {href}")


def build_site() -> None:
    draft.check()
    expected = (ROOT / "requirements.txt").read_text().strip().removeprefix("xml2rfc==")
    if importlib.metadata.version("xml2rfc") != expected:
        raise ValueError("Install the pinned formatter from requirements.txt")
    build = ROOT / "build"
    report = json.loads((build / "build.json").read_text())
    source = draft.SOURCE.read_bytes()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if report["source_sha256"] != draft.sha256(source) or report["git_commit"] != commit:
        raise ValueError("Stale build: run make build for this checkout")
    committed_source = subprocess.check_output(["git", "show", f"{commit}:{draft.BASE}.xml"], cwd=ROOT)
    if source != committed_source:
        raise ValueError("Commit manuscript edits before building a site with source-commit links")
    outputs = {}
    for ext in ("html", "txt", "xml"):
        name = report["document"] + "." + ext
        data = (build / name).read_bytes()
        if draft.sha256(data) != report["outputs"][name]:
            raise ValueError("Build output digest mismatch: " + name)
        outputs[ext] = data
    candidates = candidates_config(ROOT / "review/candidates.json")
    with tempfile.TemporaryDirectory(prefix="audit-site-") as tmp:
        work = Path(tmp)
        site = work / "site"
        site.mkdir()
        baseline_xml = (draft.ARCHIVE / (draft.BASE + "-00.xml")).read_bytes()
        baseline = outputs if source == baseline_xml else render(baseline_xml, work / "baseline")
        identities = [write_version(site / "editor", outputs, baseline, "Editor’s working copy", commit, "../index.html")]
        links = []
        for item in candidates:
            data = subprocess.check_output(["git", "show", f'{item["commit"]}:{draft.BASE}.xml'], cwd=ROOT)
            if draft.sha256(data) != item["source_sha256"]:
                raise ValueError("Pinned candidate source digest mismatch")
            slug = f'pr-{item["pr"]}-{item["commit"][:12]}'
            candidate = render(data, work / slug)
            label = f'PR #{item["pr"]} snapshot: {item["title"]}'
            identities.append(write_version(site / "candidates" / slug, candidate, baseline, label,
                                            item["commit"], "../../index.html", item["summary"], item["pr"], outputs))
            links.append(f'<article><h3><a href="candidates/{slug}/index.html">{html.escape(label)}</a></h3>'
                         f'<p>{html.escape(item["summary"])}</p><p>Snapshot commit: <code>{item["commit"][:12]}</code>. '
                         f'<a href="{REPO}/pull/{item["pr"]}">Current PR discussion</a>.</p></article>')
        body = ('<p>Task-Relative Evidence Requirements for Agent Auditing — Mikhail Sergeev.</p>'
                '<nav><a href="editor/draft.html">Read editor’s copy</a><a href="editor/changes.html">Changes from -00</a>'
                f'<a href="{REPO}/issues">Discuss</a></nav>'
                '<section><h2>Choose a version</h2><ul>'
                f'<li><a href="{PUBLISHED}">Published IETF -00</a> — authoritative posted revision.</li>'
                '<li><a href="editor/index.html">Editor’s working copy</a> — the live site follows successful main builds.</li>'
                '<li><a href="#candidates">Review snapshots</a> — pinned proposals, separate from the editor’s copy.</li></ul></section>'
                '<p>A downloaded PR artifact previews that PR’s checked revision. Its editor copy may differ from live main.</p>'
                '<section id="candidates"><h2>Review snapshots</h2>' + ''.join(links) + '</section>'
                f'<p><a href="{REPO}">Source repository</a> · <a href="site-manifest.json">Site build identity</a></p>'
                '<p>These are reading and review aids. Updating this site does not submit a revision to the IETF.</p>')
        (site / "index.html").write_text(page("AUDIT Task — read and review", body), encoding="utf-8")
        (site / "site-manifest.json").write_text(json.dumps({"site_commit": commit, "versions": identities}, indent=2) + "\n")
        (site / ".nojekyll").write_text("")
        check_links(site)
        destination = ROOT / "_site"
        # Only this generated output directory is replaced, after complete validation.
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(site, destination)
    print(f"PASS: site built with {len(identities)} versions; local href/src/poster targets and HTML fragments resolve")


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["--fetch-candidates"]:
            for candidate in candidates_config(ROOT / "review/candidates.json"):
                subprocess.run(["git", "fetch", "--no-tags", "origin", candidate["commit"]], cwd=ROOT, check=True)
        elif not sys.argv[1:]:
            build_site()
        else:
            raise ValueError("Usage: site.py [--fetch-candidates]")
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
