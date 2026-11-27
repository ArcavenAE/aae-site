#!/usr/bin/env python3
"""Copy marvel's generated command reference into this site's content tree.

Usage: scripts/sync-marvel-reference.py <path-to-marvel-checkout>

marvel commits its reference as Markdown under docs/reference/, one file per
command, generated from the cobra tree. This script turns each file into a
Starlight page: it adds the title front matter Starlight needs, drops the
duplicate top heading, moves the remaining headings up one level, points the
cross-links at the site's own paths, and removes pages for commands marvel no
longer has. It also rewrites public/llms.txt and
reference-source.txt, which records the marvel commit the copy came from.

Set MARVEL_COMMIT to record a commit other than the checkout's HEAD (for a
source tree exported with git archive). Standard library only; run it with any python3. Re-running on an unchanged
marvel checkout changes nothing.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "src" / "content" / "docs" / "reference"
LINK = re.compile(r"\]\((marvel[A-Za-z0-9_-]*)\.md(#[^)]*)?\)")


def convert(name, text):
    lines = text.splitlines()
    if not lines or not lines[0].startswith("## "):
        sys.exit(f"{name}: expected a first line '## <command>'")
    title = lines[0][3:].strip()
    body = []
    in_fence = False
    for line in lines[1:]:
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("### "):
            line = line[1:]
        body.append(LINK.sub(lambda m: f"](/reference/{m.group(1)}/{m.group(2) or ''})", line))
    # The summary is the first paragraph after the heading.
    summary = next((b.strip() for b in body if b.strip()), title)
    front = f"---\ntitle: {json.dumps(title)}\ndescription: {json.dumps(summary)}\n---\n"
    return title, summary, front + "\n".join(body).rstrip("\n") + "\n"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    marvel = Path(sys.argv[1]).resolve()
    src = marvel / "docs" / "reference"
    files = sorted(src.glob("marvel*.md"))
    if not files:
        sys.exit(f"no reference files under {src}")
    sha = os.environ.get("MARVEL_COMMIT") or subprocess.run(
        ["git", "-C", str(marvel), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()

    OUT.mkdir(parents=True, exist_ok=True)
    pages = []
    for f in files:
        title, summary, page = convert(f.name, f.read_text())
        (OUT / f.name).write_text(page)
        pages.append((f.stem, title, summary))

    # A command marvel no longer has leaves its page behind: remove the copies
    # this script wrote earlier that the source no longer carries.
    kept = {f.name for f in files}
    stale = sorted(p for p in OUT.glob("marvel*.md") if p.name not in kept)
    for p in stale:
        p.unlink()
        print(f"removed stale page {p.name}")

    llms = ["# ArcavenAE documentation", ""]
    llms += ["> Guides and references for the ArcavenAE projects. Paths are relative to the site root.", ""]
    llms += ["## Guides", "", "- [marvel in two minutes](/e1-tour/): the core loop, step by step", ""]
    llms += ["## marvel command reference", ""]
    llms += [f"- [{title}](/reference/{stem}/): {summary}" for stem, title, summary in pages]
    (SITE / "public").mkdir(exist_ok=True)
    (SITE / "public" / "llms.txt").write_text("\n".join(llms) + "\n")
    (SITE / "reference-source.txt").write_text(
        f"repository: ArcavenAE/marvel\ncommit: {sha}\npath: docs/reference\nfiles: {len(pages)}\n"
    )
    print(f"{len(pages)} pages from marvel {sha[:8]}")


if __name__ == "__main__":
    main()
