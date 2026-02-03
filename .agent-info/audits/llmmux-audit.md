# llmmux Audit Report

## 1) Scope and Assumptions

**What was reviewed:**
- README.md documentation
- orchestrator.py (380 lines, ~1 main script)
- create_agent.py (381 lines, ~1 spawner script)
- INIT_ORCHESTRATOR.md (bootstrap instructions)
- Directory structure and file organization

**Assumptions:**
- The system is intended to be a production-ready multi-agent orchestration platform
- Users are expected to manage agent lifecycle through tmux manually
- State persistence is critical for agent coordination
- The system targets multiple LLM providers (Cursor, Claude, Gemini, Codex, OpenCode)

**Out of scope:**
- Actual provider CLI implementations
- Network/API integration patterns
- Security hardening (assumes trusted environment)

---

## 2) Over-Complexity Findings

### A. Excessive Setup Layers
**Evidence from README (lines 11-19):**
```
1. Sync to Home Directory
./sync.sh copies llmmux files to ~/.llmmux/ and sets up a Python virtual environment
```
**Issue:** Three separate setup concepts (sync.sh, ~/.llmmux/, venv) before a single command runs. Adds cognitive load.

**Severity:** Medium - Could be simplified to single bootstrap step.

---

### B. Redundant Configuration Management
**Evidence from README (lines 90-109) and code:**
- `.default_env` (system-wide defaults)
- `.env` (user overrides)
- Environment variable layering in both `orchestrator.py` (lines 65-79) and `create_agent.py` (lines 26-35)
- Custom `PROVIDER_<name>` templating (orchestrator.py lines 232-252, create_agent.py lines 219-239)

**Issue:** Four independent configuration concepts with identical logic duplicated in two files. The provider command templating pattern is particularly brittle:
```python
template = os.getenv(env_key)
if not template:
    defaults = {  # Fallback embedded defaults
        "gemini": "gemini -p '{prompt}'",
        "agent": "agent '{prompt}'",
        ...
    }
```

**Severity:** High - Violates DRY principle, maintenance nightmare.

---

### C. Overly Complex State Management Design
**Evidence from INIT_ORCHESTRATOR.md (lines 67-221):**
- 5 required JSON/markdown state files per session
- Complex nested structure (run_state.json has agents dict with nested objects, constraints, artifact tracking)
- Undefined semantics: `run_state.json` is described as "compact" yet contains deeply nested agent objects with 6 fields each
- The "pointers" concept (reference files with line numbers) is error-prone and unmaintained

**Issue:** State management is theoretically comprehensive but implementation is incomplete:
- No code in `orchestrator.py` or `create_agent.py` actually creates these state files
- No validation or schema enforcement
- No state sync mechanism between agents

**Severity:** High - Design assumes state management that isn't actually implemented.

---

### D. Duplicate User Interaction Logic
**Evidence from code:**
- `get_provider()` appears in both scripts (orchestrator.py lines 169-229, create_agent.py lines 135-167)
- `get_session_name()` duplicated (orchestrator.py lines 148-155, create_agent.py lines 77-120)
- `get_provider_command()` duplicated (orchestrator.py lines 232-252, create_agent.py lines 219-239)

**Issue:** 70+ lines of identical I/O and validation logic in two scripts. Changes to provider handling require edits in both places.

**Severity:** Medium - Code maintenance hazard.

---

### E. Questionable Architecture Decisions
**Evidence from README (lines 126-135):**
```
tmux Basics
Quick commands:
- Ctrl+b w - List and switch windows
- Ctrl+b n - Next window
...
```

**Issue:** Users must learn tmux keybindings to use the system. This is a dependency on manual terminal management that could be abstracted. The README includes a full tmux cheatsheet, suggesting the complexity is expected to leak into user workflows.

**Severity:** Medium - Increases learning curve; not necessarily wrong but adds friction.

---

## 3) Missing Functionality

### A. State File Generation is Not Implemented
**Evidence from code:**
- INIT_ORCHESTRATOR.md (lines 25-28) specifies state files must be initialized
- `orchestrator.py` creates only directories (lines 274 onwards) but never writes `handoff.md`, `run_state.json`, or `tasks.json`
- `create_agent.py` creates only `{agent_name}.last.json` (lines 282-298), not the session-level state files

**Impact:** State management design is documented but not enforced. Agents run without state tracking.

**Severity:** Critical - Core functionality is missing.

---

### B. No Agent Lifecycle Management
**Evidence from README and code:**
- Only spawn and view commands are implemented
- No monitoring of agent status (agents just run in tmux windows)
- No automatic logging capture to `~/.llmmux/logs/`
- No error handling or failure detection
- No cleanup mechanism (users must manually `tmux kill-session`)

**Impact:** Users cannot inspect agent health, no persistent record of execution.

**Severity:** High - System degrades to "fire and forget."

---

### C. No Inter-Agent Communication
**Evidence from INIT_ORCHESTRATOR.md (lines 235-257):**
- Bootstrap says orchestrator should "create agents sequentially" and "respecting dependencies"
- No mechanism for agents to signal completion
- No handoff protocol between windows
- No message queue or IPC layer

**Issue:** Orchestrator is instructed to wait for agents, but code provides no way to detect this.

**Severity:** High - Breaks the multi-agent coordination promise.

---

### D. No Skill System Implementation
**Evidence from README (lines 111-124):**
- Extensive documentation of skills in provider-specific directories
- `create_agent.py` has `--skill` parameter (lines 349-352) that attempts to locate skill files
- Skill resolution is naive (lines 178-193):
  ```python
  for skill_dir in provider_dirs:
      skill_file = skill_dir / "SKILL.md"
      if skill_file.exists():
          return f"refer to skill: {skill_file}"
  ```

