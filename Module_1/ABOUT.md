# Module 1: Why Interactive Programming Environments Matter for AI and ML

Traditional Jupyter notebooks vs marimo's reactive execution. 

## Files

| File | What it is |
|------|------------|
| `1_1_jupyter_baseline.ipynb` | A standard Jupyter notebook, intentionally vulnerable to hidden state and out-of-order execution. The "before." |
| `1_2_marimo_reactive_workflow.py` | The same workflow as a marimo notebook showing its reactive capabilities. 
| `1_3_marimo_ui_elements.py` | A tour of marimo's built-in UI components (sliders, dropdowns, tables, forms, tabs). |

## Quick Reference

| Goal | Command |
|------|---------|
| Open the Jupyter baseline | `jupyter lab 1_1_jupyter_baseline.ipynb` |
| Edit the marimo notebook | `marimo edit 1_2_marimo_reactive_workflow.py` |
| Tour the UI elements | `marimo edit 1_3_marimo_ui_elements.py` |
| First-time tour of marimo | `marimo tutorial intro` |
| Convert any `.ipynb` to marimo | `marimo convert notebook.ipynb -o notebook.py` |
