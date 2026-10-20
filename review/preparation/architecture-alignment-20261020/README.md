# Architecture alignment input for the next -01 candidate

Prepared 20 October 2026. This is editor preparation material, not an IETF
publication, a merged manuscript change, or an agreement with the architecture
authors. The root manuscript, PR #3 and its site preview are unchanged.

The [mapping and shared A/B case](ALIGNMENT.md) connect the existing Auditor and
WI-4 query interface to Audit Task. The only new manuscript change is one
paragraph (two sentences) at the end of section 6.1:

> The Auditor-facing query interface proposed as WI-4 in Section 6 of [AUDIT-ARCH] is one point of application for this model. The query-response considerations in Section 5.3 identify search scope, completion, and limitations that can be material to the Auditor's Evaluation Basis.

The XML uses cross-references in place of the display labels above. No new role,
wire format, mandatory field, result code or BCP 14 requirement is introduced.
The conditional wording preserves the possibility that search information is
sufficient for a narrowly scoped Audit Task.

## Files and exact bases

- [architecture-alignment.patch](architecture-alignment.patch): incremental
  change against the Audit Store candidate XML at preparation commit
  `4d48cfff09a3b13deb1166d18f7c742c63fffe77`, SHA-256
  `d82a747d3bd88c1cd8861ff79d8790ab7550e5503220df66ef841095f8bf5445`.
- [combined-from-pr3.patch](combined-from-pr3.patch): sections 4.2, 5.3 and 6.1
  together, against PR #3 commit `4f60a2329a447e6b7c97b5508ecf4ff31a5b1ddb`,
  XML SHA-256 `895bf6162942d455538092003eae3572f1fb57e53e93ffc3db57d82abebd9406`.
- [Resulting XML](draft-sergeev-audit-task-requirements.xml): 100,249 bytes,
  SHA-256 `5c94a3d22f8f20bb127cfc5b960362704960651b4818761a182e71caa231b8c0`.
  This is a frozen review snapshot, not another editable manuscript source.
- [validation.json](validation.json) and [SHA256SUMS](SHA256SUMS): exact scope,
  checked identities and integrity results.

Choose the incremental patch OR the combined patch according to the exact
starting XML; do not apply both. If the working source has changed, reconcile
all intervening edits instead of replacing it with this snapshot. The earlier
Audit Store package is preserved and remains the base of the incremental patch.

## Verification and next integration step

Both patches passed forward/reverse application with exact byte comparisons.
The XML parses; all 86 anchors are unique and all 30 xrefs resolve. Removing
exactly the added paragraph reproduces the previous Audit Store candidate.
No new independent semantic review or protocol conformance result is claimed.

xml2rfc is unavailable in this environment; no TXT/HTML build or idnits result
is claimed for this XML. When incorporating the proposed changes into the main
manuscript, regenerate the editor reading copy and run the repository checks,
the pinned formatter and the normal publication preflight. This package does
not incorporate or dispose of all other feedback on the future -01 revision.
