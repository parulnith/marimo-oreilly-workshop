# Module 4: How to Use AI Coding Agents for AI/ML Development


### Getting set up

To use AI generation in marimo:

1. Install the required dependencies through the notebook settings
2. Configure your LLM provider in the AI tab of the settings menu

marimo works with hosted providers such as OpenAI, Anthropic, and Google, as well as local models served through Ollama and other OpenAI-compatible providers.

Several marimo AI features rely on your `marimo.toml` configuration file. Locate it with:

```bash
marimo config show | head
```

### The main entry points

There are five main ways to use AI in the editor:

- **Generate new cells** with the **Generate with AI** button at the bottom of the notebook
- **Inline autocompletion**, similar to Copilot-style tools
- **Refactor the current cell** with `Ctrl/Cmd-Shift-E`
- **Use the Chat panel** to ask notebook-level questions or generate cells from a side panel
- **Generate entire notebooks** from the command line with:

```bash
marimo new "your prompt here"
```

### Hands-on: generate and refactor inside `module_4.py`

Open `module_4.py` from Module 4.

**Task 1 — Generate a new analysis cell.** Click **Generate with AI** and prompt:

> Add a new cell below the model-comparison section that compares the top 5 occupations for rows predicted as high income versus low income.

Review the generated code, then insert it into the notebook.

**Task 2 — Refactor an existing cell.** Click into the preprocessing/modeling part of the notebook and press `Ctrl/Cmd-Shift-E`. Prompt:

> Refactor this cell so the preprocessing logic is moved into a helper function called `prepare_features`.

The point of the exercise is not to accept AI output blindly. It is to review generated code in the same notebook where it will run.

---

## 4.2 Context, prompts, and tools

The quality of AI assistance depends heavily on context. marimo improves that context in several ways.

### Variable context with `@`

marimo's AI assistant already has the notebook code as context. You can additionally pass variables and their values to the assistant by tagging them with `@`.

For example:

- `@df` includes the dataframe `df`
- `@feature_options` includes the available feature list
- `@column_selector` includes the current column-selection widget state

This is especially useful in notebook work because the assistant is not guessing your schema from text alone. It can work from the current notebook state.

### Chat panel modes

The Chat panel supports three modes:

- **Manual** — no tool access; the model responds only from the conversation and any manually injected context
- **Ask** — read-only tools plus context gathering, so the assistant can inspect the notebook
- **Agent (beta)** — everything in Ask mode plus the ability to edit notebook cells and run stale cells

```
What patterns do you see between age, hours-per-week, and income in @df?
```

### Prompt templates and custom rules

marimo provides prompt templates for common notebook tasks, which is useful when participants know roughly what they want but need a stronger prompt.

marimo also supports **custom rules** in settings so that AI output stays consistent across prompts and providers. For example:

```text
Always use matplotlib for plotting.
Prefer pandas over polars.
Use type hints for helper functions.
Use f-strings for string formatting.
```

These rules are useful in workshop settings because they keep AI-generated code aligned with the style you are teaching.

### Hands-on: compare low-context and high-context prompts

In `module_4.py`, open the Chat panel and try this plain prompt:

> Add a cell that summarizes the selected columns and shows how they relate to income.

Then try a richer prompt:

> Using @df and @column_selector, add a cell that analyzes the columns selected in the widget and compares their relationship to income.

Compare the two results. The second prompt should usually be more specific, more aligned with the notebook, and require less cleanup.

---

## 4.3 Agents, MCP, copilots, and setup choices

marimo supports richer AI workflows than just cell generation.

### Agents

marimo supports external agents such as Claude Code, Codex, and Gemini CLI. These are useful when you want the assistant to work across multiple cells or operate on the notebook as a file rather than just generating one block of code at a time.

This matters because marimo notebooks are stored as plain `.py` files. External agents can read notebook structure directly instead of trying to reason over notebook JSON.

### MCP (Model Context Protocol)

marimo supports MCP in two directions:

**As an MCP server** — marimo exposes notebook-aware AI tools to external applications. This is useful when you want external tools such as Claude Code to interact with a running marimo notebook:

```bash
# Start marimo with MCP support
uv run --with="marimo[mcp]" marimo edit notebook.py --mcp --no-token

# Connect Claude Code to the running marimo MCP server
claude mcp add --transport http marimo http://localhost:PORT/mcp/server
```

