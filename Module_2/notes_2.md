## Module 2: Reproducibility as a Baseline for Trustworthy AI


### 2.1 The "It Works on My Machine" Problem

> 💡 **Try it — `Module_2/2_1_environment_drift.ipynb`**
>
> **Example 1: scikit-learn version change**  
> The notebook uses `CalibratedClassifierCV(method="temperature")`. In scikit-learn `1.8.0`, it works. In scikit-learn `1.7.2`, it fails.
>
> **Example 2: pandas API change**  
> The notebook reads a CSV using `delim_whitespace=True`. In pandas 2.x this still works, but it is deprecated; in pandas 3.x it raises an error.
>
> | | pandas 2.x | pandas 3.x |
> |---|---|---|
> | `delim_whitespace=True` | works, with deprecation warning | raises an error |

---

### 2.2 The Hidden Culprits: Dependencies and Environments


#### How marimo helps

marimo has built-in package management. If you import a package that is missing, it can prompt you to install it using your package manager.

Outside sandbox mode, packages are installed into the active environment or project. In sandbox mode, marimo also records notebook-specific dependencies in the notebook file.

Then `--sandbox` takes it one step further: marimo uses `uv` to create an isolated environment and can install from the dependencies serialized in the notebook.

So the workflow is:

- install on import
- save dependencies with the notebook in sandbox mode
- use `--sandbox` for a clean, isolated run

> **Note:** sandbox gives the strongest reproducibility because execution happens in an isolated environment.

> 💡 **Try it — `Module_2/2_2_sandboxed_environment.py`**
>
> Run the notebook and inspect the active Python, `scikit-learn`, and `pandas` versions. Then reopen it in sandbox mode:
>
> ```bash
> marimo edit --sandbox Module_2/2_2_sandboxed_environment.py
> ```

---

### 2.3 Version Control and Reviewable Experiments


Reproducibility is not only about execution. It is also about making experiments visible, reviewable, and easy to compare over time.

Jupyter notebooks are stored as JSON files that can include code, outputs, execution counts, and metadata. A tiny code edit can therefore create a much larger Git diff when a plot output is saved with the notebook.

A marimo notebook is a plain Python file. The same parameter edit stays close to the code that changed, and rendered outputs are not stored in the notebook file.

These noisy diffs are not only difficult for an individual to read, they also make merge conflicts much harder to resolve in collaborative work.

> 💡 **Try it — compare the two diff demos**
>
> In both files, change `power = 3` to `power = 4`, save, and compare the Git diffs.
>
> marimo:
>
> ```bash
> git diff Module_2/2_3_marimo_diff_demo.py
> ```
>
> Jupyter:
>
> ```bash
> git diff Module_2/2_3_jupyter_diff_demo.ipynb
> ```
>
> If Git opens a pager, press `q` to exit. If you end up in Vim instead, use `:wq` to save and quit or `:q!` to quit without saving.
>

#### Reviewability supports reproducibility

When experimental work is easy to review, reproducibility gets stronger. Clear diffs make it easier to answer basic but important questions:

- What code changed?
- Did the data processing logic shift?
- Was a parameter updated?
- Did the result change because of the code, or because of the environment?


---

#### Editor workflow: VS Code

Because marimo notebooks are plain `.py` files, they are not locked to the
browser editor. You can open them directly in VS Code, review them like normal
Python files, and use standard Git tooling.

For a more integrated notebook experience in VS Code, install the official
marimo extension:

```text
marimo VS Code extension
https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo
```

Teaching point: marimo keeps the notebook workflow, but the file still behaves
like normal Python for editors, diffs, reviews, and project tooling.

#### Cloud workflow: molab

The same `.py` file that runs locally and in VS Code also runs in the browser —
no install, no environment setup. **molab** is marimo's hosted workspace at
[molab.marimo.io](https://molab.marimo.io). Because notebooks carry their own
inline dependencies, molab can pick up a notebook from GitHub and run it in a
sandbox with the exact same packages as your laptop.

Open any notebook from a public GitHub repo with a URL of this shape:

```text
https://molab.marimo.io/github/<user>/<repo>/blob/main/<path-to-notebook>.py
```

This is the sharing story for reviewable experiments: one URL, no setup, the
same sandboxed environment a reviewer or collaborator would get if they cloned
your repo and ran `marimo edit --sandbox` themselves.

Teaching point: the same notebook behaves identically across local CLI, VS Code,
and the cloud — that's what makes the experiment portable and reviewable.

---


### Code to Remember

```bash
marimo edit --sandbox Module_2/2_2_sandboxed_environment.py
```

Use this to show the strongest reproducibility setup: an isolated environment plus notebook-carried dependencies.

```bash
git diff Module_2/2_3_marimo_diff_demo.py
```

Use this to show that a plain Python notebook produces readable diffs.

```text
VS Code extension:
https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo
```

Use this to show that marimo notebooks can live in a normal editor workflow.

```python
# dependencies live with the notebook
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "pandas==2.3.3",
#     "scikit-learn==1.8.0",
# ]
# ///
```

Use this as the visual reminder that the environment is part of the work.
