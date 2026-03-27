# The Modern AI and ML Development Stack
## Powered by marimo

**Author:** [Your Name]

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

This booklet is your guide to a better way of working. It introduces **marimo**, a next-generation open-source Python notebook designed for reproducible, interactive, and shareable computation. Across five modules, you'll learn not just how to use marimo, but *why* it exists — and how the modern AI/ML development stack fits together.


---

## Module 1: Why Interactive Programming Environments Matter for AI and ML

This module takes you on a journey: from appreciating what notebooks do well, to seeing where they break, to experiencing a fundamentally better alternative, to getting hands-on with it yourself.

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

As marimo creator Akshay Agrawal describes it:

> "I would delete a cell, and then it would delete some variable that I forgot was defined in that cell, and it was still in memory. And other code referred to that variable. And then 4 hours later, I would realize I just had a bunch of inconsistent state."

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

This is the idea behind **reactive execution**. Instead of treating a notebook as a sequence of imperative commands that mutate a shared workspace, a reactive notebook models the cells as a **dependency graph**. It knows which cells read which variables, and which cells define them. When something changes, only the affected cells re-execute.

The result: your code and outputs are always in sync. No stale results. No ghost variables. No manual re-running.

#### Seeing It in Action

We rebuild the same compound interest calculator — the exact same logic — in a reactive notebook. But we do it in two stages.

First, in `marimo-reactive-workflow.py`, we keep the inputs as plain Python variables:

```python
principal = 1000
rate = 0.07
years = 20
```

Then we use those variables in downstream cells exactly as before: compute the growth path, print the final balance, draw the plot, and build the summary table.

The difference is that marimo now knows the dependency graph. Change `years` from 20 to 50 and run that cell, and every dependent cell updates automatically. No stale plot. No stale table. No stale printed summary.

Only after that do we swap the fixed inputs for sliders in `marimo-reactive-workflow-with-sliders.py`:

- Move the **rate slider** from 7% to 12% — the results table, the growth plot, and the rate comparison chart all update instantly
- Move the **years slider** from 20 to 50 — everything recomputes automatically
- Change the **starting amount** — same thing

The sliders are not the main idea. They are just the most visible way to feel the reactivity.

No Shift-Enter. No manual re-running. No keeping track of what depends on what. The notebook handles it.

And the things that broke before? They can't break here:

- **Out-of-order execution is impossible.** When you change a parameter, all dependent cells update. There's no way to have stale outputs.
- **Hidden state is impossible.** Delete a cell, and its variables are immediately scrubbed from memory. Downstream cells that depended on them show errors instantly. No ghosts.

#### Gallery: What's Possible

The reactive model doesn't just fix problems — it enables entirely new ways of working. Here are some examples from the marimo community gallery:

