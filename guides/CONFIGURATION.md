# Configuring Cypilot

How to customize Cypilot behavior using **prompts** (in your AI agent chat) and **terminal commands**.

> **Convention**: 💬 = paste into AI agent chat. 🖥️ = run in terminal.

---

## Table of Contents

- [1. Initial Setup](#1-initial-setup)
- [2. Agent Behavior — Navigation, Skills, Rules](#2-agent-behavior--navigation-skills-rules)
- [3. Identifiers & Traceability](#3-identifiers--traceability)
- [4. Artifact Templates, Rules, Checklists, Constraints](#4-artifact-templates-rules-checklists-constraints)
- [5. Code Generation and Review](#5-code-generation-and-review)
- [6. Workflows](#6-workflows)
- [7. Systems, Autodetect, and Codebase Registration](#7-systems-autodetect-and-codebase-registration)
- [8. Kit Management](#8-kit-management)
- [Quick Reference — Terminal](#quick-reference--terminal)
- [Quick Reference — Prompts](#quick-reference--prompts)
- [Further Reading](#further-reading)

---

## 1. Initial Setup

🖥️ **Terminal**:
```bash
cpt init
cpt generate-agents
```

This creates `cypilot/config/` with all editable config files.

💬 `cypilot on` — enable Cypilot mode in your AI agent chat

💬 `cypilot auto-config` — scan codebase, generate convention rules, register systems

---

## 2. Agent Behavior — Navigation, Skills, Rules

These settings control **what the agent knows** when it works on your project. Without them, the agent relies on generic knowledge. With them, it consistently applies your team's domain knowledge, coding standards, and project-specific context — even across different team members and AI agents.

**Use cases**: a fintech team needs the agent to always consider compliance docs; a platform team wants every generated service to follow their internal SDK patterns; a solo developer wants consistent naming conventions across sessions.

### Navigation rules (`config/AGENTS.md`)

Tell the agent which files to load for which tasks. This is the most impactful setting — it determines what context the agent sees for specific domains.

💬 `cypilot add a rule: when working on authentication, always load docs/security.md`
💬 `cypilot add a rule: when writing tests, always load docs/test-patterns.md`
💬 `cypilot add a rule: when reviewing PRs, always load docs/review-guidelines.md`

### Skill instructions (`config/SKILL.md`)

Always-on instructions loaded into the agent's context on every request. Use these for project-wide invariants that apply everywhere — API envelope format, error handling strategy, logging approach.

💬 `cypilot add a skill instruction: all REST endpoints must return JSON with {data, error, meta} envelope`
💬 `cypilot add a skill instruction: never use print() for logging, always use the logger module`

### Project rules (`config/rules/`)

Per-topic convention files — conventions, architecture, testing, patterns. The agent loads relevant rules based on the task. Unlike skill instructions (always loaded), rules are topic-scoped and can be more detailed without bloating every request.

💬 `cypilot add a convention rule: all function names must use snake_case, no abbreviations`
💬 `cypilot add an architecture rule: all services must communicate through the message bus, no direct imports`
💬 `cypilot add a testing rule: every public function must have at least one unit test`
💬 `cypilot auto-config` — regenerate all rules from codebase

---

## 3. Identifiers & Traceability

Identifiers are the backbone of Cypilot's **requirements-to-code traceability**. Every requirement, component, flow, and task gets a unique `@cpt-*` ID. These IDs connect design artifacts to each other and to implementation code, enabling automated validation that nothing is forgotten.

**Why configure this**: different projects need different traceability depth. A regulated medical device needs full code-level traceability for every requirement. An internal tool might only need document-level cross-references. A prototype might want traceability turned off entirely.

**What it affects**: `cpt validate` checks ID integrity and cross-references. `cpt spec-coverage` reports which design IDs have matching code markers. The agent uses ID kinds and templates when generating artifacts.

![Traceability Capability](../images/traceability.png)

The diagram shows the three-layer chain: **Requirements** (PRD — ambiguous intents) → **Design** (DECOMPOSITION, DESIGN, FEATURE — structured specs with `cpt-*` IDs) → **Implementation** (code with `@cpt-*` markers). Each numbered circle is a traceable ID that flows through all layers.

Configuration lives in two places:

- **`constraints.toml`** (in kit) — defines ID kinds, naming templates, cross-reference rules, code traceability
- **`artifacts.toml`** (in config) — sets traceability mode per artifact (`FULL` or `DOCS-ONLY`)

### ID format

All IDs follow: `` `cpt-{system}-{kind}-{slug}` ``

Example: `cpt-myapp-fr-user-auth`, `cpt-myapp-flow-login`, `cpt-myapp-algo-password-hash`

### ID kinds (in `constraints.toml`)

ID kinds define **what types of identifiers** exist for each artifact. For example, a FEATURE artifact might have `flow`, `algo`, `dod`, and `state` ID kinds — each with different traceability requirements.

Each ID kind has configurable properties:

| Property | What it controls |
|---|---|
| `template` | Naming pattern, e.g. `cpt-{system}-fr-{slug}` |
| `required` | Whether at least one ID of this kind must exist |
| `to_code` | Whether `@cpt-*` code markers are required for this kind |
| `task` | Whether IDs use `[ ]`/`[x]` checkboxes for tracking |
| `priority` | Whether IDs use `p1`–`p9` priority markers |
| `headings` | Which constraint headings can contain these IDs |
| `references.TARGET.coverage` | Whether cross-references to TARGET artifact are mandatory |

💬 `cypilot add a new ID kind "api-endpoint" to FEATURE constraints, template "cpt-{system}-api-{feature-slug}-{slug}", to_code = true`
💬 `cypilot update the "algo" ID kind in FEATURE constraints: set to_code = false`
💬 `cypilot update the "dod" ID kind in FEATURE constraints: set task = false, priority = false`
💬 `cypilot add a cross-reference rule: DESIGN component IDs must reference DECOMPOSITION with coverage = true`

### What `cpt validate` checks

When you run `cpt validate`, the tool performs these checks on IDs:

- **ID format** — every ID matches `cpt-{system}-{kind}-{slug}` and the `template` for its kind
- **Cross-references** — if `coverage = true`, the target artifact must contain a reference to this ID. Missing reference = validation error
- **Task checkboxes** (`task = true`) — IDs use `[ ]` (not done) / `[x]` (done) checkboxes. Validation enforces consistency: if a reference is marked `[x]`, the definition must also be `[x]`. A reference with `[x]` pointing to a definition with `[ ]` is an error
- **Priority markers** (`priority = true`) — IDs use `` `p1` ``–`` `p9` `` markers. These are informational for ordering; validation checks they are present when required
- **Code markers** (`to_code = true`, traceability `FULL`) — validation checks that:
  - Definition has `[x]` checkbox → code `@cpt-*` marker **must** exist
  - Definition has `[ ]` checkbox → code marker **must not** exist (not implemented yet)
  - Definition has no checkbox → code marker **must** exist
  - Every `@cpt-begin` has a matching `@cpt-end`, no empty blocks, no orphan markers

### Nested identifiers

IDs form a hierarchy that mirrors your project structure. The depth depends on how many levels you define in `artifacts.toml`:

| Level | Pattern | Example |
|---|---|---|
| System | `cpt-{system}-{kind}-{slug}` | `cpt-saas-fr-user-auth` |
| Subsystem | `cpt-{system}-{subsystem}-{kind}-{slug}` | `cpt-saas-core-comp-api-gateway` |
| Component | `cpt-{system}-{subsystem}-{component}-{kind}-{slug}` | `cpt-saas-core-auth-flow-login` |

Cross-references flow **top-down**: a PRD defines requirements → DECOMPOSITION references them → DESIGN references DECOMPOSITION → FEATURE references DESIGN. Each level adds its slug to the ID prefix, creating a traceable chain from business requirements to implementation tasks.

### CDSL and instruction-level traceability

Inside FEATURE artifacts, behavioral sections (flows, algorithms, state machines) are written in **CDSL** — a plain-English specification language. Every CDSL step has its own checkbox, phase, and instruction ID:

```
1. [x] - `p1` - Validate user credentials - `inst-validate`
2. [ ] - `p2` - Generate session token - `inst-gen-token`
3. [x] - `p1` - Log audit trail - `inst-audit`
```

- **`[ ]` / `[x]`** — implementation status. `[x]` = implemented, `[ ]` = not yet
- **`p1`–`p9`** — implementation phase (which sprint/iteration)
- **`inst-{id}`** — unique instruction ID within the flow scope

These instruction IDs map directly to **code block markers**. The full code marker combines the artifact ID + phase + instruction:

```python
# @cpt-flow:cpt-myapp-feature-auth-flow-login:p1          ← scope (function level)
def login_flow(request):
    # @cpt-begin:cpt-myapp-feature-auth-flow-login:p1:inst-validate   ← step 1
    if not request.username:
        raise ValidationError("Missing credentials")
    # @cpt-end:cpt-myapp-feature-auth-flow-login:p1:inst-validate

    # @cpt-begin:cpt-myapp-feature-auth-flow-login:p1:inst-audit      ← step 3
    audit_log.record(request.username, "login_attempt")
    # @cpt-end:cpt-myapp-feature-auth-flow-login:p1:inst-audit
```

Validation connects the chain: CDSL step `[x]` on `inst-validate` → code marker `@cpt-begin:...:inst-validate` must exist. Step `[ ]` on `inst-gen-token` → code marker must **not** exist yet. This gives you per-instruction implementation tracking.

💬 `cypilot create FEATURE for user authentication` — generates a FEATURE with CDSL flows
💬 `cypilot implement cpt-myapp-feature-auth-flow-login phase p1` — generates code with markers for all `[x]` p1 steps

### Traceability mode (in `artifacts.toml`)

Controls whether code `@cpt-*` markers are validated for an artifact type. Change this when you want to relax or tighten validation per artifact kind — e.g., ADRs typically don't need code markers, but FEATURE specs usually do.

- **`FULL`** — all checks above are active, including code marker validation
- **`DOCS-ONLY`** — code markers are prohibited; only document-level ID and cross-reference checks apply

💬 `cypilot configure FEATURE artifacts to use DOCS-ONLY traceability`
💬 `cypilot configure ADR artifacts to use FULL traceability`

### Code markers

When `to_code = true`, implementation code must contain `@cpt-*` markers linking back to artifact IDs. This creates a bidirectional link: from the design document you can find the code, and from the code you can find the requirement. Useful for impact analysis ("what code implements this requirement?") and orphan detection ("is this code still needed?").

```python
# @cpt-flow:cpt-myapp-feature-auth-flow-login:p1        ← scope marker
def login_flow(request):
    # @cpt-begin:cpt-myapp-feature-auth-flow-login:p1:inst-validate  ← block start
    if not request.username:
        raise ValidationError("Missing username")
    # @cpt-end:cpt-myapp-feature-auth-flow-login:p1:inst-validate    ← block end
```

💬 `cypilot implement cpt-myapp-feature-auth-flow-login with code traceability markers`
💬 `cypilot check which IDs are missing code markers`

🖥️ `cpt validate` — validates artifact IDs, cross-references, and code markers
🖥️ `cpt spec-coverage` — shows which `to_code` IDs have/lack code markers

### ID search and navigation

🖥️ `cpt list-ids` — list all IDs across all artifacts
🖥️ `cpt list-ids --kind fr` — list only functional requirement IDs
🖥️ `cpt where-defined --id cpt-myapp-fr-user-auth` — find where an ID is defined
🖥️ `cpt where-used --id cpt-myapp-fr-user-auth` — find all references to an ID

💬 `cypilot find all IDs of kind "flow" in the auth feature`
💬 `cypilot show which artifacts reference cpt-myapp-fr-user-auth`
💬 `cypilot check cross-reference coverage for DESIGN components`

---

## 4. Artifact Templates, Rules, Checklists, Constraints

These resources control **how artifacts are generated and validated**. Templates define the structure, rules define generation/validation behavior, checklists define what the agent checks during review, and constraints define the structural schema.

**Why configure this**: your team may need extra sections (e.g., compliance, migration plan), stricter validation (e.g., every ADR must list alternatives), or domain-specific review criteria (e.g., check for GDPR implications). Editing these resources ensures every artifact follows your standards — whether generated by a junior developer or a senior architect.

**What it affects**: `cypilot create` uses templates when generating artifacts. `cpt validate` checks artifacts against constraints. The agent uses rules during generation and checklists during review.

Each artifact kind (ADR, PRD, DESIGN, FEATURE, etc.) has resource files. Paths are in `config/core.toml` under `[kits.sdlc.resources]`.

🖥️ `cpt resolve-vars --flat | grep adr` — find where ADR resources live

### Templates — control artifact generation structure

Templates define what sections a new artifact gets. Edit these when the default structure doesn't match your process — e.g., your ADRs need a "Migration Plan", or your PRDs need a "Compliance" section.

💬 `cypilot add a required section "## Migration Plan" to the ADR template, after "## Consequences"`
💬 `cypilot update the PRD template: add a "## Compliance Requirements" section`
💬 `cypilot create a new FEATURE template section "## Performance Targets"`

### Rules — control generation and validation behavior

Rules tell the agent what to enforce when generating or validating an artifact. They are more specific than templates — e.g., "every flow must have error handling" or "components must list dependencies".

💬 `cypilot add an ADR rule: the "Migration Plan" section must contain at least one checklist item`
💬 `cypilot add a FEATURE rule: every flow must have at least one error handling path`
💬 `cypilot update DESIGN rules: components must list all dependencies explicitly`

### Checklists — control semantic review criteria

Checklists are used by the agent during artifact review (`cypilot analyze`). They define what the agent should verify beyond structural constraints — business logic, completeness, consistency.

💬 `cypilot add to the DESIGN review checklist: verify that all external API calls have timeout and retry configuration`
💬 `cypilot add to the FEATURE review checklist: check that every DoD item has a priority marker`
💬 `cypilot add to the ADR review checklist: verify alternatives were evaluated with pros/cons`

### Structural constraints — control heading structure, ID placement

Constraints define the exact heading structure that `cpt validate` enforces. They are the most strict form of validation — a missing required heading fails validation. Edit these when you add new template sections that should be mandatory.

Each heading entry in `constraints.toml` needs `id`, `level`, `required`, `pattern`.

💬 `cypilot add a required level-2 heading "Migration Plan" to ADR constraints, id "adr-migration-plan"`
💬 `cypilot update FEATURE constraints: make "## Performance Targets" optional instead of required`

🖥️ `cpt validate-kits` — validate constraint definitions
🖥️ `cpt validate` — validate artifacts against constraints

---

## 5. Code Generation and Review

These settings control **how the agent writes and reviews code**. Code rules apply when the agent generates or modifies source files. The code review checklist applies when the agent reviews code (e.g., during `cypilot analyze` on a source file).

**Why configure this**: prevent common mistakes before they happen. If your team has had incidents with SQL injection, add a rule forbidding string interpolation in queries. If secrets have leaked, add a review checklist item. These rules act as a persistent safety net that applies to every code change.

### Code generation rules

Apply when the agent writes or modifies source code. Use these for security policies, style enforcement, and antipattern prevention.

💬 `cypilot add a code rule: all database queries must use parameterized statements, never string interpolation`
💬 `cypilot add a code rule: all async functions must have explicit timeout handling`
💬 `cypilot add a code rule: never import from internal modules using relative paths`

### Code review checklist

Used when the agent reviews code. Each item becomes a check the agent performs and reports on.

💬 `cypilot add to the code review checklist: verify no secrets or API keys are hardcoded`
💬 `cypilot add to the code review checklist: check that all new public functions have docstrings`
💬 `cypilot add to the code review checklist: verify error messages include correlation IDs`

---

## 6. Workflows

Workflows are **multi-step agent procedures** — they define the exact sequence of actions the agent takes for complex tasks like generating an artifact, reviewing a PR, or planning a feature.

**Why configure this**: if the default workflow misses a step your team cares about (e.g., checking for migration files, asking about backward compatibility), you can add it. If a step is unnecessary for your project, you can remove it.

**What it affects**: every `cypilot create`, `cypilot review`, and `cypilot plan` request follows the corresponding workflow. Changes here affect the agent's behavior globally for that task type.

Paths are in `core.toml` as `kits.sdlc.resources.workflow_*`.

💬 `cypilot update the PR review workflow: after fetching the diff, check if any migration files were changed and flag them`
💬 `cypilot update the generate workflow: always ask about backward compatibility before writing`

---

## 7. Systems, Autodetect, and Codebase Registration

The artifacts registry (`config/artifacts.toml`) tells Cypilot **what your project looks like** — where artifacts live, where source code lives, and how they're organized.

**Why configure this**: Cypilot can only validate and trace what it knows about. If you add a new microservice, a new artifact directory, or switch from Python to Go, you need to update the registry. Without it, `cpt validate` won't find your artifacts and `cpt spec-coverage` won't scan your code.

**Use cases**: monorepo with multiple services; project adding a new language; team splitting a service into sub-modules; migrating ADRs to a different directory structure.

It has three layers:

### Systems

A system is a top-level grouping with a `name`, `slug`, and `kit`. The slug becomes part of every ID (`cpt-{slug}-...`). Most projects have one system; monorepos may have several.

💬 `cypilot add a new system "billing" with slug "billing", using kit "sdlc", artifacts at billing/architecture`

### Autodetect patterns

Autodetect tells Cypilot where to find artifacts and codebases automatically using glob patterns. This is the preferred way to register artifacts — when you add a new FEATURE spec file matching the pattern, Cypilot picks it up without config changes.

Each artifact pattern has:

| Property | What it controls |
|---|---|
| `pattern` | Glob pattern relative to `artifacts_root`, e.g. `PRD.md`, `ADR/**/*.md`, `features/*.md` |
| `traceability` | `FULL` (code markers validated) or `DOCS-ONLY` (no code markers) |
| `required` | Whether the artifact must exist |

💬 `cypilot add autodetect for FEATURE artifacts: pattern "features/*.md", traceability FULL, required false`
💬 `cypilot update ADR autodetect pattern to "decisions/**/*.md"`
💬 `cypilot configure PRD autodetect: set required = true`

You can also register a specific artifact manually (not via autodetect):

💬 `cypilot add a manual artifact "Execution Plans" at architecture/features/execution-plans.md, kind FEATURE, traceability DOCS-ONLY`

### Codebase entries

Each codebase entry tells Cypilot where source code lives and how to parse comments for `@cpt-*` markers. Without a codebase entry, `cpt spec-coverage` and `cpt validate` can't find your code markers.

| Property | What it controls |
|---|---|
| `name` | Display name, e.g. "Backend" |
| `path` | Directory path relative to system root |
| `extensions` | File extensions to scan, e.g. `[".py"]`, `[".ts", ".tsx"]` |
| `singleLineComments` | Comment prefixes, e.g. `["#"]`, `["//"]` |
| `multiLineComments` | Multi-line comment delimiters, e.g. `[{start = '"""', end = '"""'}]` |

💬 `cypilot add codebase "Frontend" at web/src, TypeScript (.ts, .tsx), single-line comments "//"`
💬 `cypilot add codebase "Mobile" at mobile/lib, Dart (.dart), single-line comments "//"`
💬 `cypilot update codebase "Backend": add multiLineComments for Python triple-quotes`

### Ignore patterns

Exclude files from validation. Use this for test fixtures with synthetic `@cpt-*` markers, generated files, or legacy code you don't want validated yet.

💬 `cypilot add an ignore pattern: tests/test_fixtures/** with reason "synthetic test data"`

🖥️ `cpt validate` — validate registry and all artifacts

---

## 8. Kit Management

Kits are modular packages that provide templates, rules, checklists, constraints, and workflows. When a kit is updated upstream, you pull changes with `kit update` — it shows a file-level diff so you can accept or decline each change.

**Why configure this**: keep your artifact standards up to date with the latest kit version; install a custom kit for your organization; switch between kit versions.

🖥️ **Terminal only**:
```bash
cpt kit install /path/to/my-kit    # install a kit
cpt kit update                      # update kit files (interactive diff)
cpt update                          # update Cypilot core + all kits
```

---

## Quick Reference — Terminal

| What you want | Command |
|---|---|
| Initialize project | `cpt init` |
| Auto-generate rules | `cpt auto-config` |
| Install a kit | `cpt kit install <path>` |
| Update kit files | `cpt kit update` |
| Update core + kits | `cpt update` |
| Validate artifacts + code | `cpt validate` |
| Validate kit config | `cpt validate-kits` |
| ID coverage in code | `cpt spec-coverage` |
| List all IDs | `cpt list-ids` |
| List IDs by kind | `cpt list-ids --kind <kind>` |
| Find ID definition | `cpt where-defined --id <id>` |
| Find ID references | `cpt where-used --id <id>` |
| See current config | `cpt info` |
| Resolve resource paths | `cpt resolve-vars --flat` |
| Generate agent files | `cpt generate-agents --agent windsurf` |

## Quick Reference — Prompts

| Category | Prompt |
|---|---|
| **Setup** | |
| Enable Cypilot | `cypilot on` |
| Scan and configure | `cypilot auto-config` |
| **Agent behavior** | |
| Navigation rule | `cypilot add a rule: when working on <topic>, always load <file>` |
| Skill instruction | `cypilot add a skill instruction: <instruction>` |
| Convention rule | `cypilot add a convention rule: <rule>` |
| Architecture rule | `cypilot add an architecture rule: <rule>` |
| Testing rule | `cypilot add a testing rule: <rule>` |
| **Identifiers** | |
| Add ID kind | `cypilot add a new ID kind "<kind>" to <KIND> constraints, template "cpt-{system}-<kind>-{slug}", to_code = <true/false>` |
| Change to_code | `cypilot update the "<kind>" ID kind in <KIND> constraints: set to_code = <true/false>` |
| Add cross-ref rule | `cypilot add a cross-reference rule: <KIND> <kind> IDs must reference <TARGET> with coverage = true` |
| Change traceability | `cypilot configure <KIND> artifacts to use <FULL/DOCS-ONLY> traceability` |
| Implement with markers | `cypilot implement <cpt-id> with code traceability markers` |
| Find missing markers | `cypilot check which IDs are missing code markers` |
| **Artifacts** | |
| Edit template | `cypilot add a section "<heading>" to the <KIND> template` |
| Edit rules | `cypilot add a <KIND> rule: <rule>` |
| Edit checklist | `cypilot add to the <KIND> review checklist: <criteria>` |
| Edit constraints | `cypilot add a required level-<N> heading "<title>" to <KIND> constraints, id "<id>"` |
| **Code** | |
| Code rule | `cypilot add a code rule: <rule>` |
| Code checklist | `cypilot add to the code review checklist: <criteria>` |
| **Generate** | |
| Create artifact | `cypilot create <KIND> for <topic>` |
| Update artifact | `cypilot update the <KIND> at <path>: <what to change>` |
| Implement code | `cypilot implement <feature/requirement description>` |
| **Analyze** | |
| Validate all | `cypilot validate all` |
| Validate artifact | `cypilot validate <path>` |
| Check coverage | `cypilot check spec coverage` |
| Find ID | `cypilot find where <cpt-id> is defined` |
| Show references | `cypilot show all references to <cpt-id>` |
| **Registry** | |
| Add system | `cypilot add a new system "<name>" with slug "<slug>", using kit "sdlc", artifacts at <path>` |
| Add autodetect | `cypilot add autodetect for <KIND> artifacts: pattern "<glob>", traceability <FULL/DOCS-ONLY>` |
| Update autodetect | `cypilot update <KIND> autodetect pattern to "<glob>"` |
| Add manual artifact | `cypilot add a manual artifact "<name>" at <path>, kind <KIND>, traceability <FULL/DOCS-ONLY>` |
| Add codebase | `cypilot add codebase "<name>" at <path>, <language>, single-line comments "<prefix>"` |
| Add ignore pattern | `cypilot add an ignore pattern: <glob> with reason "<reason>"` |

---

## Further Reading

| Topic | Spec / Schema |
|---|---|
| core.toml format | `schemas/core-config.schema.json` |
| artifacts.toml format | `schemas/artifacts.schema.json`, `architecture/specs/artifacts-registry.md` |
| Kit system | `architecture/specs/kit/kit.md` |
| Templates | `architecture/specs/kit/template.md` |
| Rules | `architecture/specs/kit/rules.md` |
| Checklists | `architecture/specs/kit/checklist.md` |
| Constraints & IDs | `architecture/specs/kit/constraints.md`, `schemas/kit-constraints.schema.json` |
| Traceability & markers | `architecture/specs/traceability.md` |
| CDSL language | `architecture/specs/CDSL.md` |
| CLI commands | `architecture/specs/cli.md` |
| System prompts | `architecture/specs/sysprompts.md` |
| Workspace config | `schemas/workspace.schema.json` |
