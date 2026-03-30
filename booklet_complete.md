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

First, in `marimo-reactive-workflow.py`, we keep the inputs as plain Python variables:

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
| `marimo edit Module_1/marimo-reactive-workflow.py` | Opens a specific workshop notebook in the editor |
| `marimo edit --sandbox notebook.py` | Same, with isolated per-notebook dependencies |
| `marimo run Module_1/marimo-reactive-workflow-with-sliders.py` | Runs a notebook as a read-only app (code hidden) |
| `python Module_1/marimo-reactive-workflow.py` | Executes a notebook as a script (no UI) |

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

> 💡 **Try it — `Module_2/2.1.ipynb`**
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

> 💡 **Try it — `Module_2/2.1.ipynb`**
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

> 💡 **Try it — `Module_2/2.2.py`**
>
> Run the notebook and inspect the active Python, `pandas`, and `matplotlib` versions. Then reopen it in sandbox mode:
> ```bash
> marimo edit --sandbox Module_2/2.2.py
> ```


#### The file format problem

Jupyter notebooks are stored as JSON. Two lines of code become dozens of lines of structural wrapping — cell type, execution count, output blobs, metadata. Re-run a single cell and all of that updates, even if your code didn't change. The signal is buried in the noise.

A marimo notebook is a plain `.py` file. Change one cell and the diff shows exactly that cell. You can review it in a pull request, use `git blame` on a specific line, and resolve merge conflicts in any text editor.

> 💡 **Try it — `Module_2/2.2.py`**
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

#### Part 1: Explore the data interactively

Start with the Adult Income dataset and use marimo's built-in data tools:

- `mo.ui.dataframe(df)` for interactive table inspection
- `mo.ui.data_explorer(df)` for chart-based exploration
- `mo.ui.data_editor(df)` for editable tabular input

Use these to inspect columns, scan values, explore distributions, and understand the dataset before modeling. The notebook also includes a small reactive summary below the editable sample so participants can see that edits flow into downstream output immediately.

#### Part 2: Control the modeling workflow

The notebook includes live controls such as:

- `mo.ui.multiselect(...)` for feature selection
- `mo.ui.slider(...)` for training split
- `mo.ui.slider(...)` for error-table preview settings

As these controls change, the notebook updates automatically. The selected features feed directly into preprocessing, training, and evaluation without requiring a manual rerun sequence.

#### Part 3: Compare models without breaking flow

The notebook trains:

- **TabICL** as the modern tabular foundation model
- **Random Forest** as a familiar baseline

Participants can change features and train split, then immediately see:

- overall model accuracy
- per-class accuracy
- differences between TabICL and Random Forest in the plots
- how the two models react differently to the same feature choices

This keeps the emphasis on how interactivity changes model development: exploration and experimentation happen in one continuous loop.

#### Part 4: Use visual feedback for debugging

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

AI coding agents have become a standard part of the ML development workflow. But how useful they are depends heavily on *when* you use them, *what information* they have access to, and *which setup* matches your constraints. A well-integrated agent in the right environment feels like a fast, knowledgeable collaborator. A poorly integrated one produces generic code that doesn't know what variables you have, what your data looks like, or what you just tried.

This module is practical. It covers the three decisions that determine how much value you actually get from AI assistance in ML work: when to use it, how to give it context, and how to choose your setup.

---

### 4.1 When to Let AI Agents Write Code for You

#### The concept: acceleration, not replacement

AI coding agents are best used for tasks where the *structure* of what you need is clear but the *implementation* is tedious, unfamiliar, or repetitive. In ML work, those tasks come up constantly:

- Boilerplate preprocessing pipelines — encoding categoricals, scaling numerics, splitting data
- Plotting code — you know what you want to see, the matplotlib API is just in the way
- Metric computation and reporting — accuracy, F1, confusion matrices, classification reports
- Refactoring — turning a messy exploratory cell into a clean function
- Library lookups — you know *what* you need, not *how* the API spells it

Where agents provide less value: core scientific reasoning, hypothesis formation, deciding which features are worth engineering, interpreting results. Those require your domain knowledge and judgment. The agent writes the code; you decide what the code should do.

#### marimo's AI features

marimo has AI assistance built directly into the editor — no plugin, no separate window. There are two modes:

