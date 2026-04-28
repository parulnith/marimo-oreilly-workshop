# Module 1 Preparation Notes


# 1.1 Interactive Environments in the Modern AI/ML Stack

Slides only



# 1.2 When Traditional Notebook Systems Break Down

1. Switch to Jupyter (live demo)

Show simple code:

a = 1
b = 2
a + b

Ask:

What will this output?


Then do:

Run a = 1, b = 2
Run a + b

Add new cell:

b = 11

→ run it

Delete that cell
Run a + b again


The code for b = 11 is gone, but the value is still in memory.

3. Go back to slides (name the problems)

The problem you saw is the classic  Hidden State issue

Title: Hidden State

Content:

Variables remain in memory  
even after the code is gone  


This is hidden state. The notebook is carrying information that is not visible in the code.

Slide: Out-of-Order Execution


This happens when I change something upstream but don’t rerun everything downstream.

4. Add the “run all is not practical” point

Show:

import time
time.sleep(10)


5. Transition to compound interest

Say:

That was a tiny example. Let’s look at a slightly more realistic workflow.

Then move into your compound interest example.



This creates two common issues.

The first is **out-of-order execution**.

This happens when cells are run in a different order than they appear in the notebook.

The second is **hidden state**.

This happens when old variables remain in memory even when the notebook no longer shows where they came from.

This is why a notebook can look correct and still be wrong.

For example, suppose one cell defines:

```python
principal = 1000
rate = 0.07
years = 20
```

Then the next cells calculate a result, draw a chart, and build a summary table.

Now I change `years` from `20` to `50`, but I only rerun that one cell.

The code now says 50 years, but the printed result may still say 20 years. The chart may still show 20 years. The table may still be based on 20 years.

Nothing looks obviously broken, but the notebook is now inconsistent.

This is the risk. Traditional notebooks give us speed, but they rely heavily on the user to remember what needs to be rerun.


# 1.3 Why Reactive Execution Is a Better Alternative


This is where **reactive execution** helps.

Instead of treating the notebook as a loose list of cells, a reactive notebook treats it as a **dependency graph**.

That means the notebook knows which cells define which variables, and which cells depend on them.

So when one value changes, dependent cells can update.

If a downstream cell is expensive, it can be marked as stale instead of rerunning right away.

If a cell is deleted, the variables from that cell are removed from memory.

This gives us a cleaner model:

**the code on screen, the variables in memory, and the outputs we see stay connected.**

You can think of it like a spreadsheet. When one value changes, the formulas that depend on it update too.

This matters a lot in AI and ML because we are constantly making small changes and reading the results.

If the environment does not track dependencies, it is easy to trust an old output by mistake.

So the point is not just a nicer notebook interface. The point is a better execution model.

## Live demo plan

Use the compound interest example here in marimo

### Step 1: Show the plain setup

```python
principal = 1000
rate = 0.07
years = 20
```

### Step 2: Show downstream cells

Explain that downstream cells:

**calculate growth**
**print the final balance**
**draw a chart**
**build a summary table**
**create a report**

### Step 3: Change `years`

Change:

```python
years = 20
```

to:

```python
years = 50
```

Then show what happens in marimo.

The connected cells update, or in lazy mode, become stale.

### Step 4: Delete a defining cell

Delete the function or variable cell and show that downstream cells fail right away.

Say:

> This may feel strict, but it is exactly what we want. I would rather see the error now than carry a ghost variable that breaks later.

## Explain the DAG

Use this language:

marimo builds a **DAG**, or **directed acyclic graph**, from your notebook.

It checks what each cell defines and what each cell reads.

From that, it builds the notebook’s dataflow.

When you delete a cell:

1. marimo removes the cell's variables from memory
2. Dependent cells are invalidated immediately

It's like a spreadsheet: change a cell and the formulas update. The dependency graph is the thing that makes everything else possible — reactivity, no hidden state, deterministic execution, and the ability to run notebooks as apps or scripts.

## Explain lazy mode

Use this language:

Reactive execution does not mean everything must rerun immediately all the time.

In ML, some cells are expensive. A cell may train a model, call an API, or process a large dataset.

That is where **lazy mode** helps.

In lazy mode, marimo still tracks what changed, but instead of rerunning expensive downstream cells right away, it marks them as **stale**.

So I know the output is no longer current, and I can decide when to rerun it.

This gives us a useful middle ground:

**the notebook tracks correctness, but I stay in control of expensive execution.**


# 1.4 Hands On with marimo: A Modern Programming Environment


Now that we have seen the reactive execution model in action, let us take a few minutes to walk through the marimo environment itself.


## 1. Start from the terminal

Show:

```bash
marimo edit Module_1/1_2_marimo_reactive_workflow.py
```

Say:

I am starting from the terminal because marimo notebooks are Python files. They are not trapped inside a notebook-only format.

We can open them, edit them, run them, and later execute them like regular Python programs.

You can also show this briefly:

```bash
python Module_1/1_2_marimo_reactive_workflow.py
```

Say:

We will come back to this later in the workshop, especially when we talk about scripts, apps, artifacts, and reusable modules.


## 2. Show the center cell area

At the center, we have the main **cell area**.

This is where we write code, markdown, and explanations.

It still feels familiar if you have used notebooks before. You write a cell, run it, and see the output below it.


## 3. Show the Variables panel


The first useful panel is the **Variables** panel.

This shows the variables currently defined in the notebook. You can see names, types, and values.

This is useful because notebook state is no longer hidden.

Instead of wondering what is sitting in memory, you can inspect it directly.

For AI and ML workflows, this matters a lot.

You may have a dataframe, a feature list, a trained model, a set of predictions, or evaluation metrics in memory.

The variables panel gives you a quick way to see what exists and where you are in the workflow.

## 4. Show the Dependency graph


Next is the **Dependency graph**.

This is one of the most important parts of marimo.

It shows how the notebook cells depend on each other.



## 5. Show lazy mode


Now I want to show **lazy mode**, because this matters for ML work.

Reactive execution is useful, but some cells are expensive.

You may have a cell that trains a model, calls an API, or processes a large dataset.

You may not want that cell to rerun immediately every time an input changes.

That is where lazy mode helps.

In lazy mode, marimo still tracks what changed, but it marks affected cells as stale instead of running them immediately.

So I know the output is no longer current, but I decide when to rerun it.


## 6. Show UI elements

Now let us look at **UI elements**.

In marimo, sliders, dropdowns, tables, and plots can connect directly to Python.

A UI element is just a Python object. You can read its current value and use it in another cell.

This means you can build small interactive tools inside the notebook itself.

For example, you can choose a model, adjust a threshold, filter a dataframe, select points in a chart, or change a parameter and immediately see how the output changes.

This is where marimo starts to feel like an interactive workspace.

## 8. Show terminal or logs panel


There is also a **logs** panel and terminal-related workflow support.

When code prints output, raises errors, or runs as a script, you can inspect that from the environment or the terminal.

It keeps notebook work close to how Python projects are actually run.

## 9. Show command palette and editor tools

You also have a **command palette**, package help, documentation support, and code editing features.


## 10. Mention Python file format

One more practical detail: marimo notebooks are stored as **plain Python files**.

It means the notebook is easier to inspect in Git, easier to review, easier to open in a normal editor, and easier to run as a script.





