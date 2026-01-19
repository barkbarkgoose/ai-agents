import argparse
import asyncio
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from agents import (
    Agent,
    ModelSettings,
    Runner,
    WebSearchTool,
    set_default_openai_api,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.mcp import MCPServerStdio
from openai.types.shared import Reasoning

# Load .env from the script's directory first (for defaults),
# then from cwd (for project-specific overrides)
SCRIPT_DIR = Path(__file__).parent
load_dotenv(SCRIPT_DIR / ".env", override=False)
load_dotenv(override=True)  # Load from cwd, overriding script defaults

set_default_openai_api(os.getenv("OPENAI_API_KEY"))

# Default to looking for agents/skills in the current working directory
DEFAULT_AGENTS_DIR = Path.cwd() / "agents"
DEFAULT_SKILLS_DIR = Path.cwd() / "skills"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        tuple: (frontmatter dict, remaining content)
    """
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        frontmatter = {}

    return frontmatter, parts[2].strip()


def load_skill_instructions(skill_path: Path) -> str:
    """
    Load skill instructions from a SKILL.md file.

    Returns:
        str: The skill instructions (without frontmatter)
    """
    if not skill_path.exists():
        return ""

    content = skill_path.read_text()
    _, instructions = parse_frontmatter(content)

    return instructions


def discover_agents(agents_dir: Path, skills_dir: Path) -> dict[str, dict]:
    """
    Discover all available agents from the agents directory.

    Returns:
        dict: Mapping of agent name to agent config
    """
    agents = {}

    if not agents_dir.exists():
        return agents

    for agent_file in agents_dir.glob("*.md"):
        content = agent_file.read_text()
        frontmatter, body = parse_frontmatter(content)

        if not frontmatter.get("name"):
            continue

        agent_name = frontmatter["name"]

        # Try to find and load the skill file
        skill_path = skills_dir / agent_name / "SKILL.md"
        skill_instructions = load_skill_instructions(skill_path)

        agents[agent_name] = {
            "name": agent_name,
            "model": frontmatter.get("model", "gpt-5"),
            "description": frontmatter.get("description", ""),
            "readonly": frontmatter.get("readonly", False),
            "instructions": skill_instructions or body,
            "file_path": str(agent_file),
            "skill_path": str(skill_path) if skill_path.exists() else None,
        }

    return agents


def create_agent_from_config(
    config: dict,
    codex_mcp_server,
    include_web_search: bool = False,
) -> Agent:
    """
    Factory function to create an Agent from a config dict.
    """
    tools = []
    if include_web_search:
        tools.append(WebSearchTool())

    return Agent(
        name=config["name"],
        instructions=(
            f"{RECOMMENDED_PROMPT_PREFIX}\n\n"
            f"{config['instructions']}\n\n"
            "When creating or modifying files, call Codex MCP with "
            '{\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}.'
        ),
        model=config.get("model", "gpt-5"),
        tools=tools if tools else None,
        mcp_servers=[codex_mcp_server],
    )


def build_agent_registry_prompt(agents: dict[str, dict]) -> str:
    """
    Build a prompt section describing all available agents.
    """
    lines = ["## Available Agents\n"]

    for name, config in agents.items():
        desc = config.get("description", "No description")
        lines.append(f"- **{name}**: {desc}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a multi-agent workflow with Codex CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
            python multi_agent_example.py "Build a todo app with Vue 3 and a Django backend"
            python multi_agent_example.py "Get instructions from task.md"
            python multi_agent_example.py "Use multi-agent-orchestrator to add dark mode toggle"
            python multi_agent_example.py --file requirements.txt
            python multi_agent_example.py --list-agents
        """,
    )

    parser.add_argument(
        "prompt",
        nargs="?",
        help="Natural language prompt describing what to build",
    )

    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Path to a file containing the task description",
    )

    parser.add_argument(
        "--agents-dir",
        type=str,
        default=None,
        help="Directory containing agent definition files (default: ./agents)",
    )

    parser.add_argument(
        "--skills-dir",
        type=str,
        default=None,
        help="Directory containing skill definition files (default: ./skills)",
    )

    parser.add_argument(
        "--list-agents",
        action="store_true",
        help="List all available agents and exit",
    )

    return parser.parse_args()


def get_task_prompt(args: argparse.Namespace) -> str:
    """
    Get the task prompt from command-line args.
    Priority: --file flag > positional prompt argument > interactive input
    """
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)

        with open(args.file, "r") as f:
            return f.read()

    if args.prompt:
        return args.prompt

    print("No prompt provided. Enter your task description (Ctrl+D when done):")
    return sys.stdin.read().strip()


