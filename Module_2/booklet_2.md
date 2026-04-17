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

Jupyter notebooks are stored as JSON. Even a small code change can produce a large diff because execution counts, output blobs, and metadata are stored alongside the code.

That makes review harder. It becomes difficult to see what actually changed and what is just notebook noise.

A marimo notebook is a plain `.py` file. If one cell changes, the diff shows that code change directly. That makes pull requests easier to review, merge conflicts easier to resolve, and version history easier to understand.

> 💡 **Try it — `Module_2/2.2.py`**
>
> Run the notebook. It shows a live one-line diff for a small code change, then the equivalent Jupyter diff for the same change.

#### Reviewability supports reproducibility

When experimental work is easy to review, reproducibility gets stronger. Clear diffs make it easier to answer basic but important questions:

- What code changed?
- Did the data processing logic shift?
- Was a parameter updated?
- Did the result change because of the code, or because of the environment?

Plain-text notebooks help because the important changes are visible. That makes collaboration more reliable and reduces the chance that a meaningful experimental change is hidden inside formatting noise.

This matters for trustworthy AI because reproducibility is not only technical. It is also social. Other people need to inspect what changed, understand why it changed, and verify that the result still deserves confidence.

> **On outputs:** marimo does not store outputs in the notebook file, which keeps diffs cleaner and makes code review easier.

**Script cue:**  
Reproducibility is easier to maintain when changes are easy to inspect. Reviewable experiments make trustworthy workflows more realistic for teams, not just individuals.

---

### Closing

Reproducibility is the baseline that makes trustworthy AI possible. It is not only about whether code runs again, but whether results remain stable across environments, collaborators, and time.

In this module, the key takeaway is that trustworthy AI depends on more than models and metrics. It also depends on controlled environments, reviewable changes, and workflows that remain stable over time.

**Script cue:**  
If a result cannot be reproduced clearly and consistently, it should not be treated as fully trustworthy.