**Inline cell generation** — Click the **Generate with AI** button that appears when hovering over any cell, or open the **Chat panel** from the sidebar. Describe what you want in plain English. marimo generates a new cell or refactors an existing one. The result is inserted directly into your notebook, reactive and ready to run.

**Agents** — Full coding agents that can read your notebook, write and edit multiple cells, run code, observe outputs, and iterate. Supported agents include Claude Code, Gemini Agent, Codex, and OpenCode. Agents operate on the `.py` file directly — because marimo notebooks are plain Python, the agent can read, understand, and edit the entire notebook as source code, with no JSON parsing or cell format translation.

**Generate entire notebooks** — From the marimo home screen, describe a notebook you want and marimo generates the full structure — cells, Markdown, UI elements — as a starting point. Useful for scaffolding a new experiment quickly before diving in to customise it.

#### Hands-on: use AI to extend your Adult Income notebook

Open `module_3.py` from Module 3. Hover over the Cell 7 (per-class accuracy bar chart) and click **Generate with AI**.

Prompt: *"Add a ROC curve plot below this cell using the test predictions. Use matplotlib, same style as the bar chart."*

marimo generates the cell. Review it — does it reference `preds`, `y_test`, and `X_test` correctly? If so, run it. If the variable names are slightly off, edit them. The point is that you didn't write the matplotlib boilerplate; you described the intent and reviewed the result.

Now try the Chat panel. Open it from the sidebar and type: *"Refactor the preprocessing in Cell 5 into a reusable function called `preprocess_data` that takes a dataframe and a list of feature names."*

The agent edits Cell 5. Because marimo's variable context is automatically included, the agent already knows the shape of `df`, the names of your features, and how `X_train` is currently defined. It doesn't need you to paste anything.

> **Tip — where AI helps most in ML work:** Use it for Cell 7-style visualisation code and Cell 5-style preprocessing refactors. Don't use it for the scientific decisions — which features to include, how to interpret the error clusters from Cell 8, whether the per-class accuracy gap indicates a fairness problem. Those are yours.

---

### 4.2 Giving AI Coding Agents the Context They Need

#### The concept: context is everything

The difference between a useful AI suggestion and a useless one is almost always context. An agent that doesn't know your variable names generates placeholder names. An agent that doesn't know your dataframe's schema generates column names that don't exist. An agent that doesn't know what you've already tried suggests things you've already ruled out.

In traditional notebooks, providing this context is manual work — you paste error messages, copy schema outputs, describe your data in the prompt. The agent works from a description of your state, not the state itself.

marimo changes this structurally in two ways.

#### Automatic variable context

When you invoke AI assistance in marimo — either the inline generator or the Chat panel — marimo automatically includes the **names, types, and current values** of all variables in scope. The agent sees that `df` is a `DataFrame` with shape `(45,222, 14)`, that `selected_features` is currently `["age", "education-num", "hours-per-week"]`, that `acc` is `0.847`. You don't tell it this. marimo tells it.

This is possible because marimo's reactive runtime always knows the current state of every variable — there is no hidden state, no out-of-order execution, no stale values. The variable panel you can see in the sidebar is exactly the context the agent receives.

In practice this means your prompts can be much shorter and more direct. Instead of: *"I have a pandas dataframe called df with columns age, education-num, hours-per-week and a target column called income. Please write code to..."* — you just write: *"Plot the distribution of each selected feature, coloured by income."* The agent already knows what the variables are.

#### Custom rules

For persistent preferences that should apply across all AI interactions in a notebook, marimo supports **custom rules** — instructions you write once that the AI always follows. Set them in the AI settings panel:

```
Always use matplotlib for plotting, not seaborn or plotly.
Use f-strings for string formatting.
Prefer pandas over polars.
Never use global variables — wrap logic in functions.
```

These rules travel with the notebook's configuration. If you share the notebook with a colleague, they get the same AI behaviour.

#### Skills for Claude Code

If you use Claude Code as your agent, marimo supports **skills** — reusable markdown files that teach Claude how to work with your specific codebase, conventions, or domain. A skill might define how your team structures preprocessing pipelines, which internal libraries to import, or what format model evaluation outputs should take.

