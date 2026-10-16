# Task-Relative Evidence Requirements for Agent Auditing

Public editing workspace for **draft-sergeev-audit-task-requirements**,
an individual Internet-Draft by **Mikhail Sergeev**, with intended status
**Informational**. It is not an adopted working-group document or an IETF
consensus statement.

**Published baseline:** revision **-00**, posted to the IETF archive on
**16 October 2026**. The date inside the document is 15 October 2026.
This repository starts with the exact published XML and TXT, not a new revision.

## Read, review, and contribute

| Resource | Purpose |
| --- | --- |
| [Published -00](https://datatracker.ietf.org/doc/draft-sergeev-audit-task-requirements/00/) | The authoritative IETF revision |
| [Published HTML](https://www.ietf.org/archive/id/draft-sergeev-audit-task-requirements-00.html) | Read the published document |
| [Editor's reading copy](review/editor-copy.md) | Generated from the working XML; not a separate published revision |
| [Working RFCXML](draft-sergeev-audit-task-requirements.xml) | The only editable manuscript source |
| [Frozen XML/TXT and checksums](published/00/) | Exact published baseline for comparisons |
| [Issues](https://github.com/MikhailSergeev369/draft-audit-task-requirements/issues) / [pull requests](https://github.com/MikhailSergeev369/draft-audit-task-requirements/pulls) | Questions, counterexamples, and proposed edits |
| [Builds and review artifacts](https://github.com/MikhailSergeev369/draft-audit-task-requirements/actions/workflows/build.yml) | Generated XML/TXT/HTML, source diff from -00, and build logs |

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
```

Open `build/index.html` locally. Each successful CI artifact includes the exact
working XML, both renderings, the diff from published -00, resolved package
versions, source/output hashes, and formatter logs. Generated build files are
not committed. Network access is needed to install dependencies; manuscript
rendering disables network reference resolution and local-file includes.

These checks concern source integrity and rendering, not the correctness of
the model, legal clearance, interoperability, or IETF acceptance. They do not
claim a fresh online idnits run or bibliographic review. The normal IETF checks
and author confirmation still apply when submitting a future revision.

## Revision policy

The root XML is the working source for future edits. `published/00/` is frozen;
do not update it when preparing -01. Label a future revision in the working
source before submission, leaving already posted files unchanged. Until
Datatracker actually posts that revision, it remains editor's work in progress.

No workflow sends email, submits to Datatracker, creates a release or tag,
or merges a pull request. Continuous integration has read-only repository
permissions. Publication and access changes are separate maintainer actions.

The public history begins at the published document. No earlier private Git
history, private correspondence, unpublished partner text, or research logs
are imported. See [LICENSE.md](LICENSE.md) for document and tooling terms.
