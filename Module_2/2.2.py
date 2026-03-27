# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.0",
#     "pandas==2.2.3",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import re
    import sys
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return Path, mo, pd, plt, re, sys


@app.cell
def _(Path, re, sys):
    notebook_path = Path(__file__)
    source = notebook_path.read_text()
    metadata_match = re.search(r"(?s)^# /// script\n(.*?)# ///", source)
    metadata_body = metadata_match.group(1) if metadata_match else ""
    metadata_block = "# /// script\n" + metadata_body + "# ///" if metadata_match else ""

    requires_match = re.search(r'requires-python = "([^"]+)"', metadata_body)
    dependency_matches = re.findall(r'"([^"]+)"', metadata_body)

    requires_python = requires_match.group(1) if requires_match else "unknown"
    dependencies = [dep for dep in dependency_matches if dep != requires_python]
    runtime_python = sys.version.split()[0]
    return dependencies, metadata_block, notebook_path, requires_python, runtime_python


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Section 2.2 — The Hidden Culprits: Dependencies and Environments

        This notebook shows the environment story **from inside the notebook itself**.

        marimo tracks dependencies inside the file when you run with `--sandbox`, and that metadata is readable as ordinary Python text.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, notebook_path, pd, plt, requires_python, runtime_python):
    mo.md(
        f"""
        ## Step 1: Inspect the current runtime

        - notebook file: `{notebook_path.name}`
        - running Python: **{runtime_python}**
        - file requires Python: **{requires_python}**
        - pandas loaded right now: **{pd.__version__}**
        - matplotlib loaded right now: **{plt.matplotlib.__version__}**
        """
    )
    return


@app.cell(hide_code=True)
def _(metadata_block, mo):
    return mo.vstack(
        [
            mo.md(
                "## Step 2: Read the inline metadata directly from this file\n\n"
                "This block is not pasted into the slide deck. The notebook is reading its own source code."
            ),
            mo.md(f"```python\n{metadata_block}\n```"),
        ]
    )


@app.cell
def _(dependencies, pd, plt):
    loaded_versions = {
        "pandas": pd.__version__,
        "matplotlib": plt.matplotlib.__version__,
    }

    rows = []
    for dependency in dependencies:
        if "==" in dependency:
            package, pinned_version = dependency.split("==", maxsplit=1)
        else:
            package, pinned_version = dependency, "unversioned"

        loaded_version = loaded_versions.get(package, "n/a in this cell")
        rows.append(
            {
                "dependency": dependency,
                "loaded_version": loaded_version,
                "matches_runtime": pinned_version in {"unversioned", loaded_version},
            }
        )

    rows
    return (rows,)


@app.cell(hide_code=True)
def _(mo, rows):
    lines = "\n".join(
        f"- `{row['dependency']}` -> loaded `{row['loaded_version']}` | match: **{row['matches_runtime']}**"
        for row in rows
    )
    mo.md(
        f"""
        ## Step 3: Compare the metadata to the active runtime

        {lines}

        In other words, the notebook can verify from inside the session that its runtime matches the versions pinned in the file.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Step 4: What changes in sandbox mode

        If you open this notebook with:

        ```bash
        marimo edit --sandbox Module_2/2.2.py
        ```

        then marimo manages the environment from the metadata block above.

        Add a new import like `import scipy`, run the cell, approve the install, and marimo updates the `# /// script` block automatically.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    return mo.callout(
        mo.md(
            """
            The key point of Section 2.2:

            **the notebook and its environment spec live in the same file.**
            """
        ),
        kind="success",
    )


if __name__ == "__main__":
    app.run()