async def main(
    task_prompt: str,
    *,
    agents_dir: Path = DEFAULT_AGENTS_DIR,
    skills_dir: Path = DEFAULT_SKILLS_DIR,
) -> None:
    # Discover available agents
    available_agents = discover_agents(agents_dir, skills_dir)

    if not available_agents:
        print(f"Warning: No agents found in {agents_dir}")
        print("The PM will operate with default built-in agents.")

    # Build the agent registry for the PM's context
    agent_registry_prompt = build_agent_registry_prompt(available_agents)

    async with MCPServerStdio(
        name="Codex CLI",
        params={"command": "npx", "args": ["-y", "codex", "mcp"]},
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:

        # Create agents from discovered configs
        created_agents: dict[str, Agent] = {}

        for name, config in available_agents.items():
            # Determine if this agent should have web search
            # (e.g., designer, research-oriented agents)
            include_web_search = "design" in name.lower() or "research" in name.lower()

            created_agents[name] = create_agent_from_config(
                config,
                codex_mcp_server,
                include_web_search=include_web_search,
            )

        # Create the Project Manager agent
        project_manager_agent = Agent(
            name="Project Manager",
            instructions=(
                f"{RECOMMENDED_PROMPT_PREFIX}\n"
                """
                You are the Project Manager and Orchestrator for a multi-agent coding workflow.

                Your job is to:
                1. Analyze the user's request
                2. Determine which agents are needed from the available roster
                3. Create task files and coordinate handoffs between agents
                4. Ensure work is completed in the correct order

                """
                f"{agent_registry_prompt}"
                """

                ## Process

                1. **Analyze the Request**
                   - If the user prompt references a file (e.g., "get instructions from task.md"), read that file first using Codex MCP.
                   - If the user mentions a specific orchestrator or workflow (e.g., "use multi-agent-orchestrator"), load and follow that agent's instructions.
                   - Determine which agents are needed based on the work required.

                2. **Create Planning Documents** (write in project root):
                   - REQUIREMENTS.md: concise summary of product goals, target users, key features, and constraints.
                   - AGENT_TASKS.md: one section per agent containing:
                     - Required deliverables (exact file names and purpose)
                     - Key technical notes and constraints
                     - Dependencies on other agents' work

                3. **Coordinate Handoffs**
                   - Hand off to agents in the correct order based on dependencies
                   - Wait for each agent to complete before proceeding to dependent work
                   - Verify deliverables exist before advancing

                ## Rules
                - Resolve ambiguities with minimal, reasonable assumptions
                - Create files using Codex MCP with {"approval-policy":"never","sandbox":"workspace-write"}
                - Do NOT respond with status updates. Just handoff to the next agent until the project is complete.
                - If an agent is not in the available roster, note this and proceed with available agents.

                ## Agent Selection Guidelines
                - Backend work (APIs, models, business logic) → django-backend-dev or backend-focused agents
                - Frontend work (UI, components, state) → vue3-typescript or frontend-focused agents
                - Styling work (CSS, Tailwind, visual design) → tailwind-bem-stylist or styling agents
                - If unsure which agent to use, check the agent descriptions above
                """
            ),
            model="gpt-5",
            model_settings=ModelSettings(
                reasoning=Reasoning(effort="medium"),
            ),
            handoffs=list(created_agents.values()) if created_agents else [],
            mcp_servers=[codex_mcp_server],
        )

        # Set up bidirectional handoffs
        for agent in created_agents.values():
            agent.handoffs = [project_manager_agent]

        result = await Runner.run(project_manager_agent, task_prompt, max_turns=30)
        print(result.final_output)


if __name__ == "__main__":
    args = parse_args()

    # Use provided paths or fall back to defaults (cwd-relative)
    agents_dir = Path(args.agents_dir) if args.agents_dir else DEFAULT_AGENTS_DIR
    skills_dir = Path(args.skills_dir) if args.skills_dir else DEFAULT_SKILLS_DIR

    # Handle --list-agents
    if args.list_agents:
        available = discover_agents(agents_dir, skills_dir)

        if not available:
            print(f"No agents found in {agents_dir}")
            sys.exit(0)

        print("Available Agents:\n")
        for name, config in available.items():
            print(f"  {name}")
            print(f"    Model: {config.get('model', 'default')}")
            print(f"    Description: {config.get('description', 'N/A')}")
            if config.get("skill_path"):
                print(f"    Skill: {config['skill_path']}")
            print()

        sys.exit(0)

    task_prompt = get_task_prompt(args)

    if not task_prompt:
        print("Error: No task prompt provided.")
        sys.exit(1)

    print(f"Starting multi-agent workflow with prompt:\n{task_prompt}\n")
    asyncio.run(main(task_prompt, agents_dir=agents_dir, skills_dir=skills_dir))
