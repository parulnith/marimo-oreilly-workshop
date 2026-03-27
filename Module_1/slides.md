---
title: Module 1 — Interactive Environments in the Modern AI/ML Stack
marp: true
theme: default
paginate: true
---

<!--
  MODULE 1 | SECTION 1.1
  Interactive Environments in the Modern AI/ML Stack
-->

## MODULE 1 | SECTION 1.1

# Interactive Environments in the Modern AI/ML Stack

Why the world's most impactful AI research happens inside notebooks

---

## Notebooks Are Where Breakthroughs Happen

Interactive code-writing environments such as Jupyter Notebook are beloved by data analysts and ML researchers because they combine software code, computational output, and explanatory text in a single document.

> **Alec Radford & the GPT Origin Story**
>
> The first author of the original GPT paper — and the researcher behind GPT-2, CLIP, DALL-E, and Whisper — did much of his groundbreaking work inside Jupyter Notebooks. No PhD. No fancy IDE. Just a notebook and a big idea.
>
> *Sam Altman called him an "Einstein-level genius."*

---

## The Core Loop of AI/ML Work

AI development isn't like building a web app. You don't write code, compile, and ship. You explore, experiment, and iterate — constantly moving between code, data, and results.

| **Write** | → | **See** | → | **Adjust** |
|---|---|---|---|---|
| A few lines of code — a transform, a model call, a visualization | | Immediately inspect the result — a chart, a table, a model's prediction | | Change a parameter, fix an assumption, try a different approach |

*This loop runs hundreds of times a day. The faster it runs, the faster you learn.*

---

## Where This Loop Matters Most

**Exploring a New Dataset**
Shapes, distributions, missing values, outliers — you need to see your data before you can model it.

**Evaluating Model Outputs**
Reading predictions, comparing responses, tweaking prompts — you judge quality by looking, not by compiling.

**Tuning Experiments**
Change a hyperparameter, re-train, check the loss curve. Repeat. The feedback loop is the experiment.

**Feature Engineering**
Try a transform, visualize the effect, keep it or discard it. Every decision needs immediate visual proof.

**In every case, you need to see intermediate results to decide what to do next.**

---

## Let's See It in Action

Enough theory. Let's open a real analysis — train a model, change something, and see what happens.

---

<!--
  MODULE 1 | SECTION 1.2
  When Traditional Notebook Systems Break Down
-->

## MODULE 1 | SECTION 1.2

# When Traditional Notebook Systems Break Down

The notebook you're looking at might not be telling you the truth

---

## The Imperative Trap

In a Jupyter notebook, you run a cell and it mutates memory. Then you run another cell and it mutates memory again. But Jupyter doesn't know how your cells are related. It has no dependency graph. So two things go wrong:

**Out-of-Order Execution**
You change a value in one cell, but forget to re-run the cells that depend on it. Now the code on your screen doesn't match the variables in memory. Your notebook becomes a patchwork of outputs from different states.

**Hidden State**
You delete a cell, but the variable it defined is still alive in memory. Other code still refers to it. Four hours later, you realize you've been working with inconsistent state the entire time.

---

## This Isn't a Minor Issue

A landmark study examined **1,159,166 Jupyter notebooks** from **264,023 GitHub repositories** (Pimentel et al., 2019):

| Finding | Result |
|---|---|
| Executed without errors | **24.11%** |
| Reproduced stored outputs | **4.03%** |
| Cells executed out of order | **36%** |
| Skips in execution counters (hidden state) | **77%** |

Out-of-order execution and hidden state are **the norm, not the exception**.

> Pimentel, J.F., Murta, L., Braganholo, V., and Freire, J. "A Large-scale Study about Quality and Reproducibility of Jupyter Notebooks." *MSR*, 2019.

---

## Let Me Show You

Let's go back to our notebook from 1.1 and break it — in ways you might not notice.

**Demo 1** Change a value, don't re-run downstream

**Demo 2** Delete a cell, ghost variable survives

---

<!--
  MODULE 1 | SECTION 1.3
  What If the Notebook Knew About Dependencies?
-->

## MODULE 1 | SECTION 1.3

# What If the Notebook Knew About Dependencies?

**Change a value** → Everything downstream updates automatically

**Delete a cell** → Its variables are scrubbed from memory automatically
