## Module 4: How to Use AI Coding Agents for AI/ML Development
AI coding agents are most useful when they are integrated directly into your development environment and can work with the actual state of your notebook. While coding assistants can write code but for ML/AI, it makes more sense that they also have context about 
dataframes, model outputs, variables, and dependencies in memory.

 In ML and AI workflows, their value depends on:

- when you let them generate or modify code
- what notebook context they can see
- what tools they are allowed to use
- whether you run them through a hosted provider or a local/private setup

The core idea of this module is better context leads to better AI assistance, and marimo is designed to provide that context inside the workflow itself.

### Hands-on Exercise (guided in marimo)

Use marimo's AI features inside `Module_4/module_4.py`:

- generate or modify code directly in the active notebook
- refactor an existing cell without leaving the editor
- provide explicit variable context such as `@df`
- compare the quality of a low-context prompt and a context-rich prompt
- discuss the tradeoffs between local and cloud-hosted setups


---

### AI-assisted coding in marimo

marimo is an AI-native editor with support for full-cell AI code generation. marimo's AI assistant is specialized for working with data. Unlike traditional assistants that only see the text of your program, marimo's assistant can also work with the values of variables in memory.


#### Getting set up

To use AI generation in marimo:

1. Install the required dependencies through the notebook settings
2. Configure your LLM provider in the AI tab of the settings menu

marimo works with hosted providers such as OpenAI, Anthropic, and Google, as well as local models served through Ollama and other OpenAI-compatible providers.

Several marimo AI features rely on your `marimo.toml` configuration file. Locate it with:

```bash
marimo config show | head
```

#### The main entry points

There are four main ways to use AI in the editor:

- **Generate new cells** with the **Generate with AI** button at the bottom of the notebook
- **inline autocompletion, similar to Copilot-style tools**
- **Refactor the current cell** with `Ctrl/Cmd-Shift-E`
- **Use the Chat panel** to ask notebook-level questions or generate cells from a side panel
- **Generate entire notebooks** from the command line with:

```bash
marimo new "your prompt here"
```

#### 4.1 Hands-on: generate and refactor inside `module_4.py`

Open `module_4.py` from Module 4.

**Task 1 — Generate a new analysis cell.** Click **Generate with AI** and prompt:

*"Add a new cell below the model-comparison section that compares the top 5 occupations for rows predicted as high income versus low income."*

Review the generated code, then insert it into the notebook.

**Task 2 — Refactor an existing cell.** Click into the preprocessing/modeling part of the notebook and press `Ctrl/Cmd-Shift-E`.

Prompt:

*"Refactor this cell so the preprocessing logic is moved into a helper function called `prepare_features`."*

The point of the exercise is not to accept AI output blindly. It is to review generated code in the same notebook where it will run.

---

### 4.2 Context, prompts, and tools

The quality of AI assistance depends heavily on context. marimo improves that context in several ways.

#### Variable context with `@`

marimo's AI assistant already has the notebook code as context. You can additionally pass variables and their values to the assistant by tagging them with `@`.

For example:

- `@df` includes the dataframe `df`
- `@feature_options` includes the available feature list
- `@column_selector` includes the current column-selection widget state

This is especially useful in notebook work because the assistant is not guessing your schema from text alone. It can work from the current notebook state.

#### Chat panel modes

The Chat panel supports three modes:

- **Manual** — no tool access; the model responds only from the conversation and any manually injected context
- **Ask** — read-only tools plus context gathering, so the assistant can inspect the notebook
- **Agent (beta)** — everything in Ask mode plus the ability to edit notebook cells and run stale cells

```
What patterns do you see between age, hours-per-week, and income in @df?
```


#### Prompt templates and custom rules

marimo provides prompt templates for common notebook tasks, which is useful when participants know roughly what they want but need a stronger prompt.

marimo also supports **custom rules** in settings so that AI output stays consistent across prompts and providers. For example:

```text
Always use matplotlib for plotting.
Prefer pandas over polars.
Use type hints for helper functions.
Use f-strings for string formatting.
```

These rules are useful in workshop settings because they keep AI-generated code aligned with the style you are teaching.

