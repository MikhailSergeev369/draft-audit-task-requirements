# Task-Relative Evidence Requirements for Agent Auditing

**Generated editor's reading copy, not a separate IETF publication.**

Source SHA-256: `e83c17d6a43fe66a010502655a94dae067195b36e9001f9f8de11e5fb164dc5a`. Edit the [RFCXML](../draft-sergeev-audit-task-requirements.xml), not this file.

[Published -00](https://datatracker.ietf.org/doc/draft-sergeev-audit-task-requirements/00/) · [Contributing](../CONTRIBUTING.md)

## Abstract

Agent auditing can rely on information produced by users, agents, tools, services, policy components, and other systems across multiple administrative domains. The evidence needed to answer one auditing question is not necessarily the evidence needed to answer another. Successful verification of available evidence also does not, by itself, establish that the evidence is applicable or sufficient for the question being evaluated.

This document describes a representation-independent model for stating an Audit Task, alternative evidence requirements for that task, expectations about evidence production, and the basis for an audit result. It distinguishes verification of evidence from evaluation of the Audit Task, missing evidence from a negative observation, and validity of individual records from cross-domain sufficiency. It defines no audit record format, verification mechanism, authorization model, completeness mechanism, storage protocol, or auditing policy.

## Discussion Venues

This is an individual working draft, not a working-group document.

Related discussion is archived on the [AUDIT mailing list](https://mailarchive.ietf.org/arch/browse/audit/). Discussion does not establish IETF or working-group consensus.

<a id="introduction"></a>

# Introduction

Cross-domain agent auditing requires more than collecting records and checking their integrity.

A single logical operation can produce evidence at several boundaries. A user interface can record an approval. An authorization component can record a decision. An agent or gateway can record an invocation. A service can record a request or resulting state change. These records can refer to the same operation while supporting answers to different questions.

For example, evidence that a refund was authorized does not establish that it was invoked. Evidence that it was invoked does not establish that the provider committed the refund. A provider-side record stating that a refund was committed does not, by itself, establish that the action was authorized. A signature, receipt, or transparency registration can establish properties of an artifact without establishing the truth of every assertion carried by that artifact.

Across administrative domains, no single participant necessarily has complete visibility into the interaction chain. Different participants can use different record formats, observe different boundaries, and apply different retention, disclosure, or verification mechanisms. Missing evidence can mean that an expected item is unavailable, that no item was expected from a participant, that an event fell outside the participant's coverage, or that the applicable expectation is unknown.

This document describes a task-relative model for making those distinctions explicit. The model is intended as problem-space and requirements input for possible AUDIT work.

The model can be used by an Auditor in the architecture described in [AUDIT-ARCH](#AUDIT-ARCH) to identify the evidence needed for a particular auditing question and report the basis and limitations of the result.

<a id="key-separations"></a>

## Key Separations

The model depends on four separations.

**Audit Scope is not Evidence Coverage.** Audit Scope identifies what the auditor is trying to evaluate. Evidence Coverage describes what a particular source or mechanism is represented or expected to observe or record.

**Evidence Requirements are not Evidence Production Expectations.** Evidence requirements identify what is needed to answer an Audit Task. Production expectations identify what a particular source or mechanism was expected to produce.

**The Audit Evidence Set is not the Evaluation Basis.** The Audit Evidence Set is what is available to an auditor. The Evaluation Basis identifies what evidence, procedures, profiles, and assumptions were actually used to produce a result.

**An Evidence Verification Result is not an Audit Evaluation Result.** Verification reports properties established by a verification procedure. An Audit Evaluation Result answers the substantive Audit Task to the extent supported by the Evaluation Basis.

These separations allow a specification or deployment to report a bounded result without silently turning record presence, successful verification, or record absence into a stronger conclusion.

<a id="goal"></a>

## Goal

This document provides a common vocabulary for describing:

- the auditing question and its scope;
- one or more alternative evidence combinations sufficient to evaluate that question;
- what identified participants or mechanisms are expected to produce;
- what evidence is available, verified, and applicable;
- what evidence and assumptions were actually used;
- and the bounded Audit Evaluation Result that follows.

The model supports identifying task-sufficient evidence combinations. Different combinations can satisfy the same task-relative requirements under stated assumptions. The model does not define a minimization criterion or require a unique minimum.

<a id="scope-and-non-goals"></a>

## Scope and Non-Goals

This document addresses task-relative evidence requirements and evaluation for observable audit information in distributed and delegated systems.

It does not define:

- an audit record or conversation format;
- an Audit Store or query protocol;
- a transport or context-propagation protocol;
- a new identity, authorization, or enforcement mechanism;
- a verification, attestation, transparency, or omission-control mechanism;
- a trust score, assurance level, or compliance framework;
- a relying-party decision policy;
- or a model of internal reasoning or hidden chain-of-thought.

The model describes evidence properties, sources, Observation Boundaries, Evidence Coverage, Evidence Relations, Evidence Applicability, and Evidence Verification Results independently of any particular record format, field name, extension point, container, or serialization. A profile or mapping can bind these semantic requirements to concrete representations.

The document does not attempt to establish why an agent internally selected an action. It deals with observable evidence and represented relationships.

The specification that defines a native record or result remains authoritative for its semantics. This document does not reinterpret native authorization, execution, effect, attestation, or transparency results. It describes how those bounded results can be required, expected, combined, or found insufficient for a cross-domain Audit Task.

An **Audit Task** in this document is an auditing question. It is not an agent-protocol task, workload object, dialog state, or execution unit.

This document specifies no BCP 14 requirements.

<a id="terminology"></a>

# Terminology

The following terms are limited to the task-relative model.

<a id="audit-task"></a>

## Audit Task

**Audit Task:** A specific question to be evaluated using audit evidence.

Examples include whether an action was authorized, whether an operation was invoked, whether an external effect was observed, whether a distributed workflow was internally consistent, or whether an action was within the authority applicable at a particular time.

Different Audit Tasks concerning the same logical operation can require different evidence.

<a id="audit-scope"></a>

## Audit Scope

**Audit Scope:** The actors, events, states, relationships, resources, and time interval to which an Audit Task applies.

Audit Scope describes what is being evaluated.

<a id="audit-evidence-item"></a>

## Audit Evidence Item

**Audit Evidence Item:** A record, observation, disclosed portion of a record, receipt, attestation result, external-state artifact, response, measurement, or other information considered when evaluating an Audit Task.

An item can be authentic, structurally valid, or successfully verified while still being inapplicable, insufficient, contradictory, or unable to support a stronger conclusion.

The term is generic audit terminology and does not redefine **Evidence** as used by the Remote ATtestation procedureS (RATS) architecture [RFC9334](#RFC9334).

<a id="audit-evidence-set"></a>

## Audit Evidence Set

**Audit Evidence Set:** The collection of Audit Evidence Items available to a particular auditor for evaluating an Audit Task.

An item that exists elsewhere in a system is not necessarily part of the Audit Evidence Set available to that auditor. Different auditors can therefore have different Audit Evidence Sets for the same underlying events.

<a id="evidence-requirement-set"></a>

## Evidence Requirement Set

**Evidence Requirement Set:** A set of conditions on evidence that, when satisfied under the applicable assumptions, is sufficient to evaluate an Audit Task to a stated extent.

A set can identify required evidence classes, sources, recipients or holders, delivery or retention conditions, Observation Boundaries, temporal or historical-state conditions, coverage properties, and relationships among items.

An Audit Task can have multiple alternative Evidence Requirement Sets. An Evidence Requirement Set states semantic conditions on evidence; it does not prescribe carrier-native fields or extension points. The document does not assume one unique or globally minimal evidence set.

An Evidence Requirement Set in this document is an auditor-side condition for evaluating an Audit Task. It is distinct from any native pre-execution or admission evidence requirement used by an executor or enforcement boundary.

An Evidence Requirement Set identifies the conclusion, or class of conclusions, it can support under stated assumptions. Failure to satisfy that set does not establish the opposite conclusion.

A set can make an individual requirement conditional. The condition and its effect on that requirement are explicit in the set or a referenced profile. The Evaluation Basis identifies the condition and the evidence or stated assumptions used to determine whether it applies. Failure to establish the condition does not establish that the requirement is inapplicable. Whether a requirement applies is distinct from whether an available item satisfies it.

<a id="evidence-production-expectation"></a>

## Evidence Production Expectation

**Evidence Production Expectation:** An expectation that a specified Evidence Source will produce or make available a specified class of Audit Evidence Items for qualifying events within a stated scope.

A production expectation has an identifiable basis, such as a specification, profile, deployment agreement, participant commitment, or operational policy.

Where delivery or retention matters, that basis separately identifies the expected producer, the required recipient or holder, the party responsible for delivery or retention, and the relevant deadline or interval. These roles can be held by different parties. The source searched by the auditor can also differ from those parties. A holder does not become the Evidence Source of the original assertion merely by storing the item.

Where timing is material, an evaluation distinguishes an expectation that applied during the audited interval from one introduced only during later analysis.

<a id="evidence-source"></a>

## Evidence Source

**Evidence Source:** The role, component, person, service, or administrative party responsible for the information asserted or observed by an Audit Evidence Item.

The Evidence Source is not necessarily the component that transports, stores, serializes, registers, or presents the item.

For example, a transparency service can provide evidence that a statement was registered without becoming the source of the statement's assertion about an external event.

Where control is material to an Audit Task, the Evaluation Basis identifies who controlled the relevant observation, evidence-production, or disclosure path. Organizational separation alone does not establish independent observation. Conversely, evidence produced at the acting boundary can be subject to an external constraint, anchor, or witness that materially limits unilateral control over its production.

<a id="observation-boundary"></a>

## Observation Boundary

**Observation Boundary:** A point in a system at which an event, state, input, output, or transition can be observed for audit purposes.

Examples include a user-approval interface, an agent-to-tool boundary, a pre-tool hook, a policy decision point, a gateway, an execution mediator, or an external service.

An Observation Boundary limits what evidence produced there can directly support. Observation of authorization does not establish execution; observation of invocation does not establish an external effect.

An Observation Boundary describes where a fact can be observed. Evidence Source describes who is responsible for the information asserted or observed there.

An Observation Boundary is a semantic property of what can be observed at a system boundary. It is not established merely by the presence of a carrier-specific field, record type, extension, or label.

<a id="evidence-coverage"></a>

## Evidence Coverage

**Evidence Coverage:** The set of events, actors, paths, states, resources, or time intervals that an Evidence Source or mechanism is represented or expected to cover.

Declared Evidence Coverage does not by itself establish that the represented coverage was effective throughout the audited interval. It also does not establish that every qualifying event was recorded, that omissions are detectable, or that the observation path could not be bypassed.

Evidence Coverage is distinct from Audit Scope.

<a id="evidence-relation"></a>

## Evidence Relation

**Evidence Relation:** A relationship between Audit Evidence Items, or between an Audit Evidence Item and the subject of an Audit Task, that is relevant to evaluating the task.

Examples include correlation, ordering, transaction membership, subject or destination binding, semantic consistency, derivation, delegation lineage, and causation.

Establishing one relation does not establish a stronger one. Correlation does not establish derivation; ordering does not establish causation; a common identifier does not establish semantic consistency; and a relation established at one crossing does not automatically establish the same relation across an end-to-end chain. The crossing distinction is illustrated by Sumit Ahuja's example [AHUJA-CROSSING](#AHUJA-CROSSING).

A carrier-native reference establishes only the Evidence Relation defined for that reference by the applicable specification, profile, or mapping. Cryptographic protection, co-location in one container, or use of a common identifier does not by itself strengthen that relation.

<a id="evidence-applicability"></a>

## Evidence Applicability

**Evidence Applicability:** Whether an Audit Evidence Item, or a claimed relation involving it, applies to the subject, actor, destination, resource, time, context, and scope relevant to an Audit Task.

Evidence Applicability is distinct from validity and authenticity.

An item can verify correctly while referring to a different transaction, destination, authorization interval, policy version, delegation context, or audited event.

Where a requirement concerns production, delivery, or retention, applicability is evaluated against the relevant role, destination, and interval. Evidence from the correct producer can support production without establishing delivery to the required recipient or retention by the required holder. The destination of the audited action and the recipient or holder of its evidence are not necessarily the same party. These questions about an item differ from the conditional applicability of a requirement in [evidence-requirement-set](#evidence-requirement-set).

<a id="evidence-verification-result"></a>

## Evidence Verification Result

**Evidence Verification Result:** The result of applying an identified verification procedure to one or more Audit Evidence Items.

An Evidence Verification Result reports the checks actually performed, such as schema validation, signature verification, checks of canonical form where required by the applicable specification, hash or chain verification, receipt-to-record binding, transparency inclusion, attestation appraisal, or a profile-defined semantic predicate.

A successful Evidence Verification Result does not answer the Audit Task unless the verified properties are sufficient for that task.

The result is scoped to the checks actually performed and to their material assumptions and limitations. A negative verification result, an inability to perform a check because required inputs are unavailable, and a successful check of a narrower property are distinct conditions.

Where a verification result includes an omission- or completeness-related property, the result also identifies the applicable population or coverage and the party or mechanism by which an omission is detectable.

<a id="evaluation-basis"></a>

## Evaluation Basis

**Evaluation Basis:** The Audit Evidence Items, Evidence Verification Results, evaluation procedures, applicable specification, profile, or mapping versions, evidence-selection rules, and material assumptions actually used to produce an Audit Evaluation Result.

The Evaluation Basis is not necessarily the whole Audit Evidence Set.

The Evaluation Basis identifies the applicable Evidence Requirement Set or Sets, including the version or identifiable revision used, and the basis of any production expectation material to the result.

Where a result depends on an item not being found, the Evaluation Basis also identifies the declared sources, the query, the search cutoff and its as-of meaning, whether the applicable search completed for each source, and material limitations. A search cutoff is distinct from a deadline for production or delivery, or an interval of required retention.

Omitting materially contradictory applicable evidence from the positive support path does not make that evidence irrelevant. Where materially relevant evidence is excluded, the Evaluation Basis identifies the applicable selection or exclusion rule.

<a id="audit-evaluation-result"></a>

## Audit Evaluation Result

**Audit Evaluation Result:** The result of evaluating an Audit Task against an Evaluation Basis at a stated time.

A result can support a positive or negative conclusion, identify insufficient or conflicting evidence, or remain unresolved. This document defines no closed result-code set.

An operational state recorded in evidence, such as `pending`, `denied`, or `execution_lost`, is not by itself an Audit Evaluation Result.

A result distinguishes evidence satisfying a requirement from an explicit condition making that requirement inapplicable, and from an inability to determine applicability or satisfaction. It identifies the condition, its supporting basis, and which part of the Audit Task has been resolved. Conditional non-applicability is not evidence that an event did not occur.

Additional evidence can strengthen, weaken, contradict, or leave unchanged an earlier result. A later result does not imply that an earlier, correctly bounded result was erroneous.

When an Audit Evaluation Result is propagated, summarized, or aggregated, its evaluator or source, Audit Task and Audit Scope, evaluation time, and Evaluation Basis (or a stable reference to that basis) remain attributable. Otherwise a bounded result can become an unattributed conclusion as it moves between systems.

<a id="evidence-availability-states"></a>

## Availability, Observations, and Evaluation States

The following distinctions concern different aspects of an audit. They are not values of one closed result-code set.

*Expectations and availability.*

**Expected but Not Found:** An applicable Evidence Production Expectation indicates that an item should have been produced or made available, but no qualifying item was found after completing the applicable search over all declared sources for the declared query and cutoff.

**Expected but Search Incomplete:** An applicable Evidence Production Expectation indicates that an item should have been produced or made available, but the item is not available to the auditor and the applicable search is incomplete, for example because a necessary source cannot be checked.

**Expected but Not Found** supports only a bounded finding about the declared sources, query, and cutoff. **Expected but Search Incomplete** does not support that finding over all declared sources. Neither state, by itself, establishes that the item was never produced or that the underlying event did not occur.

**Not Expected:** No applicable Evidence Production Expectation calls for the item from the relevant source or boundary.

**Expectation Undetermined:** Available information is insufficient to determine whether an item should have been expected.

*Content of evidence.*

**Negative Observation:** An Audit Evidence Item affirmatively records a negative event, state, or result within an applicable Observation Boundary.

*Evaluation status and conflicts.*

**Unresolved:** The Evaluation Basis does not support a sufficiently grounded positive or negative conclusion for the Audit Task. An Unresolved result is not a Negative Observation and does not by itself refute the proposition being evaluated.

**Conflicting Evidence:** Individually usable Audit Evidence Items support incompatible observations or conclusions relevant to the same Audit Task.

Absence of an Audit Evidence Item is not, by itself, a Negative Observation.

<a id="task-relative-evidence-model"></a>

# Task-Relative Evidence Model

<a id="audit-task-and-alternative-evidence-requirements"></a>

## Audit Task and Alternative Evidence Requirements

An Audit Task identifies the question to be answered and its Audit Scope.

The task can then be associated with one or more alternative Evidence Requirement Sets.

For example, consider:

> Did operation O produce provider-side effect E?

One Evidence Requirement Set can require provider-side evidence that, under its native specification, establishes the relevant effect semantics, together with evidence binding the provider-side outcome to O.

Another can require independently obtained provider state that establishes E at the relevant time, together with Evidence Relations and stated assumptions sufficient to attribute that effect to O. A relation between O and the affected resource alone does not establish that O produced E.

A domain-specific profile can define another sufficient set.

A profile or mapping can specify how a concrete representation satisfies an Evidence Requirement Set. Mapping carrier-native fields, references, or result values into this model does not, by itself, strengthen the semantic property supported by the underlying evidence or Evidence Verification Results.

This separation allows different protocols, formats, or deployments to satisfy the same auditing question without requiring a universal record format.

It also allows a privacy-aware deployment to prefer a less-disclosing sufficient set when more than one set is available.

<a id="evidence-requirements-and-production-expectations"></a>

## Evidence Requirements and Production Expectations

Evidence requirements and production expectations answer different questions.

An Evidence Requirement Set asks:

> What evidence is sufficient to evaluate this Audit Task?

An Evidence Production Expectation asks:

> What evidence was this source or mechanism expected to produce?

An Evidence Requirement Set can call for provider-side evidence even when the provider does not participate in the auditing system. If that evidence is unavailable and no alternative applicable Evidence Requirement Set can be satisfied from the available evidence, the Audit Task remains **Unresolved**. The unavailability of the provider-side evidence does not, by itself, establish a failure to meet a production expectation.

Conversely, a gateway can be expected to produce evidence of its decision for every qualifying request even when that evidence alone is not sufficient to answer the broader Audit Task.

Interpreting missing evidence as an unmet production expectation requires an applicable expectation and an identifiable basis. Missing evidence can still limit an Audit Task even when no production expectation applied. These distinctions do not require the auditor to determine why the evidence is unavailable.

A carrier's ability to represent a class of information does not, by itself, establish an Evidence Production Expectation. An expectation that a source will produce or disclose that information requires an applicable basis as described in [evidence-production-expectation](#evidence-production-expectation).

<a id="coverage-and-effective-coverage"></a>

## Coverage and Effective Coverage

Evidence Coverage states which event classes, paths, resources, or intervals a source or mechanism is represented or expected to cover.

That representation is not proof that coverage actually held throughout the audited interval.

Outages, bypass paths, partial deployment, configuration changes, or adversarial control can reduce effective coverage.

Collection can also be deliberately limited by instrumentation settings, sampling, filtering, or truncation. Where material to the result, the Evaluation Basis identifies the collection settings applicable during the audited interval and their effects on recording, export, retention, or disclosure. A configuration that limits collection does not, by itself, remove a production, delivery, or retention expectation established on an independent basis.

A complete search of a telemetry backend does not establish complete observation or recording of the audited events. Separately stored content can be available even when associated telemetry was not recorded or exported. Conversely, an available telemetry record can refer to content that the auditor cannot obtain.

Where an Audit Evaluation Result depends on coverage having been effective, the Evaluation Basis includes either evidence supporting that condition or an explicit assumption identifying it.

In particular, a stronger conclusion that an event did not occur generally requires more than a missing record. It can depend on a defined event class and interval, an applicable production expectation, effective coverage, and grounds for believing relevant omissions or bypasses would have been detectable.

This document defines no universal completeness or omission-control mechanism.

<a id="verification-applicability-and-evaluation"></a>

## Verification, Applicability, and Evaluation

Verification establishes the properties checked by a verification procedure.

Applicability asks whether the verified item belongs to the audited subject and context.

These are separate.

A signed authorization record can verify correctly but apply to the wrong recipient. A historical status response can be authentic but outside the interval relevant to an action. A transparency receipt can verify registration of a statement while leaving the truth of the statement unresolved.

For each Audit Evidence Item used in an evaluation, the auditor distinguishes its source, where it was produced or observed, and the semantics defined by its originating specification. The Evaluation Basis identifies who controlled the relevant observation or production path where that control is material to the Audit Task. The evaluation also identifies what the item cannot establish on its own.

For example, declared model metadata does not by itself establish the model or configuration actually used. A prompt template does not by itself establish the input supplied for a particular invocation.

A recorded explanation or output labelled as reasoning does not by itself establish why an agent selected an action. Using such an artifact as evidence does not create an expectation that internal reasoning be produced or disclosed.

Authorization evidence and post-action or accountability evidence are also distinct inputs. They can arise at different Observation Boundaries and be supplied by different protocols. The presence, absence, verification result, or value of one does not by itself establish the presence, absence, or value of the other.

The auditor therefore identifies an Evaluation Basis containing the evidence, verification results, profiles, selection rules, and assumptions actually used.

The Audit Task is resolved only to the extent that this basis satisfies an applicable Evidence Requirement Set.

<a id="evidence-selection-and-conflicts"></a>

## Evidence Selection and Conflicts

The Audit Evidence Set contains what is available. The Evaluation Basis identifies what is used.

This distinction supports reproducibility, but it also creates a selection risk.

Suppose the available set contains one provider record supporting a conclusion and another applicable record contradicting it. Selecting the first item and silently excluding the second does not resolve the conflict.

The model defines no universal conflict-resolution policy. The Evaluation Basis makes the treatment of materially relevant evidence and the applicable selection rule explicit.

Evaluating one candidate basis and discovering whether another sufficient basis exists in the available evidence are separate problems. Failure of one selected Evaluation Basis, or failure to satisfy one Evidence Requirement Set, does not establish that no other sufficient basis exists in the Audit Evidence Set unless the applicable search or selection procedure justifies that conclusion.

<a id="dependency-structure"></a>

## Dependency Structure

The following figure is a dependency model, not a required processing sequence. It distinguishes specifications, deployments, or commitments that establish production expectations from carrier specifications, profiles, or mappings that interpret concrete representations for verification and applicability.

```text
 Audit Task + Audit Scope                Sources + Boundaries
            |                                    |
            v                                    v
 Evidence Requirement Set(s)               Audit Evidence Set
            |                                    |
            |                       native specs / mappings
            |                                    |
            |                       verification + applicability
            |                                    |
            |                                    v
            |                             Evaluation Basis
            |                                    |
            +------------------+-----------------+
                               |
                               v
                    Audit Task Evaluation <-------+
                               |                  |
                               v                  |
                    Audit Evaluation Result       |
                                                  |
                  Production Expectations + Coverage
                               ^
                               |
           specifications / deployments / commitments
```

The Evaluation Basis also identifies applicable mapping versions, assumptions, and evidence-selection rules. The arrows describe inputs to evaluation, not a required execution order.

<a id="representative-examples"></a>

# Representative Examples

<a id="authorized-invoked-or-effected"></a>

## Authorization, Invocation, and Effect

A user asks an agent to refund USD 100.

The available evidence can include a user approval, an authorization or delegation record, an agent-side tool invocation, a gateway dispatch record, and a provider-side effect record.

Consider three Audit Tasks.

**Was the refund authorized?** One Evidence Requirement Set can require applicable user approval and authorization evidence.

**Was the refund invoked?** Authorization evidence is insufficient. Applicable evidence from a boundary capable of observing the invocation is required by that Audit Task.

**Did the refund take effect?** Invocation evidence is insufficient. One Evidence Requirement Set can require a provider-side outcome whose originating specification establishes the relevant effect semantics, together with evidence binding that outcome to the audited refund. Another can use independently obtained provider state that establishes the refund effect, together with Evidence Relations and stated assumptions sufficient to attribute that effect to the audited refund at the relevant time.

The same Audit Evidence Set can therefore be sufficient for one task and insufficient for another.

A successful signature or chain verification of the invocation record does not change which question that record can answer.

<a id="expected-evidence-across-administrative-domains"></a>

## Expected Evidence Across Administrative Domains

Consider:

```text
User -> Agent -> Gateway -> External Service
```

The Audit Task is:

> Can the auditor reconstruct whether request R was admitted by the Gateway and then observed by the External Service?

One Evidence Requirement Set calls for:

- an Agent-side invocation record;
- a Gateway-side admission or decision record;
- a Service-side observation;
- and relations sufficient to bind the records to R, distinguish attempts where material, and establish the ordering required by the Audit Task.

Suppose the Agent and Service records are available but the Gateway record is not.

If the applicable deployment profile established that the Gateway produces a decision record for every qualifying request, the record is expected. If the applicable search over all declared sources for the declared query and cutoff is complete and no qualifying Gateway record was found, the state is **Expected but Not Found**. If the search is incomplete, the state is **Expected but Search Incomplete**. These are findings about the evidence set and the search. Neither establishes that no Gateway decision occurred.

If no applicable specification, profile, agreement, commitment, or policy called for a Gateway record for R, that record was **Not Expected**. Non-participation in a particular audit mechanism does not, by itself, establish that no production expectation applied. The available evidence can still be insufficient for the full Audit Task.

If the available information does not establish whether an Evidence Production Expectation applied to R, the state is **Expectation Undetermined**. Uncertainty about effective coverage does not, by itself, make a known production expectation undetermined.

A further case illustrates **Expected but Search Incomplete** under the applicable production expectation. Suppose the gateway slot is empty, one declared source has been searched completely, and another declared source is unavailable. The auditor can report that no qualifying record was found in the first source for the declared query and cutoff. The cross-source audit remains incomplete or Unresolved; it does not support a bounded-absence finding over all declared sources. A bounded-absence finding requires the applicable search to be complete over all declared sources for the declared query and cutoff. This distinction follows the proposed conformance cases in [IMAN-CASES](#IMAN-CASES).

This example shows why evidence requirements, production expectations, and coverage cannot be collapsed into one concept.

<a id="historical-authorization-state"></a>

## Historical Authorization State

A user grants Agent A authority to spend up to one thousand US dollars. Agent A delegates limited authority to Agent B. The authority is later narrowed or revoked, and Agent B performs a USD 500 action near the transition.

At audit time, the current authorization state is negative.

The Audit Task is:

> Was the action within the authority applicable when it was admitted?

An Evidence Requirement Set can require evidence of the historical authorization context, including the applicable status input, whether the status answer met the freshness conditions applicable at admission time, and the relation between that information and the admission decision. The Evaluation Basis identifies the evidence and material assumptions actually used to evaluate that requirement.

A negative state observed at audit time does not establish the historical state. Identifying a status source that was consulted does not establish that its answer met the freshness conditions applicable at admission time. Failure to obtain such an answer is not the same fact as a negative authorization result. A record of admission does not by itself establish that the authorization state used was sufficiently current at admission time.

If the applicable historical state cannot be reconstructed, the correct Audit Evaluation Result can remain **Unresolved**.

<a id="illustrative-refund-evaluation"></a>

## Illustrative Refund Evaluation

This fictional example illustrates a positive result under explicit assumptions. It is not a report of executed checks or an interoperability test. The labels P-R1, E1, E2, R, T, and t0 are local to the example, not standardized fields.

Consider the Audit Task: "Did provider P apply refund R of USD 100 to transaction T in its ledger before time t0?" The Audit Scope is that ledger operation, not downstream settlement or the user's original authorization.

For this example only, an illustrative profile P-R1 defines a provider confirmation as an assertion that the identified refund was applied to the identified transaction in the provider's ledger. The profile identifies the amount, currency, and time asserted for that operation. P-R1 is not an existing protocol specification, and its semantics are not attributed to another document.

One Evidence Requirement Set calls for a confirmation matching P, R, T, the amount and currency, together with verification of its provider origin and integrity, an applicable interpretation under P-R1, and a basis for using its asserted time. Satisfaction of this set depends on the stated assumptions about the provider's reporting and clock.

Suppose the Audit Evidence Set contains E1, a signed provider confirmation asserting that the operation was applied before t0, and E2, the applicable version of P-R1 obtained from an identified configuration source. The auditor also has the trust configuration needed to verify P's signing identity. Assume for illustration that the signature and identity checks succeed, that the material values match the Audit Task, and that the asserted time and permitted clock error place the operation before t0.

The Evaluation Basis identifies E1, E2, the trust configuration, the checks performed, and the assumptions that P reported its ledger state accurately and that the stated clock bound held. No materially contradictory applicable item is available in this example; that condition does not assert that all possible sources have been searched. No finding about an unmet production expectation is made.

Under those assumptions, the result supports the conclusion that P applied the specified refund in its ledger before t0. It does not establish independent observation of the ledger, completion of downstream settlement, or authorization of the original refund request. Each of those questions can require a different Evidence Requirement Set.

<a id="potential-uses-in-audit-work"></a>

# Potential Uses in AUDIT Work

This section describes ways in which the model can support possible future AUDIT work. It does not assume a particular charter outcome or document structure.

<a id="requirements-and-data-model-review"></a>

## Requirements and Data-Model Review

A use case can be reduced to explicit questions:

- What is the Audit Task and Audit Scope?
- Which alternative Evidence Requirement Sets are sufficient?
- Which sources are expected to produce which information?
- Which Observation Boundaries matter?
- What Evidence Coverage is represented?
- Which Evidence Relations are required?
- What does each relevant record mean, who asserts or observes it, and what does it not establish by itself?
- For each referenced verification procedure, what does a successful result establish, what assumptions does it rely on, and what remains outside its reach?
- Where control matters, who controlled the observation, production, or disclosure path?
- Which assumptions remain deployment-specific?

These questions separate semantic requirements from a candidate record format and help prevent a carrier or a successful verification result from silently acquiring stronger semantics in a particular deployment.

<a id="comparing-candidate-mechanisms-and-mappings"></a>

## Comparing Candidate Mechanisms and Mappings

Candidate mechanisms can be compared by asking which Audit Tasks they help evaluate, which Evidence Requirement Sets they can satisfy, which sources and boundaries they distinguish, which relations they represent, and which properties remain deployment assumptions.

A format-specific mapping can explain how the objects, fields, references, extensions, and verification procedures defined for that format support the semantic properties used by this model. Such mappings are outside the core terminology and can differ between carriers.

Two mechanisms can therefore support the same Audit Task through different evidence combinations. Different carriers can satisfy the same Evidence Requirement Set when their respective mappings establish the required semantic properties to the same stated extent.

<a id="collection-and-query-interfaces"></a>

## Collection and Query Interfaces

The model can provide requirements input to future collection or Audit Store interfaces.

An auditor can require evidence from identified sources, for a specified interval and event class, with specified relations and, where necessary, identified record or profile forms.

This document does not define how such a request is encoded or transmitted.

<a id="interoperability-and-conformance-reports"></a>

## Interoperability and Conformance Reports

The model can help bound claims made from implementation and interoperability results.

An interoperability report can identify:

- the Audit Task or property being tested;
- the evidence and vectors used;
- the applicable carrier mapping or profile version, where one is involved;
- verification procedures and specification versions;
- the semantic property established by those procedures;
- assumptions and untested stages;
- and the resulting conclusion and its limitations.

Successful parsing, schema validation, or verification of the same carrier is not sufficient evidence of semantic interoperability if implementations disagree about the Evidence Source, Observation Boundary, Evidence Relation, Evidence Applicability, or property established by verification.

The following is illustrative report wording, not a result of testing performed for this document:

> For the identified test records and profile version, both implementations verified the signatures and matched the records to the same request. Attribution of a provider-side effect to that request was not tested.

Such a report limits its claim to the identified checks rather than asserting whole-system conformance.

<a id="privacy-and-data-minimization"></a>

## Privacy and Data Minimization

Where several Evidence Requirement Sets can satisfy the same Audit Task, a deployment can prefer a set requiring less disclosure.

Task-relative requirements can therefore support minimization without requiring one universal selective-disclosure mechanism.

<a id="relationship-to-other-work"></a>

# Relationship to Other Work

<a id="audit-architecture"></a>

## AUDIT Architecture

The architecture described in [AUDIT-ARCH](#AUDIT-ARCH) identifies roles, audit record classes, audit context propagation, and supporting services. The model in this document can support the Auditor's evaluation by making the auditing question, evidence requirements, production expectations, and Evaluation Basis explicit. It does not introduce an additional architectural role or replace the architecture's record classes. References to an evaluator describe the evaluation function, not an additional role.

Interaction, Action, Delegation, and Authorization Transition Records can be considered as Audit Evidence Items, together with receipts, Attestation Results, disclosed portions of records, and other relevant observations. The required combination depends on the Audit Task; this model does not require every record class for every task.

Audit context can provide identifiers and references used when evaluating Evidence Relations. Audit Scope identifies what is being evaluated. A common identifier does not by itself establish derivation, causation, semantic consistency, or sufficient evidence for the Audit Task. The semantics of each record and reference remain those defined by the applicable specification or profile.

<a id="rats"></a>

## RATS

The RATS architecture defines roles and terminology for generating and appraising attestation Evidence and Attestation Results [RFC9334](#RFC9334).

A RATS Evidence artifact or Attestation Result can be an Audit Evidence Item in this document. This document does not redefine RATS Evidence or appraisal semantics.

A successful attestation appraisal does not, by itself, extend the Observation Boundary to an application-level event that the supporting evidence neither observed nor bound.

<a id="scitt"></a>

## SCITT

The Supply Chain Integrity, Transparency, and Trust (SCITT) architecture describes registration of Signed Statements with Transparency Services and the use of Receipts [RFC9943](#RFC9943).

A SCITT Receipt can contribute evidence about registration and transparency-related properties. Registration does not by itself establish the truth of the registered statement or completeness of all statements relevant to an Audit Task, and it does not substitute for independent observation or an independently constrained production path where those properties matter to the Audit Task.

<a id="effect-boundary-processing"></a>

## Effect-Boundary Processing

The Action Evidence Boundary (AEB) defines an executor-side processing model for consequential effects, including native artifact verification, exact-action binding, authorization, provider entry, outcome handling, and reconciliation [AEB](#AEB).

This document does not redefine AEB decisions, lifecycle states, provider-entry semantics, reconciliation rules, or deployment claims. When an AEB result or record is used as an Audit Evidence Item, AEB remains authoritative for what that native result establishes and does not establish. This document describes only how that bounded native result participates in a cross-domain Audit Task.

An AEB evidence requirement used for admission is therefore distinct from an Evidence Requirement Set used here to evaluate an Audit Task.

Other native boundary records can participate in the same way without this document redefining their native semantics.

<a id="decision-time-evidence-composition"></a>

## Decision-Time Evidence Composition

Authorization Evidence Chains (EP-AEC) defines a relying-party-controlled evidence requirement for a material action and records the basis of its evaluation [EP-AEC](#EP-AEC).

That decision-time contract is distinct from the auditor-side Evidence Requirement Set in this document. An Audit Task can consider records and results from multiple participants after the fact. This document does not redefine EP-AEC verification, acceptance, material-action matching, requirement satisfaction, or replay semantics, and it defines no replacement composition object.

<a id="execution-evidence-appraisal"></a>

## Execution-Evidence Appraisal

`draft-sergeev-claim-boundaries-02` describes analytic limits on what execution-related evidence can establish [CBEE](#CBEE). `draft-sergeev-wexp-core-01` defines carrier-neutral per-action appraisal semantics for execution evidence [WEXP](#WEXP).

This document addresses a different layer: which evidence combinations are needed or available for a particular Audit Task, what sources were expected to produce them, and what Evaluation Basis was used. It does not define execution claim levels, appraisal verdicts, or evidence-strength rankings.

<a id="expected-record-declarations"></a>

## Expected-Record Declarations

Expected-record declarations can state which participants are expected to produce or make available particular records. An applicable declaration can provide a basis for an Evidence Production Expectation. The availability cases discussed in [IMAN-CASES](#IMAN-CASES) and the recipient-or-holder and refusal cases in [a-7-produced-record-required-recipient-or-holder](#a-7-produced-record-required-recipient-or-holder) and [a-8-declined-action-and-conditional-effect-evidence](#a-8-declined-action-and-conditional-effect-evidence) illustrate questions that such declarations can address.

Whether the available records are sufficient for an Audit Task is a separate question governed by its Evidence Requirement Sets and Evaluation Basis. This document does not define a declaration mechanism or prescribe the contents of a separate expected-record specification.

<a id="opentelemetry-genai"></a>

## OpenTelemetry GenAI Semantic Conventions

OpenTelemetry GenAI semantic conventions describe spans, events, and metrics for model, agent, and tool operations [OTEL-GENAI](#OTEL-GENAI). Such telemetry can be considered as Audit Evidence Items under the applicable instrumentation and deployment assumptions. It can be sufficient for some Audit Tasks; this model neither requires nor excludes a particular telemetry format.

A mapping identifies the conventions and instrumentation versions, observation points, and collection settings relevant to the Audit Task. The Evaluation Basis identifies the mapping used. Span relationships and operation results retain their originating semantics. A logical-operation span can include retries and is not necessarily evidence of one attempt. Its presence or successful status does not, by itself, establish authorization, a provider-side effect, or collection completeness.

The "`gen_ai.evaluation.result`" event describes an evaluation of GenAI output characteristics. It is not automatically an Audit Evaluation Result as defined here. Its use depends on the question being evaluated, the evaluation method, and the evidence requirements that apply. Content-capture and external-storage settings also affect which items are available; absence of a span does not establish absence of separately stored content.

<a id="security-considerations"></a>

# Security Considerations

This document defines no wire protocol, but an evaluator or producer can manipulate how the model is applied.

The threats considered here include false assertions by an Evidence Source, selective withholding by a holder, and misrepresentation of checks, searches, or conclusions by an auditor. These parties can be under common control or act in collusion. The model makes the basis of a result explicit; it does not establish that a reported procedure was performed correctly. Where a conclusion depends on a party's correct behavior, the Evaluation Basis identifies the supporting evidence or material assumption. The SCITT threat model also considers malicious or compromised issuers, services, and auditors (see Section 9.7 of [RFC9943](#RFC9943)).

<a id="post-hoc-task-or-expectation-manipulation"></a>

## Post-Hoc Task or Expectation Manipulation

Changing the Audit Scope after examining the available evidence can create a misleading appearance of sufficiency.

Likewise, an evaluator can make a missing record appear significant by declaring a production expectation only after discovering that the record is absent.

An Audit Task can legitimately be defined after the audited events. Where timing is material, the Evaluation Basis distinguishes the time the task and scope were selected from the interval in which a production expectation applied. A later analytical requirement does not retrospectively create a participant obligation to have produced evidence.

Changes to an Evidence Requirement Set, its applicability conditions, or material assumptions can also change the result. A later evaluation identifies those changes and preserves the basis of the earlier result rather than silently applying the revised conditions to it.

<a id="evidence-selection"></a>

## Evidence Selection

An evaluator can select only evidence supporting a preferred conclusion while ignoring applicable contradictory evidence.

Material applicable evidence should not be silently excluded. Where an exclusion can materially affect the result, the Evaluation Basis preserves the selection or exclusion rule.

<a id="coverage-and-binding-errors"></a>

## Coverage and Binding Errors

A source can claim coverage that was not effective because of outages, bypass paths, partial deployment, configuration changes, or adversarial control.

An authentic artifact can also be presented for the wrong transaction, destination, resource, actor, or delegation context.

Neither declared coverage nor successful artifact verification resolves these problems by itself.

<a id="version-and-semantic-substitution"></a>

## Version and Semantic Substitution

Evidence can be interpreted differently under different versions of schemas, profiles, policies, or verification procedures.

The Evaluation Basis identifies the versions material to the result. A current profile should not silently replace the semantics applicable to historical evidence.

Where an Evaluation Basis is referenced, the reference and associated metadata identify the version used. A stable locator alone does not protect that version or the result against substitution. When results or their bases are stored or conveyed, their integrity and binding to the Audit Task, Audit Scope, and evaluation time depend on the applicable mechanism. Use of a result in a different context calls for a separate assessment of its applicability. This document specifies no result-protection format. Related protection concerns for RATS conceptual messages are discussed in Section 12.2 of [RFC9334](#RFC9334); the model here does not define such a message.

<a id="adversarial-evidence-content"></a>

## Adversarial Evidence Content

Audit Evidence Items can contain instructions, active content, or attacker-controlled references. Successful verification does not, by itself, authorize execution of that content or make it an instruction to the auditor. Automated evaluation can be subverted if evidence content is allowed to change the instructions, requirements, or policies controlling the evaluation. Safe parsing, rendering, and retrieval are responsibilities of the applicable implementation; this model defines no mechanism for isolating untrusted content. Related concerns for agent conversation records are discussed in Section 6.4 of [VACR](#VACR).

<a id="authentic-but-untruthful-evidence"></a>

## Authentic but Untruthful Evidence

A valid signature establishes properties of the signed artifact and signer relationship. It does not establish that the signed factual assertion is true.

Similarly, the ability of an independent party to verify an artifact does not establish that its production or observation was independent of the audited subject.

Independence from later cooperation is also distinct from independence of evidence production. A record created by the acting party and left in place can be evaluable later without that party's cooperation while still remaining only that party's account of itself. Conversely, evidence produced at the acting boundary can have a different control property when an external constraint, anchor, or witness prevents unilateral substitution or suppression.

<a id="privacy-considerations"></a>

# Privacy Considerations

Audit information can contain user content, identifiers, authorization state, workflow structure, business-sensitive information, and cross-domain correlation data.

Task-relative requirements can support minimization by making explicit what evidence is needed for a specific Audit Task. Where multiple Evidence Requirement Sets can satisfy the task, a deployment can prefer one that reveals less information.

Selective disclosure can cause different auditors to possess different Audit Evidence Sets. Different bounded results are not necessarily inconsistent when their Evaluation Bases differ.

Whether information was communicated to interaction participants is distinct from whether an Evidence Source observed it, whether it was recorded, and whether it is available to an auditor. Information not communicated to participants can still be available as audit evidence, and information communicated to them can be absent from an auditor's Audit Evidence Set. Neither participant visibility nor auditor availability establishes collection completeness.

An Audit Task description can itself reveal sensitive metadata, including which participants are expected in a workflow, which events are considered consequential, which observation points exist, and which relationships an auditor is attempting to reconstruct.

Confidentiality and disclosure controls can therefore apply not only to Audit Evidence Items but also to task descriptions and production expectations.

An Audit Task or Evidence Requirement Set does not grant authority to collect, retain, or disclose information. Applicable access and disclosure controls remain separate. Records, identifiers, and results that are limited for one task can enable broader correlation when combined across tasks or auditors. Hash-based references do not by themselves provide confidentiality (see Section 10 of [RFC6920](#RFC6920)). A deployment's privacy analysis therefore considers the audience, retention period, and cross-task linkability of task metadata and evidence, as well as the amount disclosed for one task. The risk that monitoring itself can be misused is discussed in [RFC7258](#RFC7258).

This document defines no privacy-preserving encoding.

<a id="open-questions"></a>

# Open Questions

The following questions are intentionally left open:

1. Which task and production-expectation information belongs in architecture, data-model profiles, operational profiles, or deployments?
2. Should any part of an Audit Task or Evidence Production Expectation be machine-readable?
3. Which Evidence Relation and Evidence Coverage semantics require interoperable representation, and which concrete encodings belong in carrier-specific profiles or mappings?
4. How should auditors request or discover evidence needed for an Audit Task?
5. How should verification procedures report the exact properties they established?
6. What information is necessary to make an Audit Evaluation Result reproducible while minimizing disclosure?
7. What mapping information needs to be preserved in the Evaluation Basis so that carrier-specific evidence can be interpreted and independently reproduced by another implementation?

<a id="iana-considerations"></a>

# IANA Considerations

This document has no IANA actions.

# Informative References

<a id="AHUJA-CROSSING"></a>

**[AHUJA-CROSSING]** Sumit P. Ahuja. [[agent2agent] Re: New I-D : A Dimensional Model for Characterizing AI Agent Protocol Proposals and Their Substrates](https://mailarchive.ietf.org/arch/msg/agent2agent/vA0cS6dOTEMSFL7Qo0ZXWTczRpU/). . 1 October 2026. 

<a id="AUDIT-ARCH"></a>

**[AUDIT-ARCH]** Mirja Kühlewind, Henk Birkholz. [An Architecture for Auditing Agent Delegation and Interactions](https://datatracker.ietf.org/doc/draft-kuehlewind-audit-architecture/01/). Internet-Draft draft-kuehlewind-audit-architecture-01. 7 September 2026. 

<a id="AEB"></a>

**[AEB]** Iman Schrock. [The Action Evidence Boundary for Consequential Agent Effects](https://datatracker.ietf.org/doc/draft-schrock-action-evidence-boundary/07/). Internet-Draft draft-schrock-action-evidence-boundary-07. 25 September 2026. 

<a id="CBEE"></a>

**[CBEE]** Mikhail Sergeev. [Claim Boundaries for Execution Evidence](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/02/). Internet-Draft draft-sergeev-claim-boundaries-02. 15 October 2026. 

<a id="WEXP"></a>

**[WEXP]** Mikhail Sergeev, Vladimir Ikher. [The Witnessed Execution Protocol (WEXP): Core Specification](https://datatracker.ietf.org/doc/draft-sergeev-wexp-core/01/). Internet-Draft draft-sergeev-wexp-core-01. 14 August 2026. 

<a id="RFC9334"></a>

**[RFC9334]** Henk Birkholz, Dave Thaler, Michael Richardson, Ned Smith, Wei Pan. [Remote ATtestation procedureS (RATS) Architecture](https://www.rfc-editor.org/info/rfc9334). RFC 9334; DOI 10.17487/RFC9334. January 2023. 

<a id="RFC9943"></a>

**[RFC9943]** Henk Birkholz, Antoine Delignat-Lavaud, Cédric Fournet, Yogesh Deshpande, Steve Lasker. [An Architecture for Trustworthy and Transparent Digital Supply Chains](https://www.rfc-editor.org/info/rfc9943). RFC 9943; DOI 10.17487/RFC9943. June 2026. 

<a id="EP-AEC"></a>

**[EP-AEC]** Iman Schrock. [Authorization Evidence Chains: Composing Heterogeneous Agent-Action Evidence (EP-AEC)](https://datatracker.ietf.org/doc/html/draft-schrock-ep-authorization-evidence-chain-08). Internet-Draft draft-schrock-ep-authorization-evidence-chain-08. 4 October 2026. 

<a id="IMAN-CASES"></a>

**[IMAN-CASES]** Iman Schrock. [Re: Charter Comments -- more specific on the scope?](https://mailarchive.ietf.org/arch/msg/audit/u04Utry2tPGRqJ_f-SmRk_EMW88). . 6 October 2026. AUDIT mailing list, proposed conformance cases

<a id="WADKINS"></a>

**[WADKINS]** Douglas Wadkins. [Independent Determinability of Agent Actions](https://datatracker.ietf.org/doc/draft-wadkins-agentproto-action-determinability/). Internet-Draft draft-wadkins-agentproto-action-determinability-00. 10 September 2026. 

<a id="MORETTO-RECIPIENT"></a>

**[MORETTO-RECIPIENT]** Francesco Marinoni Moretto. [[Audit] Re: Charter Comments -- more specific on the scope?](https://mailarchive.ietf.org/arch/msg/audit/XVTaQ0mqjOt4YHjGjpJPUye3vCY). . 7 October 2026. AUDIT mailing list, wrong-recipient-or-holder case

<a id="SIRKKAVAARA-REFUSAL"></a>

**[SIRKKAVAARA-REFUSAL]** Henri Sirkkavaara. [[Audit] Re: Charter Comments -- more specific on the scope?](https://mailarchive.ietf.org/arch/msg/audit/xCNd0SiPlas7ROG5mNLCpYveP8U). . 7 October 2026. AUDIT mailing list, declined-action case

<a id="SCHROCK-REFUSAL"></a>

**[SCHROCK-REFUSAL]** Iman Schrock. [[Audit] Re: Charter Comments -- more specific on the scope?](https://mailarchive.ietf.org/arch/msg/audit/p_gA6xAzlBBK3DIMl0SFszYUnmE). . 8 October 2026. AUDIT mailing list, decision and conditional effect evidence

<a id="VACR"></a>

**[VACR]** Henk Birkholz, Tobias Heldt, Orie Steele. [Verifiable Agent Conversation Records](https://datatracker.ietf.org/doc/html/draft-birkholz-verifiable-agent-conversations-01). Internet-Draft draft-birkholz-verifiable-agent-conversations-01. 31 August 2026. 

<a id="RFC6920"></a>

**[RFC6920]** Stephen Farrell, Dirk Kutscher, Christian Dannewitz, Borje Ohlman, Ari Keranen, Phillip Hallam-Baker. [Naming Things with Hashes](https://www.rfc-editor.org/info/rfc6920). RFC 6920; DOI 10.17487/RFC6920. April 2013. 

<a id="RFC7258"></a>

**[RFC7258]** Stephen Farrell, Hannes Tschofenig. [Pervasive Monitoring Is an Attack](https://www.rfc-editor.org/info/rfc7258). BCP 188; RFC 7258; DOI 10.17487/RFC7258. May 2014. 

<a id="OTEL-GENAI"></a>

**[OTEL-GENAI]** OpenTelemetry. [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai/tree/f3c6d0c9bb66ebd474668a3a0be25c61226f02c2). . 14 October 2026. Development snapshot, commit f3c6d0c9bb66ebd474668a3a0be25c61226f02c2

<a id="additional-cases"></a>

# Additional Cases

<a id="a-1-missing-record-or-negative-event"></a>

## Missing Record or Negative Event?

An observation mechanism is represented as recording every qualifying call. The auditor receives records `101, 102, 104, 105`.

Record `103` is absent.

The absence can reflect loss, nondisclosure, record-production failure, an uncovered path, non-participation, or no underlying event.

The interpretation depends on the production expectation, Evidence Coverage, Audit Scope, and assumptions about gap detection and bypassability.

`Record not found` is not equivalent to `event did not occur`.

<a id="a-2-locally-valid-records-globally-inconsistent-wo"></a>

## Locally Valid Records, Globally Inconsistent Workflow

An Inventory service records reservation of item A. A Payment service records a charge for item B.

Both records are authentic and carry the same high-level workflow identifier.

The Audit Task:

> Did the distributed workflow execute the intended purchase consistently?

requires a relation sufficient to compare the material semantic values across the two records.

A shared identifier establishes correlation, not semantic consistency.

<a id="a-3-recovered-task-unresolved-external-effect"></a>

## Recovered Task, Unresolved External Effect

A dialog and outstanding task are restored after a failure. A downstream operation had been invoked before the failure, but its response was lost.

The recovered task state can be sufficient for continuity while the provider-side effect remains unresolved.

Retry policy and provider semantics are outside this document.

<a id="a-4-correlation-does-not-establish-derivation"></a>

## Correlation Does Not Establish Derivation

An Action Record contains a valid parent reference to an Interaction Record.

The reference can establish correlation or predecessor identity. It does not by itself establish that the interaction content produced, transformed, selected, or caused the action.

A stronger derivation or causation conclusion requires additional Evidence Relations.

<a id="a-5-conflicting-evidence"></a>

## Conflicting Evidence

Two applicable, authentic records make incompatible assertions about the same provider operation at the same as-of time: one states that its effect was committed before that time, while the other states that its effect had never been committed by that time. Both use the same operation identity and native effect semantics.

This is conflicting evidence about one proposition. In contrast, an agent-side timeout and a provider-side committed effect can both be accurate observations at different boundaries; different result strings alone do not establish a conflict.

This document defines no universal rule selecting one source as authoritative.

<a id="a-6-valid-evidence-bound-to-the-wrong-context"></a>

## Valid Evidence Bound to the Wrong Context

A signed authorization verdict verifies correctly. It was issued for destination A but is presented as evidence for destination B.

The Evidence Verification Result can be successful while Evidence Applicability fails.

If the format carries no destination binding, the association can remain unsupported rather than contradicted. A positively identified mismatch, absence of the required binding, and inability to perform the binding check are separate findings.

<a id="a-7-produced-record-required-recipient-or-holder"></a>

## Produced Record, Required Recipient or Holder

A service P produces confirmation C. The Audit Task asks whether C was delivered to recipient R by a stated deadline and retained by holder H for a stated interval. The Evidence Requirement Set identifies R and H and the evidence that qualifies for each property.

The auditor obtains C from intermediary M. Even if C's producer and relation to the audited transaction are verified, its presence at M does not establish delivery to R or retention by H. Evidence of delivery to M does not, by itself, satisfy a requirement for delivery to R and does not, by itself, establish that no delivery to R occurred.

If a source necessary to establish delivery to R or retention by H cannot be checked, and no alternative sufficient Evaluation Basis is available, that part of the audit remains incomplete or Unresolved. The result reports C as available and the delivery or retention requirement as unresolved, rather than reporting C as absent or delivery as failed.

Evidence of receipt at one time does not by itself establish retention for a later interval.

This example applies the producer and required-recipient-or-holder distinction proposed by Francesco Marinoni Moretto and refined with Iman Schrock [MORETTO-RECIPIENT](#MORETTO-RECIPIENT). It expresses auditing questions and evidence conditions without prescribing an expected-record declaration mechanism.

<a id="a-8-declined-action-and-conditional-effect-evidence"></a>

## Declined Action and Conditional Effect Evidence

The Audit Task asks whether request R reached a terminal outcome under an identified workflow policy. Its Evidence Requirement Set requires evidence of the decision and makes evidence of a downstream effect conditional on the applicable workflow branch.

Suppose the Evaluation Basis establishes, under the applicable native semantics, a verified refusal by a party authorized to decide R, bound to the exact requested action. This can satisfy the decision-evidence requirement; signature validity or the label `denied` alone does not establish those conditions.

The effect-evidence requirement is inapplicable only if the Evidence Requirement Set or referenced profile explicitly defines this refusal as a terminal condition for this Audit Task, and the Evaluation Basis establishes that the condition applies. The result preserves the refusal, the applicable condition, and the reason no effect evidence is required for that branch.

Without that explicit rule, or when the refusal, authority, or exact-action binding cannot be established, the refusal does not remove the effect-evidence requirement. A refusal for a different action cannot satisfy the decision requirement for R.

Even with a terminal-refusal rule, the separate Audit Task "Did R produce effect E?" is not answered by the refusal alone. The refusal does not establish execution, an external effect, or their non-occurrence. Material evidence of an effect cannot be discarded solely because the policy names refusal as terminal.

The declined-action case was proposed by Henri Sirkkavaara [SIRKKAVAARA-REFUSAL](#SIRKKAVAARA-REFUSAL). Iman Schrock clarified the distinction between satisfying a decision requirement and conditionally removing an effect requirement [SCHROCK-REFUSAL](#SCHROCK-REFUSAL). The task-relative formulation here does not define their proposed declaration mechanism.

<a id="audit-task-card"></a>

# Audit Task Card

The following non-normative template can be used in requirements, implementation, or interoperability discussions.

| Field | Question |
| --- | --- |
| Audit Task | What question is being evaluated? |
| Audit Scope | Which actors, events, states, resources, relationships, and time are in scope? |
| Audit Evidence Set | Which Audit Evidence Items are available to this auditor? |
| Evidence Requirement Set(s) | Which sets and versions apply, which alternative evidence combinations are sufficient, and which explicit conditions make individual requirements apply? |
| Evidence Production Expectation | Who is expected to produce, deliver, receive, or retain the evidence, on what basis and by what deadline or for what interval? |
| Evidence Source | Who is responsible for the asserted or observed information? |
| Control over evidence | Who controlled the relevant observation, production, or disclosure path? |
| Observation Boundary | Where can the relevant fact be observed? |
| Evidence Coverage | Which event classes, paths, resources, and intervals are represented as covered, and what supports that coverage for the audited interval? |
| Evidence Relation | Which bindings or relationships must be established? |
| Carrier Mapping / Profile | If a concrete carrier is used, which mapping or profile version gives its fields, references, and checks their task-relevant semantics? |
| Evidence Verification Result | Which checks were performed, and what did they establish under which assumptions and limits? If omission is claimed detectable, by whom or what mechanism? |
| Evidence Applicability | Does each item apply to the audited subject, role, destination, time, and context, including any required recipient or holder? |
| Search Basis / Completion | When absence matters, which sources, query, cutoff, and as-of meaning apply? Was the search complete for each source, and what limits remain? |
| Evaluation Basis | Which evidence, verification results, procedures, profiles, selection rules, and assumptions were actually used? |
| Audit Evaluation Result | Who produced the result, what conclusion follows, at what time, and with what limitations or grounds for conditional non-applicability? |

<a id="non-inference-checklist"></a>

# Non-Inference Checklist

This compact checklist groups the distinctions developed above; it defines no additional requirements.

1. A valid signature or authentic record does not establish the truth of every assertion or its applicability to the audited subject, time, or event.
2. Authorization, policy decision, invocation, execution, and external effect are different facts. Evidence of one does not by itself establish the others.
3. Correlation, ordering, a parent reference, or one local delegation relation does not establish derivation, causation, semantic consistency, or uninterrupted end-to-end authority.
4. Verifying all available items does not establish collection completeness. Declared coverage, a post-hoc expectation, or an incomplete search does not justify non-occurrence or cross-source absence.
5. Independent verification and independence from later cooperation do not establish independent observation or evidence production.
6. A negative check, an unevaluated check, and an Unresolved Audit Task differ. Failure of one candidate basis does not exclude all other sufficient bases.
7. Current state does not establish historical state. Propagating or aggregating a result does not remove the need to preserve its source, task, scope, time, basis, and limitations.
8. A carrier, wrapper, common identifier, or successful parsing result does not strengthen an Observation Boundary or Evidence Relation, or establish semantic interoperability.

<a id="acknowledgments"></a>

# Acknowledgments

Discussions in the AUDIT and agent2agent communities helped shape this document. The author thanks Mirja Kuehlewind and Henk Birkholz for discussion of the problem space and verification boundaries; Francesco Marinoni Moretto and Sumit Ahuja for expected-record and cross-domain auditing discussions; and Henri Sirkkavaara, Nancy Sahu, and Gareth Wong for discussions of coverage and the meaning and limits of verification.

Iman Schrock clarified bounded absence versus incomplete observation and proposed related conformance cases. The unavailable-source example reflects that contribution. Sumit Ahuja highlighted why a relation presented at one crossing does not by itself establish an uninterrupted relation across earlier crossings. Parisa Foroughi clarified the separation of authorization evidence from post-action and accountability evidence.

Francesco Marinoni Moretto contributed the required-recipient-or-holder case, and Henri Sirkkavaara contributed the declined-action case. Iman Schrock refined the producer, holder, and searched-source distinction and the conditions under which refusal satisfies a decision requirement while a downstream effect requirement is inapplicable. The additional examples reflect these contributions to the discussion developed with Sumit Ahuja.

The distinction between independence from later cooperation and independence of evidence production was clarified through an exchange with Douglas Wadkins in connection with his action-determinability work [WADKINS](#WADKINS). These acknowledgments identify contributions and do not imply endorsement of this revision, authorship of other material, or agreement by a working group.
