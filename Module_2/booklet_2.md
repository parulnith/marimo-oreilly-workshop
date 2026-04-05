## Module 2: Reproducibility as a Baseline for Trustworthy AI

There's a big difference between just running your code again and reliably getting the same results across different computers and over time. Reproducibility means that anyone — on any machine, at any point in the future — gets the same result from the same code. That guarantee is hard to achieve and easy to lose, and losing it is particularly costly in AI work where the output of your notebook is a model or a metric that others will rely on.

---

### 2.1 The "It Works on My Machine" Problem


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


Environmental drift comes from three sources. 
**Library versions** change APIs and defaults between releases. 
**Python itself** changes behaviour across versions. 
**Transitive dependencies** shift when anything upstream updates.

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

Because marimo notebooks are plain Python files, they run consistently across every environment.

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

