# What makes an agent...

A practical guide to writing effective agents that actually work. Focus on clarity, specificity, and maintainability.

**Philosophy:** Start simple, expand through friction. You have to maintain this, so be deliberate about what you include.

---

## Table of Contents

- [1 - Commands](#1---commands)
- [2 - Project Structure](#2---project-structure)
- [3 - Tech Stack](#3---tech-stack)
- [4 - Code Style](#4---code-style)
- [5 - Git Workflow](#5---git-workflow)
- [6 - Boundaries](#6---boundaries)
- [Tips for Effective Agents](#tips-for-effective-agents)

---

## 1 - Commands

Put actual executable commands early in the file. The agent should know exactly what to run.

**What to include:**
- How to run tests
- How to start a development server
- How to build/compile
- How to run linters or formatters
- Any scripts specific to the project

**Example:**

```bash
# Testing
npm test                           # Run all tests
npm test -- --watch               # Watch mode
npm run test:coverage             # With coverage

# Development
npm run dev                        # Start dev server (http://localhost:3000)
npm run build                      # Production build
npm run lint                       # Run ESLint
npm run format                     # Fix formatting with Prettier
```

**Pro tip:** Include the expected output or where to find results. E.g., "Coverage report opens in `coverage/index.html`"

---

## 2 - Project Structure

Give the AI a map of the codebase. Be concise — only relevant directories.

**What to include:**
- Top-level folders and what they contain
- Key file locations the agent might need to modify or read
- Any non-obvious structure that would confuse someone new

**Don't include:**
- `node_modules/`, `.git/`, build artifacts
- Every single file—just the important ones

**Example:**

```
src/
├── components/          # React/Vue components
│   ├── common/         # Shared, reusable components
│   ├── layouts/        # Page layout wrappers
│   └── features/       # Feature-specific components
├── pages/              # Route handlers / page components
├── utils/              # Helper functions and utilities
├── types/              # TypeScript types (if applicable)
├── styles/             # Global styles, theme definitions
└── assets/             # Images, fonts, static files

tests/                  # Test files (mirror src/ structure)

docs/                   # Documentation
config/                 # Build and tool configs
```

**Pro tip:** Include a brief note about naming patterns in directories. E.g., "Feature components nest their own styles in a `styles.ts` file."

---

## 3 - Tech Stack

**Be specific with versions.** Generics like "React" don't help. "React 18.2.0" does.

**What to include:**
- Runtime/framework + version
- Key libraries + versions
- Build tooling + version
- Testing framework + version
- Language/compiler + version (TypeScript, Babel, etc.)
- Any critical plugins or integrations

**Format:**

```
- **Runtime:** Node.js 18.17.0
- **Frontend:** React 18.2.0 + TypeScript 5.1.6
- **Build:** Vite 4.4.0 with SWC transpiler
- **Styling:** Tailwind CSS 3.3.0
- **Testing:** Vitest 0.34.0 + React Testing Library 14.0.0
- **Linting:** ESLint 8.46.0
- **Formatting:** Prettier 3.0.0
- **Package Manager:** npm 9.8.1
```

**Why it matters:** The agent needs to know if it should write `.jsx` or `.tsx`, whether to use CommonJS or ES modules, whether type hints are available, etc.

---

## 4 - Code Style

**Show, don't tell.** One real code example beats three paragraphs.

Pick one example from the actual codebase for each category:

### Naming Conventions

```typescript
// Component names: PascalCase
const UserProfileCard = () => {};

// Functions: camelCase
const calculateTotalPrice = () => {};

// Constants: UPPER_SNAKE_CASE
const MAX_RETRIES = 3;

// Classes: PascalCase
class APIClient {}

// CSS classes (BEM): kebab-case with modifiers
// .button__primary--disabled
```

### Error Handling Patterns

Show real error handling from the codebase:

```typescript
// Standard pattern: try-catch with specific error types
async function fetchUser(id: string) {
  try {
    const response = await api.get(`/users/${id}`);

    return response.data;
  } catch (error) {
    if (error instanceof APIError) {
      console.error(`API error: ${error.message}`);

      throw new AppError('Failed to fetch user', { cause: error });
    }

    throw error;
  }
}
```

### Function Structure

Show how functions are typically organized:

```typescript
/**
 * Validates and processes user input.
 * 
 * @param input - The raw user input
 * @returns Processed and validated data
 * @throws ValidationError if input is invalid
 */
function processUserInput(input: unknown): ProcessedData {
  // 1. Type guard / validation
  if (!isValidInput(input)) {
    throw new ValidationError('Invalid input format');
  }

  // 2. Transform
  const transformed = transform(input);

  // 3. Enrich (if needed)
  const enriched = await enrichWithDefaults(transformed);

  // 4. Return
  return enriched;
}
```

### Import/Export Style

```typescript
// Preferred: Named imports on single line if <= 3
import { useState, useCallback } from 'react';

// Multi-line for 4+ imports
import {
  useState,
  useCallback,
  useEffect,
  useRef,
} from 'react';

// Export: Prefer named exports
export function MyComponent() {}
export const helper = () => {};

// Avoid default exports unless necessary
```

---

## 5 - Git Workflow

Include this **only if agents create branches and PRs.** If they don't, skip it.

**What to include:**
- Branch naming convention
- Commit message format
- PR requirements (squash? rebase? reviews?)
- When to use each

**Example:**

```
## Branch Naming
- Feature: feature/short-description
- Bug fix: fix/bug-name
- Refactor: refactor/what-changed
- Docs: docs/what-docs

Pattern: {type}/{short-description-kebab-case}

## Commit Messages
Format: {type}: {description}

Types: feat, fix, docs, refactor, test, chore, style
Example: "feat: add user profile card component"

## Pull Requests
- Squash commits on merge (one clean commit per PR)
- Require at least 1 approval before merging
- Run linters and tests before submitting
- Link related issues in the PR description
```

---

## 6 - Boundaries

Tell the AI what it should **never do**, what it should **always do**, and what requires **asking first**.

### Always Do

```
- Write new files to `docs/` or the appropriate `src/` subdirectory
- Follow the code style examples provided above
- Run linters (npm run lint) before declaring work complete
- Test new features with npm test
- Add JSDoc comments for public functions
- Use TypeScript types for all function parameters and returns
```

### Ask First

```
- Before modifying existing documents or READMEs
- Before changing any configuration files
- Before refactoring existing components
- Before adding new dependencies
- Before changing the project structure
```

### Never Do

```
- Modify code in `src/` that's outside the scope of the current task
- Edit .env files or any config with secrets
- Commit secrets or credentials
- Remove or modify tests
- Change the git history or rewrite commits
- Modify package.json versions without asking
- Delete or significantly refactor existing working code
```

---

## Tips for Effective Agents

### Keep it Scannable

Use headings, lists, and code blocks. Avoid dense paragraphs. Your agent file might be 50 KB—make it easy to navigate.

### Be Specific, Not Verbose

- **Instead of:** "Please write TypeScript code that is modern and follows best practices"
- **Do this:** "Write TypeScript 5.1+ with strict mode enabled. Use named exports and avoid `any` types."

### Include Actual Code

- **Good:** "Here's how we structure component tests: `describe('MyComponent', () => { ... })`"
- **Bad:** "Write tests that thoroughly test all aspects of components"

### Document Exceptions

If there's something unusual about the project, call it out:

```
## Exceptions

- Test files live in src/__tests__/ (not a separate tests/ directory)
- We don't use a strict naming convention for components in src/experimental/
- CSS-in-JS is forbidden; only Tailwind CSS
```

### Version Your Agent

If you update the agent significantly, add a date or version:

```yaml
---
name: my-agent
description: ...
version: 2.0
updated: 2024-01-15
---
```

This helps you know when the agent last changed and if different behavior is expected.

### Test and Iterate

Don't set it and forget it. After using the agent a few times, ask yourself:

- Did it make mistakes that should have been obvious from the agent file?
- Did it miss patterns from the codebase?
- Did it do something outside its scope?

Update the agent file accordingly. Your agent will only be as good as the guidance you give it.

---

## Quick Checklist

Before publishing your agent:

- [ ] Commands section is copy-paste ready
- [ ] Project structure matches reality (spot-check recent files)
- [ ] All tech stack versions are correct (don't guess)
- [ ] Code examples are from the actual codebase
- [ ] Boundaries are clear: always, ask first, never
- [ ] No more than 1 example per code style category
- [ ] Git workflow included (if agent needs it)
- [ ] Typos and links are verified

---

## Example: A Complete Minimal Agent Setup

This is the bare minimum for a working agent:

```markdown
---
name: my-agent
description: ...
tools: Read, Write, Glob, Grep
model: sonnet
color: blue
---

## Commands

npm test                    # Run tests
npm run lint                # Check lint
npm run build               # Production build

## Project Structure

src/
├── components/   # UI components
├── utils/        # Helper functions
└── types/        # TypeScript definitions

## Tech Stack

- Node.js 18.17.0
- React 18.2.0
- TypeScript 5.1.6
- Tailwind CSS 3.3.0

## Code Style Examples

**Component:**
const MyButton = ({ label }: { label: string }) => (
  <button className="btn btn--primary">{label}</button>
);

**Utility:**
export function formatDate(date: Date): string {
  return date.toLocaleDateString();
}

## Boundaries

Always:
- Run npm run lint before finishing
- Add TypeScript types to all functions

Never:
- Modify config files
- Delete existing tests

## Your Role

You are an expert at [specific task]. Focus on [key responsibility].
```

Keep it short, specific, and real. You can always expand when friction appears.
