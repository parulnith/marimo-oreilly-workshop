## Module 2: Reproducibility as a Baseline for Trustworthy AI

### Opening

Reproducibility is more than rerunning code on the same laptop and hoping for the same output. In trustworthy AI, reproducibility means the same code produces the same result across different machines, for different people, and at different points in time.

That standard matters because AI systems are often judged through metrics, model behaviour, and experimental results. If those results shift because of an invisible change in environment, then trust in the workflow starts to break down.


---

### 2.1 The "It Works on My Machine" Problem

One of the most common problems in technical work is the gap between local success and shared reliability. A notebook may run perfectly on one machine and fail on another, even when the code looks identical.

This happens because rerunning code is not the same as reproducing results. A rerun only tells you that something still works in your current setup. Reproducibility asks a harder question: would someone else, using the same code later or elsewhere, get the same outcome?

> 💡 **Try it — `Module_2/2.1.ipynb`**
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

The lesson is straightforward: the same code can behave differently when the surrounding environment changes. If the environment is undefined, the result is unreliable.

**Script cue:**  
When people say, "it works on my machine," they usually mean the code runs in one specific setup. That is not yet reproducibility. Reproducibility means the result survives outside that one setup.

---

### 2.2 The Hidden Culprits: Dependencies and Environments

When reproducibility breaks, the cause is often hidden in the environment rather than the notebook itself.

Three common culprits are:

- **Library versions:** package updates can change APIs, defaults, and behaviours.
- **Python versions:** language and runtime changes can affect execution.
- **Transitive dependencies:** a package you never installed directly may still change underneath your project.

These issues are easy to overlook because they are often external to the code you are reading. A notebook may appear stable while the environment around it slowly drifts.

Teams often try to manage this with a `requirements.txt` file. That helps, but it still depends on manual updates and on keeping the notebook and environment definition in sync.

#### How marimo helps

marimo has built-in package management. If you import a package that is missing, it can prompt you to install it and record that dependency inside the notebook.

That matters even outside sandbox mode, because the notebook can carry its own dependency information instead of relying only on a separate `requirements.txt`.

Then `--sandbox` takes it one step further: marimo uses `uv` to create an isolated environment and can auto-install from the dependencies serialized in the notebook.

So the workflow is:

- install on import
- save dependencies with the notebook
- use `--sandbox` for a clean, isolated run

> **Note:** sandbox gives the strongest reproducibility because execution happens in an isolated environment.

> 💡 **Try it — `Module_2/2.2.py`**
>
> Run the notebook and inspect the active Python, `pandas`, and `matplotlib` versions. Then reopen it in sandbox mode:
>
> ```bash
> marimo edit --sandbox Module_2/2.2.py
> ```

**Script cue:**  
The important idea here is that reproducibility should not depend on memory or manual documentation alone. The environment needs to be defined and carried with the work.

---

### 2.3 Version Control and Reviewable Experiments

Reproducibility is not only about execution. It is also about making experiments visible, reviewable, and easy to compare over time.

#### The file format problem

Jupyter notebooks are stored as JSON files that contain both code and outputs. That means a small code edit often does not look small in version control. Execution counts, outputs, and metadata are saved alongside the code, so a one-line change can produce a noisy diff.

That makes review harder because the real change is mixed with notebook structure.

A marimo notebook is a plain Python file. Each notebook cell is saved as Python code in the file, and marimo does not save outputs in the notebook file. Small changes to notebook code therefore create small, localized changes in the file, which makes Git diffs much easier to read. The diff corresponds closely to the code change itself, with the file changing only where the code changed.

By contrast, the equivalent Jupyter notebook diff can become dramatically larger because `.ipynb` files store outputs and notebook state alongside the code, including base64-encoded output blobs. In the marimo example, the equivalent Jupyter diff grows to tens of thousands of characters and includes many changes unrelated to the original one-character edit.

These diffs are not only difficult for an individual to read, they also make merge conflicts much harder to resolve in collaborative work.

> 💡 **Try it — `Module_2/2.2.py`**
>
> Run the notebook. It shows a live one-line diff for a small code change, then the equivalent Jupyter diff for the same change.
>
> You can also inspect the diff in the terminal:
>
> ```bash
> git diff Module_2/2.2.py
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

**Script cue:**  
Reproducibility is easier to maintain when changes are easy to inspect. Reviewable experiments make trustworthy workflows more realistic for teams, not just individuals.

---

### Closing

Reproducibility is the baseline that makes trustworthy AI possible. It is not only about whether code runs again, but whether results remain stable across environments, collaborators, and time.

In this module, the key takeaway is that trustworthy AI depends on more than models and metrics. It also depends on controlled environments, reviewable changes, and workflows that remain stable over time.

### 3 Takeaways to Remember

1. **Re-running is not the same as reproducibility.**  
   If the same code gives different results on another machine or at another time, the workflow is not yet trustworthy.

2. **The environment is part of the result.**  
   Library versions, Python versions, and transitive dependencies all affect behavior, so reproducibility requires defining and carrying the environment with the notebook.

3. **Readable diffs make experiments easier to trust.**  
   When changes are easy to inspect in Git, it is easier to review experiments, understand what changed, and resolve collaboration issues.

### Code to Remember

```bash
marimo edit --sandbox Module_2/2.2.py
```

Use this to show the strongest reproducibility setup: an isolated environment plus notebook-carried dependencies.

```bash
git diff Module_2/2.2.py
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

**Script cue:**  
Trustworthy AI starts with reproducible results. Reproducibility depends on the environment, not just the code. If changes are easy to review, results are easier to trust.

---

## Quiz

### 1. Which statement about marimo sandboxing is most accurate?

- A. Sandboxing is enabled automatically for every notebook
- B. Sandboxing uses an isolated environment and must be enabled with `--sandbox`
- C. Sandboxing only changes how Git displays diffs
- D. Sandboxing removes the need to track dependencies

**Answer:** B. Sandboxing uses an isolated environment and must be enabled with `--sandbox`

**Explanation:** Sandboxing is opt-in. It creates an isolated environment so notebook dependencies do not interfere with the rest of the system or project setup.

---

### 2. A one-line change is made in both a marimo notebook and an equivalent `.ipynb` notebook. The `.ipynb` diff is much larger. What is the best explanation?

- A. Git handles notebook files incorrectly
- B. The marimo notebook hides parts of the diff automatically
- C. The `.ipynb` file stores code together with notebook structure, execution state, and output data
- D. The `.ipynb` change must be more important than the marimo change

**Answer:** C. The `.ipynb` file stores code together with notebook structure, execution state, and output data

**Explanation:** Jupyter notebook diffs often include metadata and saved outputs, so the visible diff can be much larger than the actual code change.

---

### 3. Why are code changes usually easier to identify in a marimo notebook than in a `.ipynb` notebook?

- A. marimo notebooks do not allow outputs or markdown
- B. marimo notebooks are Python files and do not save outputs in the notebook file
- C. marimo notebooks automatically remove all metadata from Git
- D. marimo notebooks always change only one cell at a time

**Answer:** B. marimo notebooks are Python files and do not save outputs in the notebook file

**Explanation:** When outputs are not stored inside the notebook file, diffs stay closer to the actual code change instead of mixing code with notebook state and rendered results.