The MCP server exposes AI tools plus prompts such as `active_notebooks` and `errors_summary`.

**As an MCP client** — marimo connects supported MCP servers into its Chat panel. Currently supported presets:

- `marimo` for official marimo documentation, API reference, and code examples
- `context7` for up-to-date, version-specific documentation from official sources

Enable these in the AI settings UI or in `marimo.toml`:

```toml
[mcp]
presets = ["marimo", "context7"]
```

Once configured, those tools are available in the Chat panel when using Ask mode. The current docs describe MCP as an experimental feature, so it is best treated as an advanced workflow rather than the default workshop path.

Source: https://docs.marimo.io/guides/editor_features/mcp/

---

## 4.4 Claude Code for marimo: hooks, commands, and skills

When using Claude Code as an external agent for marimo development, three features let you customize and automate the workflow. Each one solves a different problem, and the key difference between them is **who triggers the behavior**:

| Feature | Who triggers it | What it does |
|---------|----------------|--------------|
| **Hook** | Claude (automatically) | Runs a script every time Claude edits a file |
| **Command** | You (manually) | Runs a prompt template when you type `/command-name` |
| **Skill** | Claude (when it detects relevance) | Loads specialized instructions on demand |

All three live in a `.claude/` folder — either at the root of your project (for project-specific config) or in your home directory at `~/.claude/` (for global defaults).

### Where everything lives

```
.claude/
├── settings.json              ← hook definitions go here
├── hooks/
│   └── marimo-check.sh        ← the script a hook runs
├── commands/
│   ├── marimo-check.md        ← slash command: lint a notebook
│   ├── create-marimo.md       ← slash command: create a notebook
│   └── fix-issue.md           ← slash command: fix a GitHub issue
└── skills/
    ├── anywidget-dev/
    │   └── SKILL.md           ← skill: how to build anywidgets
    ├── marimo-notebook/
    │   └── SKILL.md           ← skill: general marimo knowledge
    └── batch-production/
        └── SKILL.md           ← skill: production batch jobs
```

---

### 4.4.1 Hooks: automatic quality checks

#### The problem hooks solve

You ask Claude to edit a marimo notebook. Claude makes the edit, but introduces a duplicate variable definition. In marimo, each variable must be defined in exactly one cell so the runtime knows the execution order. You don't notice the problem until you try to run the notebook and marimo complains. Then you have to go back to Claude, explain the error, and wait for a fix.

A hook eliminates this entire cycle. It runs `marimo check` automatically after every file edit. If the check fails, Claude sees the error immediately and fixes it — before you ever see the broken output.

#### How hooks work

Hooks subscribe to **events** inside Claude Code. The most useful event for marimo is `PostToolUse`, which fires after Claude calls a tool like `Edit` or `Write`. You configure hooks in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/marimo-check.sh"
          }
        ]
      }
    ]
  }
}
```

This says: "Every time Claude uses the Edit or Write tool, run `marimo-check.sh`."

#### The hook script

The script receives JSON on stdin describing what Claude just did, including the file path. It then decides whether to act:

```bash
#!/bin/bash

# Read the tool output from stdin
INPUT=$(cat)

# Extract the file path that was just edited
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_response.filePath // empty')

# If no file path or file doesn't exist, do nothing
if [ -z "$FILE_PATH" ] || [ "$FILE_PATH" = "null" ]; then
    exit 0
fi

if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Check if the file is a marimo notebook
# (look for "import marimo" and "@app.cell")
if grep -q "import marimo" "$FILE_PATH" 2>/dev/null \
   && grep -q "@app.cell" "$FILE_PATH" 2>/dev/null; then

    echo "Running marimo check on $FILE_PATH..."

    # Run the marimo linter
    CHECK_OUTPUT=$(uvx marimo check "$FILE_PATH" 2>&1)
    CHECK_EXIT=$?

    echo "$CHECK_OUTPUT"

    if [ $CHECK_EXIT -ne 0 ]; then
        # Exit code 2 = BLOCK Claude and show the error
        echo "✗ Marimo check failed for $FILE_PATH" >&2
        echo "$CHECK_OUTPUT" >&2
        echo "Please fix the issues. Don't ask, just fix." >&2
        exit 2
    else
        echo "✓ Marimo check passed"
        exit 0
    fi
