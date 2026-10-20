# Decision-time non-establishment: consolidated review cases

Status: illustrative editorial cases for a proposed working -01, not an IETF publication.
No implementation run, external verifier, independent reader, protocol
conformance or interoperability result is claimed. The term and wording have
not been approved by the issue author. Local labels T01–T18 are not wire codes.

Motivation: [issue #1](https://github.com/MikhailSergeev369/draft-audit-task-requirements/issues/1).

## Common reading discipline

Distinguish (1) whether a specified item is available; (2) what its content
asserts about a participant, procedure and decision time; and (3) what the
Evaluation Basis supports for the particular Audit Task. A decision record
and a status answer are different items and may have different requirements
and production expectations. Completed search is not complete event coverage.

For the participant-level cases, G is the participant, R the exact request,
D the identified decision, and P the applicable policy/procedure. These are
illustrative names, not required fields. Qualifications concerning origin,
observation boundary, authority, applicability, native semantics, freshness,
time and reporting accuracy are evidence dependencies. They can be supplied
by related items or explicit assumptions; not every task requires an
independent witness. An item's label is not proof of the assertions it carries.

A completed negative result, a reported inability to establish an input, and
an unevaluated check differ. A report of inability is not a negative result
for the external authorization condition. Other valid authorization bases
may matter for broader tasks than the status of one grant.

The editorial check is whether the cited wording supports the expected
interpretation under the stated premises, without the prohibited inference.
It is not a Boolean executable classifier of arbitrary deployment records.

## T01. Applicable negative status result

**Scenario.** A completed check returns a negative status result. Origin, target authorization, decision relation, effective time, freshness conditions and reliance on the source are established or explicitly assumed.

**Expected interpretation.** The result is an available negative status assertion. Its native semantics and the Evaluation Basis determine whether it supports revocation of this authorization at this time.

**Inference to reject.** Do not equate an arbitrary negative code with revocation, or infer that every other possible authorization basis is invalid.

**Text basis.** §2.15 Negative Observation; §4.3 paired completed-check case.

**Provenance.** Original C3; new-file T01; X6 boundary.

## T02. Recorded timeout; no permitted result

**Scenario.** Policy P requires a usable status input for decision D on request R. The status query times out, no result permitted by P is available, and a qualifying record states the refusal and its grounds.

**Expected interpretation.** The item is available and reports non-establishment under the procedure and conditions. It can satisfy a task about what decision and grounds G recorded. An inference about the actual attempt depends on the stated basis for that assertion.

**Inference to reject.** The same accurate timeout report is compatible with an active or revoked authorization. It does not supply the missing status answer, establish global unavailability, settle all search obligations, or impose refusal outside P.

**Text basis.** §2.15 new description; §4.3 separate refusal case.

**Provenance.** Original C2 and controls 2–4; new-file T02.

## T03. Expected record not found after complete declared search

**Scenario.** An applicable production expectation identifies a decision record. The applicable search over all declared sources for the declared request query and cutoff is complete, and no qualifying item is found.

**Expected interpretation.** Expected but Not Found applies to that item within the declared search scope. Search completeness is not complete event coverage.

**Inference to reject.** Do not infer no decision, no record ever produced, no action, or the participant’s inability to establish the input. The same search may follow loss of a previously produced record.

**Text basis.** §2.15 existing availability definition, unchanged.

**Provenance.** Original C1 and control 1; new-file T03.

## T04. Necessary search source unavailable

**Scenario.** The expected decision record is unavailable to the auditor, and a necessary source cannot be checked; other search parameters are the same as in T03.

**Expected interpretation.** Expected but Search Incomplete applies; a result over all declared sources has not been established.

**Inference to reject.** Do not report Expected but Not Found for the complete declared search, or infer participant-time non-establishment from the auditor’s incomplete search.

**Text basis.** §2.15 existing incomplete-search definition, unchanged.

**Provenance.** Original control 5; new-file T04.

## T05. Refusal record with no disclosed grounds

**Scenario.** A record bound to D and R states DENY; no reason is disclosed. The properties needed to rely on the reported decision are considered separately.

**Expected interpretation.** Evaluate the requirement for a decision separately from a requirement for its grounds. DENY is compatible with a negative status, a timeout or another policy reason.

**Inference to reject.** Do not infer non-establishment or successful downstream enforcement from the label alone.

**Text basis.** §2.14; §2.15; existing Appendix A.8.

**Provenance.** Original control 7; new-file T05.

## T06. Unqualified candidate record

**Scenario.** A candidate reports non-establishment, but origin or a required relation to the relevant request or decision cannot be established.

**Expected interpretation.** Report the limitation. The candidate cannot yet be used as qualified evidence for a requirement needing that property. A narrower task about the text received can differ.

**Inference to reject.** Do not silently treat the item as verified, applicable or sufficient. Do not conclude that every possible Audit Task is Unresolved.

**Text basis.** §2.15 Evidence Applicability/Evaluation Basis qualifier; existing §2.11–2.13.

**Provenance.** New-file T06.

## T07. Failed optional refresh; permitted cache remains

**Scenario.** A new query fails, but G holds a cached result still permitted by the applicable policy and procedure for D.

**Expected interpretation.** Failure of that query does not establish inability to obtain the required input. The actual decision and historical authorization still require their own evaluation.

**Inference to reject.** Do not impose a live-query requirement or universal fail-closed behavior.

**Text basis.** §4.3 final contrast; §2.15 applicable procedure and conditions.

**Provenance.** New-file T07.

## T08. Cache no longer permitted; required refresh fails

**Scenario.** The cached status is outside the conditions permitted by P, a required fresh result is not obtained by D, and no other permitted result is available.

**Expected interpretation.** A qualifying item can report non-establishment under P. The failed attempt does not refresh the cached answer’s as-of time. Refusal follows only under the named policy.

**Inference to reject.** Do not infer revocation, reuse an invalidated cache as current, or apply P to every deployment.

**Text basis.** §2.15; §4.3 no-result and as-of explanations.

**Provenance.** New-file T08.

## T09. Other historical evidence resolves the auditor’s task

**Scenario.** In addition to the T02 record, the auditor later obtains a different sufficient basis for the authorization state at the time of D.

**Expected interpretation.** The historical Audit Task can be resolved under that basis without changing what G had established or what G recorded at D.

**Inference to reject.** Do not force the later auditor to remain Unresolved, or infer that G possessed or used the later evidence.

**Text basis.** §4.3 task separation; Appendix C item 6.

**Provenance.** New-file T09; previous X4.

## T10. Record found; another necessary source not searched

**Scenario.** The T02 record is available, but a separate item or necessary source for the larger Audit Task has not been checked.

**Expected interpretation.** Keep the found item and the incomplete search obligation separate. Availability of this item can coexist with an incomplete search for other evidence.

**Inference to reject.** Do not turn one found record into a complete evidence set or a completed search over all sources.

**Text basis.** §2.15 paragraph on separate requirements and search.

**Provenance.** New-file T10; original common scope.

## T11. Refusal and external effect observed

**Scenario.** A refusal record and separate applicable evidence of an external effect are found. Their propositions, boundaries, exact-action relations and times must be compared.

**Expected interpretation.** Preserve both observations. There is no automatic contradiction: a refusal is not necessarily an assertion of global non-occurrence. Apply Appendix A.8’s explicit terminal-condition rule to its specified task only.

**Inference to reject.** Do not discard effect evidence or remove an effect requirement merely because a refusal is present. A genuine incompatibility, if established, is not to be ignored.

**Text basis.** §4.3 cross-reference; Appendix A.8 (unchanged); §2.15 Conflicting Evidence.

**Provenance.** New-file T11.

## T12. Reader cannot determine from limited specification text

**Scenario.** A reader reports cannot-tell because its consulted texts leave an interpretation open. This scenario is hypothetical; no reader run is performed for this candidate.

**Expected interpretation.** Describe what was read, the property evaluated and the resulting limitation under existing §5.4/Evaluation Basis. Keep text-interpretation uncertainty separate from runtime input unavailability.

**Inference to reject.** Do not infer implementation non-conformance, runtime non-establishment or a missing event. Do not treat this as a measurement of the proposed patch.

**Text basis.** Existing §5.4 and Evaluation Basis; optional P5 remains unapplied.

**Provenance.** New-file T12; adjacent source-of-uncertainty discussion.

## T13. Positive check completed; revocation not yet discoverable

**Scenario.** G completed a positive check using a result accepted by the applicable procedure. A change in authorization was not yet reflected in the information available to G.

**Expected interpretation.** Non-discovery of that change does not by itself show non-establishment of the required input. Evaluate historical status and correctness of D separately.

**Inference to reject.** Do not relabel every undiscovered revocation as a timeout/non-establishment, or infer that the accepted answer necessarily represented the actual historical status.

**Text basis.** §4.3 final contrast.

**Provenance.** Previous X1; fourth contrast accepted in the consolidation.

## T14. Required check was not started

**Scenario.** A required check was not run before D; the record only reports that no result was obtained. There is no stated basis showing inability under the procedure.

**Expected interpretation.** Distinguish an unevaluated check or absent result from reported inability. Assess any separate procedural omission against the applicable policy, not against a new universal AUDIT rule.

**Inference to reject.** Do not infer could-not-establish from did-not-establish alone, or presume that permitted alternatives were exhausted.

**Text basis.** §2.15 first new paragraph; Appendix C item 6.

**Provenance.** Previous X2.

## T15. Response arrives after the decision

**Scenario.** At D, G has no permitted result and records that fact. A response arrives later. Its receipt time and the effective time or as-of time of the assertion are distinct.

**Expected interpretation.** The response can support a historical task only if its semantics and time binding cover the relevant condition at D. Late receipt does not imply G used the response at D.

**Inference to reject.** Do not rewrite the participant’s knowledge at D; a later-time status assertion alone does not establish the historical status.

**Text basis.** §4.3 original historical-state distinction and new later-evidence paragraph; Appendix C item 6.

**Provenance.** Previous X3.

## T16. Genuinely incompatible participant-state assertions

**Scenario.** Two individually usable, applicable items make mutually exclusive assertions: for the same participant, D, input, procedure and cutoff, one asserts the input was established before D; the other asserts it was not. Scope or timing differences do not explain them.

**Expected interpretation.** Identify Conflicting Evidence for the relevant task and retain both items and grounds for their qualification. It is not the mere existence of two different record labels that makes the conflict.

**Inference to reject.** Do not accept the non-establishment statement automatically, or use the warning about false conflicts in T11 to overlook an actual incompatibility.

**Text basis.** §2.15 existing Conflicting Evidence; new applicability qualifier.

**Provenance.** Previous X5.

## T17. Generic negative code without revocation semantics

**Scenario.** A completed status call returns a generic negative code. Native semantics do not establish that the relevant authorization was revoked with effect at D.

**Expected interpretation.** Record the narrower negative result actually supported. Revocation is not established by this code alone, even though the call completed.

**Inference to reject.** Do not replace timeout with revoked, or replace generic negative with revoked. A different sufficient historical basis may still answer the audit task.

**Text basis.** §4.3 paired-case qualification; Appendix C alternative bases.

**Provenance.** Previous X6; explicit boundary of T01.

## T18. Later reconstruction presented as decision-time recording

**Scenario.** An item produced after D reports G’s state at D. A signature or timestamp string is present, but no sufficient evidence or stated assumption establishes contemporaneous recording.

**Expected interpretation.** The item may be available and report decision-time state. Its label does not establish when it was created. The contemporaneity claim requires its own supporting basis.

**Inference to reject.** Do not reject all retrospective evidence, and do not prove at-decision recording solely from the name of the description, signature or timestamp string.

**Text basis.** §2.15 explicit time-of-recording paragraph; existing authenticity limits.

**Provenance.** Original timing control 6; terminology refinement in the accepted review.

## Crosswalk and review limits

Original C1 → T03; C2 → T02; C3 → T01. Original controls 1–7 are preserved
by T03, T02, T01/T02, T01/T02/T17, T04, T18 and T05/T11 respectively.
The later proposal's T01–T12 retain their identifiers. Earlier additional
X1–X6 map to T13, T14, T15, T09, T16 and T17. T18 makes the original recording-
time control explicit. T12 is an adjacent check against existing §5.4, not
an acceptance dependency for P1–P4; optional P5 is not in the candidate.

All 18 cases have been compared with the proposed text as an editorial
exercise. This does not establish how an independent reader will interpret
it. The separate blinded exercise is prepared but has not been performed.
Source parsing, regression tests, patch round trips and build status are
separate technical checks. They do not prove the substantive conclusions.
