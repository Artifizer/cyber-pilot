# <p align="center"><img src="images/cypilot-kit.png" alt="Cypilot Banner" width="100%" /></p>

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.6-green.svg)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)]()
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=cyberfabric_cyber-pilot&metric=coverage)](https://sonarcloud.io/summary/new_code?id=cyberfabric_cyber-pilot)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=cyberfabric_cyber-pilot&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=cyberfabric_cyber-pilot)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=cyberfabric_cyber-pilot&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=cyberfabric_cyber-pilot)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=cyberfabric_cyber-pilot&metric=bugs)](https://sonarcloud.io/summary/new_code?id=cyberfabric_cyber-pilot)

**Version**: 3.6

**Status**: Active

**Audience**: Developers using AI coding assistants, technical leads, engineering teams

## Cyber Pilot — Deterministic orchestration for AI agents

Cyber Pilot (*Cypilot*) is **not another coding model or AI agent**.

Cyber Pilot is a **deterministic orchestration and validation layer** that sits on top of AI agents and helps them transform one kind of document into another, or into code, while preserving strict format, structural consistency, and cross-artifact alignment through identifiers.

A delivery chain such as **requirements -> design -> decomposition -> implementation -> validation** is one important example of that broader idea.

In practice, this means Cyber Pilot helps you:

- **Transform artifacts** from one stage into the next, such as `PRD -> DESIGN -> DECOMPOSITION -> FEATURE -> CODE`.
- **Enforce structure** with templates, constraints, workflows, and deterministic checks.
- **Keep traceability** between documents, decisions, tasks, and code.
- **Work across repositories and extensible project boundaries** through workspace and multi-repo support.
- **Reduce context drift** on large tasks by turning them into executable plans.
- **Use existing AI tools better** instead of pretending to replace them.

> **Convention**: 💬 = paste into AI agent chat. 🖥️ = run in terminal.

---

## Table of Contents

<!-- toc -->

- [Cyber Pilot — Deterministic orchestration for AI agents](#cyber-pilot--deterministic-orchestration-for-ai-agents)
- [Table of Contents](#table-of-contents)
- [Why Cyber Pilot exists](#why-cyber-pilot-exists)
- [What Cypilot is and is not](#what-cypilot-is-and-is-not)
  - [What it is](#what-it-is)
  - [What it is not](#what-it-is-not)
  - [Where it is strongest / weakest](#where-it-is-strongest--weakest)
- [Expectation setting](#expectation-setting)
- [A critical clarification about IDs and code generation](#a-critical-clarification-about-ids-and-code-generation)
- [Why plans matter so much](#why-plans-matter-so-much)
- [How to think about Cypilot with other tools](#how-to-think-about-cypilot-with-other-tools)
- [What Cypilot does not replace](#what-cypilot-does-not-replace)
- [What Cypilot provides](#what-cypilot-provides)
  - [1. Core platform](#1-core-platform)
  - [2. SDLC kit](#2-sdlc-kit)
- [Prerequisites](#prerequisites)
- [Quick start](#quick-start)
  - [1. Install the CLI](#1-install-the-cli)
  - [2. Initialize a project](#2-initialize-a-project)
  - [2.5 Update an existing installation](#25-update-an-existing-installation)
  - [3. Enable Cypilot mode in your AI tool](#3-enable-cypilot-mode-in-your-ai-tool)
  - [4. Start with one of the three main workflows](#4-start-with-one-of-the-three-main-workflows)
- [Configuration at a glance](#configuration-at-a-glance)
- [Workflow model](#workflow-model)
- [Best practices](#best-practices)
- [Agent tools](#agent-tools)
- [Multi-repo workspaces](#multi-repo-workspaces)
- [RalphEx delegation](#ralphex-delegation)
- [Extensibility](#extensibility)
- [Further reading](#further-reading)
- [Feedback and issues](#feedback-and-issues)
- [Bottom line](#bottom-line)
- [Contributing](#contributing)
- [License](#license)

<!-- /toc -->


## Why Cyber Pilot exists

The main problem Cyber Pilot solves is **not** “how to get more raw code out of an LLM.”

The main problem it solves is this:

When work becomes larger than a single prompt, teams need a reliable way to transform one artifact into another, or into code, without losing structure, meaning, and consistency.

That usually breaks down in four places:

- **Cross-stage transformation breaks**
  
  One document does not cleanly become the next, or code diverges from the documents that should guide it.

- **LLMs lose structural discipline**
  
  A model may write plausible content, but it does not reliably preserve required sections, traceability, checklist coverage, or consistent conventions across a long chain of artifacts.

- **Large tasks overflow context**
  
  As soon as a task becomes multi-step, the working context gets noisy and brittle. Important details are dropped, repeated, or contradicted.

- **Tooling is fragmented**
  
  Teams use Claude Code, Cursor, Windsurf, Copilot, terminal commands, CI, templates, reviews, and custom conventions. Without a common layer, every workflow becomes ad hoc.

Cyber Pilot exists to add a missing layer between the human intent and the agent output:

- **Structured workflows with deterministic routing and gates**
  
  The task is routed through a defined workflow, with fixed checkpoints and explicit rules for when the next step is allowed.
- **Deterministic validation**
  
  Anything that can be checked by scripts instead of model judgment is validated the same way every time.
- **Deterministic structure**
  
  Templates, constraints, and required sections keep documents and outputs in a predictable shape.
- **Deterministic traceability**
  
  Identifiers and references make it possible to reliably connect requirements, design, tasks, and code.

The LLM still does the reasoning and writing.

Cyber Pilot makes the surrounding process far more controlled.

This is also what makes Cyber Pilot different from most AI coding tools, which are strongest at **local generation**:

- **Controlled artifact transformation**
  
  Cyber Pilot is built around moving from one artifact to another, or from artifacts into code, in a controlled way, not just answering one prompt well.

- **Deterministic enforcement where possible**
  
  If something can be validated without an LLM, Cyber Pilot pushes it into scripts and rules instead of leaving it to model judgment.

- **Templates, checklists, constraints, and IDs as first-class tools**
  
  The structure layer is not a side feature. It is the product.

- **Multi-repo support and project extensibility**
  
  Cyber Pilot can work across repository boundaries through workspaces and extensible project configuration instead of assuming everything lives in one local repo.

- **Plans for context preservation**
  
  For large tasks, Cyber Pilot can split work into smaller executable phases so the agent does not have to carry everything in one overflowing conversation.

- **Complementary architecture**
  
  Cyber Pilot is meant to work with Claude Code, Cursor, Copilot, Windsurf, OpenAI tools, CI, and optional delegation systems like RalphEx.

---

## What Cypilot is and is not

### What it is

| Statement | Explanation |
|---|---|
| Cypilot is a structured transformation, validation, and coordination layer for AI agents | It adds workflows, validation, traceability, workspaces, and execution planning around existing agents. |
| Cypilot is primarily a system for transforming structured artifacts into other artifacts or into code | Its core value is controlled document-to-document and document-to-code transformation. |
| Cypilot is a way to make AI-assisted work more controlled where deterministic rules are possible | It pushes validation, structure, and routing into scripts, constraints, and workflow logic wherever possible. |
| Cypilot is a coordination layer, not just a prompt prefix | Its value comes from workflows, kits, validation, traceability, context loading, planning, and workspace support working together. |

### What it is not

| Statement | Explanation |
|---|---|
| Cypilot is not a replacement for Claude Code, Cursor, Copilot, Windsurf, or other coding agents | It is designed to work through those tools, not replace them. |
| Cypilot is not a magic code generator | It can improve artifact-to-code flows, but it does not turn vague intent into perfect code by itself. |
| Cypilot does not replace good source documents | Weak requirements, weak design, or weak decomposition still produce weak downstream results. |
| Cypilot does not make code good just because identifiers exist | IDs improve traceability and consistency control, not architecture quality or implementation judgment. |
| Cypilot does not replace human architecture judgment | It helps structure and validate decisions; it does not eliminate the need for good thinking. |
| Cypilot does not replace human review | It improves consistency and catches many classes of issues, but review responsibility still remains with people. |
| Cypilot does not replace specialized tools in your stack | It complements your IDE, coding agent, CI, review tools, design workflows, and other supporting systems. |

### Where it is strongest / weakest

| Statement | Explanation |
|---|---|
| Cypilot is strongest where the workflow can be made structured and partially deterministic | This is where templates, constraints, checklists, IDs, validators, and routing rules provide the most leverage. |
| Cypilot is especially useful for large tasks because plans preserve context | Planning reduces context overflow, keeps tasks bounded, and makes progress easier to inspect. |
| Cypilot is more about process reliability than raw generation speed | Its main advantage is controlled transformation and validation, not maximal speed of first-draft output. |
| Cypilot is not the best first tool for highly ambiguous visual or frontend exploration | If the task is still open-ended and the structure is not yet clear, freer exploration is often a better first step. |

---

## Expectation setting

Cyber Pilot works best when the task has enough structure to benefit from workflows, validation, traceability, and planning.

It is usually a weaker first move for tiny edits, throwaway spikes, heavily token-constrained work, open-ended discovery, or purely visual exploration where structure is not yet the priority.

That tradeoff is intentional: Cyber Pilot spends more process and context budget to gain more control, stronger repeatability, and clearer validation boundaries.

For the full fit / non-fit guidance and practical decision rules, use **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

---

## A critical clarification about IDs and code generation

Identifiers and traceability improve control: they link artifacts, track what was specified and implemented, support deterministic consistency checks, and help find drift.

They do **not** guarantee good requirements, good architecture, good design, or good implementation judgment.

For the practical anti-pattern behind this misunderstanding, use **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

---

## Why plans matter so much

For large tasks, planning is one of Cypilot’s highest-leverage features because it keeps context bounded, makes progress inspectable, and turns “do everything” into a controlled execution sequence.

If the task is likely to overflow one conversation, `plan` is usually the right starting point.

For planning heuristics and workflow-choice guidance, use **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

---

## How to think about Cypilot with other tools

Cypilot should usually be viewed as a **coordination layer**, not as a competitor.

| Tool / actor | What it is good at | What Cypilot adds |
|---|---|---|
| Claude Code / Cursor / Windsurf / Copilot / Codex | Local coding, editing, reasoning, interactive implementation | Structured workflow routing, context discipline, deterministic validation, traceability, plans |
| Human engineer | Judgment, tradeoffs, business understanding, architecture responsibility | A repeatable structure around those decisions |
| Human reviewer | Nuanced review, organizational context, product risk awareness | Repeatable checklists and deterministic gates before or alongside review |
| CI pipeline | Reproducible automation | Cypilot-compatible validation, status, and workflow outputs |
| RalphEx | Optional delegated execution | Structured handoff through plan-driven flows |

---

## What Cypilot does not replace

- **Good initial problem framing**
  
  If the task is underspecified, the result will still be underspecified.

- **Good source documents**
  
  Cypilot can help improve them, but it does not eliminate the need for clear requirements and design.

- **Other specialized tools**
  
  It does not replace your IDE, your coding agent, your review tool, your design tool, or your deployment stack.

- **Review discipline**
  
  You should still validate important changes with human judgment.

- **Product discovery**
  
  If you are exploring what should be built at a highly ambiguous level, Cypilot is usually not the very first tool to reach for.

---

## What Cypilot provides

Cypilot has two main layers:

### 1. Core platform

The core provides:

- **Deterministic skill engine**
- **Universal workflows** for `plan`, `generate`, and `analyze`
- **Agent integrations** for Windsurf, Cursor, Claude, Copilot, and OpenAI-compatible environments
- **CLI command** through `cpt`
- **Configuration and kit management**
- **Traceability infrastructure** for IDs and code markers
- **Execution plans** for phased work
- **Optional delegation support** through RalphEx

### 2. SDLC kit

The SDLC kit provides an artifact-first pipeline with templates, rules, checklists, examples, and validation for documents such as:

- **PRD**
- **DESIGN**
- **ADR**
- **DECOMPOSITION**
- **FEATURE**

This is one concrete kit that makes structured document-to-document and document-to-code flows practical.

Repository: **[cyberfabric/cyber-pilot-kit-sdlc](https://github.com/cyberfabric/cyber-pilot-kit-sdlc)**

---

## Best practices

Operational usage guidance now lives in **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

In short:

- **Use `plan`** for large, risky, or context-heavy work
- **Use `generate`** for bounded creation, modification, and implementation
- **Use `analyze`** for validation, inspection, comparison, and review
- **Keep inputs structured** and validate early instead of waiting until the end
- **Separate generation from review** and avoid carrying stale context across unrelated tasks
- **Require final human review** even after successful validation and AI review

For situation-by-situation guidance, prompt patterns, context hygiene, brownfield advice, workspace federation, and delegation safety, use the full guide.

---

## Agent tools

Host-specific guidance now lives in **[guides/AGENT-TOOLS.md](guides/AGENT-TOOLS.md)**.

In short:

- Cypilot works across **Claude Code, Cursor, GitHub Copilot, OpenAI Codex, and Windsurf**
- Host tools differ on **subagent support, read-only enforcement, model selection, and isolation**
- **Claude Code** is the highest-fidelity host for Cypilot subagents and worktree-style isolation
- **Cursor, Copilot, and Windsurf** are useful partly because they can be **multi-model hosts**
- **Windsurf** has no subagents, so you should use manual chat separation or Cypilot-generated next-chat prompts as a workaround

For the support matrix, model guidance, Windsurf-specific workarounds, and tool-by-tool recommendations, use the full guide.

---

## Prerequisites

- **Python 3.11+**
  
  Required for the CLI and skill engine.

- **Git**
  
  Used for project detection, workspace handling, and normal repository workflows.

- **An AI agent**
  
  Cypilot is designed to work through tools such as Windsurf, Cursor, Claude Code, Copilot, and OpenAI-compatible environments.

- **`pipx`**
  
  Recommended for installing the CLI globally.

- **`gh` CLI** *(optional)*
  
  Useful for PR review and PR status workflows.

- **`RalphEx`** *(optional)*
  
  Needed only if you want to use the delegation path through `cypilot-ralphex` or `cpt delegate`.

---

## Quick start

### 1. Install the CLI

🖥️ **Terminal**:

```bash
pipx install git+https://github.com/cyberfabric/cyber-pilot.git
```

Update later with:

```bash
pipx upgrade cypilot
```

This installs `cpt` globally.

The CLI is a thin entrypoint. On use, it resolves to the cached or project-local Cypilot engine.

Project links:

- **`pipx`**: [pipx.pypa.io](https://pipx.pypa.io/)
- **Homebrew**: [brew.sh](https://brew.sh/)
- **Scoop**: [scoop.sh](https://scoop.sh/)

**macOS note**

If you do not have `pipx` yet, the recommended install path is **Homebrew**:

```bash
brew install pipx
pipx ensurepath
```

Then open a new terminal, or reload the shell config that `pipx ensurepath` updated.
For example, with the default macOS `zsh` setup:

```bash
source ~/.zshrc
```

**Windows note**

If you do not have `pipx` yet, the recommended install path is **Scoop**:

```bash
scoop install pipx
pipx ensurepath
```

Then open a new terminal so the updated `PATH` is picked up.

### 2. Initialize a project

🖥️ **Terminal**:

```bash
cpt init
cpt generate-agents
```

This creates the Cypilot directory for your project and prepares agent-specific integrations.

`cpt init` creates three main areas:

| Directory | Purpose | Editable? |
|---|---|---|
| `.core/` | Read-only core workflows, skills, schemas, and requirements | No |
| `.gen/` | Generated aggregate files for agent consumption | No |
| `config/` | Project configuration and installed kit material | Yes |

It also creates `config/core.toml` and `config/artifacts.toml`, defines a root system, and injects the managed root `AGENTS.md` block.

`cpt generate-agents` supports: `windsurf`, `cursor`, `claude`, `copilot`, `openai`.

It generates workflow entry points, skill outputs, and subagents where the host tool supports them.

### 2.5 Update an existing installation

🖥️ **Terminal**:

```bash
cpt update
```

This refreshes `.core/`, regenerates `.gen/`, and updates kit files in `config/kits/` with file-level diffs.

### 3. Enable Cypilot mode in your AI tool

💬 **AI agent chat**:

```text
cypilot on
```

### 4. Start with one of the three main workflows

**Analyze**

💬 **AI agent chat**:

```text
cypilot analyze: validate architecture/DESIGN.md
```

**Generate**

💬 **AI agent chat**:

```text
cypilot generate: implement the approved auth feature from the current FEATURE spec
```

**Plan**

💬 **AI agent chat**:

```text
cypilot plan: break this migration into safe implementation phases
```

---

## Configuration at a glance

All user-editable configuration lives under `config/` inside your Cypilot directory.

| File | What it controls |
|---|---|
| `core.toml` | Project settings, installed kits, workspace configuration, and resource bindings |
| `artifacts.toml` | Registered systems, artifact kinds, codebase paths, and traceability modes |
| `AGENTS.md` | Navigation rules for what the agent should load for which tasks |
| `SKILL.md` | Always-on project-specific skill instructions |
| `rules/*.md` | Topic-specific project rules, conventions, architecture, testing, and patterns |

To inspect resolved kit resource paths:

🖥️ **Terminal**:

```bash
cpt resolve-vars --flat
```

For full configuration details, see **[Configuration guide](guides/CONFIGURATION.md)**.

---

## Workflow model

Cypilot has three core workflows:

💬 **AI agent chat**:

- **`/cypilot-plan`**
  
  Use it when the task is too large, too risky, or too context-heavy for one conversation.

- **`/cypilot-generate`**
  
  Use it when you want to create, update, implement, or configure something.

- **`/cypilot-analyze`**
  
  Use it when you want to validate, review, inspect, compare, or audit.

For default routing priorities and detailed workflow-choice advice, use **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

---

## Multi-repo workspaces

Cypilot supports **multi-repo workspaces** so artifacts, code, and kits do not all have to live in one repository.

For practical guidance on when to use workspace federation, orchestration-repo patterns, and how to keep multi-repo setups manageable, see **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

For the full workspace model and configuration rules, see **[requirements/workspace.md](requirements/workspace.md)**.

---

## RalphEx delegation

RalphEx support is optional.

When available, Cyber Pilot can delegate execution through the dedicated `cypilot-ralphex` path.

For when to delegate, how to supervise autonomous loops, and how RalphEx safeguards interact with human review, use **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

---

## Extensibility

Cypilot is extensible through **kits**.

A kit can define:

- **artifact kinds**
- **templates**
- **rules**
- **checklists**
- **constraints**
- **examples**
- **workflows**

The built-in SDLC kit is one important example; see **[cyber-pilot-kit-sdlc](https://github.com/cyberfabric/cyber-pilot-kit-sdlc)**. The architecture is meant to support additional domains and project-specific structure layers.

---

## Further reading

- **[Best practices guide](guides/BEST-PRACTICES.md)**
- **[Agent tools guide](guides/AGENT-TOOLS.md)**
- **[Configuration guide](guides/CONFIGURATION.md)**
- **[Story-driven walkthrough](guides/STORY.md)**
- **[Architecture and ADRs](architecture/)**
- **[Requirements and checklists](requirements/)**
- **[Workspace specification](requirements/workspace.md)**
- **[Contributing guide](CONTRIBUTING.md)**
- **Kit, traceability, and schema specs:** [architecture/specs/](architecture/specs/) and [schemas/](schemas/)

---

## Feedback and issues

If you think a prompt is not optimized, a workflow or instruction stack has behavioral bugs, an agent instruction is weak for LLM use, a script behaves incorrectly, or important corner cases are missing, please open a GitHub issue.

- **Issues list:** [github.com/cyberfabric/cyber-pilot/issues](https://github.com/cyberfabric/cyber-pilot/issues)
- **Create a new issue:** [github.com/cyberfabric/cyber-pilot/issues/new/choose](https://github.com/cyberfabric/cyber-pilot/issues/new/choose)

Good issue categories include:

- **Prompt quality problems**
- **Prompt or instruction bugs**
- **Workflow routing or behavior bugs**
- **Script or CLI failures**
- **Validation gaps**
- **Missing corner-case coverage**
- **Documentation inconsistencies or unclear guidance**

A practical GitHub-style issue template:

```md
## Summary
Short description of the problem.

## Type
- Prompt optimization
- Prompt bug
- Instruction quality
- Workflow bug
- Script / CLI bug
- Missing edge case
- Documentation issue

## Scope
What file, workflow, script, command, prompt, or artifact is affected?

## Expected behavior
What should happen?

## Actual behavior
What happened instead?

## Steps to reproduce
1. ...
2. ...
3. ...

## Evidence
Logs, validator output, screenshots, failing examples, or prompt snippets.

## Environment
- OS:
- Host tool:
- Model if relevant:
- Cypilot version / branch / commit if known:

## Impact
Why this matters: wrong routing, unsafe behavior, broken validation, poor LLM performance, missing coverage, etc.

## Additional context
Anything else that helps narrow the issue.
```

For prompt and instruction issues, include the smallest reproducible prompt or instruction slice you can share.

For script or validator issues, include the exact command, exit status, and relevant output if possible.

---

## Bottom line

Cypilot is best understood as a **deterministic transformation, structure, and validation layer for AI-assisted engineering**.

It is strongest when you need:

- **document-to-document and document-to-code transformation**
- **deterministic validation**
- **structured review**
- **traceability**
- **planning for large tasks**

It is weakest when you expect it to replace:

- **thinking**
- **discovery**
- **good documents**
- **good code review**
- **specialized tools**

Used correctly, it does not replace your stack.

It makes your stack work together more reliably.

---

## Contributing

If you want to contribute, start with **[CONTRIBUTING.md](CONTRIBUTING.md)**.

---

## License

Cyber Pilot is licensed under the **Apache License 2.0**. See **[LICENSE](LICENSE)** for details.