fi

# Not a marimo notebook — do nothing
exit 0
```

#### Exit codes explained

The exit code of your hook script determines what happens next:

- **`exit 0`** — everything is fine, Claude continues normally
- **`exit 2`** — the hook failed; Claude is **blocked** and sees whatever you wrote to stderr as feedback, giving it a chance to auto-fix the problem

This is the key mechanism. By exiting with code 2 and writing a helpful error message to stderr, you create a feedback loop: Claude edits → hook catches the error → Claude sees the error → Claude fixes it → hook runs again → check passes.

#### Seeing hook activity

Press `Ctrl+O` in Claude Code to open the tool-use log. You can see exactly when hooks triggered, what they returned, and whether they blocked Claude.

#### When to use hooks

Hooks are best when you want **zero-friction enforcement** — a rule that applies to every edit, automatically, without you needing to think about it. The marimo linter is a perfect fit because duplicate variable definitions are easy to introduce and easy to fix, but annoying to catch manually.

If you find the automatic checking too noisy (for example, during early prototyping when you know the notebook is incomplete), you can disable the hook temporarily and use a command instead.

---

### 4.4.2 Commands: on-demand prompt templates

#### The problem commands solve

Some tasks come up often enough that you want a pre-written prompt, but not so often that they should run automatically. For example: "lint this specific notebook," "create a new marimo notebook with these conventions," or "fix this GitHub issue."

Without commands, you'd retype the same multi-paragraph prompt every time. With commands, you type `/marimo-check notebook.py` and the full prompt — including any shell output — is assembled and sent to Claude for you.

#### How commands work

Commands are markdown files stored in `.claude/commands/`. Each file becomes a slash command named after the file. When you type `/command-name` in Claude Code, the markdown content becomes Claude's prompt.

Two special features make commands powerful:

1. **`$ARGUMENTS`** — a placeholder that gets replaced with whatever you type after the command name
2. **`!`backtick syntax** — runs a shell command and injects its output into the prompt before Claude sees it

#### Example 1: lint a notebook on demand

**File:** `.claude/commands/marimo-check.md`

```markdown
---
allowed-tools: Bash(uvx marimo check:*), Edit()
---

## Context

This is the output of the "uvx marimo check --fix $ARGUMENTS" command:

!`uvx marimo check --fix $ARGUMENTS || true`

## Your task

Only (!) if the context suggests we need to edit the notebook, read the file
$ARGUMENTS, then fix any warnings or errors shown in the output above. Do
not make edits or read the file if there are no issues.
```

**Usage:** `/marimo-check module_4.py`

What happens step by step:

1. `$ARGUMENTS` is replaced with `module_4.py`
2. The `!`backtick command runs `uvx marimo check --fix module_4.py`
3. The linter output is inserted into the prompt
4. Claude reads the full prompt (with the linter output embedded) and acts on it
5. The `|| true` at the end prevents a non-zero exit code from breaking the command

#### Example 2: create a new notebook

**File:** `.claude/commands/create-marimo.md`

```markdown
---
allowed-tools: Bash(*), Edit(), Write()
---

## Instructions

Create a new marimo notebook based on the user's description: $ARGUMENTS

Follow these guidelines:
- Use `import marimo as mo` and the `@app.cell` decorator pattern
- Prefer polars over pandas when possible
- Each cell should define at most one variable
- Use `mo.ui.*` elements for interactivity
- Run `uvx marimo check` on the finished file and fix any issues
```

**Usage:** `/create-marimo "slider that controls a scatter plot"`

This is essentially a system prompt for notebook creation. The key benefit over putting this in your `CLAUDE.md` file is that commands only consume context tokens when you invoke them.

#### Example 3: fix a GitHub issue

**File:** `.claude/commands/fix-issue.md`

```markdown
---
allowed-tools: Bash(gh:*), Bash(uvx marimo check:*), Edit(), Read()
---

## Context

Fetch the details of GitHub issue #$ARGUMENTS:

!`gh issue view $ARGUMENTS || true`

## Your task

