# Module 4: How to Use AI Coding Agents for AI/ML Development


Live notebook:

```bash
marimo edit Module_4/4_ai_features_demo.py
```

---

## 4.1 When to Let AI Agents Write Code for You

### What to teach

- **Generate with AI**: add a new cell from a prompt.
- **Inline autocomplete**: complete code while typing.
- **Refactor current cell**: modify one existing cell with `Ctrl/Cmd-Shift-E`.
- **Chat panel**: ask notebook-level questions or insert generated cells.
- **`marimo new`**: generate a whole notebook from the command line.

### Setup checkpoint

Before the demos:

1. Open marimo notebook settings.
2. Install AI dependencies if prompted.
3. Open the **AI** tab.
4. Choose a hosted provider or local Ollama model.

Find the config file:

```bash
marimo config show | head
```

### Demo: Generate with AI

Notebook section: **1. Generate with AI**

Prompt:

```text
Using df, add a new cell that groups rows by segment and shows average revenue,
average profit, and average satisfaction. Return a dataframe named
segment_summary.
```

Review:

- Did it reuse `df`?
- Did it avoid recreating data?
- Is the output variable clear?

### Demo: Inline autocomplete

Notebook section: **2. Inline autocompletion**

In the `autocomplete_workspace` cell, type:

```python
# Return True when revenue is above 60000 and satisfaction is at least 8.
def flag_high_value_account(row):
```

Then add:

```python
df["high_value"] = df.apply(flag_high_value_account, axis=1)
df
```

### Demo: Refactor current cell

Notebook section: **3. Refactor the current cell**

Click into the repetitive `region_revenue_summary` cell and press
`Ctrl/Cmd-Shift-E`.

Prompt:

```text
Refactor this cell into a helper function named summarize_region_metric that
takes df and metric as inputs, then returns the same region-level summary.
Keep the output dataframe named region_revenue_summary.
```

Teaching point: AI is strongest for small changes when you can immediately run
and inspect the result.

---

## 4.2 Giving AI Coding Agents the Context They Need

Your code is only part of the story. For AI/ML work, the assistant also needs
execution state, dataframe schemas, widget values, model outputs, and dependency
information.

### Context in marimo

marimo helps because notebooks are reactive and stateful:

- `@df` gives the assistant dataframe context.
- `@metric_selector` gives the current widget value.
- `@segment_selector` gives the selected segment values.
- Existing variables and cell dependencies make the notebook easier to inspect.

### Demo: Chat with variable context

Notebook section: **4. Chat panel with variable context**

Chat panel modes:

- **Manual**: no tool access; the model responds only from the conversation and
  manually injected context.
- **Ask**: read-only tools plus context gathering, so the assistant can inspect
  the notebook.
- **Agent (beta)**: everything in Ask mode plus the ability to edit notebook
  cells and run stale cells.

Prompt A:

```text
What patterns do you see in this data?
```

Prompt B:

```text
Using @df, @metric_selector, and @segment_selector, add a cell that summarizes
the selected metric for the selected segments and creates a simple matplotlib
bar chart.
```

Teaching point: the second prompt is better because it gives the agent concrete
notebook state instead of asking it to guess.

### Custom instructions and rules

Use custom rules in marimo settings to keep AI output consistent across prompts
and providers:

```text
Use pandas for tabular transformations.
Use matplotlib for plots.
Keep generated cells small.
Avoid reloading data that already exists in the notebook.
```

For external agents, keep project-level instructions short and concrete. Good
instructions include:

- which notebook command to run
- which style to follow
- whether to prefer pandas, polars, matplotlib, or plotly
- whether to run `marimo check` after edits

Teaching point: prompts are for one task; custom rules and project instructions
are for repeated behavior.

### Linting and safety loop

AI can write valid Python that is invalid marimo. Always check after AI edits:

```bash
uvx marimo check Module_4/4_ai_features_demo.py
```

Apply safe fixes when available:

```bash
uvx marimo check --fix Module_4/4_ai_features_demo.py
```

Strict final check:

```bash
uvx marimo check --strict Module_4/4_ai_features_demo.py
```

What it catches:

- duplicate variable definitions
- dependency cycles
- invalid notebook structure
- formatting issues that marimo cannot parse or execute reliably

For agent workflows, JSON output can be useful:

```bash
uvx marimo check --format=json Module_4/4_ai_features_demo.py
```

For shared workshop repos, this can also become a CI quality gate:

