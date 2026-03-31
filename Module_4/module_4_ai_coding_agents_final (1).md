# Module 4: How to Use AI Coding Agents for AI/ML Development

**Duration:** 35 minutes
**Format:** Presentation (~10 min) → Hands-on exercise (~22 min) → Wrap-up (~3 min)
**Notebook:** `Module_3/module_3.py`

---

## Presentation: AI Coding Agents in Your Development Environment

AI coding agents integrated directly into the notebook environment can act like fast collaborators rather than detached text generators. In ML and AI workflows, their value depends on:

- when you let them generate or modify code
- what notebook context they can see
- what tools they are allowed to use
- whether you run them through a hosted provider or a local/private setup

The core idea of this module is practical: better context leads to better AI assistance, and marimo is designed to provide that context inside the workflow itself.

### The problem with fragmented AI workflows

In most AI/ML workflows today, the tools are disconnected. You write preprocessing code in one place, paste it into ChatGPT to ask for help, copy the response back, fix it, and repeat. The AI never sees your actual data. It does not know your column names, your feature distributions, your model outputs, or your variable dependencies. Every prompt starts from zero.

This matters because AI/ML development is iterative and stateful. You are not writing isolated scripts — you are building pipelines where each step depends on the output of the last. When the AI cannot see that state, it guesses. It hallucinates column names. It writes preprocessing code that does not match your schema. It suggests model evaluation logic that conflicts with how you split your data.

The fix is not a better model. It is better context.

### What changes when AI is inside the notebook

When AI is integrated directly into your development environment — not as a separate chat window, but as part of the notebook where your code, data, and results already live — the quality of assistance changes fundamentally.

The AI can see your variables in memory: the dataframe you are working with, the features you selected, the model you trained, the predictions it produced. It can reference your actual schema instead of guessing. It can generate code that fits into your existing pipeline instead of producing standalone snippets that need heavy editing.

marimo is a reactive Python notebook where AI has access to execution context — not just the text of your code, but the current values of your variables. The notebook becomes both the prompt and the runtime.

marimo's AI assistant is specialized for working with data. Unlike traditional assistants that only see the text of your program, marimo's assistant can also work with the values of variables in memory.

### When to trust AI assistance in AI/ML work

AI coding agents are not equally useful across all parts of an ML workflow. Knowing where to trust them and where to stay hands-on is a practical skill.

**Let AI handle the repetitive and structural work:**

- Data loading, imports, and boilerplate setup
- Exploratory analysis: summary statistics, distributions, missing value checks
- Generating initial visualizations (histograms, scatter plots, confusion matrices)
- Refactoring code into functions or reorganizing pipeline steps
- Extending an existing analysis with additional metrics or comparisons
- Transforming code (Python ↔ SQL)

These are tasks where the AI saves time and the risk of subtle errors is low. You can verify the output quickly by running it.

**Be careful with:**

- Evaluation logic and metric selection — the AI does not know your business context
- Edge cases in preprocessing — the AI may silently drop rows or mishandle categories
- Feature engineering decisions — domain knowledge matters more than code generation
- Production-critical pipelines — AI-generated code needs careful review before deployment

The principle is simple: use AI for speed on tasks you can verify, and keep control on tasks where mistakes are expensive or hard to detect.

### Context determines quality

The single most important factor in AI-assisted coding is not the model — it is the context you provide. A vague prompt produces vague code. A prompt that includes your actual variables, your data structure, and your intent produces code that runs with minimal editing.

This is what the hands-on exercise will demonstrate directly.

### Understanding LLM pricing

Before diving into the hands-on, it helps to understand how AI assistance is priced — because this directly affects which setup makes sense for your workflow.

Cloud models charge per token. A token is roughly ¾ of a word, so a 1,000-word notebook cell is about 1,300 tokens. Most providers charge separately for input tokens (your prompt + context) and output tokens (the generated code), with output tokens typically costing 3–5× more than input.

This matters for notebook work because the `@variable` context you pass to the AI adds input tokens. A large dataframe schema, a long feature list, or a complex notebook state all increase cost per request.

