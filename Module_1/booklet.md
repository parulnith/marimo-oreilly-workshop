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