Read the issue above, understand what needs to change, and implement a fix.
After making changes, run `uvx marimo check` on any modified marimo notebooks.
```

**Usage:** `/fix-issue 42`

This fetches the issue details from GitHub using the `gh` CLI, injects them into the prompt, and tells Claude to work on a fix.

#### When to use commands

Commands are best for **repeatable tasks that you want to trigger intentionally**. They sit between hooks (fully automatic) and free-form prompting (fully manual). Good candidates:

- Linting a specific file when you don't want hooks running on every edit
- Creating notebooks from a template with consistent conventions
- Integrating with external tools like GitHub, CI, or data pipelines
- Any multi-step workflow you find yourself prompting for repeatedly

---

### 4.4.3 Skills: agent-triggered knowledge

#### The problem skills solve

Some knowledge is specialized — Claude needs it sometimes, but not always. For example, building an anywidget requires specific patterns (use vanilla JS in `_esm`, wrap the widget with `mo.ui.anywidget()`, include `_css` for styling). If you put these instructions in `CLAUDE.md`, they consume context tokens on every conversation, even when you're doing something completely unrelated to anywidgets.

Skills solve this by letting Claude **decide** when to load the instructions. Only a short description is read at startup; the full instructions are loaded on demand.

#### How skills work

Each skill is a markdown file stored in its own folder under `.claude/skills/`:

```
.claude/skills/anywidget-dev/SKILL.md
```

The file has a YAML frontmatter block with two fields:

```yaml
---
name: anywidget-generator
description: Generate anywidget components for marimo notebooks.
---
```

**At startup**, Claude reads only the `name` and `description` for every installed skill. This is cheap — a few tokens per skill.

**During a conversation**, if Claude recognizes that your request matches a skill's description, it reads the full body of the SKILL.md file and follows those instructions. If the skill isn't relevant, the body is never loaded.

#### Example: anywidget generation

**File:** `.claude/skills/anywidget-dev/SKILL.md`

```markdown
---
name: anywidget-generator
description: Generate anywidget components for marimo notebooks.
---

When writing an anywidget use vanilla javascript in `_esm` and do not
forget about `_css`. The css should look bespoke in light mode and dark
mode. Keep the css small unless explicitly asked to go the extra mile.
When you display the widget it must be wrapped via
`widget = mo.ui.anywidget(OriginalAnywidget())`.

<example title="Example anywidget implementation">
import anywidget
import traitlets

