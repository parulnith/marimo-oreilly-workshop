# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import difflib
    from pathlib import Path

    import marimo as mo

    return Path, difflib, mo


@app.cell
def _(Path):
    notebook_path = Path(__file__)
    source = notebook_path.read_text()
    return notebook_path, source


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Section 2.3 — Version Control and Reviewable Experiments

        This notebook shows the file-format argument from inside the notebook.

        Instead of asking you to imagine what a clean diff looks like, the notebook reads its own `.py` source and computes the one-line diff directly.
        """
    )
    return


@app.cell
def _(source):
    source_lines = source.splitlines()
    x_line_index = next(
        i for i, line in enumerate(source_lines) if line.strip() == "x = 10"
    )
    start = max(0, x_line_index - 2)
    end = min(len(source_lines), x_line_index + 4)
    source_excerpt = "\n".join(source_lines[start:end])
    return source_excerpt, x_line_index


@app.cell(hide_code=True)
def _(mo, notebook_path, source_excerpt):
    left = mo.md(
        f"""
        ## Step 1: This notebook is just a Python file

        File: `{notebook_path.name}`

        ```python
        {source_excerpt}
        ```
        """
    )
    right = mo.md(
        """
        ## Why this matters

        A reviewer can open this file in any editor and read it as ordinary source code.

        There is no JSON wrapper, no output blob, and no notebook-specific diff format needed to understand the change.
        """
    )
    return mo.hstack([left, right], widths="equal")


@app.cell
def _(difflib, source, x_line_index):
    updated_lines = source.splitlines()
    updated_lines[x_line_index] = updated_lines[x_line_index].replace("x = 10", "x = 20", 1)
    updated_source = "\n".join(updated_lines)
    diff_lines = difflib.unified_diff(
        source.splitlines(),
        updated_source.splitlines(),
        fromfile="2.3.py",
        tofile="2.3.py",
        lineterm="",
        n=1,
    )
    diff_text = "\n".join(diff_lines)
    return diff_text, updated_source


@app.cell(hide_code=True)
def _(diff_text, mo):
    mo.md(
        f"""
        ## Step 2: The notebook computes its own one-line diff

        ```diff
        {diff_text}
        ```

        This is the exact advantage of a plain `.py` notebook:
        a tiny code change stays a tiny diff.
        """
    )
    return


@app.cell
def _():
    x = 10
    print(x)
    return (x,)


@app.cell(hide_code=True)
def _(mo, x):
    jupyter_diff = """-   "execution_count": 1,
+   "execution_count": 2,
-      "text": ["10\\n"],
+      "text": ["20\\n"],
-   "source": ["x = 10\\n"]
+   "source": ["x = 20\\n"]"""
    marimo_diff = """-    x = 10
+    x = 20"""

    return mo.vstack(
        [
            mo.md(
                f"""
                ## Step 3: Compare the formats

                Current value in this notebook: **{x}**

                **Typical Jupyter diff**

                ```diff
                {jupyter_diff}
                ```
                """
            ),
            mo.md(
                f"""
                **Equivalent marimo diff**

                ```diff
                {marimo_diff}
                ```
                """
            ),
        ]
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Step 4: The same file also runs as a script

        Because this notebook is ordinary Python, the same file can run with:

        ```bash
        python 2.3.py
        ```

        So the notebook is simultaneously:

        - an interactive notebook
        - a reviewable source file
        - an executable Python script
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    return mo.callout(
        mo.md(
            """
            The key point of Section 2.3:

            **plain Python makes notebook changes reviewable, mergeable, and runnable anywhere Python runs.**
            """
        ),
        kind="success",
    )


if __name__ == "__main__":
    app.run()
