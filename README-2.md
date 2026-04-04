# <p align="center"><img src="images/cypilot-kit.png" alt="Cypilot Banner" width="100%" /></p>
 
 [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
  ![Version](https://img.shields.io/badge/version-3.6.0--beta-green.svg)
  ![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
  [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=cyberfabric_cyber-pilot&metric=coverage)](https://sonarcloud.io/summary/new_code?id=cyberfabric_cyber-pilot)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=cyberfabric_cyber-pilot&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=cyberfabric_cyber-pilot)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=cyberfabric_cyber-pilot&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=cyberfabric_cyber-pilot)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=cyberfabric_cyber-pilot&metric=bugs)](https://sonarcloud.io/summary/new_code?id=cyberfabric_cyber-pilot)
 
**Version**: 3.6.0-beta

**Status**: Active

**Audience**: Developers using AI coding assistants, technical leads, engineering teams

## Cyber Pilot — tooling for traceable, reviewable AI-assisted software changes

It adds bounded phases, stable identifiers, and verifiable checks to AI-assisted work that has outgrown a single chat. It is **not** another coding model, IDE, or AI host.

It works alongside tools such as Claude Code, Cursor, GitHub Copilot, OpenAI Codex, and Windsurf to keep larger changes reviewable and traceable to approved requirements and design.

Use it when a change spans multiple AI-assisted steps and you need evidence that the final code still lines up with approved requirements, design, tasks, and constraints.

It adds three controls that plain prompting does not preserve well at larger scope:

- **reuse the same stable identifiers from requirements and design through tasks, code, and checks so drift and missing links become visible**
- **break large or risky work into bounded, reviewable phases**
- **run deterministic checks on structure, references, consistency, and traceability**

The model itself is still **non-deterministic**. Cyber Pilot does not try to change that. Instead, it adds structure and checks around the parts of the workflow that *can* be made explicit and verifiable.

### Who this is for

Use Cyber Pilot if you already work with an AI coding assistant and need more control over larger or riskier work.

- **Engineers** — to keep larger changes bounded, reviewable, and easier to continue safely
- **Tech leads and architects** — to reduce drift between approved requirements, design, and implementation
- **Product and delivery leads** — to see how approved scope maps to implementation and what review evidence supports it

Cyber Pilot is usually **not** the right starting point for tiny edits, throwaway spikes, or open-ended exploration where speed matters more than structure.

### What changes in practice

Without Cyber Pilot, larger AI-assisted tasks often collapse into one long mixed-purpose thread, making scope drift easier to miss and review harder to trust.

With Cyber Pilot, you split the work into explicit planning, generation, review, and traceability checks instead of one long mixed-purpose thread:

- **`plan`** — break large or risky work into bounded phases
- **`generate`** — implement or produce something within approved scope
- **`analyze`** — review, validate, compare, or look for gaps
- **traceability checks** — verify that requirements, design decisions, tasks, and code changes still line up through the same stable identifiers

In practice, this usually means:

- **fewer long mixed-purpose chats**
- **clearer implementation boundaries**
- **better alignment between approved docs and code**
- **earlier detection of drift and missing links**
- **more reliable review before merge**

### One practical path from idea or PoC to production

Cyber Pilot is strongest when an early idea or PoC needs to become a production-ready change without losing scope or design intent.

A typical path is: approve the requirement and design, split the change into bounded phases, implement one phase at a time, review each phase against the same identifiers, then verify before merge that the shipped code still traces back to the approved requirement, design, and tasks.

> **Convention**: 💬 = paste into AI agent chat. 🖥️ = run in terminal.

## Jump to

- [Quick start](#quick-start)
- [What success looks like after 5 minutes](#5-what-success-looks-like-after-5-minutes)
- [Host support at a glance](#host-support-at-a-glance)
- [Workflow model](#workflow-model)
- [Configuration at a glance](#configuration-at-a-glance)
- [Further reading](#further-reading)

---

### Start here if you're evaluating Cypilot

- **Use it when**
  - you have multi-step work across requirements, design, implementation, validation, and review
  - you want repeatable workflows, stronger validation, and less drift between stages

- **Do not start with it when**
  - the task is a tiny edit, throwaway spike, or open-ended exploration
  - speed matters more than structure and the shape of the work is still unclear

- **Who gets value first**
  - engineers: safer large changes, better validation, less drift
  - architects and leads: clearer design flow, review discipline, and traceability
  - PMs and product-minded readers: cleaner handoffs between requirements, design, and delivery
  - technical writers: more consistent source material and cleaner inputs for writing product and application guides
  - testers and QA: clearer acceptance flow, more structured review, and better visibility into gaps and regression risk

- **Start small first**
  - run 🖥️ `cpt init`
  - run 🖥️ `cpt generate-agents`
  - try 💬 `cypilot analyze: ...` on one existing document or 💬 `cypilot plan: ...` on one large task
  - adopt the SDLC kit, workspaces, and delegation only if you need them

- **Before / after**
  - before: one long chat, drifting documents, fuzzy review, hard-to-track changes
  - after: plan the work, generate in bounded steps, validate deterministically, and review with clearer traceability

### What to expect after setup

After a basic setup, Cypilot gives you a small but concrete operating surface:

- **A project Cypilot directory** with `.core/`, `.gen/`, and `config/`
- **Generated host entry points** for the AI tool you use
- **A portable chat interface** based on 💬 `cypilot <workflow>: ...`
- **A deterministic CLI surface** based on 🖥️ `cpt <command>`

You do **not** need to understand kits, workspaces, delegation, or deeper configuration on day one.

### Where Cypilot helps first

These are the cases where new users usually see value first.

- **Requirements or design into implementation** — move from approved artifacts into code with less drift
- **Large or risky changes** — split work into bounded, inspectable phases
- **Review and validation** — run deterministic checks and structured analysis instead of trusting one generation pass
- **Prompt, workflow, and agent review** — inspect instruction stacks, prompts, and behavioral gaps
- **Brownfield understanding** — understand an existing system before modifying it
- **Multi-repo coordination** — keep artifacts, code, and shared assets aligned across repositories
- **CI-backed quality gates** — use deterministic 🖥️ `cpt` checks in local and pre-merge flows
- **Delegated execution with supervision** — hand off bounded work while keeping validation and human review in the loop

### Prerequisites

For a first trial, the practical minimum is: Python, Git, one supported AI host, and `pipx`.

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
  
  Needed only if you want to use the delegation path through the `cypilot-ralphex` integration or 🖥️ `cpt delegate`.

---

### Quick start

#### 1. Install the CLI

🖥️ **Terminal**:
```bash
pipx install git+https://github.com/cyberfabric/cyber-pilot.git
```

Update later with:

```bash
pipx upgrade cypilot
```

This installs 🖥️ `cpt` globally.

The CLI is a thin entrypoint. On use, it resolves to the cached or project-local Cypilot engine.

Project links:

- **`pipx`**: [pipx.pypa.io](https://pipx.pypa.io/)
- **Homebrew**: [brew.sh](https://brew.sh/)
- **Scoop**: [scoop.sh](https://scoop.sh/)

**macOS note**

If you do not have `pipx` yet, the recommended install path is **Homebrew**:

🖥️ **Terminal**:
```bash
brew install pipx
pipx ensurepath
```

Then open a new terminal, or reload the shell config that `pipx ensurepath` updated.
For example, with the default macOS `zsh` setup:

🖥️ **Terminal**:
```bash
source ~/.zshrc
```

**Windows note**

If you do not have `pipx` yet, the recommended install path is **Scoop**:

🖥️ **Terminal**:
```bash
scoop install pipx
pipx ensurepath
```

Then open a new terminal so the updated `PATH` is picked up.

#### 2. Initialize a project

🖥️ **Terminal**:

```bash
cpt init
cpt generate-agents
```

This creates the Cypilot directory for your project and prepares agent-specific integrations.

For most projects, the default directory is `cypilot/`. In the self-hosted Cyber Pilot repository itself, the equivalent directory is `.bootstrap/`.

🖥️ `cpt init` creates three main areas inside that directory:

| Directory | Purpose | Editable? |
|---|---|---|
| `.core/` | Read-only core workflows, skills, schemas, and requirements | No |
| `.gen/` | Generated aggregate files for agent consumption | No |
| `config/` | Project configuration and installed kit material | Yes |

It also creates `config/core.toml` and `config/artifacts.toml`, defines a root system, and injects the managed root `AGENTS.md` block.

🖥️ `cpt generate-agents` supports: `windsurf`, `cursor`, `claude`, `copilot`, `openai`.

It generates workflow entry points, skill outputs, and subagents where the host tool supports them.

- **Workflow commands** — entry points for `plan`, `generate`, `analyze`, and supported kit workflows
- **Skill outputs** — host-visible Cypilot skill entry points that route into the core instructions
- **Subagents** — isolated task-specific agents where the host supports them

#### 2.5 Update an existing installation

🖥️ **Terminal**:

```bash
cpt update
```

This refreshes `.core/`, regenerates `.gen/`, and updates kit files in `config/kits/` with file-level diffs.

#### 3. Enable Cypilot mode in your AI tool

💬 **AI agent chat**:

```text
cypilot on
```

In practice, this tells the agent to use Cypilot's workflow routing and control layer instead of a generic chat-only interaction style.

#### 4. Start with one of the three main workflows

**Analyze**

💬 **AI agent chat**:

```text
cypilot analyze: review this implementation plan and tell me what is missing or inconsistent
```

**Generate**

💬 **AI agent chat**:

```text
cypilot generate: implement the approved login flow from the current plan and keep the existing behavior outside that scope unchanged
```

**Plan**

💬 **AI agent chat**:

```text
cypilot plan: break this migration into safe implementation phases
```

In hosts where 🖥️ `cpt generate-agents` created slash commands, 💬 `/cypilot-plan`, 💬 `/cypilot-generate`, and 💬 `/cypilot-analyze` are legacy aliases for the same three workflows.

#### 5. What success looks like after 5 minutes

You should now have:

- a Cypilot directory in your project with `.core/`, `.gen/`, and `config/`
- generated host entry points for your AI tool
- a chat workflow that can respond to 💬 `cypilot on`, 💬 `cypilot analyze: ...`, 💬 `cypilot generate: ...`, and 💬 `cypilot plan: ...`

A good first trial is:

- ask 💬 `cypilot analyze: review this plan and tell me what is missing`
- ask 💬 `cypilot plan: break this migration into safe phases`
- ask 💬 `cypilot generate: implement this approved change and keep behavior outside scope unchanged`

For more artifact-specific prompt shapes, use **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

### Host support at a glance

Cypilot works across multiple AI hosts, but not all hosts expose the same control surfaces.

| Host | Best first use | Notes |
|---|---|---|
| Claude Code | Full Cypilot experience | Best support for subagents, isolation, and generation/review separation |
| Cursor | Strong daily-driver IDE | Good general-purpose choice, especially if you want multi-model use |
| GitHub Copilot | Structured assistance and review | Works well, but host-level control is less expressive than Claude Code |
| OpenAI Codex | Bounded analysis and review | Best when tasks stay narrow and validation is explicit |
| Windsurf | Manual separation with Cypilot workflows | Works without subagents; use separate chats for generation and review |

If you are unsure where to start, **Claude Code** is currently the strongest first experience.

For a full support matrix, host-specific guidance, and practical tradeoffs, use **[guides/AGENT-TOOLS.md](guides/AGENT-TOOLS.md)**.

---

## Operating model

### Command surfaces at a glance

The most important thing for a user is that Cypilot adds the **`cypilot` skill** to your AI host.

| Surface | Form | Role |
|---|---|---|
| Primary AI surface | 💬 `cypilot <workflow>: <request>` | Main user-facing skill entry point for routing work into `plan`, `generate`, or `analyze` |
| Terminal surface | 🖥️ `cpt <command>` | Normal CLI surface for deterministic commands such as `init`, `validate`, `update`, and `toc` |
| Legacy chat aliases | 💬 `/cypilot-plan`, 💬 `/cypilot-generate`, 💬 `/cypilot-analyze` | Older host-specific slash aliases that may be generated by 🖥️ `cpt generate-agents` |

If you are unsure what to use in chat, start with the `cypilot` skill and write 💬 `cypilot <workflow>: ...`. Treat slash commands as legacy aliases for the same workflows.

### How to think about Cypilot

Cypilot is best understood as a **deterministic layer around your existing AI tools and workflow**.

- **Use the LLM for**
  - reasoning
  - writing
  - transformation
  - implementation judgment

- **Use Cypilot for**
  - workflow routing
  - context loading
  - templates, rules, and checklists
  - deterministic validation
  - traceability
  - planning large tasks into bounded steps

- **What is deterministic?**
  - config and resource resolution
  - routing into workflows and specialized commands
  - validation of structure, IDs, cross-references, TOC, and traceability rules
  - file-backed plans and repeatable CLI checks

- **What is not deterministic?**
  - the model's reasoning, writing quality, and implementation judgment
  - human review decisions

- **What tradeoff does Cypilot make?**
  - more process and context budget in exchange for more control, auditability, and repeatability

For the full fit / non-fit guidance, practical anti-patterns, planning heuristics, and workflow-choice rules, use **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

### What Cypilot provides

Cypilot has two main parts:

- **Core platform** - the infrastructure and operating model around AI-assisted work
- **Kits** - optional file packages that add domain-specific rules, templates, workflows, and validation material

Most new users should start with the core platform and add a kit later only if they want a ready-made delivery model for a specific domain or way of working.

#### 1. Core platform

At a very high level, the core platform is organized around one agent-facing entry point and a few supporting layers.

- **The `cypilot` skill** - the agent entry point and router, backed by the stdlib-only Python script implementation behind Cypilot. It tells the agent how to resolve 🖥️ `cpt`, when to call deterministic commands, when to open a workflow, which extra methodology files to load for the current task, and remains the source of truth for planning, validation, traceability, config, kits, workspaces, delegation, and generated host entry points.
- **The `cpt` CLI tool** - the thin globally installed launcher. It resolves the cached or project-local Cypilot install and forwards execution to the project-level engine.
- **Workflows** - Markdown procedures for `plan`, `generate`, `analyze` and `workspace`.
- **Methodologies & checklists** - task-specific guidance that the skill loads as needed, including `execution-protocol`, planning requirements, `code-checklist`, `bug-finding`, `prompt-engineering`, `prompt-bug-finding`, `consistency-checklist`, `reverse-engineering`, `workspace`, and `auto-config`.

Use the core platform when you want Cypilot's control layer without committing to any one domain methodology.

#### 2. Kits

Kits are optional. Core Cypilot works without them.

Use a kit when you want a ready-made structured delivery model for a specific domain or workflow.

Kits sit on top of the core platform. They package the domain-specific content that the core itself does not own: document kinds, templates, rules, checklists, examples, constraints, workflows, scripts, and skill content.

The official SDLC kit is one important example. It provides a structured delivery model for requirements, design, decomposition, implementation, and review.

One major part of that kit is a document pipeline for artifacts such as:

- **PRD** *(product requirements)*
- **DESIGN** *(technical design)*
- **ADR** *(architecture decision record)*
- **DECOMPOSITION** *(task breakdown)*
- **FEATURE** *(implementable feature spec)*

This makes structured document-to-document and document-to-code flows practical, while also providing reusable review and validation material around them.

Repository: **[cyberfabric/cyber-pilot-kit-sdlc](https://github.com/cyberfabric/cyber-pilot-kit-sdlc)**

---

### Configuration at a glance

All user-editable configuration lives under `config/` inside your Cypilot directory.

You do not need to understand all of this on day one. Most new users can start with 🖥️ `cpt init`, then use 💬 `cypilot on` and the three workflows, and come back here later.

| File | What it controls |
|---|---|
| `core.toml` | Project settings, installed kits, workspace configuration, and where shared resources resolve from |
| `artifacts.toml` | Registered systems, artifact kinds, codebase paths, and traceability modes |
| `AGENTS.md` | Task-based navigation rules that tell the agent which files to load for which jobs |
| `SKILL.md` | Always-on project-specific instructions that apply across requests |
| `rules/*.md` | Topic-specific rules the agent loads when they are relevant to the task |

To inspect resolved kit resource paths:

🖥️ **Terminal**:

```bash
cpt resolve-vars --flat
```

For full configuration details, see **[Configuration guide](guides/CONFIGURATION.md)**.

---

### Workflow model

Cypilot has three core workflows. Each one has a portable chat form and, in supporting hosts, a generated slash-command alias.

| Workflow | Portable chat form | Generated alias in supporting hosts | Use it when |
|---|---|---|---|
| Plan | 💬 `cypilot plan: ...` | 💬 `/cypilot-plan` | the task is too large, risky, or context-heavy for one conversation |
| Generate | 💬 `cypilot generate: ...` | 💬 `/cypilot-generate` | you want to create, update, implement, or configure something |
| Analyze | 💬 `cypilot analyze: ...` | 💬 `/cypilot-analyze` | you want to validate, review, inspect, compare, or audit |

The portable 💬 `cypilot <workflow>: ...` form is the best default for documentation because the `cypilot` skill is the main cross-host mental model. Slash commands are legacy host-specific aliases for the same workflows, not separate capabilities.

For default routing priorities and detailed workflow-choice advice, use **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

---

### Optional capabilities

You do not need these on day one. Add them when your use case justifies the extra surface area.

#### Multi-repo workspaces

Cypilot supports **multi-repo workspaces** so artifacts, code, and kits do not all have to live in one repository.

Use this when docs, code, or shared kit assets live in separate repos and still need to stay aligned.

For practical guidance, see **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**. For the full model and configuration rules, see **[requirements/workspace.md](requirements/workspace.md)**.

#### RalphEx delegation

RalphEx support is optional.

When available, Cyber Pilot can delegate execution through the dedicated `cypilot-ralphex` path.

Use this when you want bounded execution handoff with supervision rather than only interactive use inside the current host.

For when to delegate and how human review fits, see **[guides/BEST-PRACTICES.md](guides/BEST-PRACTICES.md)**.

#### Project extensibility

Cypilot supports **project-level extensibility**, not just installable kits.

At a high level, 🖥️ `cpt generate-agents` can discover and merge project-defined:

- **skills**
- **agents / subagents**
- **workflows**
- **rules**

This is driven by `manifest.toml` files and a layered resolution model so repo-local definitions can override shared defaults.

For the full manifest model, includes semantics, layer resolution rules, orchestrator repo pattern, and concrete examples, see **[guides/PROJECT-EXTENSIBILITY.md](guides/PROJECT-EXTENSIBILITY.md)**.

---

### FAQ

- **Is Cypilot a replacement for Claude Code, Cursor, Copilot, or another AI host?**

  No. Cypilot sits on top of those hosts and adds routing, context loading, validation, and traceability.

- **When is Cypilot clearly a good fit?**

  Large, risky, multi-step work; structured transformations; repeatable review; brownfield understanding; multi-repo coordination.

- **When should I avoid Cypilot?**

  Tiny edits, loose ideation, throwaway spikes, pure UI exploration, or any task where speed matters more than control.

- **Do I need a kit to use Cypilot?**

  No. Core Cypilot works without kits. The SDLC kit is the easiest way to get a full artifact-first delivery model.

  Start with core. Add a kit only when you want domain templates, rules, and review material.

- **What part is deterministic?**

  Config resolution, workflow routing, validation, TOC checks, ID and traceability checks, and file-backed plans are deterministic. The model's reasoning and generation quality are not.

- **Which host is the best first experience?**

  Claude Code currently provides the highest-fidelity Cypilot experience, especially for subagents and isolation. Other supported hosts still work and may fit different team preferences.

- **When is Cypilot overkill?**

  If one short prompt and one small edit are enough, Cypilot is probably too much process.

- **What is the safest way to start if I am unsure?**

  Run 🖥️ `cpt init`, run 🖥️ `cpt generate-agents`, then try one focused 💬 `cypilot analyze: ...` request.

- **Can I use Cypilot on a brownfield project?**

  Yes. Start with 💬 `cypilot analyze: ...`, use 💬 `cypilot plan: ...` for risky changes, and use 💬 `cypilot auto-config` when you need project-specific rules.

- **Will this help me ship faster?**

  For larger or riskier changes, yes by reducing rework. For tiny tasks, usually no.

- **When should I use `plan` first?**

  When the task spans multiple files, steps, constraints, or review cycles.

- **Is this useful for validation work?**

  Yes. It is good for checklist-based review, consistency checks, and gap finding.

- **Is this good for refactors and migrations?**

  Yes, especially when the work is risky, multi-step, or easy to derail in one long chat.

- **Will this help me understand an unfamiliar codebase?**

  Yes, mainly through focused analysis and bounded planning, not through magic code understanding.

- **Will this help keep requirements, design, and code aligned?**

  Yes. That is one of the strongest reasons to use it.

- **Do I need to use `plan`, `generate`, and `analyze` every time?**

  No. Use only the workflow that matches the job.

- **Can I adopt this gradually?**

  Yes. Start with one workflow and one use case, not the whole system at once.

- **Is this useful if my team already has a process?**

  Yes, if you want that process to be more repeatable inside AI-assisted work.

- **Can this replace testing, code review, or security tooling?**

  No. It strengthens the workflow around those activities; it does not replace specialized tools or human judgment.
 
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

If you think a workflow is unclear, an instruction stack has behavioral bugs, a script behaves incorrectly, or important corner cases are missing, please open a GitHub issue.

- **Issues list:** [github.com/cyberfabric/cyber-pilot/issues](https://github.com/cyberfabric/cyber-pilot/issues)
- **Create a new issue:** [github.com/cyberfabric/cyber-pilot/issues/new/choose](https://github.com/cyberfabric/cyber-pilot/issues/new/choose)

The most useful issue reports usually include:

- **A short summary**
- **Affected file, workflow, script, or command**
- **Expected vs actual behavior**
- **Evidence** such as logs, validator output, screenshots, or minimal prompt slices
- **Environment details** such as OS, host tool, model, and Cypilot version if known

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