class CounterWidget(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      let count = () => model.get("number");
      let btn = document.createElement("button");
      btn.innerHTML = `count is ${count()}`;
      btn.addEventListener("click", () => {
        model.set("number", count() + 1);
        model.save_changes();
      });
      model.on("change:number", () => {
        btn.innerHTML = `count is ${count()}`;
      });
      el.appendChild(btn);
    }
    export default { render };
    """
    _css = """button { font-size: 14px; }"""
    number = traitlets.Int(0).tag(sync=True)

widget = mo.ui.anywidget(CounterWidget())
widget
</example>

When sharing the anywidget, keep the example minimal. No need to combine
it with marimo ui elements unless explicitly stated to do so.
```

When you prompt Claude with "create a marimo notebook with a fireworks widget," Claude sees the description, decides this skill is relevant, reads the full instructions, and follows the pattern — including the `mo.ui.anywidget()` wrapper and vanilla JS in `_esm`.

#### Example: production batch jobs

**File:** `.claude/skills/batch-production/SKILL.md`

```markdown
---
name: batch-production
description: Convert a marimo notebook into a production-ready batch job with pydantic parameters, CLI support, and optional W&B logging.
---

When converting a notebook for production use:
- Define a pydantic model for all configurable parameters
- Add `mo.cli_args()` support so the notebook runs from the command line
- Add slider/input widgets tied to the pydantic model for interactive use
- If the user uses Weights & Biases, log all parameters from the pydantic class

Ask the user which parameters should be configurable before starting.
```

This skill only activates when Claude detects that you're trying to productionize a notebook. The rest of the time, it costs nothing.

#### Don't repeat yourself across skills

If you have a general marimo skill that covers notebook conventions, your specialized skills (anywidget, batch, etc.) should not repeat those conventions. The general skill will be loaded alongside the specialized one when Claude detects relevance. Keep each skill focused on what it adds beyond the baseline.

#### Manual triggering

You can also trigger skills manually by typing `/skills` in Claude Code. This lists all installed skills and lets you select one to load explicitly. This is useful when Claude didn't auto-detect the skill and you want to force it, or when you're testing a new skill you just wrote.

#### When to use skills

Skills are best for **specialized knowledge that is only relevant some of the time**:

- How to build anywidgets
- How to convert Jupyter notebooks to marimo (using `marimo convert` instead of reading the `.ipynb`)
- How to structure a notebook for production batch processing
- Library-specific patterns you use in your project

If the knowledge is relevant to every single conversation, put it in `CLAUDE.md` instead. Skills are for the long tail of context that would bloat your system prompt.

---

### 4.4.4 Installing pre-built skills

The marimo team maintains a public repository of skills at [github.com/marimo-team/skills](https://github.com/marimo-team/skills). At the time of writing, it includes skills for anywidget generation, Jupyter-to-marimo conversion, production batch jobs, and general marimo notebook creation.

The repository uses the `skills.sh` standard (from Forcell), which gives you an interactive installer:

1. Copy the install command from the repository README
2. Paste it in your terminal
3. Select which skills you want (use spacebar to toggle)
4. Choose which agents to install for (Claude Code, OpenCode, etc.)
5. Choose local or global installation
6. Optionally create symlinks (recommended — one source of truth per skill file)

The symlink approach means the actual skill file lives in one place. If you edit it, every agent that references it via symlink sees the update immediately.

**A word of caution:** don't install every skill. When too many skills are loaded, Claude may trigger the wrong one, or trigger multiple skills when you only wanted one. Install only what your current project needs and rely on `/skills` for manual control when the situation calls for it.

---

### 4.4.5 Putting hooks, commands, and skills together

Here is a practical setup for a marimo ML project:

**Always on (hook):**
- `marimo check` runs after every file edit — catches duplicate variable definitions, cycle errors, and syntax issues automatically

**On demand (commands):**
- `/create-marimo` — generates a new notebook with your team's conventions
- `/marimo-check` — manual lint when the hook is disabled
- `/fix-issue` — pulls a GitHub issue and starts working on a fix

**When needed (skills):**
- `anywidget-dev` — loads when you ask Claude to build a custom widget
- `batch-production` — loads when you're converting a notebook for production
- `marimo-notebook` — general marimo knowledge, loaded alongside other skills

You don't need all three mechanisms for every project. A small exploratory notebook might only need the hook. A team project with shared conventions might add commands. A project with custom widget work might add the anywidget skill. Mix and match based on what actually saves you time.

---

### 4.4.6 Hands-on: set up Claude Code automation for marimo

**Task 1 — Set up the marimo check hook.**

1. Create `.claude/settings.json` in your project root with the hook configuration shown in 4.4.1
2. Create the `marimo-check.sh` script and make it executable (`chmod +x`)
3. Start Claude Code and ask it to "add two cells that both assign `a = 1`" to a marimo notebook
4. Watch the hook trigger automatically — Claude should detect the duplicate definition and fix it
5. Press `Ctrl+O` to inspect the hook activity in the tool-use log

**Task 2 — Create a slash command.**

1. Create `.claude/commands/marimo-check.md` with the command shown in 4.4.2
2. Restart Claude Code and type `/marimo-check module_4.py`
3. Observe how the linter output is injected into the prompt and Claude responds to it

**Task 3 — Try a skill.**

1. Create `.claude/skills/anywidget-dev/SKILL.md` with the skill shown in 4.4.3
2. Start Claude Code and prompt: "Create a new marimo notebook with a widget that shows an interactive color picker"
3. Check whether Claude loaded the anywidget skill automatically (look for the skill name in `Ctrl+O` output)
4. Run the generated notebook with `marimo run` and test the widget

---

## 4.5 Local versus cloud-hosted setups

For marimo, Ollama is the most straightforward local path when you want notebook AI without sending notebook context to a hosted provider.

Use [Ollama-Setup.md](/Users/parulpandey/Desktop/Marimo%20Workshop/Module_4/Ollama-Setup.md) as the setup handout. The booklet only covers where Ollama fits in the workflow.

### Option A: Use Ollama inside marimo

After Ollama is running locally, pull one of the workshop models:

```bash
ollama pull gemma3:270m
ollama pull gemma2:2b
```

Then in marimo settings → AI, set:

```toml
[ai.completion]
model = "ollama/gemma2:2b"
base_url = "http://localhost:11434"
```

This gives you local AI assistance inside marimo without sending notebook context to a hosted provider.

### Option B: Use Claude Code through Ollama

If you want an external coding agent experience, Ollama can also launch Claude Code directly:

```bash
ollama launch claude --model qwen3-coder-next:cloud
```

This is useful when you want the agent to work across the notebook file, terminal, and surrounding project instead of only inside marimo's editor UI.

### Hands-on: compare the two workflows

**Step 1 — Test marimo with a local model.** In `module_4.py`, hover over the empty cell near the end of the notebook and click Generate with AI. Use this prompt:

> Add a new cell that uses @df and @column_selector to summarize the selected columns and visualize how one or two selected features relate to income.

Run the result. Does it use the selected columns correctly? Does it reference `df` and the widget state properly?

**Step 2 — Try the same task with Claude Code launched through Ollama.** Compare the output quality, how it handles notebook structure, and how many edits you need to make before running it.

**Step 3 — Set your custom rules** in AI settings, then regenerate. Notice how the output quality improves when the agent has persistent preferences to follow:

```
Use marimo UI elements (mo.ui.*) for interactivity wherever applicable.
Use matplotlib for all plots with figsize=(7, 4) and tight_layout.
One primary variable returned per cell. Wrap intermediate logic in functions.
```

The main point is not to pick one tool universally. It is to understand the tradeoff:

- marimo + local Ollama keeps context private and works well for notebook-scoped generation
- Claude Code via `ollama launch` is useful when you want broader project-level assistance
- Ollama Cloud is a good fallback when you want larger models without local downloads

The right AI setup is the one that fits your data constraints, your workflow speed, and your task complexity. What all three options share is marimo's automatic variable context — your current state is always available to the agent, so your prompts stay short and your iterations stay fast regardless of which model is doing the work.

---

## 4.6 marimo check: linting for agents and humans

AI coding agents are capable of writing marimo notebooks quickly, but they sometimes violate marimo-specific rules — like redefining a variable across two cells, or creating a circular dependency. `marimo check` gives both you and your agent a fast feedback loop to catch and fix these issues before running the notebook.

### What it catches

`marimo check` focuses exclusively on marimo-specific correctness rules. It deliberately does not duplicate what tools like `ruff` or `mypy` already do. Key checks include:

- **Multiple definitions** — the same variable name defined in more than one cell
- **Circular dependencies** — cell A depends on cell B, which depends on cell A
- **Formatting issues** — notebook structure that marimo cannot parse or execute reliably

Error messages are actionable: they tell you exactly which cells conflict and suggest fixes (for example, renaming a variable with an underscore prefix to make it cell-local).

### Running the linter

Check a single notebook:

```bash
marimo check notebook.py
```

Check all notebooks in the current directory:

```bash
marimo check .
```

### Automated fixes

For issues with obvious solutions, pass `--fix` to let marimo resolve them automatically:

```bash
marimo check --fix notebook.py
```

For more complex issues where the fix might change behaviour, use `--unsafe-fixes`:

```bash
marimo check --unsafe-fixes notebook.py
```

This is useful after an AI agent generates a notebook — run `marimo check --fix` as a cleanup step before opening the notebook.

### JSON output for agents

When an agent is doing the linting loop itself, the `--format=json` flag makes the output machine-readable:

```bash
marimo check --format=json notebook.py | jq '.issues[] | select(.severity == "breaking")'
```

This lets the agent read only the breaking issues and decide what to fix next, without parsing human-readable text.

### CI integration

Add a quality gate to your CI pipeline with the `--strict` flag, which treats warnings as errors:

```yaml
# .github/workflows/check-notebooks.yml
name: Check Notebooks
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: astral-sh/setup-uv@v1
      - run: uv run marimo check --strict .
```

### Hands-on: lint the workshop notebook

Run `marimo check` on the notebook you have been editing in this module:

```bash
marimo check Module_4/module_4.py
```

If there are issues, try:

```bash
marimo check --fix Module_4/module_4.py
```

Then open the notebook and verify it runs cleanly end to end.

---
