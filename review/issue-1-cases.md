# Issue #1: editorial review cases

These are synthetic reading cases for the proposed decision-time input
clarification in [Issue #1](https://github.com/MikhailSergeev369/draft-audit-task-requirements/issues/1).
They are not normative conformance tests or observations of a deployment.
On 18 October 2026, the assistant checked each expected reading below against
the working XML. This is a semantic text review, not an independently authored
implementation or an external reviewer's approval.

Reviewed XML SHA-256:
`4e82b2e915450be128d82a2b77990a00b67e2204fcdd8b7d7ed98bfe29830590`.

All 17 readings below are supported by the identified text under the case's
stated premises. No actual status service, MolTrust implementation, or runtime
decision procedure was executed in this review. A real audit would still need
to establish the applicable procedure, source semantics and factual premises.

| Case | Stated situation | Reading and limit | Text basis |
| --- | --- | --- | --- |
| C01 | A completed check returns a usable negative result. | An input result exists. Its native semantics determine what is negative; a negative result is not missing input. | §2.15; §4.3 |
| C02 | A required retrieval times out, no usable alternative is established, and the decision record is found. | The record can support the decision and its stated grounds. A timeout does not establish revocation. | §2.15; §4.3 |
| C03 | A record is expected; the applicable search of every declared source is complete for the query and cutoff; no qualifying record is found. | Expected but Not Found is bounded by that search. It does not establish non-production, non-decision, or no external effect. | §2.15 |
| C04 | A record is expected but a necessary source cannot be checked or its retrieval is incomplete. | Expected but Search Incomplete preserves any narrower result from checked sources; it does not establish absence across all sources. | §2.15; §4.2 |
| C05 | Only DENY is recorded, without grounds. | The decision label alone does not identify a timeout, negative input result, or omitted check. | §2.15; Appendix A.8 |
| C06 | Origin or applicability to the identified decision is not established. | Report that qualification limit; do not treat the candidate as already applicable evidence of this decision. | §2.15; §4.3 |
| C07 | An extra live request fails, but a cached answer remains usable under the applicable procedure. | The failed attempt alone does not establish that the required input was not established. | §2.15; §4.3 |
| C08 | A cached answer is unusable under the procedure, and no usable alternative is established. | Some status bytes being present does not establish a usable input. Preserve the grounds for unusability. | §2.15; §4.3 |
| C09 | A required check was not performed. | Preserve that condition and the known or unspecified cause; do not turn omission into demonstrated technical impossibility. | §2.15 |
| C10 | An answer arrives after the decision. | Distinguish arrival time, decision time and the answer's historical reference time; later availability is not earlier use. | §2.15; §4.3 |
| C11 | Another sufficient historical basis later becomes available. | The later auditor may resolve the input question without changing what the participant had established then. | §4.3; Appendix C, item 6 |
| C12 | The non-establishment record is found, but another required source remains unchecked. | Record availability and incompleteness of the wider search can coexist. | §2.15; §4.3 |
| C13 | A refusal record and separate applicable evidence of an external effect are available. | Preserve both; refusal does not establish no effect. Compare exact propositions before claiming a conflict. | §2.15; Appendix A.8 |
| C14 | Two individually usable items support incompatible conclusions about the same input, decision, time and meaning. | Report Conflicting Evidence and the resolution or remaining limit; different times or tasks alone are not such a conflict. | §2.15 |
| C15 | A generic negative status result is available. | Use the source's native semantics; do not infer a particular cause such as revocation from an aggregate negative value. | §4.3 |
| C16 | A positive answer was accepted under the procedure, while a later revocation was undiscovered. | Non-discovery alone establishes neither input non-establishment nor correctness of the authorization decision. | §4.3 |
| C17 | A later-created record describes the participant's decision-time state. | Its content and evidence of decision-time recording are different claims. | §2.15; §4.3 |

The reader experiment, differences between rejection rules, and cumulative
budget examples are separate research questions. They are not prerequisites
for evaluating this focused wording change. The existing two search-outcome
definitions and Appendix A.8 are unchanged.
