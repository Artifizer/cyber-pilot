---
cypilot: true
type: requirement
name: Bug-Finding Methodology
version: 1.0
purpose: Compact language-agnostic methodology for high-recall bug discovery in source code
---

# Bug-Finding Methodology

**Scope**: Source-code analysis for correctness, logic, reliability, security, concurrency, performance, and integration defects across programming languages.

**Non-goal**: guarantee `100%` bug detection. That is not achievable in the general case because programs depend on incomplete specifications, runtime environment, dynamic inputs, external systems, and nondeterministic behavior. The practical target is **maximum recall with explicit uncertainty, evidence, and escalation paths**.

## Core Principles

- Combine complementary signals. Pattern rules, semantic reasoning, data-flow review, dynamic checks, and historical evidence catch different bug classes.
- Optimize for recall first, then calibrate precision with evidence. Missing a bug is usually worse than investigating one plausible candidate.
- Work from **invariants and failure modes**, not from language syntax alone. This keeps the method portable across languages.
- Never claim `all bugs found`. Report confidence and residual uncertainty explicitly.
- Load only the code needed for the current reasoning slice. Expand context only when call graph, state flow, or boundary contracts require it.
- A single LLM pass is insufficient. CodeRabbit-like quality requires a **layered review stack**, not just a better prompt.

## Layer Map

| Layer | Question |
|---|---|
| L1 | Where are the real risk hotspots? |
| L2 | What contracts and invariants must always hold? |
| L3 | Which paths, states, and interleavings can violate them? |
| L4 | Which universal bug classes apply here? |
| L5 | Can a concrete counterexample be constructed? |
| L6 | What dynamic check would confirm or refute the finding? |
| L7 | What is the confidence, impact, and next action? |

## L1: Risk Hotspot Mapping

Focus first on code that is most likely to contain high-impact defects.

- Start from changed code, entry points, trust boundaries, persistence boundaries, async boundaries, and externally visible behavior.
- Prioritize authentication, authorization, money movement, state transitions, retries, parsing, serialization, migrations, caching, and cleanup logic.
- Expand to callers, callees, shared utilities, and configuration only when they influence the active path.
- Use repository signals when available: churn, incident history, bug-fix patterns, flaky tests, complex functions, and modules with many dependencies.

## L2: Contract & Invariant Extraction

Extract what must be true before, during, and after execution.

- Preconditions: input shape, nullability, permissions, ordering, initialization, feature flags, units, and schema assumptions.
- Postconditions: returned value, persisted state, emitted events, side effects, idempotency, and cleanup guarantees.
- Cross-step invariants: uniqueness, monotonicity, ownership, transactional boundaries, retry safety, and consistency between cache, database, and outbound messages.
- If the contract is not explicit, infer it from tests, names, types, assertions, error messages, docs, and call sites, but mark it as inferred rather than proven.

## L3: Path, State, and Interleaving Exploration

Trace how bugs emerge when the happy path breaks.

- Check the main path, unhappy path, edge values, repeated invocation, partial failure, timeout, retry, stale state, invalid config, startup, shutdown, and rollback behavior.
- For stateful logic, trace creation, mutation, persistence, invalidation, and cleanup.
- For async or concurrent logic, examine races, double delivery, out-of-order completion, missing awaits, lock ordering, cancellation, and duplicate side effects.
- For distributed flows, examine retries, deduplication, eventual consistency gaps, and split-brain assumptions between services.

## L4: Universal Bug-Class Sweep

Apply the same defect lenses regardless of language.