Skills live in `.claude/commands/` in your project directory. Invoke one by typing `/skill-name` in the Claude Code terminal — Claude loads those instructions as persistent context for the session.

This workshop ships a skill at `.claude/commands/marimo-notebook.md`. It covers:

- The `@app.cell` structure and how parameters and return values wire cells together
- `hide_code=True`, `mo.md()`, and `@app.function` conventions
- How to write reactive UI elements (`mo.ui.slider`, `mo.ui.table`, etc.)
- PEP 723 dependency block — where to add new packages
- Workshop conventions: matplotlib only, one output per cell, no global state

To use it, run Claude Code in the workshop directory and type:

```
/marimo-notebook
```

Claude now understands marimo's cell model, the workshop's conventions, and the key files — without you explaining any of it in the prompt.

Skills are particularly valuable in ML work because the same patterns repeat across experiments: the same feature encoding logic, the same evaluation suite, the same plotting style. Rather than re-explaining these to the agent in every session, you define them once and invoke them in one word.

#### The .py format advantage

Because marimo notebooks are plain `.py` files, agents that operate at the file level — Claude Code, Codex, OpenCode — can read the entire notebook as source code. They see the `@app.cell` structure, the function signatures, the variable dependencies. They understand which cells depend on which variables. This is structurally impossible with `.ipynb` files, where the agent sees JSON metadata interleaved with code, and has no way to understand the execution graph.

In practice: if you tell Claude Code "the preprocessing in this notebook is too slow — can you optimise it?", it can read the whole file, identify the bottleneck cells, understand their dependencies, and propose targeted changes. It's working from the actual program structure, not a description of it.

#### Hands-on: prompt with context

In `module_3.py`, open the Chat panel. Without pasting anything, type:

*"The per-class accuracy gap between the two income classes seems large. What features might explain this? Suggest a cell that analyses feature distributions split by correct vs incorrect predictions."*

The agent's response will reference your actual variable names — `results_df`, `correct`, `errors`, `selected_features` — because marimo has already provided that context. If the suggestion looks right, insert the generated cell and run it.

Then set a custom rule: *"All matplotlib figures should use `figsize=(7, 4)` and `plt.tight_layout()`."* Regenerate the ROC curve cell from 4.1. Notice the style is now consistent without you specifying it in the prompt.

---

### 4.3 Choosing the Right AI Coding Agent Setup

#### The concept: three real options

Picking an AI coding setup comes down to four tensions: **capability** vs **privacy**, and **task scope** vs **cost**. Rather than listing every possible provider, this section evaluates three setups that cover the most common situations in ML/AI work and that marimo supports natively: **Claude Code** (cloud agent), **OpenCode** (open-source agent), and **Ollama** (local inference).

#### Claude Code — best for marimo work, highest capability

Claude Code is a full agentic coding assistant from Anthropic that runs in your terminal alongside marimo. Of all the supported agents, it has the deepest integration with marimo: it understands the `@app.cell` structure natively, can reason about the reactive dependency graph, and has a dedicated guide in the marimo docs with slash commands, hooks, and skills specifically for notebook workflows.

Connect it from the marimo agents panel in the sidebar, or run it from the terminal in the same directory as your notebook. Once connected, Claude Code can read your entire `.py` notebook file, write and edit multiple cells autonomously, execute code, observe outputs, and iterate — without you managing the loop.

**Where it excels in ML work:**
- Multi-cell refactors — "refactor this preprocessing pipeline into a reusable function and update all cells that call it"
- Debugging dependency issues — it reads the reactive graph and understands what depends on what
- Generating complete analysis sections from a description — "add a fairness analysis section that compares error rates across age groups"
- Working with marimo-specific patterns — `mo.ui.*`, `mo.md()`, cell structure — without needing explanation

**The tradeoff:** It's a cloud service. Your notebook code and variable context are sent to Anthropic's API. For public datasets and research work this is fine. For proprietary data or model weights under NDA, it's not.

**Setup:**
```bash
npm install -g @anthropic-ai/claude-code
claude  # authenticate once
# Then connect from marimo's agents panel
```

