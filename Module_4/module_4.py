# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair==6.0.0",
#     "marimo",
#     "matplotlib==3.10.8",
#     "mcp==1.26.0",
#     "numpy==2.4.4",
#     "pandas==2.3.3",
#     "plotly==6.6.0",
#     "scikit-learn==1.8.0",
#     "seaborn==0.13.2",
#     "tabicl",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Interactive ML Workflow

    Interactive computation as a unified system means that data, models,
    visualizations, and user input are all part of the same live graph. In
    marimo, widgets are variables, tables can become inputs, model outputs can
    feed new analysis, and visual changes propagate automatically through the
    notebook.

    This notebook presents that idea as one end-to-end workflow: start with the
    data, move into visual exploration, then fit models and use their outputs to
    guide the next step of analysis.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np

    import matplotlib.pyplot as plt
    from sklearn.datasets import fetch_openml


    return fetch_openml, mo


@app.cell
def _(fetch_openml):
    data = fetch_openml("adult", version=2, as_frame=True)
    df = data.frame.copy()
    df["income"] = (df["class"].str.strip() == ">50K").astype(int)
    df = df.drop(columns=["class"]).dropna()
    feature_options = [col for col in df.columns if col != "income"]
    return df, feature_options


@app.cell(hide_code=True)
def _(df):
    df
    return


@app.cell
def _(feature_options, mo):
    column_selector = mo.ui.multiselect(
        options=feature_options,
        value=feature_options,
        label="Select Columns"
    )
    column_selector
    return (column_selector,)


@app.cell
def _(column_selector):

    column_selector.value
    return


@app.cell
def _():


    return


if __name__ == "__main__":
    app.run()
