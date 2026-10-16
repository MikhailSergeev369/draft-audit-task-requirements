#!/usr/bin/env python3
"""Small editorial helpers. RFCXML validation/rendering is delegated to xml2rfc.

No online idnits, rights attestation, submission, or protocol conformance claim.
SPDX-License-Identifier: BSD-3-Clause
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import importlib.metadata
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "draft-sergeev-audit-task-requirements"
SOURCE = ROOT / (BASE + ".xml")
READING = ROOT / "review/editor-copy.md"
ARCHIVE = ROOT / "published/00"
POSTED = {
    BASE + "-00.xml": "e83c17d6a43fe66a010502655a94dae067195b36e9001f9f8de11e5fb164dc5a",
    BASE + "-00.txt": "532a14ef7757cf68cce7ce77e4404810d1afc9bfe9926f2e5884fb353b3804f5",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_source(data: bytes) -> ET.Element:
    if re.search(br"<!\s*(?:DOCTYPE|ENTITY)\b", data, re.I):
        raise ValueError("Use standalone RFCXML, without DTDs or external entities")
    root = ET.fromstring(data)
    if root.tag != "rfc" or root.get("version") != "3":
        raise ValueError("Expected RFCXML v3")
    if not re.fullmatch(re.escape(BASE) + r"-\d{2}", root.get("docName", "")):
        raise ValueError("Unexpected document identity")
    for element in root.iter():
        if element.tag == "{http://www.w3.org/2001/XInclude}include" or element.get("src"):
            raise ValueError("External or local file includes are not supported")
    anchors = [e.get("anchor") for e in root.iter() if e.get("anchor")]
    if len(anchors) != len(set(anchors)):
        raise ValueError("Duplicate XML anchor")
    if any(x.get("target") not in anchors for x in root.iter("xref")):
        raise ValueError("Unresolved internal cross-reference")
    if root.find("front/title") is None or not root.findall("front/author"):
        raise ValueError("Missing title or author metadata")
    return root


def inline(element: ET.Element | None) -> str:
    if element is None:
        return ""
    result = html.escape(element.text or "", quote=False)
    for child in element:
        value = inline(child)
        if child.tag in ("strong", "em", "tt"):
            marker = {"strong": "**", "em": "*", "tt": "`"}[child.tag]
            value = marker + value + marker
        elif child.tag == "xref":
            target = child.attrib["target"]
            value = f"[{value or target}](#{target})"
            if child.get("section"):
                value = f"Section {child.get('section')} of {value}"
        elif child.tag == "eref":
            target = child.attrib["target"]
            value = f"[{value or target}]({target})"
        result += value + html.escape(child.tail or "", quote=False)
    return result


def block(element: ET.Element, level: int = 1) -> str:
    tag = element.tag
    if tag == "section":
        anchor = html.escape(element.get("anchor", ""), quote=True)
        heading = f'<a id="{anchor}"></a>\n\n' if anchor else ""
        heading += "#" * min(level, 6) + " " + inline(element.find("name")) + "\n\n"
        return heading + "".join(block(c, level + 1) for c in element if c.tag != "name")
    if tag == "t":
        return " ".join(inline(element).split()) + "\n\n"
    if tag in ("ul", "ol"):
        lines = []
        for index, item in enumerate(element.findall("li"), 1):
            value = "".join(block(c, level) for c in item).strip() or inline(item).strip()
            prefix = f"{index}. " if tag == "ol" else "- "
            lines.append(prefix + value.replace("\n", "\n  "))
        return "\n".join(lines) + "\n\n"
    if tag in ("artwork", "sourcecode"):
        return "```text\n" + (element.text or "").strip("\n") + "\n```\n\n"
    if tag == "blockquote":
        return "\n".join("> " + line for line in "".join(block(c, level) for c in element).strip().splitlines()) + "\n\n"
    if tag == "table":
        rows = []
        for index, row in enumerate(element.findall(".//tr")):
            cells = [" ".join(inline(c).split()).replace("|", r"\|") for c in row]
            rows.append("| " + " | ".join(cells) + " |")
            if index == 0:
                rows.append("| " + " | ".join("---" for _ in cells) + " |")
        return "\n".join(rows) + "\n\n"
    if tag == "references":
        return "# Informative References\n\n" + "".join(block(c) for c in element if c.tag == "reference")
    if tag == "reference":
        anchor = element.attrib["anchor"]
        front = element.find("front")
        if front is None:
            raise ValueError("Reference has no front matter")
        authors = ", ".join(a.get("fullname") or a.get("surname") or inline(a.find("organization")) for a in front.findall("author"))
        date = front.find("date")
        when = " ".join(date.get(k, "") for k in ("day", "month", "year")).strip() if date is not None else ""
        title = inline(front.find("title"))
        if element.get("target"):
            title = f"[{title}]({element.get('target')})"
        series = "; ".join(c.get("name", "") + " " + c.get("value", "") for c in element.findall("seriesInfo"))
        details = " ".join(inline(c) for c in element.findall("refcontent"))
        return f'<a id="{html.escape(anchor, quote=True)}"></a>\n\n**[{anchor}]** {authors}. {title}. {series}. {when}. {details}\n\n'
    return "".join(block(c, level) for c in element)


def render_reading(data: bytes) -> str:
    root = parse_source(data)
    front = root.find("front")
    assert front is not None
    out = "# " + inline(front.find("title")) + "\n\n"
    out += "**Generated editor's reading copy, not a separate IETF publication.**\n\n"
    out += f"Source SHA-256: `{sha256(data)}`. Edit the [RFCXML](../{BASE}.xml), not this file.\n\n"
    out += f"[Published -00](https://datatracker.ietf.org/doc/{BASE}/00/) · [Contributing](../CONTRIBUTING.md)\n\n"
    abstract = front.find("abstract")
    if abstract is not None:
        out += "## Abstract\n\n" + block(abstract)
    for note in front.findall("note"):
        out += "## " + inline(note.find("name")) + "\n\n"
        out += "".join(block(c) for c in note if c.tag != "name")
    for part in ("middle", "back"):
        element = root.find(part)
        if element is not None:
            out += block(element)
    return out.rstrip() + "\n"


def verify_archive(directory: Path = ARCHIVE) -> None:
    expected_lines = []
    for name, expected in POSTED.items():
        if sha256((directory / name).read_bytes()) != expected:
            raise ValueError("Published snapshot changed: " + name)
        expected_lines.append(f"{expected}  {name}\n")
    if (directory / "SHA256SUMS").read_text(encoding="utf-8") != "".join(expected_lines):
        raise ValueError("Published checksum list changed")


def check() -> None:
    data = SOURCE.read_bytes()
    root = parse_source(data)
    verify_archive()
    if READING.read_text(encoding="utf-8") != render_reading(data):
        raise ValueError("Reading copy is stale: run make review")
    print(f"PASS: source identity {root.get('docName')}, anchors/xrefs, published hashes, and reading copy")
    print("This is not a grammar, semantic, rights, online-reference, or conformance verdict.")


def build() -> None:
    check()
    expected = (ROOT / "requirements.txt").read_text().strip().removeprefix("xml2rfc==")
    actual = importlib.metadata.version("xml2rfc")
    if actual != expected:
        raise ValueError(f"Expected xml2rfc {expected}, got {actual}; install requirements.txt")
    formatter = shutil.which("xml2rfc")
    if formatter is None:
        raise RuntimeError("xml2rfc command is missing; install requirements.txt")
    data = SOURCE.read_bytes()
    name = parse_source(data).attrib["docName"]
    output = ROOT / "build"
    output.mkdir(exist_ok=True)
    # Invalidate a previous success record before any fallible rendering.
    manifest = output / "build.json"
    manifest.unlink(missing_ok=True)
    artifacts = {}
    with tempfile.TemporaryDirectory(prefix="audit-render-") as temporary:
        temporary = Path(temporary)
        for ext, flag in (("txt", "--text"), ("html", "--html")):
            copies = []
            for attempt in (1, 2):
                destination = temporary / str(attempt) / f"{name}.{ext}"
                destination.parent.mkdir(exist_ok=True)
                command = [formatter, str(SOURCE), flag, "--no-network", "--skip-config-files", "--out", str(destination)]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
                (output / f"xml2rfc-{ext}-{attempt}.log").write_text(
                    "$ " + " ".join(command) + "\n\n" + result.stdout + "\n" + result.stderr,
                    encoding="utf-8")
                if result.returncode != 0:
                    raise RuntimeError(f"xml2rfc failed for {ext}; see build log")
                copies.append(destination.read_bytes())
            if copies[0] != copies[1]:
                raise RuntimeError(f"Repeated {ext} build differs in this environment")
            (output / f"{name}.{ext}").write_bytes(copies[0])
            artifacts[f"{name}.{ext}"] = sha256(copies[0])
    (output / f"{name}.xml").write_bytes(data)
    artifacts[f"{name}.xml"] = sha256(data)
    old = (ARCHIVE / (BASE + "-00.xml")).read_text(encoding="utf-8")
    new = data.decode("utf-8")
    diff = "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile="published/-00.xml", tofile="working.xml"))
    (output / "diff-from-00.txt").write_text(diff or "No source changes: working XML matches published -00 byte-for-byte.\n", encoding="utf-8")
    comparison = difflib.HtmlDiff(wrapcolumn=110).make_file(old.splitlines(), new.splitlines(), "Published -00", "Working XML", context=True, numlines=3)
    (output / "diff-from-00.html").write_text(comparison, encoding="utf-8")
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None
    report = {
        "scope": "Official RFCXML rendering and same-environment repeat; not online idnits or semantic validation",
        "git_commit": commit, "document": name, "source_sha256": sha256(data),
        "formatter": "xml2rfc", "formatter_version": actual, "python": sys.version.split()[0],
        "same_environment_repeat": True, "outputs": artifacts,
        "source_matches_published_00": data == (ARCHIVE / (BASE + "-00.xml")).read_bytes(),
        "txt_matches_published_00": artifacts[name + ".txt"] == POSTED[BASE + "-00.txt"],
        "submission_performed": False,
    }
    manifest.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / "SHA256SUMS").write_text("".join(f"{digest}  {file}\n" for file, digest in sorted(artifacts.items())), encoding="utf-8")
    (output / "index.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>AUDIT editor build</title>'
        '<h1>AUDIT editor build</h1><p>This is a generated working copy, not a separate IETF publication.</p>'
        f'<p>Commit: <code>{html.escape(commit or "uncommitted local build")}</code><br>Source SHA-256: <code>{sha256(data)}</code></p>'
        f'<p><a href="{name}.html">Read HTML</a> · <a href="{name}.txt">TXT</a> · <a href="{name}.xml">XML</a></p>'
        f'<p><a href="diff-from-00.html">Source diff from -00</a> · <a href="https://datatracker.ietf.org/doc/{BASE}/00/">Published IETF -00</a></p>'
        '<p>Build success is not proof of model correctness or IETF endorsement.</p></html>\n', encoding="utf-8")
    print(json.dumps(report, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("review", "check", "build"))
    args = parser.parse_args()
    try:
        if args.command == "review":
            READING.parent.mkdir(exist_ok=True)
            READING.write_text(render_reading(SOURCE.read_bytes()), encoding="utf-8")
            print(READING.relative_to(ROOT))
        elif args.command == "check":
            check()
        else:
            build()
    except (OSError, ValueError, RuntimeError, ET.ParseError, importlib.metadata.PackageNotFoundError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
