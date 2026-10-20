# Task-Relative Evidence Requirements for Agent Auditing

An individual Internet-Draft on the evidence needed to answer specific
questions about agent activity across administrative domains.

[![Build and check draft](https://github.com/MikhailSergeev369/draft-audit-task-requirements/actions/workflows/build.yml/badge.svg?branch=main&event=push)](https://github.com/MikhailSergeev369/draft-audit-task-requirements/actions/workflows/build.yml)

Public editing workspace for **draft-sergeev-audit-task-requirements**,
an individual Internet-Draft by **Mikhail Sergeev**, with intended status
**Informational**. It is not an adopted working-group document or an IETF
consensus statement.

**Published baseline:** revision **-00**, posted to the IETF archive on
**16 October 2026**. The date inside the document is 15 October 2026.
The public workspace was initialized from the exact published XML and TXT;
subsequent changes to the working source are not a new IETF publication.

## Read, review, and contribute

**To read or comment, no installation is needed.** Start with the
[editor site](https://MikhailSergeev369.github.io/draft-audit-task-requirements/),
[published HTML](https://www.ietf.org/archive/id/draft-sergeev-audit-task-requirements-00.html),
or [GitHub reading copy](review/editor-copy.md), then
[open a feedback issue](https://github.com/MikhailSergeev369/draft-audit-task-requirements/issues/new?template=feedback.md)
or reply by email. A section reference and a concrete question or suggested
change are enough; writing code or opening a pull request is not required.

| Resource | Purpose |
| --- | --- |
| [Published -00](https://datatracker.ietf.org/doc/draft-sergeev-audit-task-requirements/00/) | The authoritative IETF revision |
| [GitHub releases](https://github.com/MikhailSergeev369/draft-audit-task-requirements/releases) | Revision tags, release notes, and byte-verified XML/TXT downloads |
| [Published HTML](https://www.ietf.org/archive/id/draft-sergeev-audit-task-requirements-00.html) | Read the published document |
| [Editor's HTML](https://MikhailSergeev369.github.io/draft-audit-task-requirements/editor/draft.html) | Latest successfully deployed working text from `main` |
| [Readable changes from -00](https://MikhailSergeev369.github.io/draft-audit-task-requirements/editor/changes.html) | Review text changes without XML markup |
| [Pinned review candidates](https://MikhailSergeev369.github.io/draft-audit-task-requirements/#candidates) | Separate previews of selected PR revisions, with their source commits |
| [Editor's reading copy](review/editor-copy.md) | Generated from the working XML; not a separate published revision |
| [Working RFCXML](draft-sergeev-audit-task-requirements.xml) | The only editable manuscript source |
| [Frozen XML/TXT and checksums](published/00/) | Exact published baseline for comparisons |
| [Issues](https://github.com/MikhailSergeev369/draft-audit-task-requirements/issues) / [pull requests](https://github.com/MikhailSergeev369/draft-audit-task-requirements/pulls) | Questions, counterexamples, and proposed edits |
| [Builds and review artifacts](https://github.com/MikhailSergeev369/draft-audit-task-requirements/actions/workflows/build.yml) | Generated XML/TXT/HTML, source diff from -00, and build logs |

The site distinguishes the published -00, the working text from `main`, and
selected review candidates. A candidate is pinned to the commit and XML hash
listed in [review/candidates.json](review/candidates.json); its preview does
not track later PR edits automatically or imply acceptance. Check its linked
PR for the current discussion. Until the first Pages deployment, use the
GitHub reading copy or download the `editor-site` artifact from a successful CI run.

For a focused review, start with these sections:

- Architecture and Audit Store: section 6.1, then 4.2 and 5.3.
- Expected Records: section 3.2, then 4.2 and 6.7.
- First reading: Key Separations, then the refund examples in section 4.

Please read [CONTRIBUTING.md](CONTRIBUTING.md). Feedback by email is equally
welcome: [AUDIT mailing list](mailto:audit@ietf.org),
[public discussion archive](https://mailarchive.ietf.org/arch/browse/audit/),
or [the editor](mailto:mikhailsergeev369@gmail.com).
GitHub participation is not required. Repository merges are editorial decisions,
not working-group decisions or contributor endorsements.

## Scope

The model distinguishes an audit question and scope, alternative evidence
requirements, evidence-production expectations, available evidence,
verification, applicability, and the basis of an audit result. It separates
a completed search that finds no qualifying record from incomplete observation.

It defines no universal minimum record inventory, declaration mechanism,
record format, authorization model, or completeness mechanism. Native AEB,
EP-AEC, WEXP, and other specifications retain the semantics of their own
artifacts and results. Expected-record declarations are discussed in section
6.7 as separate work; this repository does not implement or prescribe that
mechanism. Attribution in the published acknowledgments is preserved.

## Edit and build

**This is a document repository, not an agent-auditing software implementation.**
The Python files in `tools/` and `tests/` support document preparation: generating
the reading copy, checking links and archive hashes, running the official
xml2rfc formatter, and comparing revisions. They do not evaluate agent actions
or implement the draft's audit model. The build badge reports those editorial
checks, not protocol conformance or approval of the document.

Python **3.12** is the CI environment; the formatter is pinned in
`requirements.txt`. The reading-copy and source-integrity commands use only
the Python standard library.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
# Edit draft-sergeev-audit-task-requirements.xml, then:
make review     # refresh the GitHub-readable Markdown
make check      # source links, archive hashes, reading-copy consistency
make test       # tooling regression tests, not protocol conformance
make build      # official xml2rfc TXT/HTML, repeated in one environment
# Commit manuscript edits before building a site with exact source-commit links.
python tools/site.py --fetch-candidates  # fetch the configured commit pins
make site       # editor site, readable comparisons, and pinned candidates
```

Open `build/index.html` locally. Each successful CI artifact includes the exact
working XML, both renderings, the diff from published -00, resolved package
versions, source/output hashes, and formatter logs. Generated build files are
not committed. Network access is needed to install dependencies; manuscript
rendering disables network reference resolution and local-file includes.

Open `_site/index.html` for the complete review site. Building candidate
previews needs the pinned commits locally; use a full clone, or fetch those
commits with `python tools/site.py --fetch-candidates` before `make site`.
Run `make build` again after a commit so its build identity is current.
Only their manuscript XML is read: the current
checkout's tools and formatter build every preview. `_site/` is generated and
is not committed. CI also preserves this directory as an `editor-site` artifact.

## Editor site deployment

One-time setup: select **Settings → Pages → Build and deployment → Source →
GitHub Actions**. Once this workflow is merged, a successful push or manual
run on `main` builds and deploys the editor site. A pull request builds a
downloadable review artifact; it does not deploy the site. The deployment
job uses the `github-pages` environment and follows its protection rules.

Pages exposes the latest successful build, so check the source commit shown
on the page when discussing a revision. Updating a candidate means deliberately
updating its pin in `review/candidates.json` after reviewing that revision.
Publishing an editor site does not submit an Internet-Draft or create a release.

These checks concern source integrity and rendering, not the correctness of
the model, legal clearance, interoperability, or IETF acceptance. They do not
claim a fresh online idnits run or bibliographic review. The normal IETF checks
and author confirmation still apply when submitting a future revision.

## GitHub releases

Release titles follow the I-D revision (`-00`, `-01`, ...); tags use the full
document name, such as `draft-sergeev-audit-task-requirements-00`. Each release
records an already posted IETF revision and includes its XML, TXT, and
`SHA256SUMS`. The IETF archive remains authoritative.

For a future revision, first complete the ordinary IETF submission and keep its
exact files and checksum list under `published/NN/`, without changing older
snapshots. From Actions, run
[Release a published IETF revision](https://github.com/MikhailSergeev369/draft-audit-task-requirements/actions/workflows/release.yml)
on `main`, entering the two-digit revision and the full commit SHA containing
that source and snapshot. A short revision summary is optional.

The workflow verifies both files against the live IETF archive before creating
the GitHub release, then downloads the release assets to check them again.
It refuses a mismatched existing tag or assets rather than overwriting them.
Rerunning a matching release verifies it without publishing a duplicate.
Network failure or different bytes stop the operation. No release is created
by an ordinary commit, pull request, or tag push; future releases are explicitly
started by a maintainer. No extra signed form or CLA is required.

## Revision policy

The root XML is the working source for future edits. `published/00/` is frozen;
do not update it when preparing -01. Label a future revision in the working
source before submission, leaving already posted files unchanged. Until
Datatracker actually posts that revision, it remains editor's work in progress.

No workflow sends email, submits to Datatracker, or merges a pull request.
The build job retains read-only repository permissions. The separate Pages
deployment job has Pages and OIDC permissions; it cannot edit repository
contents. Only the release job has contents-write permission to create the
requested GitHub tag, release, and assets; it does not change manuscript files
or access settings. GitHub releases do not replace IETF submission or author
confirmation.

The public history begins at the published document. No earlier private Git
history, private correspondence, unpublished partner text, or research logs
are imported. See [LICENSE.md](LICENSE.md) for document and tooling terms.
