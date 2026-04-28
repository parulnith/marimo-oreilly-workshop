# The Modern AI and ML Development Stack
## Powered by marimo
---

## Table of Contents

- [Preface](#preface)
- [Module 1: Why Interactive Programming Environments Matter for AI and ML](#module-1-why-interactive-programming-environments-matter-for-ai-and-ml)
  - [1.1 Interactive Environments in the Modern AI/ML Stack](#11-interactive-environments-in-the-modern-aiml-stack)
  - [1.2 When Traditional Notebook Systems Break Down](#12-when-traditional-notebook-systems-break-down)
  - [1.3 Why Reactive Execution Is a Better Alternative](#13-why-reactive-execution-is-a-better-alternative)
  - [1.4 Hands On with marimo: A Modern Programming Environment](#14-hands-on-with-marimo-a-modern-programming-environment)
- [Module 2: Reproducibility as a Baseline for Trustworthy AI](#module-2-reproducibility-as-a-baseline-for-trustworthy-ai)
  - [2.1 The "It Works on My Machine" Problem](#21-the-it-works-on-my-machine-problem)
  - [2.2 The Hidden Culprits: Dependencies and Environments](#22-the-hidden-culprits-dependencies-and-environments)
  - [2.3 Version Control and Reviewable Experiments](#23-version-control-and-reviewable-experiments)
- [Module 3: Why Interactivity Accelerates AI Discovery](#module-3-why-interactivity-accelerates-ai-discovery)
  - [3.1 Interactive Computation as a Unified System](#31-interactive-computation-as-a-unified-system)
  - [3.2 Interactive Data in Model Development](#32-interactive-data-in-model-development)
  - [3.3 Visual Feedback for Analysis and Debugging](#33-visual-feedback-for-analysis-and-debugging)
- [Module 4: How to Use AI Coding Agents for AI/ML Development](#module-4-how-to-use-ai-coding-agents-for-aiml-development)
  - [4.1 When to Let AI Agents Write Code for You](#41-when-to-let-ai-agents-write-code-for-you)
  - [4.2 Giving AI Coding Agents the Context They Need](#42-giving-ai-coding-agents-the-context-they-need)
  - [4.3 Choosing the Right AI Coding Agent Setup](#43-choosing-the-right-ai-coding-agent-setup)
- [Module 5: From Interactive Work to Reusable Systems](#module-5-from-interactive-work-to-reusable-systems)
  - [5.1 Turning Your Work Into Executable Scripts](#51-turning-your-work-into-executable-scripts)
  - [5.2 Publishing Flexible, Interactive Data Apps](#52-publishing-flexible-interactive-data-apps)
  - [5.3 From Outputs to Published Artifacts](#53-from-outputs-to-published-artifacts)
  - [5.4 From Interactive Code to Importable Modules](#54-from-interactive-code-to-importable-modules)

---

## Preface

Interactive code-writing environments such as Jupyter Notebook are beloved by data scientists and ML researchers because they combine software code, computational output, and explanatory text in a single document. They are where the biggest breakthroughs in AI were built — from GPT to CLIP to DALL-E.

But these traditional notebooks carry real limitations. Hidden state, out-of-order execution, and poor reproducibility undermine the very work they're meant to support. A 2019 study of 1.4 million Jupyter notebooks on GitHub found that only 24% could be executed without errors, and a mere 4% actually reproduced their original results.

This course is your guide to a better way of working with notebooks. It introduces **marimo**, a next-generation open-source Python notebook designed for reproducible, interactive, and shareable computation. Across five modules, you'll learn not just how to use marimo, but *why* it exists — and how the modern AI/ML development stack fits together.


---

## Module 1: Why Interactive Programming Environments Matter for AI and ML

In this module we'll see where notebooks do well, to seeing where they break, to experiencing a fundamentally better alternative, to getting hands-on with it yourself.

### 1.1 Interactive Environments in the Modern AI/ML Stack

#### Why Notebooks Matter

Interactive programming environments are a fundamental part of today's AI and ML development stack. They aren't a nice-to-have — they're where the actual work happens.

AI development isn't like building a web app. You don't write code, compile, and ship. You explore, experiment, and iterate — constantly moving between code, data, and results. This tight loop is the core rhythm of ML work:

1. **Write** — A few lines of code: a transform, a model call, a visualization
2. **See** — Immediately inspect the result: a chart, a table, a prediction
3. **Adjust** — Change a parameter, fix an assumption, try a different approach

This loop runs hundreds of times a day. The faster it runs, the faster you learn.

#### Where This Loop Matters Most

This write-see-adjust cycle shows up everywhere in AI/ML work:

- **Exploring a new dataset** — You need to see shapes, distributions, missing values, and outliers before you can model anything.
- **Evaluating model outputs** — You judge quality by looking at predictions, comparing responses, tweaking prompts — not by compiling.
- **Tuning experiments** — Change a hyperparameter, re-train, check the loss curve. Repeat. The feedback loop *is* the experiment.
- **Feature engineering** — Try a transform, visualize the effect, keep it or discard it. Every decision needs immediate visual proof.

In every case, you need to see intermediate results to decide what to do next.

#### The People Who Built AI Used Notebooks

This isn't a niche workflow for beginners. Alec Radford — the first author of the original GPT paper and the researcher behind GPT-2, CLIP, DALL-E, and Whisper — did much of his groundbreaking work inside Jupyter Notebooks. No PhD. No fancy IDE. Just a notebook and a big idea. Sam Altman called him an "Einstein-level genius."

The most consequential AI breakthroughs of the last decade were prototyped in notebooks. There's a reason for that: notebooks match how AI research actually works.

#### Hands-On: A Working Notebook

To experience this firsthand, we build a simple compound interest calculator in a Jupyter notebook. It's not an ML problem — intentionally. The point is the *workflow*, not the domain.

```python
def compound_interest(principal, rate, years):
    """Calculate compound interest year by year."""
    values = [principal]
    for year in range(1, years + 1):
        values.append(values[-1] * (1 + rate))
    return values
```

We set parameters, compute results, and plot the growth curve:

```python
principal = 1000
rate = 0.07
years = 20

growth = compound_interest(principal, rate, years)
print(f"After {years} years: ${growth[-1]:,.2f}")
```

Then we compare multiple rates on a single chart and build a summary table. The notebook flows naturally: define, compute, visualize, compare. Each cell builds on the last. Change a parameter, re-run the cells below, and see how the results shift.

This is the write-see-adjust loop in its simplest form. And it works beautifully — until it doesn't.

---

### 1.2 When Traditional Notebook Systems Break Down

#### The Imperative Trap

In a Jupyter notebook, you run a cell and it mutates memory. Then you run another cell and it mutates memory again. But Jupyter doesn't know how your cells are related. It has no dependency graph.

This means two things go wrong.

#### Problem 1: Out-of-Order Execution

You change a value in one cell but forget to re-run the cells that depend on it. Now the code on your screen doesn't match the variables in memory. Your notebook becomes a patchwork of outputs from different states — and nothing warns you.

In our compound interest notebook, one cell sets the parameters:

```python
principal = 1000
rate = 0.07
years = 20
```

Downstream cells then:

- compute the growth path
- print the final balance
- draw a plot titled with the number of years
- build a summary table with a `years_used` column
- run a simulated expensive downstream step that stores a report

Now change `years = 20` to `years = 50` and re-run **only the parameter cell**.

What happens?

- The code on screen now says `years = 50`
- But the printed result still says `After 20 years`
- The plot title still says `20 years`
- The summary table still shows `years_used = 20`
- The expensive report still reflects 20 years

The notebook looks plausible at a glance, but it is now inconsistent. A careful user can manually re-run every downstream cell and fix it. The problem is that Jupyter gives you no structural protection if you forget one.

#### Problem 2: Hidden State

You delete a cell, but the variable it defined is still alive in memory. Other code still refers to it. Your notebook looks clean, but invisible state is silently driving your results.

Delete the `compound_interest()` function cell from the notebook. The cells that call it still work — the function is a ghost in memory. Restart the kernel and run all, and it crashes: `NameError: name 'compound_interest' is not defined`. The notebook that looked perfect was broken the entire time.


#### This Isn't a Minor Issue

A landmark study by Pimentel et al. (2019) examined 1,159,166 unique Jupyter notebooks collected from 264,023 GitHub repositories. The findings were stark:

- **Only 24.11%** of notebooks executed without errors
- **Only 4.03%** produced the same results as their stored outputs
- **36%** of notebooks had cells executed out of order
- **77%** had skips in execution counters, indicating hidden state

These aren't contrived edge cases. Out-of-order execution and hidden state are the norm, not the exception. The better the notebook experience feels, the more dangerous these issues become — because you trust the tool.

> **Source:** Pimentel, J.F., Murta, L., Braganholo, V., and Freire, J. "A Large-scale Study about Quality and Reproducibility of Jupyter Notebooks." *IEEE/ACM International Conference on Mining Software Repositories*, 2019.

---

### 1.3 Why Reactive Execution Is a Better Alternative

#### What If the Notebook Knew About Dependencies?

What if changing a value in one cell automatically updated everything that depends on it? What if deleting a cell also scrubbed its variables from memory?

This is the idea behind **reactive execution**. Instead of treating a notebook as a sequence of imperative commands that mutate a shared workspace, a reactive notebook models the cells as a **dependency graph**. 

#### Seeing It in Action

We rebuild the same compound interest calculator — the exact same logic — in a reactive notebook. But we do it in two stages.

First, in `1_2_marimo_reactive_workflow.py`, we keep the inputs as plain Python variables:

```python
principal = 1000
rate = 0.07
years = 20
```

And the things that broke before? They can't break here:

- **Out-of-order execution is impossible.** When you change a parameter, all dependent cells update. There's no way to have stale outputs.
- **Hidden state is impossible.** Delete a cell, and its variables are immediately scrubbed from memory. Downstream cells that depended on them show errors instantly. No ghosts.

#### Gallery: What's Possible

The reactive model doesn't just fix problems — it enables entirely new ways of working. Here are some examples from the marimo community gallery:

- **Embedding Visualizer** — Select points in embedding space and get them back as a dataframe in Python. Your visualization is an input, not just an output.

- **Reactive Plots** — Select data points on a chart, get the selection back in Python, run analysis, see the plot update. A tight bidirectional loop.
- **Federated Learning Simulation** — Interactive simulation of hospitals training local models with FedAvg aggregation. Serious ML research in a notebook.

These are all built in the same tool, using the same reactive model.

---

### 1.4 Hands On with marimo: A Modern Programming Environment

#### What Is marimo?

The reactive notebook you just experienced is called **marimo**. It's an open-source Python notebook [github.com/marimo-team/marimo](https://github.com/marimo-team/marimo)

#### Installing marimo

This is the simplest way to get ready for the workshop.

**In the browser (zero install):**

If you do not want to install anything locally, open:

- [https://molab.marimo.io](https://molab.marimo.io)
- [https://marimo.new](https://marimo.new)

This opens marimo in the browser using Molab.

**Locally with pip:**

If you want to work locally, this is the easiest option for most participants.

Mac / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install marimo
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install marimo
```

If that works, marimo is installed correctly.

Before opening the workshop files, start with the official intro notebook:

```bash
marimo tutorial intro
```

This is a good way to quickly see the main parts of the marimo interface before moving into the course materials.

**Clone the workshop repository:**

Once marimo is installed, clone the workshop repository and move into it.

```bash
git clone https://github.com/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop.git
cd marimo-for-ai-and-ml-development-oreilly-workshop
```

If you want the virtual environment inside the repo folder, you can create and activate it there before installing marimo.

Mac / Linux:

```bash
git clone https://github.com/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop.git
cd marimo-for-ai-and-ml-development-oreilly-workshop
python3 -m venv .venv
source .venv/bin/activate
pip install marimo
```

Windows PowerShell:

```powershell
git clone https://github.com/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop.git
cd marimo-for-ai-and-ml-development-oreilly-workshop
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install marimo
```

**Optional: install with uv**

`uv` is a faster Python environment and package tool. If you already use it, you can install marimo this way instead.

Mac / Linux:

```bash
uv venv
source .venv/bin/activate
uv pip install marimo
marimo tutorial intro
```

Windows PowerShell:

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install marimo
marimo tutorial intro
```

You may also see `uvx` in the marimo docs. `uvx` is for quickly running a tool without installing it into your project. For this workshop, `pip` or `uv pip install` is easier.

**Per-notebook sandbox (isolated dependencies):**

Later in the workshop, we will use sandbox mode for reproducibility:

```bash
marimo edit --sandbox notebook.py
```

This gives a notebook its own isolated environment.

#### Essential Commands

| Command | What it does |
|---|---|
| `marimo.new` | Opens a new notebook in molab (browser, zero install) |
| `marimo edit` | Opens the file browser to pick or create a notebook |
| `marimo edit Module_1/1_2_marimo_reactive_workflow.py` | Opens a specific workshop notebook in the editor |
| `marimo edit --sandbox notebook.py` | Same, with isolated per-notebook dependencies |
| `marimo run Module_1/1_3_marimo_ui_elements.py` | Runs a notebook as a read-only app (code hidden) |
| `python Module_1/1_2_marimo_reactive_workflow.py` | Executes a notebook as a script (no UI) |

#### The Editor Interface

When you open a marimo notebook, you'll see:

**Cell area (center)** — Where your code lives. Each cell is independent. Output renders directly below. Hover over a cell to see its controls: run, add, delete, move, hide code.

**Keyboard shortcuts:**

- `Ctrl/Cmd + Enter` — run the current cell
- `Shift + Enter` — run and move to the next cell

**Cell status indicators:**

- Green — up to date
- Yellow — stale (inputs changed, needs re-run; only in lazy mode)
- Red — error
- Spinner — currently running

**Sidebar panels (right side):**

- **Variables** — Every variable in your notebook: which cell defines it, its type, current value. The "no hidden state" guarantee, made visible.
- **Dependency graph** — The actual DAG. Cells are nodes, variable references are edges. Click a node to jump to that cell.
- **Live Docs** — Hover over a function, see its docstring, parameters, and examples. No need for `help()`.
- **Package management** — Import a missing package, marimo prompts you to install with a click.
- **Logs** — Print statements and execution logs.

**Edit mode vs. App mode:**

- **Edit mode** — The default. Full editing capability, code visible.
- **App mode** — Toggle in the editor or run `marimo run notebook.py` from the CLI. Code is hidden. Only outputs and UI elements are visible. Your notebook becomes an interactive web app — zero code changes needed.

At this point in a live session, it is useful to show participants how to run a cell, how outputs appear below the cell, and what the sidebar panels expose. Once they have seen the mechanics, the deeper ideas land much more easily.

#### Editor Features That Matter in Practice

The marimo editor is not just a place to type code. It is a browser-based IDE designed for notebook work, with features that are especially useful when you are working with data and experiments.

**Dataflow tools**

marimo includes several tools for understanding notebook structure:

- **Variables panel** — inspect current variables, types, and values
- **Dependency graph** — see how cells depend on one another
- **Minimap / dataflow navigation** — move through larger notebooks more easily

These features make the notebook's execution model visible. Instead of guessing what depends on what, you can inspect the graph directly.

**Sidebar and developer panel**

The sidebar is designed to keep notebook state, docs, logs, and tools close at hand. In practice, this means you can inspect variables, check logs, look at documentation, and manage packages without leaving the editor.

Both the sidebar and the developer panel are customizable:

- Reorder panels by dragging them within a section
- Move panels between the sidebar and developer panel by dragging them
- Hide panels by right-clicking a panel icon and choosing the relevant option

These layout preferences persist across sessions. Panels also adapt to where they are placed: a compact vertical layout in the sidebar, and a wider horizontal layout in the developer panel.

**Package management**

marimo integrates package management into the editor. If you import something that is missing, marimo can prompt you to install it directly instead of forcing you to drop out to the shell first.

**Module autoreloading**

If your notebook imports code from a local Python module and that module changes, marimo can detect it and tell you which cells need to be rerun. This is especially useful when notebooks are part of a larger project rather than isolated files.

**Code intelligence**

marimo supports modern code-editing features expected from an IDE:

- code completion
- language server support (LSP) for diagnostics and code intelligence
- live documentation previews
- optional AI-assisted coding

This matters because marimo is not asking you to trade away real editor features in exchange for notebook interactivity.

**Right-click menus**

marimo supports context-sensitive right-click menus in the editor. Right-click on a cell to open actions relevant to that cell. Right-click on the create-cell button (the plus icon) to choose what type of cell to create. This is especially useful in a live workshop because participants can discover common actions directly from the interface instead of memorizing commands.

**Command palette**

Hit `Cmd/Ctrl+K` to open the command palette. This is a fast way to discover and run editor actions without hunting through the interface.

**Slides from notebooks**

marimo notebooks can also be used to create slides. This is useful when you want one artifact to serve both as a working notebook and as a presentation. In practice, this means you can build an interactive explanation in marimo and then present it directly, instead of rewriting the same material in a separate slide tool.

For this workshop, the key point is conceptual: marimo is not just a notebook runtime. It is also a presentation surface. That makes it easier to move from exploration to explanation without leaving the same environment.

**Share on the online playground**

You can also get a shareable link to a notebook through marimo's online playground. This is useful when you want to send someone a live notebook experience without asking them to install anything locally.

The playground uses WebAssembly, so many packages work there, but not every package on PyPI is supported. Local files are also not synchronized automatically to the playground.

**Export to static HTML**

If you want to share the current view of a notebook as a static artifact, marimo can export it to HTML from the notebook menu. This is useful when the audience does not need to run the code and you just want to share the rendered results.

#### How It Works: The DAG

Every marimo notebook is modeled as a **directed acyclic graph (DAG)** on cells. marimo reads your code using static analysis — without running it — and determines what each cell defines and what it references. From there, it builds a dependency graph.

When you run a cell:

1. marimo checks what variables that cell defines
2. It finds all other cells that reference those variables
3. It re-runs those cells automatically — or, in **lazy mode**, marks them as stale (shown in yellow) and waits for you to run them manually

Lazy mode is useful when cells are expensive to run — a model training step, a large data load, a slow API call. Rather than re-running everything on every change, marimo marks affected cells as stale and lets you decide when to update them. Toggle it in the notebook's runtime settings.

When you delete a cell:

1. marimo removes the cell's variables from memory
2. Dependent cells are invalidated immediately

It's like a spreadsheet: change a cell and the formulas update. The dependency graph is the thing that makes everything else possible — reactivity, no hidden state, deterministic execution, and the ability to run notebooks as apps or scripts.

#### A Quick UI Demo

Before moving into the workshop notebooks, it can be helpful to show a few UI elements in a tiny marimo notebook so participants see that interactivity is built directly into the Python workflow:

```python
import marimo as mo

model = mo.ui.dropdown(
    options=["Logistic Regression", "Random Forest", "XGBoost"],
    value="Random Forest",
    label="Model",
)
threshold = mo.ui.slider(start=0.1, stop=0.9, step=0.1, value=0.5, label="Decision threshold")
split = mo.ui.dropdown(
    options=["Train", "Validation", "Test"],
    value="Validation",
    label="Dataset split",
)

mo.vstack([model, threshold, split])
```

Then, in a second cell:

```python
mo.md(
    f"""
    Evaluating **{model.value}** on the **{split.value}** split
    with a decision threshold of **{threshold.value:.1f}**.
    """
)
```

This is a useful live demo because it lets you quickly point out several things at once:

- UI elements are ordinary Python objects
- their current values are available through `.value`
- downstream cells update automatically when inputs change
- the notebook can feel like an app without any callback wiring


#### No Magic Commands

Jupyter inherits IPython's "magic commands" — special directives prefixed with `%` or `%%` that control kernel behaviour. A common one is `%matplotlib inline`, which tells the kernel to render plots inside the notebook rather than launching a separate window:

```python
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.show()
```

These aren't Python — they're interpreted by the IPython layer and have no meaning outside it. New users trip over them; they don't appear in autocomplete; they make copy-pasted code fail in plain scripts.

marimo doesn't use magic commands. The same plot just works:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.show()
```

This is valid Python in any context — a script, a CI job, a text editor. Nothing extra required.

#### Cell Outputs

In marimo, the **last expression in a cell** is its output — displayed directly below the cell by the editor. Outputs can be anything: a plot, a dataframe, a number, a trained model summary. You don't need `print()` for most things; just put the value last:

```python
import matplotlib.pyplot as plt
import numpy as np

plt.plot(np.array([0, 1, 4, 9, 16]))
plt.gca()   # this is the output — the plot renders below the cell
```

This matters because it keeps cells clean and intentional. Each cell has one primary output, and that output is always visible and always in sync with the code above it.

#### Markdown and LaTeX

Cells don't have to contain Python. marimo supports **Markdown cells** for documentation, explanations, and section headers — the same way Jupyter does, but written in Python using `mo.md()`:

```python
import marimo as mo

mo.md("""
# Experiment Results

This section compares the loss curves for three learning rates.
The optimal rate was found to be **0.01** across all runs.
""")
```

Markdown cells can also include **LaTeX** for mathematical notation, using standard `$...$` inline syntax or `$$...$$` for display equations:

```python
mo.md(r"""
The cross-entropy loss is defined as:

$$L = -\sum_{i} y_i \log(\hat{y}_i)$$

where $y_i$ is the true label and $\hat{y}_i$ is the predicted probability.
""")
```

This makes marimo notebooks self-documenting — code, results, and explanation all in one readable document that can be exported as HTML or PDF for sharing.

#### Constraints

To keep the dependency graph clean, marimo enforces two rules:

1. **No duplicate variable names across cells.** For example, if one cell says:

```python
x = 10
```

and another cell says:

```python
x = 20
```

then downstream cells would not know which `x` to use. marimo shows an error immediately instead of allowing that ambiguity.

2. **No cycles between cells.** For example, if one cell says:

```python
a = b + 1
```

and another says:

```python
b = a + 1
```

then neither cell can run first. That creates a cycle, and marimo prevents it.

These constraints have a small learning curve but are easy to understand. And they encourage you to write functional, well-structured code — which is good practice regardless.

#### The .py File Format

Every marimo notebook is stored as a pure Python file. Open it in any text editor:

```python
import marimo

app = marimo.App()

@app.cell
def _(mo):
    mo.md("# Hello, marimo!")
    return

@app.cell
def _():
    x = 42
    return (x,)

@app.cell
def _(x):
    y = x + 1
    y
    return (y,)

if __name__ == "__main__":
    app.run()
```

Each cell is a function decorated with `@app.cell`. The function's parameters are the variables it reads; its return values are the variables it defines. The `if __name__ == "__main__"` block means you can run it as a script: `python notebook.py`.

This is just Python. You can version it with Git, review it in a pull request, import functions from it, or run it as a script. That's fundamentally different from Jupyter's JSON format.

marimo notebooks can also be **exported as standalone HTML or PDF** — a static snapshot of your code and outputs that anyone can view without installing Python. From the editor, use the export button in the top bar. From the CLI:

```bash
marimo export html notebook.py -o notebook.html
marimo export pdf notebook.py -o notebook.pdf
```

This makes it easy to share results with stakeholders who don't need to run the code — just the document.



#### What's Next
Quiz

---

## Module 2: Reproducibility as a Baseline for Trustworthy AI

There's a big difference between just running your code again and reliably getting the same results across different computers and over time. Running code again just means pressing a button. Reproducibility means that anyone — on any machine, at any point in the future — gets the same result from the same code. That guarantee is hard to achieve and easy to lose, and losing it is particularly costly in AI work where the output of your notebook is a model or a metric that others will rely on.

This module covers where reproducibility breaks down, what causes it, and how marimo addresses it directly — through environment pinning, pure-Python file format, and consistent execution wherever Python runs.

---

### 2.1 The "It Works on My Machine" Problem

*Reproducibility needs to be built into the environment itself — not bolted on afterwards.*

You write code, it runs cleanly, and you send it to a colleague. They run the same code in a slightly different environment and get a different result — or it fails entirely. The problem is not the logic. The problem is everything around it.

The Pimentel study measured this at scale: of 1.4 million Jupyter notebooks on GitHub, only 4% reproduced their original results when re-run. The majority of failures were not bugs — they were environmental drift. Code that was never wrong, running in a context that no longer matched the one it was written for.

> 💡 **Try it — `Module_2/2_1_environment_drift.ipynb`**
>
> **Example 1 — scikit-learn version change.** The notebook uses `CalibratedClassifierCV(method="temperature")`. Run it in scikit-learn `1.8.0` and it works. Run it in `1.7.2` and it fails. Same code, different outcome.
>
> **Example 2 — pandas API change.** The notebook reads a CSV using `delim_whitespace=True`, an argument removed in pandas 3.0. In pandas 1.x it runs silently. In pandas 3.x it raises an error.
>
> | | pandas 1.x | pandas 3.x |
> |---|---|---|
> | `delim_whitespace=True` | works | raises an error |
>
> Two failure modes, one pattern: same code, different environment, different outcome, no warning.

---

### 2.2 The Hidden Culprits: Dependencies and Environments

*Reproducibility needs to be built into the environment itself — not bolted on afterwards.*

You write code, it runs cleanly, and you send it to a colleague. They run the same code in a slightly different environment and get a different result — or it fails entirely. The problem is not the logic. The problem is everything around it.

The Pimentel study measured this at scale: of 1.4 million Jupyter notebooks on GitHub, only 4% reproduced their original results when re-run. The majority of failures were not bugs — they were environmental drift. Code that was never wrong, running in a context that no longer matched the one it was written for.

> 💡 **Try it — `Module_2/2_1_environment_drift.ipynb`**
>
> **Example 1 — scikit-learn version change.** The notebook uses `CalibratedClassifierCV(method="temperature")`. Run it in scikit-learn `1.8.0` and it works. Run it in `1.7.2` and it fails. Same code, different outcome.
>
> **Example 2 — pandas API change.** The notebook reads a CSV using `delim_whitespace=True`, an argument removed in pandas 3.0. In pandas 1.x it runs silently. In pandas 3.x it raises an error.
>
> | | pandas 1.x | pandas 3.x |
> |---|---|---|
> | `delim_whitespace=True` | works | raises an error |
>
> Two failure modes, one pattern: same code, different environment, different outcome, no warning.

---

### 2.3 Version Control and Reviewable Experiments

*Your environment shapes your results, even when you cannot see it.*

Environmental drift comes from three sources. **Library versions** change APIs and defaults between releases. **Python itself** changes behaviour across versions. **Transitive dependencies** shift when anything upstream updates.

The usual fix is a `requirements.txt`. But it lives outside the notebook and depends on manual updates. It goes out of date quickly.

#### How marimo solves this: inline dependencies

When you run a marimo notebook with `--sandbox`, it creates an isolated environment using `uv` and stores everything inside the notebook file itself:

If you import a missing library, marimo prompts you to install it and updates this block automatically. The next time the notebook runs in sandbox mode, the environment is rebuilt before execution. No separate file. No manual sync. The notebook and its environment stay together.

> **Note:** this only applies to `--sandbox`. In a standard `.venv`, you still manage dependencies yourself.

> 💡 **Try it — `Module_2/2_2_sandboxed_environment.py`**
>
> Run the notebook and inspect the active Python, `pandas`, and `matplotlib` versions. Then reopen it in sandbox mode:
> ```bash
> marimo edit --sandbox Module_2/2_2_sandboxed_environment.py
> ```


#### The file format problem

Jupyter notebooks are stored as JSON. Two lines of code become dozens of lines of structural wrapping — cell type, execution count, output blobs, metadata. Re-run a single cell and all of that updates, even if your code didn't change. The signal is buried in the noise.

A marimo notebook is a plain `.py` file. Change one cell and the diff shows exactly that cell. You can review it in a pull request, use `git blame` on a specific line, and resolve merge conflicts in any text editor.

> 💡 **Try it — `Module_2/2_2_sandboxed_environment.py`**
>
> Run the notebook. It shows a live one-line diff for a single code change, then the equivalent Jupyter diff for the same change. The difference is immediate.

#### Running marimo everywhere

Because marimo notebooks are plain Python files, they run consistently across every environment — no format conversion, no extra configuration.

| Environment | How |
|---|---|
| **Terminal** | `marimo edit notebook.py` — open as an interactive notebook |
| **App** | `marimo run notebook.py` — serve as a web app, code hidden and uneditable |
| **Sandbox** | `marimo edit --sandbox notebook.py` |
| **VS Code** | Open the `.py` file directly in VS Code, or use the official [marimo VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) for a more integrated notebook experience |
| **molab** | [molab.marimo.io](https://molab.marimo.io) — marimo in the cloud, no install needed |
| **JupyterLab** | Install the [marimo JupyterLab extension](https://github.com/marimo-team/marimo-jupyter-extension) |
| **Script** | `python notebook.py` |

for script,

```
x = 10
y = 20
print("Sum =", x + y)
```

The same `.py` file works in all of them. No conversion, no format mismatch, no "it worked in Jupyter but not here."

> **On outputs:** marimo doesn't store outputs in the file — which keeps diffs clean. When you do want a visual record, export to HTML or IPYNB from the command line, or enable auto-snapshot to save outputs to a local folder as you work.

---

## Module 3: Why Interactivity Accelerates AI Discovery

Interactivity is most valuable when it turns a notebook into a single live system: data, controls, models, visualizations, and selections all working together and updating automatically. In this module, participants use one prepared marimo notebook, `module_3.py`, to move through that workflow end to end.

---

### Presentation

Interactive computation as a unified system means that data, models, visualizations, and user input are all part of the same live graph. In marimo, widgets are variables, tables can become inputs, model outputs can feed new analysis, and visual changes propagate automatically through the notebook.

That is the core idea of this module. The goal is not to write a notebook from scratch. The goal is to experience what it feels like when exploration, modeling, and debugging happen in one place without breaking flow.

### Hands-on Exercise (guided in marimo)

Open the prepared notebook:

```bash
marimo edit --sandbox Module_3/module_3.py
```

This notebook already contains the full workflow. Participants work through it as a guided exercise.

#### Part 1: Start with the data

Start with the Adult Income dataset itself before moving into visual exploration:

- the plain `df` output for a baseline table view
- `mo.ui.data_editor(df)` for editable tabular input

Use these to inspect columns, scan values, and show that tabular data can
become part of the computation. The notebook includes a reactive summary below
the editable sample so participants can see that edits flow into downstream
output immediately.

Presenter cue:

- For `mo.ui.data_editor(df)`: explain that it is a data editor component for editing tabular data.

#### Part 2: Move into visual exploration

The notebook then introduces marimo's visual exploration tools:

- `mo.ui.data_explorer(df)` for chart-based exploration
- `mo.ui.dataframe(df)` for interactive table inspection

Use these to explore distributions, inspect patterns, and decide what is worth
carrying forward into the modelling step.

Presenter cues:

- For `mo.ui.data_explorer(df)`: build a quick chart with `occupation` on the x-axis, `count` on the y-axis, and color by `sex` so participants can see how the explorer helps surface patterns visually without writing plotting code.
- For `mo.ui.dataframe(df)`: use the `workclass` column as an example. Show attendees how to sort that column and then clear the sort again.

#### Part 3: Control the modeling workflow

The notebook includes live controls such as:

- `mo.ui.multiselect(...)` for feature selection
- `mo.ui.slider(...)` for error-table preview settings

As these controls change, the notebook updates automatically. The selected features feed directly into preprocessing, training, and evaluation without requiring a manual rerun sequence. The notebook uses a standard scikit-learn split with a fixed `test_size=0.2`, `random_state=42`, and `stratify=y`.

Presenter cue:

- Point out that the split is intentionally conventional here: `train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)`. The interactive part is the feature selection and downstream analysis, not the split parameter itself.

#### Part 4: Compare models without breaking flow

The notebook trains:

- **TabICL** as the modern tabular foundation model
- **Random Forest** as a familiar baseline

Participants can change features and train split, then immediately see:

- overall model accuracy
- per-class accuracy
- differences between TabICL and Random Forest in the plots
- how the two models react differently to the same feature choices

This keeps the emphasis on how interactivity changes model development: exploration and experimentation happen in one continuous loop.

#### Part 5: Use visual feedback for debugging

The same notebook then shifts from evaluation to debugging:

- `mo.ui.radio(...)` switches the debugging view between TabICL and Random Forest
- an error plot shows where predictions are failing
- `mo.ui.table(...)` lets participants select misclassified rows
- the selected subset is sent back into Python for further summary and inspection

This creates the full interactive cycle:

**explore data → fit models → inspect errors → make a change → observe the result**

That is the main takeaway of Module 3. Interactivity is not a convenience layer on top of notebook work. It changes the way experimentation happens.

#### What's Next
Quiz

Use `Module_3/module-3-quiz-viewer.html` to review the key ideas from the notebook.

Module 4 takes this further: what happens when you bring AI coding agents into this environment, and let them help you write and iterate on the notebook itself.

---

## Module 4: How to Use AI Coding Agents for AI/ML Development
AI coding agents are most useful when they are integrated directly into your development environment and can work with the actual state of your notebook. In marimo, the point is not just that AI can write code. The point is that AI can work inside a live notebook that already has dataframes, model outputs, variables, and dependencies in memory.

### Presentation

AI coding agents integrated directly into the notebook environment can act like fast collaborators rather than detached text generators. In ML and AI workflows, their value depends on:

- when you let them generate or modify code
- what notebook context they can see
- what tools they are allowed to use
- whether you run them through a hosted provider or a local/private setup

The core idea of this module is practical: better context leads to better AI assistance, and marimo is designed to provide that context inside the workflow itself.

### Hands-on Exercise (guided in marimo)

Use marimo's AI features inside `Module_3/module_3.py`:

- generate or modify code directly in the active notebook
- refactor an existing cell without leaving the editor
- provide explicit variable context such as `@df`
- compare the quality of a low-context prompt and a context-rich prompt
- discuss the tradeoffs between local and cloud-hosted setups

The goal is to let participants experience AI as part of a live notebook workflow, not as a separate code-generation website.

---

### 4.1 AI-assisted coding in marimo

marimo is an AI-native editor with support for full-cell AI code generation:

- generating new cells from a prompt
- refactoring existing cells from a prompt
- generating entire notebooks
- inline autocompletion, similar to Copilot-style tools

marimo's AI assistant is specialized for working with data. Unlike traditional assistants that only see the text of your program, marimo's assistant can also work with the values of variables in memory.

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
- **Refactor the current cell** with `Ctrl/Cmd-Shift-E`
- **Use the Chat panel** to ask notebook-level questions or generate cells from a side panel
- **Generate entire notebooks** from the command line with:

```bash
marimo new "your prompt here"
```

#### Hands-on: generate and refactor inside `module_3.py`

Open `module_3.py` from Module 3.

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
- `@selected_features` includes the currently selected feature list
- `@results_df` includes the current results table

This is especially useful in notebook work because the assistant is not guessing your schema from text alone. It can work from the current notebook state.

#### Chat panel modes

The Chat panel supports three modes:

- **Manual** — no tool access; the model responds only from the conversation and any manually injected context
- **Ask** — read-only tools plus context gathering, so the assistant can inspect the notebook
- **Agent (beta)** — everything in Ask mode plus the ability to edit notebook cells and run stale cells

Use these modes differently:

- choose **Manual** when you want a pure explanation
- choose **Ask** when you want notebook-aware reasoning without edits
- choose **Agent** when you want the assistant to actually modify the notebook

#### Tools inside the AI workflow

marimo's AI workflow is tool-aware. The assistant can inspect notebook structure, gather context, and in stronger modes interact with notebook cells rather than just producing text. This is what makes it feel integrated into the editor instead of bolted on.

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

In `module_3.py`, open the Chat panel and try this plain prompt:

*"Add a cell that explores which features are associated with model mistakes."*

Then try a richer prompt:

*"Using @df, @selected_features, and the current results table, add a cell that compares the distributions of selected features for correct versus incorrect predictions."*

Compare the two results. The second prompt should usually be more specific, more aligned with the notebook, and require less cleanup.

---

### 4.3 Agents, MCP, copilots, and setup choices

marimo supports richer AI workflows than just cell generation.

#### Agents

marimo supports external agents such as Claude Code, Codex, and Gemini CLI. These are useful when you want the assistant to work across multiple cells or operate on the notebook as a file rather than just generating one block of code at a time.

This matters because marimo notebooks are stored as plain `.py` files. External agents can read notebook structure directly instead of trying to reason over notebook JSON.

#### MCP

marimo also supports the **Model Context Protocol (MCP)**:

- **as an MCP server** — marimo can expose notebook-aware AI tools to external applications
- **as an MCP client** — marimo can connect MCP servers into its own Chat panel

In practice, this means notebook AI can become more connected and tool-aware. It can interact with documentation servers, notebook-aware services, or external coding environments through a standard protocol.

#### AI completion and copilots

marimo also supports inline AI completion, which is lighter-weight than full cell generation. This covers:

- **GitHub Copilot**
- **Windsurf**
- **Custom copilots** through your own configured provider

This is useful to mention because not every AI workflow needs a full agent. Sometimes completion inside the editor is enough.

#### Local versus cloud-hosted setups

There is no single best setup. The right choice depends on cost, speed, privacy, and control.

**Cloud-hosted providers**

- usually stronger models
- less local setup
- faster to get started
- less privacy and control over sensitive code or data

**Local or private setups**

- better for sensitive data and controlled environments
- more privacy and more deployment control
- often slower or less capable than frontier hosted models
- more setup overhead

For marimo, Ollama is the most straightforward local path when you want notebook AI without sending notebook context to a hosted provider.

#### Discussion prompt

After demonstrating AI-assisted coding in `module_3.py`, ask:

- Which parts of this workflow would you trust to a hosted provider?
- Which parts would you keep local because of privacy or control?
- When is inline completion enough, and when do you actually want an agent?

That discussion ties the whole module together: AI quality depends on context, but the right setup depends on your constraints.

Run this in a plain Python script first. If you get a clean response, you're ready to connect to marimo.

**Step 6 — Connect to marimo.** In marimo settings → AI, set:

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

> **Practical notes:**
> - Bigger models need more RAM/VRAM and disk space — check the model page on [ollama.com/library](https://ollama.com/library) for size requirements before pulling
> - If a model is too slow on your machine, step down to a smaller variant (e.g. `:3b` instead of `:7b`)
> - Ollama can run multiple models — pull several and switch between them in marimo settings to find the right speed/quality balance for your hardware

---


#### Hands-on: configure and evaluate

**Step 1 — Set up Ollama** (works for everyone, no API key needed):

```bash
ollama pull qwen2.5-coder:7b
```

In marimo settings → AI, set `model: ollama/qwen2.5-coder:7b` and `base_url: http://localhost:11434`.

**Step 2 — Test with a real task.** In `module_3.py`, hover over Cell 5 and click Generate with AI. Prompt:

*"Refactor this into a function called `prepare_data` that takes df, selected_features, and train_size as arguments and returns X_train, X_test, y_train, y_test."*

Run the result. Does it handle the `LabelEncoder` correctly? Does it reference `df` properly?

**Step 3 — Try the same prompt with Claude Code** if you have access. Compare the output quality, how it handles the marimo variable context, and how many edits you need to make before running it.

**Step 4 — Set your custom rules** in AI settings, then regenerate. Notice how the output quality improves when the agent has persistent preferences to follow:

```
Use marimo UI elements (mo.ui.*) for interactivity wherever applicable.
Use matplotlib for all plots with figsize=(7, 4) and tight_layout.
One primary variable returned per cell. Wrap intermediate logic in functions.
```

The right setup for your work will become clear quickly once you run the same task through both. For most ML development with non-sensitive data, start with Claude Code. For anything proprietary, Ollama with `deepseek-coder-v2` is the pragmatic choice.

---

The right AI setup is the one that fits your data constraints, your workflow speed, and your task complexity. What all three options share is marimo's automatic variable context — your current state is always available to the agent, so your prompts stay short and your iterations stay fast regardless of which model is doing the work.

Module 5 brings everything full circle: once your interactive, AI-assisted, reproducible notebook is working, how do you turn it into reusable systems that others can depend on?

---

## Module 5: From Interactive Work to Reusable Systems

Everything you've built across this course — the reactive notebook, the reproducible environment, the interactive ML pipeline, the AI-assisted workflow — has lived in a single `.py` file. This module shows you how to take that file and do four things with it that are impossible with a traditional Jupyter notebook: run it as a script, serve it as a web app, publish it as a shareable artifact, and import from it as a Python module.

Each section uses `module_3.py` from Module 3 as the working example. By the end of this module, the same file you built interactively will be running in four different modes — no duplication, no reformatting, no export step.

---

### 5.1 Turning Your Work Into Executable Scripts

#### The concept: one file, two modes

Every marimo notebook is a valid Python program. The `if __name__ == "__main__": app.run()` block at the bottom means you can execute it directly from the command line, just like any other Python script. The reactive graph runs top to bottom, cells execute in dependency order, and outputs print to stdout.

This matters for ML pipelines because it means your interactive exploration and your production pipeline are the same file. You don't maintain a notebook for exploration and a separate script for automation. You have one file that does both.

#### Hands-on: run as a script

**Step 1 — Run the notebook directly:**

```bash
python module_3.py
```

The notebook executes: data loads, preprocessing runs, TabICL fits, accuracy prints. No browser, no kernel, no UI. The reactive graph determines execution order automatically.

**Step 2 — Add command-line arguments with argparse.** Open `module_3.py` and add a setup cell at the top (right-click the first cell → "Add setup cell"):

```python
import argparse
import sys

parser = argparse.ArgumentParser(description="Adult Income classifier")
parser.add_argument("--train-size", type=float, default=0.7,
                    help="Fraction of data for training (default: 0.7)")
parser.add_argument("--features", nargs="+",
                    default=["age", "education-num", "hours-per-week"],
                    help="Feature columns to include")
parser.add_argument("--output", type=str, default=None,
                    help="Path to save accuracy results as CSV")

# Only parse when running as script, not in marimo editor
args = parser.parse_args([] if "marimo" in sys.modules else None)
```

**Step 3 — Wire the arguments to your existing UI controls.** Update the cell that defines `selected_features` and `train_size` to use the parsed args when running as a script:

```python
import marimo as mo

# In interactive mode, use sliders. In script mode, use args.
if mo.running_in_notebook():
    feature_selector = mo.ui.multiselect(
        options=["age", "education-num", "hours-per-week",
                 "capital-gain", "capital-loss"],
        value=args.features,
        label="Features to include"
    )
    train_size_slider = mo.ui.slider(
        start=0.1, stop=0.9, step=0.1,
        value=args.train_size,
        label="Training set size"
    )
    mo.vstack([feature_selector, train_size_slider])
    selected_features = feature_selector.value
    train_size = train_size_slider.value
else:
    selected_features = args.features
    train_size = args.train_size
```

**Step 4 — Run with arguments:**

```bash
python module_3.py --train-size 0.5 --features age hours-per-week capital-gain
```

The same notebook that runs interactively with sliders now accepts CLI arguments for automation. One file, both modes.

**Step 5 — Schedule it.** Because it's a plain Python script, you can run it on a schedule with cron:

```bash
# Run every day at 6am, log output
0 6 * * * python /path/to/module_3.py --train-size 0.8 >> /logs/daily_run.log 2>&1
```

Or in a GitHub Action:

```yaml
- name: Run notebook as script
  run: python module_3.py --train-size 0.8
```

> **Docs:** [docs.marimo.io/guides/scripts](https://docs.marimo.io/guides/scripts/) — covers `argparse` and `simple-parsing` integration and scheduled execution patterns.

---

### 5.2 Publishing Flexible, Interactive Data Apps

#### The concept: code hidden, interactivity kept

App mode is the other side of the same file. Run `marimo run` instead of `marimo edit` and the notebook becomes a web app: all code is hidden, only outputs and UI elements are visible. The reactive graph still runs — sliders still update the model, tables still reflect selections — but your collaborator sees a clean interface, not a notebook.

There is no conversion step, no framework to learn, no separate deployment file. The notebook you built is already the app.

#### Hands-on: serve as a web app

**Step 1 — Launch in app mode:**

```bash
marimo run module_3.py
```

Open the URL in your browser. You see the `mo.ui.dataframe()` explorer, the feature multiselect, the train size slider, the accuracy output, and the error scatter plot — all working reactively. The TabICL fit, the preprocessing pipeline, the matplotlib code — none of it is visible. It looks like a dashboard.

**Step 2 — Clean up for non-technical users.** Add a Markdown header cell at the top of your notebook (it will appear at the top of the app):

```python
mo.md("""
# Adult Income Prediction Explorer

Use the controls below to explore how different features and training
set sizes affect the model's accuracy and error patterns.

**No coding required** — adjust the sliders and dropdowns to run experiments.
""")
```

**Step 3 — Control layout.** By default, app mode stacks outputs vertically. For a more polished layout, arrange outputs side by side using `mo.hstack`:

```python
mo.hstack([
    mo.vstack([feature_selector, train_size_slider]),
    mo.md(f"### Accuracy: `{acc:.1%}`")
])
```

**Step 4 — Preview without leaving edit mode.** In the marimo editor, click the **Preview** button (bottom-right) to see exactly what the app looks like without switching modes.

**Step 5 — Share with a teammate.** If you're both on the same network:

```bash
marimo run module_3.py --host 0.0.0.0 --port 8080
```

Your teammate opens `http://your-ip:8080` and gets the full interactive app. No Python, no marimo, no setup required on their end.

> **App layouts:** marimo supports vertical (default), grid (drag-and-drop), and slides layouts. Switch between them in the app preview dropdown. For a presentation-style walkthrough of your results, slides layout lets you step through cells one at a time.

> **Docs:** [docs.marimo.io/guides/apps](https://docs.marimo.io/guides/apps/)

---

### 5.3 From Outputs to Published Artifacts

#### The concept: static snapshots and live previews

Not everyone needs the live app. Sometimes you want to send a link to a static report, embed results in documentation, or publish a notebook that others can view — or fork and run themselves. marimo supports all of these through export and publishing.

#### Hands-on: export and publish

**Step 1 — Export to static HTML.** This captures your current notebook state — code, outputs, plots — as a single self-contained HTML file:

```bash
marimo export html module_3.py -o report.html
```

Open `report.html` in any browser. No Python, no server. Share it as an email attachment, add it to a documentation site, or commit it to a repo. The plots, tables, and Markdown are all there.

To include pre-rendered outputs (so the HTML shows results immediately without running anything):

```bash
marimo export html module_3.py -o report.html --include-outputs
```

**Step 2 — Export to PDF:**

```bash
marimo export pdf module_3.py -o report.pdf
```

**Step 3 — Publish to molab.** Push your notebook to a GitHub repository, then generate a shareable molab preview URL:

```
https://molab.marimo.io/github/<your-username>/<your-repo>/blob/main/module_3.py
```

Anyone with this URL sees a live preview of your notebook. They can fork it into their own molab workspace and run it — with the same sandbox environment, the same inline dependencies — without installing anything. This is the sharing story for research: one URL, fully reproducible.

**Step 4 — Generate a WASM-powered interactive HTML.** This exports your notebook as a self-contained HTML file that runs entirely in the browser via WebAssembly — no server needed, fully interactive:

```bash
marimo export html-wasm module_3.py -o interactive_report.html
```

Open `interactive_report.html`. The sliders work. The model runs. Everything is live — powered by Python compiled to WebAssembly, running in the browser tab. You can host this on GitHub Pages, embed it in a documentation site, or send it directly.

**Step 5 — Publish to GitHub Pages** with a GitHub Action. Create `.github/workflows/publish.yml`:

```yaml
name: Publish notebook to GitHub Pages
on:
  push:
    branches: [main]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install marimo
      - run: marimo export html-wasm module_3.py -o docs/index.html
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs/
      - uses: actions/deploy-pages@v4
```

Every push to `main` rebuilds and republishes your notebook as a live interactive page on `https://<your-username>.github.io/<your-repo>`.

> **Docs:** [docs.marimo.io/guides/exporting](https://docs.marimo.io/guides/exporting/) and [docs.marimo.io/guides/publishing/github](https://docs.marimo.io/guides/publishing/github/)

---

### 5.4 From Interactive Code to Importable Modules

#### The concept: the notebook is the module

In Jupyter, when you want to reuse code from a notebook in another file, your options are: copy-paste, convert to a `.py` script manually, or import the notebook with a hack that executes the entire file. None of these are good.

In marimo, the notebook *is already* a Python module. Because it's stored as a `.py` file with proper function definitions, you can import from it directly — the same way you'd import from any other Python module. No conversion, no copy-paste, no hacks.

The only requirement is the **setup cell**: a special cell that runs before the reactive graph, designed specifically for top-level definitions that should be importable. Functions and classes defined in the setup cell become the notebook's public interface.

#### Hands-on: make your notebook importable

**Step 1 — Create a setup cell.** In `module_3.py`, right-click the first cell and select **"Convert to setup cell"** (or add one via the cell menu). The setup cell is marked with a special indicator in the editor and always runs first.

**Step 2 — Move reusable logic into the setup cell:**

```python
# setup cell
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd

def prepare_data(df, selected_features, train_size=0.7):
    """
    Encode and split the Adult Income dataset.

    Returns X_train, X_test, y_train, y_test.
    """
    X = df[selected_features].copy()
    for col in X.select_dtypes(include="object").columns:
        X[col] = LabelEncoder().fit_transform(X[col].astype(str))
    y = (df["class"] == ">50K").astype(int).values
    return train_test_split(X, y, train_size=train_size,
                            random_state=42, stratify=y)


def evaluate_model(clf, X_test, y_test):
    """
    Return accuracy and per-class accuracy dict.
    """
    from sklearn.metrics import accuracy_score
    preds = clf.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, preds),
        "class_0": accuracy_score(y_test[y_test == 0], preds[y_test == 0]),
        "class_1": accuracy_score(y_test[y_test == 1], preds[y_test == 1]),
    }
```

**Step 3 — Import from another file.** Create `pipeline.py` in the same directory:

```python
# pipeline.py — a separate script that reuses notebook logic
from adult_income_explorer import prepare_data, evaluate_model
from sklearn.datasets import fetch_openml
from tabicl import TabICLClassifier

data = fetch_openml("adult", version=2, as_frame=True)
df = data.frame.dropna()

X_train, X_test, y_train, y_test = prepare_data(
    df,
    selected_features=["age", "education-num", "hours-per-week", "capital-gain"],
    train_size=0.8
)

clf = TabICLClassifier()
clf.fit(X_train, y_train)

results = evaluate_model(clf, X_test, y_test)
print(f"Accuracy: {results['accuracy']:.1%}")
print(f"Class 0: {results['class_0']:.1%}  |  Class 1: {results['class_1']:.1%}")
```

Run it:

```bash
python pipeline.py
```

The functions from your interactive notebook run in a plain Python script. The notebook is still fully editable and interactive in marimo. There is no duplication — `pipeline.py` imports from the notebook, it doesn't copy from it.

**Step 4 — Test your functions with pytest.** Because the functions are proper Python, you can test them directly:

```python
# test_pipeline.py
from adult_income_explorer import prepare_data
from sklearn.datasets import fetch_openml
import pandas as pd

def test_prepare_data_shape():
    data = fetch_openml("adult", version=2, as_frame=True)
    df = data.frame.dropna()
    X_train, X_test, y_train, y_test = prepare_data(
        df, ["age", "education-num"], train_size=0.7
    )
    assert X_train.shape[1] == 2
    assert len(X_train) + len(X_test) == len(df)

def test_prepare_data_no_nulls():
    data = fetch_openml("adult", version=2, as_frame=True)
    df = data.frame.dropna()
    X_train, X_test, _, _ = prepare_data(df, ["age", "education-num"])
    assert X_train.isnull().sum().sum() == 0
```

```bash
pytest test_pipeline.py -v
```

Your interactive notebook is now part of a tested, importable codebase. This is what "from interactive work to reusable systems" actually means — not a metaphor, but a concrete workflow where the notebook, the pipeline script, and the test suite all point to the same source of truth.

> **Docs:** [docs.marimo.io/guides/reusing_functions](https://docs.marimo.io/guides/reusing_functions/)

---

The four sections of this module represent the four ways a single marimo notebook can be deployed: as a script for automation, as an app for non-technical collaborators, as a published artifact for sharing, and as a module for larger codebases. In every case, the file is the same. The work you did interactively doesn't need to be translated into something else to be useful. It already is something else — it was the whole time.