#### Hands-on: compare low-context and high-context prompts

In `module_4.py`, open the Chat panel and try this plain prompt:

*"Add a cell that summarizes the selected columns and shows how they relate to income."*

Then try a richer prompt:

*"Using @df and @column_selector, add a cell that analyzes the columns selected in the widget and compares their relationship to income."*

Compare the two results. The second prompt should usually be more specific, more aligned with the notebook, and require less cleanup.

---

### 4.3 Agents, MCP, copilots, and setup choices

marimo supports richer AI workflows than just cell generation.

#### Agents

marimo supports external agents such as Claude Code, Codex, and Gemini CLI. These are useful when you want the assistant to work across multiple cells or operate on the notebook as a file rather than just generating one block of code at a time.



This matters because marimo notebooks are stored as plain `.py` files. External agents can read notebook structure directly instead of trying to reason over notebook JSON.

#### MCP

marimo also supports the **Model Context Protocol (MCP)**:

- **as an MCP server** — marimo exposes notebook-aware AI tools to external applications
- **as an MCP client** — marimo connects supported MCP servers into its Chat panel

The current docs describe MCP as an experimental feature, so it is best treated as an advanced workflow rather than the default workshop path.

**Server mode** is useful when you want external tools such as Claude Code to interact with a running marimo notebook. The docs show starting marimo with MCP support like this:

```bash
uv run --with="marimo[mcp]" marimo edit notebook.py --mcp --no-token
```

Once running, Claude Code can connect to the marimo MCP server with:

```bash
claude mcp add --transport http marimo http://localhost:PORT/mcp/server
```

The docs also note that marimo's MCP server exposes AI tools plus prompts such as `active_notebooks` and `errors_summary`.

**Client mode** is useful inside marimo itself. According to the docs, marimo currently supports these MCP server presets in the Chat panel:

- `marimo` for official marimo documentation, API reference, and code examples
- `context7` for up-to-date, version-specific documentation from official sources

You can enable these in the AI settings UI or in `marimo.toml`:

```toml
[mcp]
presets = ["marimo", "context7"]
```

Once configured, those tools are available in the Chat panel when using Ask mode.

Source: https://docs.marimo.io/guides/editor_features/mcp/

#### AI completion and copilots

marimo also supports inline AI completion, which is lighter-weight than full cell generation. This covers:

- **GitHub Copilot**
- **Windsurf**
- **Custom copilots** through your own configured provider


This is useful to mention because not every AI workflow needs a full agent. Sometimes completion inside the editor is enough.

---

### 4.4 Local versus cloud-hosted setups

For marimo, Ollama is the most straightforward local path when you want notebook AI without sending notebook context to a hosted provider.

Use [Ollama-Setup.md](/Users/parulpandey/Desktop/Marimo%20Workshop/Module_4/Ollama-Setup.md) as the setup handout. The booklet only covers where Ollama fits in the workflow.

#### Option A: Use Ollama inside marimo

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

#### Option B: Use Claude Code through Ollama

If you want an external coding agent experience, Ollama can also launch Claude Code directly:

```bash
ollama launch claude --model qwen3-coder-next:cloud
```

This is useful when you want the agent to work across the notebook file, terminal, and surrounding project instead of only inside marimo's editor UI.

#### Hands-on: compare the two workflows

**Step 1 — Test marimo with a local model.** In `module_4.py`, hover over the empty cell near the end of the notebook and click Generate with AI. Use this prompt:

*"Add a new cell that uses @df and @column_selector to summarize the selected columns and visualize how one or two selected features relate to income."*

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

---

The right AI setup is the one that fits your data constraints, your workflow speed, and your task complexity. What all three options share is marimo's automatic variable context — your current state is always available to the agent, so your prompts stay short and your iterations stay fast regardless of which model is doing the work.

Module 5 brings everything full circle: once your interactive, AI-assisted, reproducible notebook is working, how do you turn it into reusable systems that others can depend on?

#### What's Next
Quiz

Use `Module_4/module-4-quiz-viewer.html` to review the key ideas from this module.

---
