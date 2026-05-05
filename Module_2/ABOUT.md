# Module 2: Reproducibility as a Baseline for Trustworthy AI

Two reproducibility problems in real notebook work, environment drift and noisy git diffs, and how marimo addresses both.

## Files

| File | What it is |
|------|------------|
| `2_1_environment_drift.ipynb` | A Jupyter notebook that breaks when the environment changes. |
| `2_2_sandboxed_environment.py` | The same kind of work in marimo, with dependencies pinned in the file's own `# /// script` header. |
| `2_3_jupyter_diff_demo.ipynb` | Change one line, see how much `git diff` reports. Jupyter stores rendered outputs as JSON, so the diff bloats. |
| `2_3_marimo_diff_demo.py` | Same one-line change in a marimo notebook. The diff is just the line you changed. |

## Quick Reference

| Goal | Command |
|------|---------|
| Open the drift notebook | `jupyter notebook 2_1_environment_drift.ipynb` |
| Open the marimo sandbox notebook | `marimo edit --sandbox 2_2_sandboxed_environment.py` |
| Open the Jupyter diff demo | `jupyter notebook 2_3_jupyter_diff_demo.ipynb` |
| Open the marimo diff demo | `marimo edit 2_3_marimo_diff_demo.py` |
| See the Jupyter diff balloon | `git diff Module_2/2_3_jupyter_diff_demo.ipynb` |
| See the small marimo diff | `git diff Module_2/2_3_marimo_diff_demo.py` |
| Run any marimo notebook in molab | [molab.marimo.io](https://molab.marimo.io). Preview from GitHub or fork into your workspace |
