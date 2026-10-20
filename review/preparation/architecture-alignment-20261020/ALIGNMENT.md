# AUDIT Architecture / Audit Task alignment

Editor's proposed mapping, 20 October 2026. This records a concrete point of
composition; it does not claim agreement by the architecture authors or the WG.

## Pinned inputs

- Architecture: `draft-kuehlewind-audit-architecture-01`, repository commit
  [`2ab1e6c57e18285e2e9d99f1d82ba7e99c50ffd6`](https://github.com/mirjak/draft-audit-architecture/blob/2ab1e6c57e18285e2e9d99f1d82ba7e99c50ffd6/draft-kuehlewind-audit-architecture.md).
- Audit Task: PR #3 commit
  [`4f60a2329a447e6b7c97b5508ecf4ff31a5b1ddb`](https://github.com/MikhailSergeev369/draft-audit-task-requirements/pull/3),
  followed by the unchanged XML/patch in the
  [Audit Store preparation package](../audit-store-query-20261020/README.md).
- This package adds only the explicit WI-4 connection in section 6.1.

## Responsibilities and section mapping

| Architecture location | Audit Task location | Proposed connection and boundary |
| --- | --- | --- |
| Section 4.3, Auditor | Sections 2.1, 2.5, 2.13-2.14 and 6.1 | Audit Task makes the question, alternative sufficient requirements, evaluation basis and bounded result explicit for the existing Auditor role. It adds no role or universal audit policy. |
| Section 5, record classes | Sections 2.3 and 6.1 | Architecture records can be Audit Evidence Items. The evidence category also admits receipts, Attestation Results and other relevant observations; it is not a competing record format. |
| Section 3.1 and WI-6, Audit Context | Sections 2.10 and 6.1 | Context identifiers can help evaluate relations. Correlation alone does not establish causation, derivation or sufficiency. |
| Section 4.2, Audit Store; section 6, WI-4 | Sections 2.13, 4.2 and 5.3; the added paragraph in 6.1 | A response's search scope, completion and material limitations can affect the Auditor's Evaluation Basis. The concrete request/response representation belongs to an interface specification or profile. |
| Sections 3.3 and 4.2; WI-2 and WI-3 | Sections 2.12, 3.4 and 6.2-6.3 | Verification results retain their native RATS/SCITT semantics and assumptions. Successful verification contributes only the properties actually established. |
| Section 8, corroboration and trust assumptions | Sections 2.8-2.9, 3.3-3.4 and 7 | Observation, effective coverage and control of evidence production limit an audit conclusion. No universal independent witness or completeness mechanism is introduced. |
| Section 9, privacy; WI-4 and WI-5 | Sections 5.5 and 8 | Requirements can support evidence minimization. Access limitations must not be interpreted as absence; a response need not disclose the existence of protected records. |
| Architecture record-production duties | Sections 3.2 and 6.7 | Applicable duties or declarations can establish production expectations. Meeting those expectations and satisfying a particular audit question remain separate assessments. |

The last column is a proposed mapping, not a claim that the architecture has
adopted Audit Task terminology. Native record and verification specifications
remain authoritative. The model is useful beyond Audit Store queries.

## Shared illustrative case for WI-4

Assume the same declared sources A and B, query for the gateway decision record
for request R, matching criteria, time bounds, and cutoff with the same as-of
meaning. No other evidence resolves whether a qualifying record is available.
Both responses contain an empty record set; only completion of the B search
differs. For this example, the stated search results are accepted under
identified evidence or assumptions about the search procedure.

| Case | A | B | Supported interpretation |
| --- | --- | --- | --- |
| Incomplete search | Fully searched; no match | Unavailable; not searched | No match was found in A within the stated bounds. The search over A+B is incomplete. |
| Completed search | Fully searched; no match | Fully searched; no match | No qualifying record was found across A+B within the stated bounds. |

The response and its applicable profile should let the recipient distinguish
these cases. An empty list is not itself an error. The problem is a final
interpretation that hides the incomplete search. This is an illustrative
semantic check, not an executable conformance test or a prescribed API schema.

Neither result alone establishes that the gateway failed to create the record,
that no decision was taken, or that an external effect did not occur. A claimed
search-completion result is not automatically independent proof of completion.
The example uses neutral descriptions; applying the `Expected but ...` labels
also requires an established production expectation.

## Existing discussion locations

- [Architecture issue #18](https://github.com/mirjak/draft-audit-architecture/issues/18):
  purpose and placement of the Audit Store interface; the A/B case belongs here.
- [#30](https://github.com/mirjak/draft-audit-architecture/issues/30): observations
  at a boundary versus external effects.
- [#31](https://github.com/mirjak/draft-audit-architecture/issues/31): Recorder
  independence and the transparency alternative.
- [#32](https://github.com/mirjak/draft-audit-architecture/issues/32): interpretation
  and verification limits; an editor proposal is already present.
- [#34](https://github.com/mirjak/draft-audit-architecture/issues/34): parent
  references and action derivation.
- [#35](https://github.com/mirjak/draft-audit-architecture/issues/35): coverage
  boundaries of Service-side corroboration.

Keep these substantive questions in their respective discussions. A future
architecture change can describe the interface's purpose and semantic needs,
with encodings left to a separate specification. A reciprocal informative
reference is an option for the architecture authors, not a prerequisite or a
claimed decision. No architecture PR is included in this package.
