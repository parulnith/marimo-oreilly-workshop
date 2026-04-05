## Running marimo everywhere

One of marimo's most practical advantages is that a notebook is just a Python
file. You do not need to convert it into a different format to use it in
different settings. The same `.py` notebook can be edited, shared, reviewed,
and executed across multiple environments.

---

### One notebook, many runtimes

| Environment | How it works |
|---|---|
| **Terminal / Notebook mode** | `marimo edit notebook.py` opens the notebook as an interactive notebook interface. |
| **App mode** | `marimo run notebook.py` serves the notebook as a web app, with code hidden from view. |
| **Sandbox mode** | `marimo edit --sandbox notebook.py` runs the notebook in an isolated environment for cleaner dependency management. |
| **VS Code** | Open the `.py` file directly in VS Code, or use the official [marimo VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) for a more integrated notebook experience. |
| **molab** | [molab.marimo.io](https://molab.marimo.io) lets you use marimo in the cloud without a local installation. |
| **JupyterLab** | marimo notebooks can also be used through the [marimo JupyterLab extension](https://github.com/marimo-team/marimo-jupyter-extension). |
| **Script execution** | `python notebook.py` runs the notebook directly as a Python script. |

---

### Why this matters

The key idea is simple: one notebook, many ways to run it.

Because marimo notebooks are stored as plain Python files, they fit naturally
into normal development workflows while still supporting interactive notebook
use. That means fewer format mismatches, cleaner version control, and fewer
situations where a notebook only works in one tool.

For example, a simple marimo notebook still remains valid Python:

```python
x = 10
y = 20
print("Sum =", x + y)
```

The same file can be reviewed like source code, run like a script, or opened as
an interactive notebook.

> **On outputs:** marimo does not store outputs in the notebook file itself,
> which keeps diffs clean. When you want a visual record, you can export to HTML
> or IPYNB, or enable auto-snapshot while you work.
