# Audit Store: minimal change for the -01 candidate

Prepared on 20 October 2026. Stored as material for preparing the next -01 candidate; not published as a new I-D revision. The change has not been integrated into the root source or the original PR #3.

Storage branch: `preparation/audit-store-query-20261020`. This directory contains a pinned snapshot for comparison; it is not a second editable manuscript source. Further integration should use the primary RFCXML source and a separate focused PR, in accordance with the repository rules.

Base: draft PR #3 in MikhailSergeev369/draft-audit-task-requirements, commit 4f60a2329a447e6b7c97b5508ecf4ff31a5b1ddb.
Base XML SHA-256: 895bf6162942d455538092003eae3572f1fb57e53e93ffc3db57d82abebd9406.

## Changes

- §5.3: adds a paragraph on search sources, criteria, time bounds, completeness, and material limitations. The context may be conveyed in the response or established by the applicable profile together with information about the particular response. No request or response format is defined.
- §4.2: extends the existing two-source example with an interface implication: an empty record set alone does not distinguish a complete search from an incomplete one. Adds a reference to §5.3.
- Security Considerations is unchanged: it already covers false search reports and the need to account for evidence or material assumptions in the Evaluation Basis.

No new fields, statuses, APIs, infrastructure requirements, or BCP 14 keywords are introduced. All prior changes in the PR #3 candidate are preserved. The date and version number are unchanged: this is an editorial candidate, not a newly published revision.

## Validation

Checks covered XML syntax, internal reference resolution, changes being limited to two sections, and exact application of the patch to the base XML. These are editorial checks, not protocol conformance tests. During initial preparation and when this package was stored, xml2rfc was unavailable; TXT/HTML builds and idnits were not run on the modified XML. Successful checks on the original PR #3 do not validate this modified XML.

## Illustrative semantic check

With identical criteria and cutoff: (1) the first source has been fully searched and the second is unavailable — an empty response does not establish a complete search across both sources; (2) both sources have been fully searched with no matches — Expected but Not Found may apply under the applicable production expectation. Neither case, by itself, proves that the Gateway made no decision.

The package includes the modified XML and a unified diff against the stated base.
## Identity and repeat checks when stored

The package was obtained from `AUDIT_store_query_candidate.zip` (SHA-256 `87dd12642fb5f9c99a97bb00263f30344614a3cdb45e04d3709326dde62824e5`). The XML and patch were preserved byte for byte; the README was clarified for inclusion in the repository.

- [Original PR #3 base](https://github.com/MikhailSergeev369/draft-audit-task-requirements/blob/4f60a2329a447e6b7c97b5508ecf4ff31a5b1ddb/draft-sergeev-audit-task-requirements.xml): 98 986 bytes, SHA-256 `895bf6162942d455538092003eae3572f1fb57e53e93ffc3db57d82abebd9406`.
- [XML with the addition](draft-sergeev-audit-task-requirements.xml): 99 901 bytes, SHA-256 `d82a747d3bd88c1cd8861ff79d8790ab7550e5503220df66ef841095f8bf5445`.
- [Patch](audit-store-query.patch): SHA-256 `a6a8ca6d5c42fff34aa79e990b486a5791998c6d2a61c213e2de3ea527971204`.
- [SHA256SUMS](SHA256SUMS) allows local files to be checked by running `sha256sum -c SHA256SUMS` in this directory.

On 20 October 2026, the base XML was fetched again at the stated commit and verified by SHA-256. Checks covered forward and reverse patch application with byte-for-byte equality, XML syntax, uniqueness of 86 anchors, and resolution of all 28 xrefs. Changes are limited to the sections with anchors `expected-evidence-across-administrative-domains` (§4.2) and `collection-and-query-interfaces` (§5.3). These are integrity and editorial structure checks, not an independent semantic review or a conformance suite.

## Use when preparing the next candidate

1. Use the patch as a proposed addition to the exact PR #3 base, rather than as a replacement for the current root XML on `main`: when the package was stored, `main` still contained -00.
2. If the working base has changed, compare both affected sections and preserve all intervening changes and attributions. Successful patch application alone does not replace this comparison.
3. After integration into the primary source, run `make review`, `make check`, `make test`, and a build with the pinned xml2rfc version; produce a new candidate and its checksums. Before submission, run a current idnits check and the usual publication checks.
4. Consider this package together with the other comments on -01. It preserves only the agreed Audit Store addition and does not establish that all other comments on the future revision have been addressed.

Storing the package does not change the pinned PR #3 preview, the published -00, tags, or releases, and does not submit an I-D.