Full guide: [docs.marimo.io/guides/generate_with_ai/using_claude_code](https://docs.marimo.io/guides/generate_with_ai/using_claude_code/)

---

#### OpenCode — open-source agent, your choice of model

OpenCode is an open-source terminal-based coding agent that works with any LLM provider — including local models. It's the right choice when you want agent-level autonomy (read file, edit multiple cells, run and observe) but need flexibility over which model backs it, or want to avoid vendor lock-in.

Because OpenCode is model-agnostic, you can point it at Claude, GPT-4, a Bedrock endpoint, or a local Ollama model. The agent behaviour — reading files, making edits, running commands — is the same regardless of the underlying model. This makes it useful as a transition path: start with a cloud model while you're learning, switch to a local model once your workflow is established and data sensitivity requires it.

**Where it excels:**
- Teams that want a consistent agent interface across different model backends
- Organisations that need to audit or customise agent behaviour (it's open source)
- Researchers who want agent-level capability with a local model for sensitive data

**The tradeoff:** Capability depends entirely on the model you choose. OpenCode with a frontier cloud model matches Claude Code closely. OpenCode with a local model has the same capability ceiling as that local model — which is meaningfully lower for complex reasoning tasks.

**Setup:**
```bash
npm install -g opencode-ai
opencode  # configure your preferred model
# Then connect from marimo's agents panel
```

---

#### Ollama — local inference, nothing leaves your machine

Ollama runs open-weight models entirely on your local hardware. No API key, no data egress, no per-token cost. marimo routes inline AI requests to Ollama the same way it routes to any other provider — configure it once and the Generate with AI button and Chat panel work exactly as they do with cloud models.

**Where it excels:**
- Proprietary datasets, patient data, unreleased model weights — anything that cannot leave your machine
- Air-gapped research environments
- Rapid inline generation of boilerplate — preprocessing functions, plot skeletons, metric cells — where frontier reasoning isn't needed
- Cost-free iteration when you're doing high-volume repetitive generation

**The tradeoff:** Requires a machine with enough VRAM or RAM to run the model (16GB+ recommended for larger models). Inference is slower than cloud on equivalent hardware. For complex tasks — multi-cell architectural decisions, nuanced debugging — local models are noticeably less capable than frontier cloud models.

#### Setting up Ollama

**Step 1 — Install.** Download from [ollama.com/download](https://ollama.com/download) and verify:

```bash
ollama --version
```

**Step 2 — Start the local server:**

```bash
ollama serve
```

This starts Ollama at `http://localhost:11434`. Keep this running in a terminal tab while you work.

**Step 3 — Pull a code model.** For ML/data work, `qwen2.5-coder:7b` is a strong choice — capable on pandas, sklearn, and matplotlib patterns, fast on modern laptops:

```bash
ollama pull qwen2.5-coder:7b
```

Browse the full model library at [ollama.com/library](https://ollama.com/library). If `qwen2.5-coder:7b` feels slow on your hardware, try a smaller variant first.

**Step 4 — Quick test in terminal:**

```bash
ollama run qwen2.5-coder:7b
```

Type a prompt. If it responds, the server is working.

**Step 5 — Verify with Python** before connecting to marimo:

```python
import requests

r = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5-coder:7b",
        "prompt": "Write a pandas one-liner to drop rows with missing values.",
        "stream": False,
    },
    timeout=60
)
r.raise_for_status()
print(r.json()["response"])
```

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

#### Comparative evaluation

The honest assessment across the three options for common ML/AI tasks:

| Task | Claude Code | OpenCode + cloud | Ollama local |
|---|---|---|---|
| Generate a preprocessing cell | ✅ Excellent | ✅ Excellent | ✅ Good |
| Refactor multi-cell pipeline | ✅ Excellent | ✅ Good | ⚠️ Limited |
| Debug reactive dependency issue | ✅ Excellent | ✅ Good | ❌ Poor |
| Generate a matplotlib figure | ✅ Excellent | ✅ Excellent | ✅ Good |
| Sensitive/proprietary data | ❌ Cloud only | ⚠️ Depends on model | ✅ Safe |
| Cost per session | Per token | Per token (cloud) / Free (local) | Free |
| Setup complexity | Low | Medium | Medium |

The pattern is clear: Claude Code wins on capability and marimo integration, Ollama wins on privacy and cost, OpenCode sits in the middle and gives you the agent interface without the vendor commitment.

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
