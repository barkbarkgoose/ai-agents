# AI Agents & Skills

A skill-first collection of AI agents and skills for **OpenCode** (and Kilo via OpenCode compatibility). This repository serves as both a working configuration and a template for setting up your own AI-assisted development workflows.

---

## What Are Agents and Skills?

Modern AI coding assistants can be extended with custom instructions that guide their behavior for specific tasks. Different tools call these extensions different things, but in this repository we treat:

- **Agents** — top-level personas the user picks as their main mode (advisor, orchestrator, research, etc.).
- **Skills** — reusable instruction sets that any agent can load for a specific domain (Django, Vue, Tailwind, etc.).

Agents are intentionally small. Specialized behavior lives in skills so multiple agents can share the same expertise.

---

## Quick Start

### 1. Clone the Repository

```bash
git clone git@github.com:barkbarkgoose/ai-agents.git
cd ai-agents
```

### 2. Run the Sync Script

The sync script copies agents, commands, and skills to your OpenCode-compatible home directories:

```bash
chmod +x sync.sh
./sync.sh
```

This syncs the shared `./agents`, `./commands`, and `./skills` to:
- `~/.config/opencode/` — read by stock OpenCode.
- `~/.config/kilo/` — read by Kilo (Kilo's XDG global root, distinct from `~/.config/opencode/`).

**Note:** The sync only touches the `agents/`, `commands/`, and `skills/` subdirectories.

### 3. Verify Installation

- **OpenCode**: Run `opencode` and check that agents are available via `/agents` or `Ctrl+P`.
- **Kilo**: Run `kilo`. Kilo reads `~/.config/kilo/` as its XDG global root (not `~/.config/opencode/`).

---

## Repository Structure

```
ai-agents/
├── agents/                    # Agent definitions
│   ├── advisor.md             # Ask-only advisor (no writes)
│   ├── research.md            # Research agent (delegates to gemini-researcher skill)
│   ├── small-model-orchestrator.md  # Smart orchestrator
│   └── small-subagent.md      # Implementation subagent
├── commands/                  # Custom slash commands (reserved)
├── skills/                    # Skill definitions
│   └── <skill-name>/
│       └── SKILL.md
├── agent-frontmatter/         # Harness-specific frontmatter templates
├── docs/                      # Documentation
├── sync.sh                    # Deployment script
└── README.md                  # You are here
```

---

## Agents

| Agent | Mode | Model | Purpose |
|-------|------|-------|---------|
| `advisor` | primary | `openai/gpt-5.4` | Ask-only questions, design discussion, debugging advice. No writes/edits. |
| `research` | subagent | (defaults) | Conducts external research using the `gemini-researcher` skill. |
| `small-model-orchestrator` | primary | `openai/gpt-5.5` | Plans work and delegates all writes/edits to `small-subagent`. Reviews each phase and spawns follow-up tasks for corrections. |
| `small-subagent` | subagent | `lmstudio/gemma-4-26b` | Performs scoped edits, traces imports/usages, reports back. |

### Smart Orchestrator Workflow

The `small-model-orchestrator` follows this loop for every implementation request:

1. **Plan** the change set, files, and validation steps.
2. **Spawn** a `small-subagent` task with precise, scoped instructions.
3. **Review** the diff and changed files itself.
4. If correct, summarize what changed and validation results.
5. If adjustments are needed, **spawn another `small-subagent`** with concrete correction instructions.

The orchestrator never writes or edits files directly.

---

## How It Works

### The Sync Workflow

```
┌─────────────────────┐         ┌─────────────────────┐
│   This Repository   │         │   Home Directory    │
│                     │         │                     │
│  ./skills/          │ ──────► │  ~/.<harness>/skills/  │
│  ./commands/        │ ──────► │  ~/.<harness>/commands/│
│  ./agents/          │ ──────► │  ~/.<harness>/agents/  │
│                     │         │                     │
└─────────────────────┘         └─────────────────────┘
        Edit here                   Used by AI tools
```

1. **Edit** agents and skills in this repository
2. **Commit** changes to version control
3. **Run** `./sync.sh` to deploy to your home directory
4. **Use** the updated agents in your AI tools

---

## Documentation

- **[Agent Setup Guide](docs/AGENT_SETUP_GUIDE.md)** - OpenCode/Kilo + oh-my-pi setup details, frontmatter requirements, and file structures.
- **[Writing Useful Agents](docs/WRITING_USEFUL_AGENTS.md)** - How to write agents and skills that actually work.
- **[LLM Agent Context Limitations](docs/llm-agent-context-limitations.md)** - Why self-contained prompts beat modular file chains.
- **[Running Local Models](docs/LOCAL_MODELS.md)** - Set up llama.cpp / LM Studio with OpenCode-compatible CLIs.

---

## Troubleshooting

### Agents not appearing

1. Verify the sync completed: `./sync.sh`
2. Check file permissions: `ls -la ~/.config/opencode/agents/ ~/.config/kilo/agents/`
3. Restart your AI tool
4. Verify frontmatter syntax (YAML is whitespace-sensitive)

### Sync script errors

- Ensure `rsync` is installed: `which rsync`
- Check directory permissions
- Run with verbose output to debug: `bash -x sync.sh`

---

## Resources

- [OpenCode Documentation](https://opencode.ai/docs)
- [Kilo Documentation](https://kilo.ai/docs)
- [oh-my-pi](https://github.com/oh-my-pi)
