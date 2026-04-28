## Module 2: Reproducibility as a Baseline for Trustworthy AI


### 2.1 The "It Works on My Machine" Problem

> 💡 **Try it — `Module_2/2_1_environment_drift.ipynb`**
>
> **Example 1: scikit-learn version change**  
> The notebook uses `CalibratedClassifierCV(method="temperature")`. In scikit-learn `1.8.0`, it works. In scikit-learn `1.7.2`, it fails.
>
> **Example 2: pandas API change**  
> The notebook reads a CSV using `delim_whitespace=True`. In older pandas versions this works, but in pandas 3.x it raises an error.
>
> | | pandas 1.x | pandas 3.x |
> |---|---|---|
> | `delim_whitespace=True` | works | raises an error |

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
> Run the notebook and inspect the active Python, `pandas`, and `matplotlib` versions. Then reopen it in sandbox mode:
>
> ```bash
> marimo edit --sandbox Module_2/2_2_sandboxed_environment.py
> ```

---

### 2.3 Version Control and Reviewable Experiments

Reproducibility is not only about execution. It is also about making experiments visible, reviewable, and easy to compare over time.

#### The file format problem

Jupyter notebooks are stored as JSON files that contain both code and outputs. That means a small code edit often does not look small in version control. Execution counts, outputs, and metadata are saved alongside the code, so a one-line change can produce a noisy diff.

That makes review harder because the real change is mixed with notebook structure.

A marimo notebook is a plain Python file. Each notebook cell is saved as Python code in the file, and marimo does not save outputs in the notebook file. Small changes to notebook code therefore create small, localized changes in the file, which makes Git diffs much easier to read. The diff corresponds closely to the code change itself, with the file changing only where the code changed.

By contrast, the equivalent Jupyter notebook diff can become dramatically larger because `.ipynb` files store outputs and notebook state alongside the code, including base64-encoded output blobs. In the marimo example, the equivalent Jupyter diff grows to tens of thousands of characters and includes many changes unrelated to the original one-character edit.

These diffs are not only difficult for an individual to read, they also make merge conflicts much harder to resolve in collaborative work.

> 💡 **Try it — `Module_2/2_2_sandboxed_environment.py`**
>
> Run the notebook. It shows a live one-line diff for a small code change, then the equivalent Jupyter diff for the same change.
>
> You can also inspect the diff in the terminal:
>
> ```bash
> git diff Module_2/2_2_sandboxed_environment.py
> ```
>
> If Git opens a pager, press `q` to exit. If you end up in Vim instead, use `:wq` to save and quit or `:q!` to quit without saving.
>
> A simple live demo is:
>
> ```python
> a = 10
> b = 20
> c = a + b
> c
> ```
>
> Show this first in the notebook, then open the saved `.py` file and point out that each cell is stored as Python code and the output is not saved in the file. Then change `a = 10` to `a = 15` and show the Git diff. The file change stays small and readable.

#### Reviewability supports reproducibility

When experimental work is easy to review, reproducibility gets stronger. Clear diffs make it easier to answer basic but important questions:

- What code changed?
- Did the data processing logic shift?
- Was a parameter updated?
- Did the result change because of the code, or because of the environment?

Plain-text notebooks help because the important changes are visible. That makes collaboration more reliable and reduces the chance that a meaningful experimental change is hidden inside formatting noise.

This is the core advantage of treating notebooks as Python rather than JSON: the file stays closer to the logic you actually want to review.

This matters for trustworthy AI because reproducibility is not only technical. It is also social. Other people need to inspect what changed, understand why it changed, and verify that the result still deserves confidence.

> **On outputs:** marimo does not store outputs in the notebook file, which keeps diffs cleaner and makes code review easier.


---


### Code to Remember

```bash
marimo edit --sandbox Module_2/2_2_sandboxed_environment.py
```

Use this to show the strongest reproducibility setup: an isolated environment plus notebook-carried dependencies.

```bash
git diff Module_2/2_2_sandboxed_environment.py
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