**Issue:** Skills are never validated, resolved in any priority order, or templated into the prompt. The `refer to skill: /path/to/SKILL.md` string is passed directly to the LLM—no guarantee it exists or is in the right format.

**Severity:** High - Skill system is documented but barely functional.

---

### E. No Provider Validation or Discovery
**Evidence from code:**
- Hardcoded provider list: `["gemini", "agent", "codex", "claude", "opencode"]`
- No detection of which providers are actually installed
- No fallback or graceful degradation if a provider CLI is missing
- Comments in README (line 261) warn about Gemini limitations but no code handles this

**Impact:** Users may launch agents with unavailable providers, causing silent failures.

**Severity:** Medium - Reliability issue.

---

### F. No Session Isolation or Resource Limits
**Evidence from code and README:**
- No limits on number of agents per session
- No CPU/memory constraints
- No tmux window limits
- No cleanup of orphaned sessions

**Impact:** Runaway agent spawning could consume system resources.

**Severity:** Low - Not critical but good for production readiness.

---

## 4) Recommendations (Prioritized)

### Priority 1: Fix Critical Gaps (Must Fix)

**1.1 Implement State File Generation**
- Add `initialize_session_state()` function called in `orchestrator.py:launch_orchestrator_session()`
- Generate all three state files: `handoff.md`, `run_state.json`, `tasks.json`
- Schema: Define JSON schemas for validation (use jsonschema library)
- Estimated effort: 2-3 hours

**1.2 Extract Shared Utilities Module**
- Create `~/.llmmux/utils.py` or `~/.llmmux/llmmux_core.py`
- Move to single location:
  - Provider command generation
  - Configuration loading
  - Session/provider resolution
  - Interactive prompting (if keeping interactive mode)
- Both scripts import from core module
- Benefit: DRY principle, single source of truth for provider handling
- Estimated effort: 1-2 hours

**1.3 Implement Agent Status Tracking**
- Create `get_agent_status(session_name, agent_name)` that reads from tmux
- Update `run_state.json` when agents complete (via periodic check or wrapper script)
- Add `--wait` flag to `create_agent.py` to optionally block until agent completes
- Estimated effort: 2-3 hours

---

### Priority 2: Improve Reliability (Should Fix)

**2.1 Add Provider Detection**
- At startup, verify provider CLIs exist in PATH
- Warn user if provider is misconfigured
- Provide installation instructions
- Estimated effort: 1 hour

**2.2 Robust Skill Resolution**
- Validate skill files exist before using
- Allow skill override via environment (`SKILL_<name>` pointing to custom SKILL.md)
- Fall back to generic prompt if skill not found
- Estimated effort: 1 hour

**2.3 Automated Log Capture**
- Wrap agent commands in script that pipes output to `~/.llmmux/logs/<session>/<agent>.log`
- Make log paths configurable
- Estimated effort: 1-2 hours

---

### Priority 3: Simplify Setup (Nice to Have)

**3.1 Single Bootstrap Command**
- Replace multi-step setup with single command: `llmmux-init`
- This command: checks deps, creates dirs, installs to ~/.llmmux, sets up venv, done.
- Remove sync.sh entirely
- Estimated effort: 1-2 hours

**3.2 CLI Restructure**
- Instead of two separate scripts, consider single `llmmux` command with subcommands:
  ```
  llmmux orchestrator --provider agent
  llmmux agent create --name vue --skill vue3-typescript
  llmmux session list
  llmmux session attach <name>
  ```
- Reduces cognitive load on users
- Estimated effort: 4-5 hours (medium refactor)

**3.3 Reduce tmux Complexity**
- Add convenience wrapper: `llmmux attach [session]` instead of requiring users to know `tmux attach -t`
- Add `llmmux list-agents` to show windows without tmux knowledge
- Document tmux basics separately (as reference, not primary usage path)
- Estimated effort: 2-3 hours

---

### Priority 4: Documentation Alignment (Low Effort, High Value)

**4.1 Update README with Caveats**
- Explicitly state which documented features are not yet implemented
- Example: "State management design is documented but not yet active"
- Add roadmap section
- Estimated effort: 30 min

**4.2 Remove/Update INIT_ORCHESTRATOR.md**
- Current version over-promises on state management
- Either implement state features or tone down documentation
- Consider splitting into: "design spec" vs. "implemented features"
- Estimated effort: 1 hour

---

## Summary Table

| Issue | Severity | Category | Effort |
|-------|----------|----------|--------|
| State generation not implemented | Critical | Missing | 2-3h |
| Configuration/logic duplication | High | Complexity | 1-2h |
| No agent status tracking | High | Missing | 2-3h |
| Complex state design with no enforcement | High | Complexity | Partially covered by fixes |
| No inter-agent communication | High | Missing | 3-5h |
| Skill system incomplete | High | Missing | 1h |
| Duplicate user I/O logic | Medium | Complexity | Covered by utils extraction |
| No provider validation | Medium | Missing | 1h |
| Excessive setup layers | Medium | Complexity | 1-2h |
| Tmux dependency complexity | Medium | Architecture | 2-3h |

---

## Overall Assessment

**Current State:** Prototype-grade. The architecture is sound, but implementation is incomplete. Documentation over-promises on state management, inter-agent coordination, and lifecycle features that aren't actually implemented.

**Recommendation:** Before promoting to production, prioritize:
1. State file generation (make state management real)
2. Shared utilities module (eliminate duplication)
3. Agent status tracking (enable monitoring)
4. Provider validation (improve reliability)

The remaining issues are polish and simplification. The system is usable as-is for simple single-agent tasks, but multi-agent coordination will not work as documented.

**Estimated Total Effort for Priority 1+2:** 10-15 hours of development would move this from prototype to stable beta.