For a concrete, interactive comparison of cost vs quality across models, see [sanand0.github.io/llmpricing](https://sanand0.github.io/llmpricing/) — filter by "Coding" to see what matters for notebook work. Some highlights from current pricing (as of early 2026):

- High-end models like Claude Opus 4.6 cost ~$20 per million tokens but score 95% on benchmarks
- Mid-range models like GPT-5-mini cost ~$0.69 per million tokens at 83% quality
- Budget options like Gemini 2.5 Flash cost ~$0.17 per million tokens at 66% quality
- Open-source models like Qwen3-235B or DeepSeek-V3 cost $0.22–$0.30 per million tokens at 59–73% quality
- Local models through Ollama cost nothing per token once downloaded

The price-quality tradeoff is real but not linear — you can often get 80% of the quality at 10% of the cost. For most ML notebook tasks (generating cells, creating plots, refactoring), mid-range models are more than sufficient. Reserve premium models for complex multi-step reasoning.

Also worth knowing: reasoning models (like o3, o1) generate internal "thinking" tokens that you pay for but never see. These can be 10–30× more tokens than the visible output, which makes them significantly more expensive for routine coding tasks. Use reasoning models only when accuracy substantially outweighs cost.

For a full comparison of LLM pricing, including subscription plans: [aimultiple.com/llm-pricing](https://aimultiple.com/llm-pricing)

### Local versus cloud-hosted setups

There is no single best setup. The right choice depends on cost, speed, privacy, and control.

**Cost:**

Cloud models charge per token and heavy ML iteration adds up fast (see the pricing breakdown above). Local models through Ollama are free to run once downloaded — no per-token charges, no API keys, no billing surprises. For an interactive comparison: [sanand0.github.io/llmpricing](https://sanand0.github.io/llmpricing/)

**Speed:**

Cloud models respond faster and handle complex prompts better. Local models are slower, especially on machines without a dedicated GPU. In iterative ML work where you are generating and testing dozens of cells, that latency adds up. Try the same refactor prompt through both — the response time difference is immediately obvious.

**Privacy:**

Cloud providers see your notebook context — your data, your variables, your code. For public datasets and open-source work this is fine. For proprietary data, healthcare records, financial models, or anything under NDA, it is not. Local models keep everything on your machine.

**Control:**

With local models you choose the model version, control when it updates, and can run it air-gapped. In regulated environments this matters — you can audit exactly what is running. Cloud providers can change models, deprecate endpoints, or update behavior without notice.

**Cloud-hosted providers (OpenAI, Anthropic, Google):**

- usually stronger models with better reasoning
- less local setup, faster to get started
- best for exploration, prototyping, and non-sensitive data
- cost per token and data leaves your machine

**Local or private setups (Ollama, local providers):**

- better for sensitive data and controlled environments
- more privacy and deployment control
- no API cost
- often slower or less capable than frontier hosted models
- more setup overhead

#### The free alternative: Ollama Launch

You do not need a paid subscription to get agentic coding. **Ollama Launch** lets you run coding agents like Claude Code, OpenCode, Codex, and others — all powered by local open-source models. One command, no API keys, no monthly fees, no data leaving your machine.

In many AI/ML settings — corporate environments, healthcare data, financial models, student projects with no budget — sending notebook context to a cloud provider is either not allowed or not affordable. Ollama removes both barriers while keeping the agentic workflow intact.

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Launch a coding agent — interactive model selection on first run
ollama launch claude
ollama launch opencode
ollama launch codex
```

That is it. Ollama automatically configures authentication, endpoints, and model selection. No environment variables, no config files.

#### Comparative evaluation

The honest assessment across common ML/AI tasks:

| Task | Claude Code (cloud) | Ollama Launch (local) |
|---|---|---|
| Generate a preprocessing cell | ✅ Excellent | ✅ Good |
| Refactor multi-cell pipeline | ✅ Excellent | ⚠️ Limited |
| Debug reactive dependency issue | ✅ Excellent | ❌ Poor |
| Generate a matplotlib figure | ✅ Excellent | ✅ Good |
| Sensitive/proprietary data | ❌ Cloud only | ✅ Safe |
| Cost per session | Per token | Free |
| Setup complexity | Low | Low (with `ollama launch`) |

The pattern is clear: cloud models win on capability, Ollama wins on privacy, cost, and setup simplicity. For straightforward tasks like generating preprocessing cells, creating visualizations, and writing helper functions, the gap is small. For complex reasoning tasks, cloud models still win.

#### The practical approach

- Use **cloud** (Claude Code, OpenAI) for exploration, speed, and tasks where code quality matters most — complex refactoring, multi-step analysis, debugging reactive dependencies
- Use **local** (`ollama launch`) for sensitive data, proprietary workflows, environments where data cannot leave the machine, or when you have no budget for API costs
- Many teams use **both** — cloud for development and prototyping, local for production data and deployment environments

The right setup for your work will become clear quickly once you run the same task through both. For most ML development with non-sensitive data, start with Claude Code. For anything proprietary, Ollama with a capable local model is the pragmatic choice.

The advantage of marimo's architecture is that the `@variable` context mechanism works the same regardless of which model is behind it — your prompts stay short and your iterations stay fast whether you are using Claude Code with Anthropic's frontier models or `ollama launch` with a local model running on your laptop.

- Ollama: [ollama.com](https://ollama.com)
- Ollama models: [ollama.com/library](https://ollama.com/library)
- Ollama integrations: [ollama.com launch docs](https://docs.ollama.com/integrations/overview)
- marimo agents docs: [docs.marimo.io/guides/editor_features/agents/](https://docs.marimo.io/guides/editor_features/agents/)

---

## Hands-on Exercise: AI-Assisted AI/ML Development in marimo

This exercise walks through the full spectrum of AI integration — from configuring your setup to connecting your notebook with external systems. Each step increases the scope of what AI can do, and each step demonstrates a practical capability for AI/ML work.

The working loop throughout is: idea → code → result → refine. This is where AI becomes most useful.

Open `Module_3/module_3.py` from Module 3 for the guided exercises.

---

### Step 1 — Setting up AI in your notebook

Before AI can help with your ML workflow, it needs to be connected to a model provider and configured to match how you work.

**What to do:**

- Open marimo settings and configure your **AI provider** (OpenAI, Anthropic, Google, or a local model via Ollama)
- Configure your **code completion provider** (GitHub Copilot, Windsurf, or a custom provider)
- Set **custom prompts/rules** that guide all AI output

marimo works with hosted providers such as OpenAI, Anthropic, and Google, as well as local models served through Ollama and other OpenAI-compatible providers.

Several marimo AI features rely on your `marimo.toml` configuration file. Locate it with:

```bash
marimo config show | head
```

**Why this matters for AI/ML work:**

Custom rules are where you encode your team's conventions. In ML projects, consistency matters — if half your pipeline uses pandas and the other half uses polars, debugging gets harder. If your plots use different libraries or styles, your notebooks become hard to read.

marimo supports **custom rules** in settings so that AI output stays consistent across prompts and providers. For example:

```text
Always use matplotlib for plotting.
Prefer pandas over polars.
Use type hints for helper functions.
Use f-strings for string formatting.
```

Setting rules like these means every AI-generated cell follows the same conventions, regardless of which prompt triggered it. This is not just a preference — it is a way to keep AI-generated code compatible with the rest of your pipeline.

These rules are useful in workshop settings because they keep AI-generated code aligned with the style you are teaching.

---

### Step 2 — Generating code in an active ML workflow

The most common AI use case in ML development is generating new analysis code inside an existing workflow. The key difference from using a separate chat tool is that the AI can reference your actual data.

marimo is an AI-native editor with support for full-cell AI code generation:

- generating new cells from a prompt
- refactoring existing cells from a prompt
- generating entire notebooks
- inline autocompletion, similar to Copilot-style tools

There are four main ways to use AI in the editor:

- **Generate new cells** with the **Generate with AI** button at the bottom of the notebook
- **Refactor the current cell** with `Ctrl/Cmd-Shift-E`
- **Use the Chat panel** to ask notebook-level questions or generate cells from a side panel
- **Generate entire notebooks** from the command line with `marimo new "your prompt"`

**What to do:**

Use the **Generate with AI** button in `module_3.py` with these two demo prompts:

**Data quality check:**
> *"Find missing values in @df and summarize them clearly."*

**Visualization:**
> *"Show the distribution of age for each income group using a histogram or density plot for @df."*

**Refactor an existing cell.** Click into the preprocessing/modeling part of the notebook and press `Ctrl/Cmd-Shift-E`. Prompt:

> *"Refactor this cell so the preprocessing logic is moved into a helper function called `prepare_features`."*

Review the result. Does the function signature make sense? Does the cell still run correctly?

Also demonstrate: **formatting cells** and **autocomplete** features.

**Why this matters for AI/ML work:**

In both prompts, `@df` is doing real work. The AI is not guessing your column names — it reads them from the actual dataframe in memory. When it generates a histogram of `age` grouped by `income`, it knows those columns exist because it can see the dataframe schema.

marimo's AI assistant already has the notebook code as context. You can additionally pass variables and their values to the assistant by tagging them with `@`. For example:

- `@df` includes the dataframe `df` and its current state
- `@selected_features` includes the currently selected feature list
- `@results_df` includes the current results table

This is the difference between AI that writes plausible code and AI that writes correct code. In ML workflows, where dataframes change shape as you preprocess, filter, and transform, having the AI work from the current state — not the original state — prevents a whole class of errors.

The point of the exercise is not to accept AI output blindly. It is to review generated code in the same notebook where it will run.

---

### Step 3 — Observing how context affects AI quality

This is the most important exercise. It demonstrates the core principle: context quality determines output quality.

**What to do:**

Open the **Chat panel** and use this single prompt across all three chat modes:

> *"What patterns do you see between age, hours-per-week, and income in @df?"*

The Chat panel supports three modes:

- **Manual** — no tool access; the model responds only from the conversation and any manually injected context
- **Ask** — read-only tools plus context gathering, so the assistant can inspect the notebook
- **Agent (beta)** — everything in Ask mode plus the ability to edit notebook cells and run stale cells

**Why this matters for AI/ML work:**

The same question produces different quality answers depending on how much context the AI can access. In Manual mode, the AI can only reason abstractly. In Ask mode, it can look at your data and give specific observations. In Agent mode, it can actually run analysis and show you results.

This mirrors a real decision in ML workflows: when do you want a quick explanation (Manual), when do you want data-aware reasoning (Ask), and when do you want the AI to actually do the work (Agent)? The answer depends on the task:

- choose **Manual** when you want a pure explanation
- choose **Ask** when you want notebook-aware reasoning without edits
- choose **Agent** when you want the assistant to actually modify the notebook

For understanding a concept, Manual is fine. For exploring data, Ask is better. For generating and testing analysis code, Agent saves the most time.

marimo's AI workflow is tool-aware. The assistant can inspect notebook structure, gather context, and in stronger modes interact with notebook cells rather than just producing text. This is what makes it feel integrated into the editor instead of bolted on.

The prompt templates at [docs.marimo.io/guides/generate_with_ai/prompts/](https://docs.marimo.io/guides/generate_with_ai/prompts/) provide structured starting points for common ML tasks.

---

### Step 4 — External agents editing your notebook

Sometimes you need AI to work across multiple cells — refactoring a pipeline, reorganizing a notebook, or making coordinated changes. This is where external agents come in.

marimo supports external agents such as Claude Code, Codex, and Gemini CLI. These are useful when you want the assistant to work across multiple cells or operate on the notebook as a file rather than just generating one block of code at a time.

This matters because marimo notebooks are stored as plain `.py` files. External agents can read notebook structure directly instead of trying to reason over notebook JSON.

**What to do:**

Show the **CLAUDE.md** file from the marimo docs:

- Docs: [docs.marimo.io/guides/generate_with_ai/using_claude_code/](https://docs.marimo.io/guides/generate_with_ai/using_claude_code/)
- Blog: [marimo.io/blog/claude-code](https://marimo.io/blog/claude-code)

The quickstart:

```bash
curl https://docs.marimo.io/CLAUDE.md > ~/.claude/prompts/marimo.md
```

Then run:

```bash
# Terminal 1: start marimo with file watching
marimo edit notebook.py --watch

# Terminal 2: start Claude Code
claude
```

**Why this matters for AI/ML work:**

ML notebooks grow organically. You start with data loading, add preprocessing, try a model, add evaluation, try another model, add comparison charts. Eventually the notebook needs restructuring — splitting monolithic cells, extracting helper functions, reorganizing the flow. This is tedious to do manually and risky if you break dependencies.

An external agent like Claude Code can read the entire notebook (because marimo notebooks are plain `.py` files), understand the dependency graph, and make coordinated changes across cells. The `--watch` flag means your browser updates live as the agent edits, so you stay in the loop.

The CLAUDE.md file gives the agent marimo-specific knowledge — how reactive cells work, what `@app.cell` means, how to avoid multiple-definition errors. This is the difference between an agent that writes generic Python and one that writes valid marimo notebooks.

---

### Step 5 — Generating entire ML workflows from a prompt

Once you trust AI for individual cells, the next step is letting it scaffold an entire notebook. This is useful for prototyping, creating demos, or setting up the initial structure of an analysis.

**What to do:**

```bash
marimo new "Analyze employee salary trends"
```

Or from a file with a longer, more detailed prompt:

```bash
marimo new my_prompt.txt
```

This creates a full notebook with structure, UI elements, and data workflows.

**Why this matters for AI/ML work:**

The hardest part of many ML projects is getting started — setting up the imports, loading the data, writing the first exploratory cells, choosing an initial model. `marimo new` handles all of that from a single prompt.

This is particularly useful for:

- **Prototyping:** quickly testing whether an approach is worth pursuing before investing time in a full pipeline
- **Teaching:** generating starter notebooks for workshops or courses
- **Demos:** building end-to-end examples that show a complete workflow

The generated notebook is a starting point, not a finished product. But it gets you past the blank-page problem and into the iterative loop — which is where AI assistance is most productive.

---

### Step 6 — Making your agent smarter with Skills

Skills are reusable knowledge packages that make AI agents better at specific tasks — without requiring you to repeat instructions in every prompt.

**What to do:**

Install marimo's official skills:

```bash
npx skills add marimo-team/skills
```

You can target specific agents:

```bash
npx skills add marimo-team/skills --agent claude-code
npx skills add marimo-team/skills --agent opencode
```

- Skills docs: [docs.marimo.io/guides/generate_with_ai/skills/](https://docs.marimo.io/guides/generate_with_ai/skills/)
- Skills repo: [github.com/marimo-team/skills](https://github.com/marimo-team/skills)

**Why this matters for AI/ML work:**

Skills are folders of instructions, scripts, and resources that agents load dynamically when they are relevant. Unlike slash commands (which you trigger manually), skills activate automatically when the agent recognizes that they apply.

marimo's official skills help agents:

- Convert Jupyter notebooks to marimo notebooks
- Create bespoke interactive UI elements and widgets
- Author high-quality standalone notebooks following marimo best practices

In ML work, this means your agent consistently produces notebooks that follow marimo's reactive model, use the right UI patterns, and avoid common mistakes — without you having to remind it every time. It is the difference between an agent that writes generic Python in a notebook and one that writes idiomatic marimo.

---

### Step 7 — Connecting your notebook to external systems with MCP

The Model Context Protocol (MCP) turns your notebook from a standalone environment into a connected system.

MCP connects your notebook with external tools in two directions:

- **notebook → accessible externally** (marimo as MCP server)
- **external tools → accessible in notebook** (marimo as MCP client)

This turns your workflow into a connected system.

**What to do:**

**marimo as MCP server** — your notebook becomes accessible to external tools:

```bash
uv run --with="marimo[mcp]" marimo edit notebook.py --mcp --no-token
```

**marimo as MCP client** — external tools become accessible inside your notebook's Chat panel.

Connect Claude Code to your notebook via MCP:

```bash
claude mcp add --transport http marimo http://localhost:2718
claude code
```

- MCP docs: [docs.marimo.io/guides/editor_features/mcp/](https://docs.marimo.io/guides/editor_features/mcp/)

**Why this matters for AI/ML work:**

ML development does not happen in isolation. You need to pull data from databases, check documentation, interact with deployment systems, and coordinate with other tools. MCP provides a standard protocol for these connections.

When marimo acts as an MCP server, external applications can access your notebook state — your variables, your data, your model outputs. When marimo acts as an MCP client, you can bring external capabilities into your notebook's AI workflow.

This is the step where the notebook stops being a standalone analysis tool and becomes part of a larger system. For teams working on ML pipelines, this means the notebook can be the interface between data exploration and the systems that depend on its outputs.

---

### Step 8 — Setting up local AI with Ollama

The presentation covered why local setups matter. This step shows how to set it up in marimo.

**What to do:**

**Connecting Ollama to marimo (built-in AI features):**

You can use Ollama directly with marimo's built-in AI features — Generate with AI, refactoring, chat panel, and code completion — without any external agent. In marimo settings → AI, set:

```toml
[ai.completion]
model = "ollama/qwen2.5-coder:7b"
base_url = "http://localhost:11434"
```

Optionally set these as environment variables so you can switch models without touching settings:

```bash
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=qwen2.5-coder:7b
```

**Using Ollama-powered agents with marimo:**

For the full agentic workflow (agent reads and edits your notebook), use the same `--watch` pattern as Claude Code:

```bash
# Terminal 1
marimo edit notebook.py --watch

# Terminal 2
ollama launch opencode
```

Or connect via the Agent Client Protocol (ACP) directly inside marimo: enable the agent feature flag in Settings → Lab, open the agent panel from the sidebar, and select your agent from the dropdown.

> **Practical notes:**
> - Coding agents work best with models that have at least 64K context windows — Ollama configures this automatically during launch
> - Bigger models need more RAM/VRAM — check [ollama.com/library](https://ollama.com/library) for size requirements
> - If a model is too slow, step down to a smaller variant (e.g. `:7b` instead of `:14b`)
> - Ollama can run multiple models — pull several and switch between them to find the right speed/quality balance for your hardware

**Recommended local models for ML notebook work:**

| Model | RAM needed | Best for | Notes |
|---|---|---|---|
| `qwen3-coder` | 16GB+ | General coding, refactoring | Best overall local coding model |
| `qwen2.5-coder:7b` | 8GB+ | Lighter tasks, faster responses | Good if RAM is limited |
| `deepseek-coder-v2:16b` | 24GB+ | Complex ML code | Stronger reasoning, needs more VRAM |
| `phi-4` | 8GB | Simple tasks, fast iteration | Lightweight, good for quick experiments |

**Why this matters for AI/ML work:**

Try the same prompt from Step 2 — generating a visualization or refactoring a cell — through Ollama instead of a cloud model. Compare the output quality and response time. That direct comparison makes the tradeoffs from the presentation concrete and personal to your hardware.

#### Discussion prompt

After the hands-on exercises, ask:

- Which parts of this workflow would you trust to a hosted provider?
- Which parts would you keep local because of privacy or control?
- When is inline completion enough, and when do you actually want an agent?

That discussion ties the whole module together: AI quality depends on context, but the right setup depends on your constraints.

---

## Key Takeaways

1. **Context is the differentiator.** AI that can see your actual data, variables, and pipeline state produces better code than AI working from text alone. The `@variable` mechanism is what makes this practical.

2. **Match the tool to the task.** Code completion for small edits. In-cell generation for new analysis. Chat panel for notebook-aware reasoning. External agents for multi-cell refactoring. Full notebook generation for scaffolding. Each level of AI integration serves a different part of the ML workflow.

3. **Trust AI where you can verify quickly.** Boilerplate, exploration, visualization, and refactoring are high-value AI tasks because you can check the output by running it. Reserve manual attention for evaluation logic, edge cases, and production code.

4. **Your setup should match your constraints.** Cloud for speed and quality, local for privacy and control. `ollama launch` gives you the full agentic workflow for free. The notebook architecture supports all setups — choose based on your data sensitivity and workflow needs.

5. **The notebook is the prompt.** In marimo, AI is not a separate tool you switch to — it is part of the environment where your code runs. That integration is what makes AI-assisted ML development practical rather than theoretical.

---

The right AI setup is the one that fits your data constraints, your workflow speed, and your task complexity. What all options share is marimo's automatic variable context — your current state is always available to the agent, so your prompts stay short and your iterations stay fast regardless of which model is doing the work.

Module 5 brings everything full circle: once your interactive, AI-assisted, reproducible notebook is working, how do you turn it into reusable systems that others can depend on?
