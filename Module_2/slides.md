---
title: Module 2 — Reproducibility as a Baseline for Trustworthy AI
marp: true
theme: default
paginate: true
---

## MODULE 2

# Reproducibility as a Baseline for Trustworthy AI

Reactive execution keeps things in sync within a session.
This module is about what happens when you close the notebook.

---

<!--
  MODULE 2 | SECTION 2.1
-->

## MODULE 2 | SECTION 2.1

# The "It Works on My Machine" Problem

The notebook runs cleanly on your laptop.
Your colleague runs the same code and gets different numbers.

---

## The Silent Failure

The problem isn't the code. It's everything *around* the code.

- Different Python version
- Different library versions
- Different system configuration

Your notebook doesn't raise an exception when it produces a subtly wrong result due to a version mismatch. It just runs and outputs something — and you trust it.

> Recall: Pimentel et al. (2019) found only **4%** of Jupyter notebooks reproduced their original results. Most failures weren't bugs — they were **environmental drift**.

---

## Let Me Show You

Open `2.1.ipynb` — same code, two different environments.

**Demo:** Run the pandas cell in the default kernel. Then switch to
`Python 3.10 + pandas 1.5.3 (Module 2)` and run it again.

Same chained-assignment code. In pandas 1.5.3 it mutates `df`.
In pandas 3.0.1 it doesn't.

---

<!--
  MODULE 2 | SECTION 2.2
-->

## MODULE 2 | SECTION 2.2

# The Hidden Culprits: Dependencies and Environments

---

## Why requirements.txt Isn't Enough

The standard fix — a `requirements.txt` file — has a fundamental flaw:

**It's a separate file you have to manually maintain.**

You add a library to your notebook, forget to update the file, and it's stale before the day is out. The dependency spec and the code drift apart — silently.

---

## marimo's Fix: Inline Dependencies

When you run with `--sandbox`, marimo tracks dependencies **inside the notebook file itself**:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas==2.2.1",
#   "scikit-learn==1.4.0",
# ]
# ///
```

This block travels with the file. On any machine, marimo reads it and **rebuilds the exact environment automatically** — before running a single cell.

The notebook *is* the environment spec.

---

## Let Me Show You

Open `2.2.py` — a sandboxed marimo notebook.

**Demo:** The notebook reads its own `# /// script` block, shows the pinned versions,
and verifies them against the active runtime from inside the notebook.

---

<!--
  MODULE 2 | SECTION 2.3
-->

## MODULE 2 | SECTION 2.3

# Version Control and Reviewable Experiments

---

## Jupyter Notebooks Are a Git Nightmare

Jupyter notebooks are stored as **JSON** — designed for machines, not humans.

Change one cell → the diff touches execution counters, output blobs, metadata.
Reviewing a notebook PR is nearly impossible.

marimo notebooks are stored as **plain `.py` files**.

Change one cell → the diff shows **exactly that cell, nothing more**.

---

## The Diff That Says It All

**Jupyter** — change `x = 10` to `x = 20`:
```diff
-   "execution_count": 1,
+   "execution_count": 2,
-      "text": ["10\n"],
+      "text": ["20\n"],
-   "source": ["x = 10\n"]
+   "source": ["x = 20\n"]
```

**marimo** — the same change:
```diff
-    x = 10
+    x = 20
```

One line changed. One line in the diff.

---

## Let Me Show You

Open `2.3.py` — it reads its own source and computes the one-line diff in the notebook.

```bash
python 2.3.py
```

**Demo:** Same file you edit interactively, now also executable as a reproducible script in the terminal.