- **Embedding Visualizer** — Select points in embedding space and get them back as a dataframe in Python. Your visualization is an input, not just an output.
- **Neural Networks with Micrograd** — Interactive neural net training. Change parameters, watch the network learn in real time.
- **Seam Carving** — Content-aware image resizing with live visualization. Visually stunning and educational.
- **Reactive Plots** — Select data points on a chart, get the selection back in Python, run analysis, see the plot update. A tight bidirectional loop.
- **Federated Learning Simulation** — Interactive simulation of hospitals training local models with FedAvg aggregation. Serious ML research in a notebook.
- **Signal Decomposition (Stanford)** — An interactive educational notebook from Stanford that lets students explore signal decomposition visually. A real example of marimo used in university teaching: [molab.marimo.io/notebooks/nb_3gk1j4rzKeFpz8rNwrVU5h/app](https://molab.marimo.io/notebooks/nb_3gk1j4rzKeFpz8rNwrVU5h/app)

These are all built in the same tool, using the same reactive model.

---

### 1.4 Hands On with marimo: A Modern Programming Environment

#### What Is marimo?

The reactive notebook you just experienced is called **marimo**. It's an open-source Python notebook created by Akshay Agrawal, a Stanford PhD graduate who previously worked on the TensorFlow team at Google Brain. He started building marimo after his PhD in 2022, drawing on his frustrations with Jupyter and his experience with dataflow systems. marimo launched in January 2024.

marimo was designed with educators and researchers in mind — built by someone who identifies as both, with direct input from Stanford scientists who needed a more interactive medium for teaching computer science and a more reproducible environment for computational research. In its original design it drew significant inspiration from **Pluto.jl**, a reactive notebook for the Julia language developed at MIT specifically for education. That lineage matters: reproducibility and interactivity weren't added to marimo as features — they were the founding motivation.

marimo was also inspired by Observable (for JavaScript) — part of a broader movement toward reactive dataflow programming. It has been downloaded over 2 million times and is featured in *Nature* as a tool for computational reproducibility. It's used at Stanford, BlackRock, SLAC National Accelerator Laboratory, and hundreds of other organizations.

marimo is entirely free and open source: [github.com/marimo-team/marimo](https://github.com/marimo-team/marimo)

#### Installing marimo

There are several ways to get started:

**In the browser (zero install):**

Visit [marimo.new](https://marimo.new) to open a new notebook in molab, marimo's free cloud-hosted service. No installation needed.

**With pip:**

```bash
pip install marimo
marimo tutorial intro     # verify it works
```

With recommended extras (AI features, plotting, formatting):

```bash
pip install "marimo[recommended]"
```

**With uv:**

```bash
uv venv
uv pip install marimo
uv run marimo edit
```

**Per-notebook sandbox (isolated dependencies):**

```bash
marimo edit --sandbox notebook.py
```

This creates an isolated virtual environment for the notebook. Packages are tracked in the notebook file itself.

Before jumping into your own notebooks, it is useful to open the official intro notebook once:

```bash
marimo tutorial intro
```

This gives you a quick tour of the marimo editor and lets you point out the main pieces of the interface in a concrete way:

- a code cell and its output
- the run controls for a cell
- the sidebar panels
- the variables view
- the dependency graph
- the difference between editing code and interacting with outputs

For teaching, this is a good warm-up before opening the workshop notebooks, because you can explain what each part of the environment does before introducing the course-specific examples.

#### Essential Commands

| Command | What it does |
|---|---|
| `marimo.new` | Opens a new notebook in molab (browser, zero install) |
| `marimo edit` | Opens the file browser to pick or create a notebook |
| `marimo edit notebook.py` | Opens (or creates) a specific notebook |
| `marimo edit --sandbox notebook.py` | Same, with isolated per-notebook dependencies |
| `marimo run notebook.py` | Runs the notebook as a read-only app (code hidden) |
| `python notebook.py` | Executes the notebook as a script (no UI) |

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

You do not need to dwell on every widget. The point is just to make the environment feel tangible before diving back into the larger examples.

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

#### Exercises

To solidify these concepts, try the following:

**Exercise 1: Basic reactivity.** Create three cells: one defining `a = 10`, one defining `b = 20`, one computing `c = a + b`. Change `a` to 50. Watch `c` update without re-running it.

**Exercise 2: Add a reactive UI input.** Replace the `a` cell with:

```python
import marimo as mo
threshold = mo.ui.slider(
    start=0.1,
    stop=0.9,
    step=0.1,
    value=0.5,
    label="Decision threshold",
)
threshold
```

Update the third cell to use `threshold.value`. Move the slider. Watch everything react — no callbacks, no event handlers.

**Exercise 3: Try to break it.** Define `a` in two different cells. marimo shows an error immediately. In Jupyter, this would silently work.

**Exercise 4: No ghost state.** Delete the `a` cell. The cell computing `c` immediately errors. The variable is gone — no ghost lingering in memory.

**Exercise 5: Explore the sidebar.** Open the Variables panel, the Dependency graph, and the Live Docs panel. See your notebook's structure laid bare.

#### What's Next

You've seen why interactive environments matter, where traditional notebooks break down, and how reactive execution solves those problems. You've installed marimo, toured the interface, and experienced reactivity firsthand.

But reactivity only keeps things in sync during a single session. What happens when you send your notebook to a colleague, or come back to it six months later? What happens when the same code gives different results on a different machine?

That's the subject of Module 2: **Reproducibility as a Baseline for Trustworthy AI**.

---

## Module 2: Reproducibility as a Baseline for Trustworthy AI

There's a big difference between just running your code again and reliably getting the same results across different computers and over time. Reactive execution — as you saw in Module 1 — keeps your outputs in sync *within a session*. But the moment you close your notebook, share it with a colleague, or come back to it six months later, an entirely different class of problems emerges. This module is about those problems, and how marimo addresses them at the environment level.

---

### 2.1 The "It Works on My Machine" Problem

Imagine you spend a week building a data pipeline. It runs cleanly on your laptop. You send it to a colleague. They run it and get different numbers — or it crashes entirely. You compare code. It's identical. The problem isn't the code. It's everything around the code.

This is the "it works on my machine" problem, and it's endemic to data science and ML work. The reason it's so insidious is that it fails *silently*. Your notebook doesn't raise an exception when it produces a subtly wrong result due to a library version mismatch. It just runs, outputs something, and you trust it.

The Pimentel study from Module 1 captured this at scale: of 1.4 million Jupyter notebooks on GitHub, only 4% reproduced their original results when re-run. The majority of those failures weren't bugs in the code — they were environmental drift. Different Python versions. Different library versions. Different system configurations. Code that was never wrong, running in an environment that no longer matches the one it was written for.

This is why reproducibility can't be an afterthought bolted on after the fact with a `requirements.txt` file. It needs to be built into the environment itself, from the first line of code.

#### Try it: make the problem visible

The best way to understand environmental drift is to create it deliberately. The `2.1.ipynb` notebook is set up to do exactly that by running the same cell in two different kernels.

**Step 1.** Open `Module_2/2.1.ipynb` and run this cell in the default kernel:

```python
import pandas as pd

print(f"pandas version: {pd.__version__}")

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df['b'][df['a'] > 1] = 99

print(df)
```

Note whether `df` was modified and what signal appeared.

**Step 2.** Switch the notebook kernel to:

```bash
Python 3.10 + pandas 1.5.3 (Module 2)
```

Run the same cell again. Compare:

| | pandas 1.x | pandas 2.x |
|---|---|---|
| `df` after assignment | **is modified** | **not modified** |
| Signal shown | usually no exception | `ChainedAssignmentError` message |

The code is byte-for-byte identical. In pandas 1.x, chained assignment can silently overwrite your original dataframe. In pandas 2.x, Copy-on-Write blocks the mutation entirely. Same code. Different data. This is environmental drift.

---

### 2.2 The Hidden Culprits: Dependencies and Environments

The most common sources of environmental drift are ones you don't think about while you're working, because they're invisible:

**Library versions** are the biggest offender. `pandas` changed how `groupby` handles `NaN` values between versions. `scikit-learn` changed default parameters in estimators between major releases. `numpy` changed random number generation behaviour. Code that produces correct results on version X may silently produce different results on version Y — no error, no warning, just different numbers.

**Python itself** is a dependency. Code written for Python 3.9 may behave differently on 3.11. Some libraries drop support for older versions; others introduce subtle behavioural changes.

**Transitive dependencies** — the libraries your libraries depend on — are largely invisible. You install `torch` and get dozens of packages pinned to specific versions. Update one and the chain can shift in unpredictable ways.

The standard solution is a `requirements.txt` or `pyproject.toml` file that lists your dependencies. But this approach has a fundamental flaw: it's a separate file that you have to manually maintain, and it drifts. You add a library to your notebook, forget to add it to `requirements.txt`, and the file is stale before the day is out.

#### How marimo solves this: inline dependencies

marimo takes a different approach. When you run a notebook with the `--sandbox` flag, marimo tracks your dependencies *inside the notebook file itself*. When you import a library, marimo prompts you to install it — and records that package and its exact version directly as metadata in the `.py` file, in a format called inline script metadata.

The result looks like this at the top of your notebook file:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas==2.2.1",
#   "scikit-learn==1.4.0",
#   "matplotlib==3.8.3",
# ]
# ///
```

This block travels with the file. The next time anyone opens this notebook — on any machine, at any point in the future — marimo reads this block and automatically rebuilds the exact same isolated environment before running a single cell. No `pip install`. No `requirements.txt`. No "which version did you have?" The notebook *is* the environment spec.

This means the dependency problem goes from something you manage manually and separately to something marimo handles automatically and atomically. The notebook and its environment are a single artifact.

#### Try it: watch the notebook inspect its own environment spec

Open `Module_2/2.2.py` in marimo. This notebook demonstrates the environment story from inside the notebook itself.

**Step 1.** Run the notebook and inspect the current runtime. It shows:

- the notebook filename
- the current Python version
- the Python version required by the file
- the loaded versions of `pandas` and `matplotlib`

**Step 2.** Look at the next cell. The notebook reads its own `# /// script` block from disk and displays it directly in the UI:

```python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.0",
#     "pandas==2.2.3",
# ]
# ///
```

**Step 3.** Run the comparison cell below it. The notebook checks that the pinned versions in the metadata match the versions loaded in the active runtime.

**Step 4.** Now reopen the notebook in sandbox mode:

```bash
marimo edit --sandbox Module_2/2.2.py
```

Add a new import such as `import scipy`, run the cell, approve the installation, and then look back at the top of the file. marimo updates the `# /// script` block automatically. The environment spec lives in the same file as the notebook logic.

---

### 2.3 Version Control and Reviewable Experiments

Solving the environment problem is necessary but not sufficient. You also need to be able to track how your work changes over time, collaborate with others, and run the same notebook consistently across your local machine, a CI/CD pipeline, and the cloud. This is where marimo's file format becomes the second pillar of reproducibility.

#### Pure Python means real version control

Jupyter notebooks are stored as JSON — a format designed for machines, not humans. Open a `.ipynb` file in any text editor and you'll see why. Two cells — `x = 10` and `print(x * 2)` — look like this on disk:

```json
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": ["x = 10"]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {"name": "stdout", "output_type": "stream", "text": ["20\n"]}
   ],
   "source": ["print(x * 2)"]
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "name": "python3"},
  "language_info": {"name": "python"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

Two lines of code are wrapped in dozens of lines of JSON. When you change `x = 10` to `x = 20` and re-run the cell, the execution count increments, the output blob changes, and the metadata updates — all for a one-character edit. The signal is buried in the noise.

The same notebook in marimo is a `.py` file:

```python
import marimo
app = marimo.App()

@app.cell
def _():
    x = 10
    return (x,)

@app.cell
def _(x):
    print(x * 2)
    return

if __name__ == "__main__":
    app.run()
```

It's readable, diffable, and runnable as-is. Change one cell and the diff is exactly that cell — nothing more. You can review it in a pull request, run `git blame` on a specific line, or resolve a merge conflict in any text editor. None of that is practical with `.ipynb`.

#### Try it: let the notebook show you the diff

Open `Module_2/2.3.py` in marimo. This notebook makes the file-format argument concrete from inside the notebook.

**Step 1.** Run the notebook. One cell reads the notebook's own `.py` source and displays the exact excerpt containing:

```python
x = 10
print(x)
```

**Step 2.** The next cell computes the hypothetical change from `x = 10` to `x = 20` and renders the unified diff directly in the notebook. The key output is:

```diff
-    x = 10
+    x = 20
```

**Step 3.** Compare that with the representative Jupyter diff shown in the notebook:

```diff
-   "execution_count": 1,
+   "execution_count": 2,
     "outputs": [
      {
-      "text": ["10\n"],
+      "text": ["20\n"],
       ...
      }
-   "source": ["x = 10\n"]
+   "source": ["x = 20\n"]
```

The point is that the marimo file does not need any notebook-specific tooling to explain itself. It is already plain source code, and the notebook can prove that by reading and diffing its own file.

#### Running anywhere, consistently

A marimo notebook isn't just reviewable — it's executable as a standard Python script:

```bash
python Module_2/2.3.py
```

This means you can run it in a CI/CD pipeline without any special notebook tooling. You can schedule it as a cron job. You can execute it on a remote server over SSH. Anywhere Python runs, your notebook runs — and because the inline dependencies travel with the file, the environment is always correct.

#### Try it: run your notebook as a script

Take the `2.3.py` notebook and run it directly from the terminal:

```bash
python Module_2/2.3.py
```

It executes top to bottom, outputs print to stdout, and exits cleanly — no browser, no kernel, no notebook server. The same file you edited interactively is now a reproducible script you can hand to any Python environment or automation tool.

Combine this with `--sandbox` and the picture is complete: one file, version-controlled, with its environment pinned inside it, executable anywhere.

#### molab: consistent by default in the cloud

For situations where you don't want to manage a local environment at all — or where you need to share work with someone who doesn't have Python installed — marimo offers **molab**, its free cloud-hosted notebook service at [molab.marimo.io](https://molab.marimo.io/notebooks).

molab runs your notebook in a managed cloud environment. There's no local setup, no Python version to worry about, and no environment to configure. Because notebooks run on consistent infrastructure, the "works on my machine" problem doesn't arise — there is no "your machine." You write, run, and share entirely in the browser.

Notebooks on molab are shareable by URL and can be downloaded as `.py`, `.ipynb`, or PDF. If you store notebooks on GitHub, molab can preview them directly via a stable URL that updates as your repository changes — useful for sharing the latest version of an experiment without manually exporting anything.

#### VS Code: marimo in your existing editor

If you prefer working inside VS Code or Cursor rather than the browser-based editor, marimo has a first-class extension available in both marketplaces. The extension brings the full marimo runtime into your existing editor — reactive execution, the dependency graph, the variables panel — without leaving the environment you already use for the rest of your codebase.

This matters for reproducibility in a practical sense: your notebook lives alongside your other project files, opens in the same editor, and is checked into the same repository. There's no context switch between "notebook work" and "real code." It's all the same file, the same tool, the same Git workflow.

The VS Code extension is available in the VS Code and Cursor marketplaces. Search for **marimo** to install it.

#### Try it: open your notebook in VS Code

**Step 1.** Install the marimo extension from the VS Code marketplace (search "marimo").

**Step 2.** Open your project folder in VS Code. Open `Module_2/2.2.py`. You'll see an **"Open as marimo notebook"** button at the top of the file — click it.

**Step 3.** The full marimo editor opens inside VS Code: reactive cells, the variables panel, the dependency graph — everything from the browser editor, inside your existing IDE. Your file is still a `.py` file in your project. You can switch between the notebook view and the raw source with one click.

The key point: this is the same file, the same Git repo, the same workflow. There's no export step, no format conversion, no separate notebook environment to maintain alongside your codebase.

#### JupyterLab and JupyterHub: marimo without leaving your infrastructure

If your team or institution already runs JupyterLab or JupyterHub, you don't have to choose between your existing setup and marimo. The **marimo-jupyter-extension** integrates marimo directly into JupyterLab's launcher — no separate server, no separate URL, no workflow disruption.

Once installed, marimo appears as an option in the JupyterLab launcher alongside regular notebooks. A sidebar panel shows running marimo sessions and lets you manage them. The extension also handles environment selection when creating a new notebook, embedding the chosen Python environment as PEP 723 inline metadata in the file — the same `# /// script` block from section 2.2, set up automatically.

The detail that matters most for teams migrating from Jupyter: right-click any `.ipynb` file in JupyterLab's file browser and you get a **"Convert to marimo"** option. The conversion produces a clean `.py` marimo notebook. From that point on, the file is version-controllable, sandboxable, and executable as a script — everything this module has covered — with no manual rewriting required.

Install it alongside marimo:

```bash
uv pip install 'marimo[sandbox]>=0.19.11' marimo-jupyter-extension
```

Then launch JupyterLab as normal. The marimo icon appears in the launcher immediately.

For JupyterHub deployments, the extension works with existing authenticators and spawners. Install `marimo` in each user's environment and `marimo-jupyter-extension` in Jupyter's environment, then configure the marimo path in `jupyterhub_config.py`:

```python
# Explicit path
c.MarimoProxyConfig.marimo_path = "/opt/bin/marimo"

# Or use uvx for sandboxed mode
c.MarimoProxyConfig.uvx_path = "/usr/local/bin/uvx"
```

This means an organisation that has invested in JupyterHub infrastructure doesn't have to abandon it to adopt marimo. The two coexist — and over time, as teams convert notebooks and experience the reproducibility guarantees firsthand, the migration happens naturally.

---

Reactive execution keeps your work honest within a session. Inline dependencies keep your environment honest across machines and time. Plain Python keeps your history honest in version control. molab and the VS Code extension ensure these guarantees hold regardless of where and how you work. Together, they make reproducibility the default — not something you have to think about, just something that's already there.

That sets the foundation for Module 3: how interactivity, built on top of this reproducible base, actively accelerates the pace of discovery.

---

## Module 3: Why Interactivity Accelerates AI Discovery

Interactivity isn't a convenience feature. It's a fundamentally different way of thinking about ML work. When your data, your UI controls, your model, and your visualisations are all nodes in the same reactive graph, the feedback loop that drives discovery collapses from minutes to milliseconds. This module shows what that looks like in practice — not as a demo, but as a workflow you build yourself, piece by piece, across three sections that form one continuous notebook.

By the end of section 3.3 you'll have a complete interactive ML pipeline: live data exploration, a state-of-the-art tabular foundation model that updates as you reshape your data, and a visual debugging layer that shows you exactly where and why the model is wrong — all in a single marimo notebook, all reactive, all connected.

The dataset throughout is **Adult Income** — a classic benchmark predicting whether a person earns above $50K based on age, education, occupation, hours worked, and other demographic features. It's rich enough to produce interesting results, familiar enough to reason about intuitively, and raises genuinely important questions about fairness and model behaviour that will become relevant in section 3.3.

---

### 3.1 Interactive Computation as a Unified System

#### The concept: closing the loop

In a traditional notebook, data flows in one direction. You write code, it produces output, you look at it. If you want to change a parameter, you edit a cell and re-run. The output is passive — it displays, but it doesn't participate in computation.

In marimo, this changes fundamentally. UI elements — sliders, dropdowns, multiselects, tables — are not decorations. They are variables. When you move a slider, `slider.value` changes, and every cell that references `slider.value` re-executes automatically. The output becomes an input. The display becomes part of the computation.

This is what it means for your data, models, visualisations, and user input to work as a unified system. There is no boundary between "the interface" and "the code." They are the same reactive graph.

#### Hands-on: wire up the live system

Start a new sandboxed notebook:

```bash
marimo edit --sandbox adult_income_explorer.py
```

**Cell 1 — Load the data.** The Adult Income dataset is available directly from OpenML via sklearn:

```python
from sklearn.datasets import fetch_openml
import pandas as pd

data = fetch_openml("adult", version=2, as_frame=True)
df = data.frame
df["income"] = (df["class"].str.strip() == ">50K").astype(int)
df = df.drop(columns=["class"]).dropna()
df
```

The last line outputs the dataframe directly below the cell — no `print()`, no `display()`. marimo renders it as a scrollable table automatically.

**Cell 2 — Add a live dataframe explorer.** Replace the plain `df` output with marimo's interactive dataframe viewer:

```python
import marimo as mo

mo.ui.dataframe(df)
```

Now you can search, sort, filter, and page through the entire dataset interactively — directly in the notebook. Select the `age` column header to sort. Type in the search box to filter rows. This is `mo.ui.dataframe()` — marimo's built-in infinitely scalable table, capable of handling as much data as fits in your machine's RAM.

**Cell 3 — Add UI controls that the rest of the notebook will react to:**

```python
feature_selector = mo.ui.multiselect(
    options=["age", "education-num", "hours-per-week",
             "capital-gain", "capital-loss"],
    value=["age", "education-num", "hours-per-week"],
    label="Features to include"
)

train_size_slider = mo.ui.slider(
    start=0.1, stop=0.9, step=0.1, value=0.7,
    label="Training set size"
)

mo.vstack([feature_selector, train_size_slider])
```

**Cell 4 — React to the controls:**

```python
selected_features = feature_selector.value
train_size = train_size_slider.value

mo.md(f"""
**Active configuration:**
- Features: `{selected_features}`
- Training split: `{int(train_size * 100)}% / {int((1 - train_size) * 100)}%`
- Training rows: `{int(len(df) * train_size):,}`
""")
```

Change a feature in the multiselect. Watch the markdown cell update instantly — no re-run, no Shift-Enter. This is the unified system. Everything downstream of `feature_selector.value` and `train_size_slider.value` is now live. The model you'll add in section 3.2 will be part of that same graph.

> **From the gallery:** This is the same reactive pattern behind the marimo [Embedding Visualizer](https://molab.marimo.io/github/marimo-team/gallery-examples/blob/main/notebooks/algorithms/visualizing-embeddings.py) — where selecting points in embedding space feeds back as a Python dataframe. The mechanism is identical; only the domain changes.

---

### 3.2 Interactive Data in Model Development

#### The concept: never breaking the flow

Data exploration and model development are usually two separate phases. You explore in one set of cells, decide what to keep, manually copy those decisions into another set of cells for preprocessing, then run the model. Every time you change your mind about a feature or a filter, you repeat the cycle manually.

In marimo, these phases collapse into one. Your exploration controls *are* your preprocessing pipeline. There is no handoff step, no copy-paste, no re-running a chain of cells. The data you're looking at is the data the model sees — always, automatically.

#### Hands-on: shape data, feed the model

Continue in `adult_income_explorer.py`. Add these cells below what you built in 3.1.

**Cell 5 — Transform and split, reactively:**

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Encode categoricals in selected features only
X = df[selected_features].copy()
for col in X.select_dtypes(include="object").columns:
    X[col] = LabelEncoder().fit_transform(X[col].astype(str))

y = df["income"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    train_size=train_size,
    random_state=42,
    stratify=y
)

mo.md(f"""
**Dataset ready**
- Training: `{len(X_train):,}` rows × `{len(selected_features)}` features
- Test: `{len(X_test):,}` rows
""")
```

This cell references `selected_features` and `train_size` — both defined by UI controls in Cell 3. Every time you adjust a slider or toggle a feature, this cell re-runs automatically. The train/test split always reflects your current choices.

**Cell 6 — Introduce TabICL and fit the model.**

First, install TabICL (run this once in your terminal, or let marimo prompt you when running with `--sandbox`):

```bash
pip install tabicl
```

```python
from tabicl import TabICLClassifier
from sklearn.metrics import accuracy_score

clf = TabICLClassifier()
clf.fit(X_train, y_train)

preds = clf.predict(X_test)
acc = accuracy_score(y_test, preds)

mo.md(f"### Accuracy: `{acc:.1%}`")
```

> **What is TabICL?** TabICL (Tabular In-Context Learning) is a tabular foundation model pretrained on millions of synthetic datasets. Unlike traditional models, it requires no hyperparameter tuning — you pass it data and it classifies in a single forward pass using in-context learning, the same mechanism that lets large language models solve new tasks from examples. The result is a state-of-the-art classifier that adapts entirely to the data you give it, with no configuration required. This makes it the ideal model for an interactive pipeline: there is nothing to tune, so all the interactivity focuses on the data itself. TabICL was introduced at ICML 2025 by researchers at Inria.

Now do this: **deselect `education-num`** from the feature multiselect. Watch the accuracy update. Add it back. Watch it recover. **Drag the training size slider to 0.2.** See the accuracy drop as the model has less context to learn from. Drag it back to 0.7. The entire chain — split, encode, fit, evaluate — re-runs automatically every time.

This is interactive data in model development. You are not running experiments sequentially. You are navigating a live parameter space, and the model responds in real time.

**Cell 7 — Visualise per-class accuracy to deepen the picture:**

```python
import matplotlib.pyplot as plt
import numpy as np

classes = ["≤$50K", ">$50K"]
per_class_acc = [
    accuracy_score(y_test[y_test == i], preds[y_test == i])
    for i in [0, 1]
]

fig, ax = plt.subplots(figsize=(5, 3))
bars = ax.bar(classes, per_class_acc, color=["#4C72B0", "#DD8452"])
ax.set_ylim(0, 1)
ax.set_ylabel("Accuracy")
ax.set_title(f"Per-class accuracy\n(train size: {int(train_size*100)}%,"
             f" features: {len(selected_features)})")
for bar, val in zip(bars, per_class_acc):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.02,
            f"{val:.1%}", ha="center", fontsize=11)
plt.tight_layout()
fig
```

Now the story gets interesting. Drag the training slider down. Both bars drop — but not equally. The model degrades faster on the minority class (>$50K). Remove features one by one and watch which class suffers first. You have just turned a static model evaluation into an interactive fairness probe — without writing a single extra line of analysis code.

---

### 3.3 Visual Feedback for Analysis and Debugging

#### The concept: outputs as inputs

Section 3.2 showed data flowing *into* the model. This section shows information flowing *back out* — not just as numbers, but as selections you can act on. In marimo, a visualisation isn't just a display. A table isn't just a readout. Both can be interaction surfaces that feed back into your Python environment.

When you select rows in a `mo.ui.table()`, those rows come back as a dataframe. When a chart highlights a cluster, you can get that cluster back as data. This closes the loop: explore → model → visualise → select → explore again. Every observation becomes actionable.

#### Hands-on: find and interrogate the errors

Continue in the same notebook. Add these cells below section 3.2.

**Cell 8 — Build the error map.**

> **Note:** This cell plots `age` vs `hours-per-week`. Make sure both are included in your feature selector before running it.

```python
import matplotlib.pyplot as plt

# Attach predictions and ground truth to test rows
results_df = X_test.copy()
results_df["true_label"] = y_test
results_df["predicted"] = preds
results_df["correct"] = (y_test == preds).astype(int)
results_df["income_label"] = results_df["true_label"].map(
    {0: "≤$50K", 1: ">$50K"}
)

correct = results_df[results_df["correct"] == 1]
errors = results_df[results_df["correct"] == 0]

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(correct["age"], correct["hours-per-week"],
           c="#4C72B0", alpha=0.3, s=15, label="Correct")
ax.scatter(errors["age"], errors["hours-per-week"],
           c="#C44E52", alpha=0.6, s=20, label="Misclassified")
ax.set_xlabel("Age")
ax.set_ylabel("Hours per week")
ax.set_title("Model errors: age vs hours worked")
ax.legend()
plt.tight_layout()
fig
```

Look at where the red dots cluster. Are errors concentrated in a particular age band? Among people who work unusually long or short hours? This scatter plot is your first visual signal — a pattern in the mistakes that numbers alone wouldn't surface.

**Cell 9 — Make errors selectable:**

```python
# Show only columns that are actually in the dataframe (depends on current feature selection)
feature_cols = [c for c in ["age", "education-num", "hours-per-week", "capital-gain"]
                if c in errors.columns]
error_table = mo.ui.table(
    errors[feature_cols + ["income_label", "predicted"]].rename(
        columns={"income_label": "true", "predicted": "pred"}
    ),
    label="Select misclassified rows to inspect"
)
error_table
```

Select a group of rows from the table — perhaps the ones in an age range you noticed clustering in the scatter. marimo sends those rows back to Python immediately.

**Cell 10 — Inspect the selection:**

```python
selected = error_table.value

if len(selected) > 0:
    mo.vstack([
        mo.md(f"**{len(selected)} rows selected**"),
        mo.md(f"""
| Feature | Selected mean | Full test mean |
|---|---|---|
| Age | {selected['age'].mean():.1f} | {results_df['age'].mean():.1f} |
| Hours/week | {selected['hours-per-week'].mean():.1f} | {results_df['hours-per-week'].mean():.1f} |
| Education | {selected['education-num'].mean():.1f} | {results_df['education-num'].mean():.1f} |
""")
    ])
else:
    mo.callout(mo.md("Select rows in the table above to inspect them."),
               kind="info")
```

Select the cluster of red dots you identified. The comparison table appears instantly. Are the selected errors older workers? People with high capital gains that the model hasn't seen in training? People with atypical hours patterns?

**Cell 11 — Close the loop:**

```python
mo.md("""
### What to do with this

Go back to the **feature selector** in section 3.1 and add or remove features based on what you've just found. If capital gain seems to be driving errors, include it. If education-num doesn't seem to separate errors from correct predictions, try removing it.

Watch the scatter plot in Cell 8 update. Watch the per-class accuracy bars in Cell 7 shift. Watch the error table in Cell 9 populate with a different set of rows.

You have just completed one full iteration of the interactive ML loop:
**explore data → fit model → visualise errors → form a hypothesis → adjust data → repeat.**

In a traditional notebook, this loop takes 10–15 minutes of manual re-running. In marimo, it takes as long as it takes you to think.
""")
```

> **Going deeper:** The pattern you've built here — select points, get them back as data, act on them — is the same mechanism behind the marimo [Visualizing Embeddings](https://molab.marimo.io/github/marimo-team/gallery-examples/blob/main/notebooks/algorithms/visualizing-embeddings.py) gallery notebook, and behind the published research on [Minimum-distortion Embedding](https://arxiv.org/abs/2103.02559) by Akshay Agrawal at Stanford. The notebook you just built is a simplified version of real research infrastructure.

---

The three sections of this module have built one thing: a notebook where data exploration, model evaluation, and error analysis are not separate steps but a single continuous loop. That loop is fast enough to think inside. And that speed — the ability to form a hypothesis and test it before you've forgotten why you had it — is what interactivity actually means for AI discovery.

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

Open `adult_income_explorer.py` from Module 3. Hover over the Cell 7 (per-class accuracy bar chart) and click **Generate with AI**.

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

In `adult_income_explorer.py`, open the Chat panel. Without pasting anything, type:

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

**Step 2 — Test with a real task.** In `adult_income_explorer.py`, hover over Cell 5 and click Generate with AI. Prompt:

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

Each section uses `adult_income_explorer.py` from Module 3 as the working example. By the end of this module, the same file you built interactively will be running in four different modes — no duplication, no reformatting, no export step.

---

### 5.1 Turning Your Work Into Executable Scripts

#### The concept: one file, two modes

Every marimo notebook is a valid Python program. The `if __name__ == "__main__": app.run()` block at the bottom means you can execute it directly from the command line, just like any other Python script. The reactive graph runs top to bottom, cells execute in dependency order, and outputs print to stdout.

This matters for ML pipelines because it means your interactive exploration and your production pipeline are the same file. You don't maintain a notebook for exploration and a separate script for automation. You have one file that does both.

#### Hands-on: run as a script

**Step 1 — Run the notebook directly:**

```bash
python adult_income_explorer.py
```

The notebook executes: data loads, preprocessing runs, TabICL fits, accuracy prints. No browser, no kernel, no UI. The reactive graph determines execution order automatically.

**Step 2 — Add command-line arguments with argparse.** Open `adult_income_explorer.py` and add a setup cell at the top (right-click the first cell → "Add setup cell"):

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
python adult_income_explorer.py --train-size 0.5 --features age hours-per-week capital-gain
```

The same notebook that runs interactively with sliders now accepts CLI arguments for automation. One file, both modes.

**Step 5 — Schedule it.** Because it's a plain Python script, you can run it on a schedule with cron:

```bash
# Run every day at 6am, log output
0 6 * * * python /path/to/adult_income_explorer.py --train-size 0.8 >> /logs/daily_run.log 2>&1
```

Or in a GitHub Action:

```yaml
- name: Run notebook as script
  run: python adult_income_explorer.py --train-size 0.8
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
marimo run adult_income_explorer.py
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
marimo run adult_income_explorer.py --host 0.0.0.0 --port 8080
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
marimo export html adult_income_explorer.py -o report.html
```

Open `report.html` in any browser. No Python, no server. Share it as an email attachment, add it to a documentation site, or commit it to a repo. The plots, tables, and Markdown are all there.

To include pre-rendered outputs (so the HTML shows results immediately without running anything):

```bash
marimo export html adult_income_explorer.py -o report.html --include-outputs
```

**Step 2 — Export to PDF:**

```bash
marimo export pdf adult_income_explorer.py -o report.pdf
```

**Step 3 — Publish to molab.** Push your notebook to a GitHub repository, then generate a shareable molab preview URL:

```
https://molab.marimo.io/github/<your-username>/<your-repo>/blob/main/adult_income_explorer.py
```

Anyone with this URL sees a live preview of your notebook. They can fork it into their own molab workspace and run it — with the same sandbox environment, the same inline dependencies — without installing anything. This is the sharing story for research: one URL, fully reproducible.

**Step 4 — Generate a WASM-powered interactive HTML.** This exports your notebook as a self-contained HTML file that runs entirely in the browser via WebAssembly — no server needed, fully interactive:

```bash
marimo export html-wasm adult_income_explorer.py -o interactive_report.html
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
      - run: marimo export html-wasm adult_income_explorer.py -o docs/index.html
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

**Step 1 — Create a setup cell.** In `adult_income_explorer.py`, right-click the first cell and select **"Convert to setup cell"** (or add one via the cell menu). The setup cell is marked with a special indicator in the editor and always runs first.

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
