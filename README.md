# AI Agents & Skills

A collection of reusable AI agents and skills for **Cursor**, **Claude Code**, and **Gemini CLI**. This repository serves as both a working configuration and a template for setting up your own AI-assisted development workflows.

---

## What Are Agents and Skills?

Modern AI coding assistants can be extended with custom instructions that guide their behavior for specific tasks. Different tools call these extensions different things:

| Tool | Extension Type | Purpose |
|------|---------------|---------|
| **Cursor** | Skills | Specialized instruction sets that guide the AI for specific tasks |
| **Claude Code** | Agents | Standalone task handlers with defined tools and capabilities |
| **Gemini CLI** | Both | Supports both agents (standalone) and skills (composable) |

**Think of them as:**
- A senior developer's expertise, packaged into reusable instructions
- Guardrails that keep the AI focused on your team's patterns and standards
- Specialized "modes" the AI can switch into for different types of work

---

## Quick Start

### 1. Clone the Repository

```bash
git clone git@github.com:barkbarkgoose/ai-agents.git
cd ai-agents
```

### 2. Run the Sync Script

The sync script copies agents and skills to the appropriate locations in your home directory:

```bash
chmod +x sync.sh
./sync.sh
```

This syncs:
- `./cursor/` → `~/.cursor/` (agents, commands, skills)
- `./claude/` → `~/.claude/` (agents, commands, skills)
- `./gemini/` → `~/.gemini/` (agents, commands, skills)

**Note:** The sync only touches the `agents/`, `commands/`, and `skills/` subdirectories. Other files in your home directories (like `~/.cursor/plans/`) remain untouched.

### 3. Verify Installation

- **Cursor**: Open Cursor and check that skills appear in the skills panel
- **Claude Code**: Run `claude` and verify agents are available
- **Gemini CLI**: Run `gemini` and check for available agents/skills

---

## Repository Structure

```
ai-agents/
├── cursor/                    # Cursor IDE configurations
│   ├── agents/               # (Reserved for future use)
│   ├── commands/             # Custom slash commands
│   └── skills/               # Skill definitions
│       └── <skill-name>/
│           └── SKILL.md
│
├── claude/                    # Claude Code configurations
│   ├── agents/               # Agent definitions
│   │   └── <agent-name>.md
│   ├── commands/             # (Reserved for future use)
│   └── skills/               # Skill definitions
│       └── <skill-name>/
│           └── SKILL.md
│
├── gemini/                    # Gemini CLI configurations
│   ├── agents/               # Agent definitions
│   │   └── <agent-name>.md
│   ├── commands/             # (Reserved for future use)
│   └── skills/               # Skill definitions
│       └── <skill-name>/
│           └── SKILL.md
│
├── docs/                      # Documentation
│   ├── AGENT_SETUP_GUIDE.md  # Provider-specific setup details
│   └── WRITING_USEFUL_AGENTS.md  # How to write effective agents
│
├── sync.sh                    # Deployment script
└── README.md                  # You are here
```

---

## How It Works

### The Sync Workflow

```
┌─────────────────────┐         ┌─────────────────────┐
│   This Repository   │         │   Home Directory    │
│                     │         │                     │
│  cursor/skills/     │ ──────► │  ~/.cursor/skills/  │
│  cursor/commands/   │ ──────► │  ~/.cursor/commands/│
│  claude/agents/     │ ──────► │  ~/.claude/agents/  │
│  gemini/agents/     │ ──────► │  ~/.gemini/agents/  │
│  gemini/skills/     │ ──────► │  ~/.gemini/skills/  │
│                     │         │                     │
└─────────────────────┘         └─────────────────────┘
        Edit here                   Used by AI tools
```

1. **Edit** agents and skills in this repository
2. **Commit** changes to version control
3. **Run** `./sync.sh` to deploy to your home directory
4. **Use** the updated agents in your AI tools

This approach lets you:
- Version control your AI configurations
- Share configurations across machines
- Collaborate with teammates on agent improvements
- Keep a clean separation between "source" and "deployed" configs

---

## Agentic loops

Agents in this collection, as an example, use a centralized `.agent-info/` directory structure for task tracking and audit outputs. This convention works across all platforms (Cursor, Claude, Gemini).

### Directory Structure

When running agent loops it's a good idea to have a task queuing system in place.  This _could_ help the AI by breaking down tasks and keeping context windows clean; but it also makes it easier to keep track of what the AI is doing as the human developer.

```
<your-project>/.agent-info/
├── tasks/
│   ├── pending/          # Tasks waiting to be picked up
│   ├── in_progress/      # Currently being worked on
│   └── done/             # Completed tasks
└── audits/
    └── TAILWIND_AUDIT.md # Audit reports
```

### How It Works

1. **Multi-Agent Orchestrator** breaks down complex requests into discrete task files
2. Each task file is placed in `.agent-info/tasks/pending/`
3. Sub-agents (django, vue3, tailwind) pick up tasks and move them through the workflow
4. Audit agents (like tailwind-css-auditor) output reports to `.agent-info/audits/`

### Task File Format

Each task is a descriptively-named markdown file (e.g., `add-user-dashboard-api.md`) containing:
- Target agent/skill
- Goal and acceptance criteria
- Context and dependencies
- Expected outputs
- Ready-to-run prompt

### Benefits

- **Cross-platform**: Works with Cursor, Claude Code, Gemini CLI, etc.
- **Session continuity**: Pick up where you left off across chat sessions
- **Parallel work**: Multiple agents can work on different tasks
- **Audit trail**: Clear history of what was done and why

---

## Documentation

For detailed guides on creating and managing agents:

- **[Agent Setup Guide](docs/AGENT_SETUP_GUIDE.md)** - Provider-specific setup instructions, frontmatter requirements, file structures, and migration tips between providers
- **[Writing Useful Agents](docs/WRITING_USEFUL_AGENTS.md)** - How to write agents that actually work: what to include, code examples, boundaries, and a quick checklist

---

## Troubleshooting

### Agents not appearing

1. Verify the sync completed: `./sync.sh`
2. Check file permissions: `ls -la ~/.cursor/skills/`
3. Restart your AI tool
4. Verify frontmatter syntax (YAML is whitespace-sensitive)

### Agent not being selected

- Make the `description` more specific
- Add `<example>` tags (Claude/Gemini) to help with selection
- Check that the description matches your actual use case

### Sync script errors

- Ensure `rsync` is installed: `which rsync`
- Check directory permissions
- Run with verbose output to debug: `bash -x sync.sh`

---

## Resources

- [Cursor Documentation](https://docs.cursor.com/)
- [Claude Code Documentation](https://code.claude.com/docs)
- [Gemini CLI Repository](https://github.com/google-gemini/gemini-cli)