| Class | Typical failures |
|---|---|
| Correctness & logic | Wrong branch, inverted condition, off-by-one, missing case, unreachable branch, bad default |
| Input & boundary | Missing validation, parse mismatch, encoding mismatch, unit mismatch, schema drift |
| Error handling & resilience | Swallowed error, wrong fallback, retry storm, partial commit, misleading success |
| State & lifecycle | Wrong initialization order, stale cache, missing cleanup, duplicate apply, broken rollback |
| Security & trust boundary | Authz gap, injection path, traversal, unsafe deserialization, secret or PII leak |
| Concurrency & async | Race, deadlock, lost update, double execution, missing await, cancellation bug |
| Performance & resources | N+1, unbounded loop, leak, blocking hot path, missing backpressure |
| Integration & config | Version drift, env mismatch, clock/timezone bug, feature-flag inversion, protocol mismatch |
| Testing gaps | Missing regression coverage for critical or failure paths |

## L5: Counterexample Construction

A suspected bug becomes stronger when you can describe exactly how it fails.

- Build the smallest trigger: input, prior state, ordering, timing, or configuration needed to break the invariant.
- Express the failure as `condition -> execution path -> bad outcome`.
- Search for contradictory code, assertions, tests, or guards that disprove the hypothesis.
- If no plausible trigger can be constructed, lower confidence or discard the finding.

## L6: Dynamic Escalation Strategy

When static reasoning is insufficient, specify the cheapest next proof.

- Use targeted unit tests for local logic and boundary conditions.
- Use integration tests for persistence, network, serialization, configuration, and cross-service behavior.
- Use property-based tests or fuzzing for parsers, protocol handlers, validators, and state machines.
- Use semantic static analysis or data-flow engines for taint, authorization, and multi-hop flow issues.
- Use runtime traces, logs, metrics, and production incidents for nondeterministic or environment-sensitive failures.

**Strong practical stack**:

- Fast rule-based scan on every change
- Semantic or data-flow scan for critical paths and primary languages
- Diff-aware LLM review with codebase context
- Targeted dynamic checks for high-risk hypotheses
- Feedback loop from human review, incidents, and escaped defects

This layered stack is the realistic path toward CodeRabbit-level or better results. No single model, prompt, or static analyzer is sufficient.

## L7: Reporting, Confidence, and Residual Risk

Report each finding with:

- Bug class
- Severity
- Confidence: `CONFIRMED`, `HIGH`, `MEDIUM`, or `LOW`
- Location
- Violated invariant or contract
- Minimal trigger or counterexample
- Impact
- Evidence
- Proposed fix
- Best validation step

Residual uncertainty is mandatory:

- List unproven high-risk areas.
- List required dynamic checks not yet run.
- State which bug classes were checked and which were only partially checked.
- Never collapse uncertainty into a blanket `PASS`.

## Execution Protocol

Use this sequence for each hotspot:

1. Map the boundary and impacted path.
2. Extract explicit and inferred invariants.
3. Walk the happy path and the most dangerous unhappy paths.
4. Sweep all universal bug classes.
5. Build or refute a concrete counterexample.
6. Propose the cheapest confirming dynamic check.
7. Report confidence and residual risk.

Efficiency rules:

- Prefer narrow slices over whole-repo loading.
- Expand to adjacent files only when a path, state transition, or dependency requires it.
- Summarize and drop already-processed context.
- For multi-language systems, inspect cross-language boundaries first because contract drift often hides there.

## Integration with Cypilot

- Use this methodology when the user asks to find bugs, logic errors, edge cases, regressions, hidden failure modes, or "all problems" in code.
- Use `reverse-engineering.md` to build the structural model of the system.
- Use `code-checklist.md` as the acceptance and reporting checklist.
- Use this methodology as the **search procedure** that drives what code paths and failure modes to inspect first.

## Validation

Review is complete when:

- [ ] Risk hotspots were identified and prioritized
- [ ] Explicit and inferred invariants were extracted
- [ ] Happy path and failure paths were both examined
- [ ] All universal bug classes were swept for the target scope
- [ ] Each reported issue includes a plausible trigger or counterexample
- [ ] Missing proof was converted into a concrete dynamic follow-up
- [ ] Confidence and residual uncertainty were reported explicitly
- [ ] No claim of `100%` detection or blanket coverage was made