```yaml
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

Teaching point: context improves generation; linting makes the result safe to
keep.

---

## 4.3 Choosing the Right AI Coding Agent Setup

The right setup depends on cost, speed, privacy, control, and task complexity.
Start with the built-in editor features, then move to agent workflows when the
task spans multiple cells or files.

### Option A: Built-in marimo AI

Use for:

- generating one cell
- refactoring one cell
- asking notebook-level questions
- working with `@` variable context

Best when you want fast iteration inside the notebook.

### Option B: Local models with Ollama

Use when privacy matters or you want local experimentation.

See:

```text
Module_4/Ollama-Setup.md
```

Example marimo config:

```toml
[ai.completion]
model = "ollama/gemma2:2b"
base_url = "http://localhost:11434"
```

Tradeoff: more privacy and control, but smaller local models may produce weaker
code than hosted models.

### Option C: Generate a whole notebook

Use `marimo new` when you want a fresh notebook scaffold:

```bash
marimo new "create a marimo notebook with a small sales dataframe, a dropdown for region, and a bar chart of revenue by segment"
```

Teaching point:

- **Generate with AI** adds to the current notebook.
- **Chat** works inside the current notebook.
- **`marimo new`** starts a new notebook.

### The three advanced pieces

Once the built-in editor features are clear, introduce the newer agent-facing
tools as three separate ideas:

1. **Agents / marimo pair**: connect an external coding agent to a live
   notebook.
2. **MCP**: expose notebook-aware tools or bring external tools into Chat.
3. **Skills / custom instructions**: give agents reusable behavior and project
   conventions.

### 1. Agents: marimo pair with an agent CLI

This is the important new workflow to teach.

`marimo pair` connects agent CLIs such as Claude Code, Codex, and OpenCode to a
running marimo notebook. The agent can inspect variables, test logic, run cells,
edit cells, and interact with UI elements.

Install:

```bash
npx skills add marimo-team/marimo-pair
```

or:

```bash
uvx deno -A npm:skills add marimo-team/marimo-pair
```

Pair with the demo notebook:

```text
/marimo-pair pair with me on Module_4/4_ai_features_demo.py
```

Use marimo pair for:

- fixing several broken cells
- adding a complete section
- inspecting live variable values before editing
- refactoring across multiple cells
- debugging UI behavior

Teaching point: use editor AI for cell-level work; use marimo pair when the
assistant needs live notebook state and multi-cell control.

Source: https://docs.marimo.io/guides/generate_with_ai/marimo_pair/

### 2. MCP: tool context for notebooks

MCP is experimental, but it is important to mention because it explains how
notebook-aware tools can be shared with agents and Chat.

marimo supports MCP in two directions:

- **MCP server**: exposes marimo notebook tools to external apps such as Claude
  Code, Cursor, or VS Code.
- **MCP client**: connects tools into marimo's Chat panel.

Start marimo with MCP support:

```bash
uv run --with="marimo[mcp]" marimo edit Module_4/4_ai_features_demo.py --mcp --no-token
```

Or with `uvx`:

```bash
uvx "marimo[mcp]" edit Module_4/4_ai_features_demo.py --mcp --no-token
```

Connect Claude Code to the running marimo MCP server:

```bash
claude mcp add --transport http marimo http://localhost:PORT/mcp/server
```

Enable useful MCP client presets in `marimo.toml`:

```toml
[mcp]
presets = ["marimo", "context7"]
```

Teaching point: use marimo pair for a guided agent workflow; use MCP when you
want notebook-aware tools available to external apps or Chat.

Source: https://docs.marimo.io/guides/editor_features/mcp/

### 3. Skills and custom instructions

Skills are reusable instruction bundles for coding agents.

Install marimo's official skills:

```bash
npx skills add marimo-team/skills
```

Use skills for:

- creating marimo notebooks
- converting notebooks
- building custom widgets

Custom instructions are the lightweight version of skills. Use them for project
conventions:

```text
Use marimo notebooks in Python script format.
Prefer pandas and matplotlib in workshop notebooks.
Run uvx marimo check after editing a notebook.
Keep generated cells small and readable.
```

Teaching point: use custom instructions for repeated project preferences; use
skills for specialized workflows. Do not install every skill by default. Too
much agent context can make tool choice worse.

Source: https://docs.marimo.io/guides/generate_with_ai/skills/

---

## Instructor Flow

1. Open `Module_4/4_ai_features_demo.py`.
2. Configure AI in settings.
3. Show the five editor entry points.
4. Generate one cell.
5. Show inline autocomplete.
6. Refactor one cell.
7. Compare Chat prompts with and without `@` context.
8. Add custom rules and rerun one prompt.
9. Run the linting loop: `check`, `--fix`, `--strict`.
10. Show `marimo new`.
11. Teach local versus hosted tradeoffs.
12. Teach the three advanced pieces: **agents/marimo pair**, **MCP**, and
    **skills/custom instructions**.
