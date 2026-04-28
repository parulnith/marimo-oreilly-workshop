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

marimo has built-in package management. If you import a package that is missing, it can prompt you to install it and record that dependency inside the notebook.

That matters even outside sandbox mode, because the notebook can carry its own dependency information instead of relying only on a separate `requirements.txt`.

Then `--sandbox` takes it one step further: marimo uses `uv` to create an isolated environment and can auto-install from the dependencies serialized in the notebook.

So the workflow is:

- install on import
- save dependencies with the notebook
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


### Code to Remember

```bash
marimo edit --sandbox Module_2/2_2_sandboxed_environment.py
```

Use this to show the strongest reproducibility setup: an isolated environment plus notebook-carried dependencies.

```bash
git diff Module_2/2_3_marimo_diff_demo.py
```

Use this to show that a plain Python notebook produces readable diffs.

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



