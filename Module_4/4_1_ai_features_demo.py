# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.8",
#     "mcp>=1",
#     "nbformat==5.10.4",
#     "pandas==2.3.3",
#     "pydantic>=2",
#     "ruff==0.15.12",
# ]
# ///

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop/blob/main/Module_4/4_1_ai_features_demo.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # AI features in marimo
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt

    return mo, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Setup checkpoint

    Before using the AI features, configure an LLM provider in marimo settings:

    1. Open notebook settings.
    2. If marimo prompts you to install AI packages, accept the prompt.
    3. Open the **AI** tab.
    4. Choose a hosted provider or a local Ollama model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Five editor entry points

    - **Generate new cells** with the **Generate with AI** button
    - **Inline autocompletion**, similar to Copilot-style tools
    - **Refactor the current cell** with `Ctrl/Cmd-Shift-E`
    - **Use the Chat panel** for notebook-level questions and generated cells
    - **Generate entire notebooks** from the command line with `marimo new`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Demo data

    The examples below use a small dataframe named `df`.
    """)
    return


@app.cell
def _(pd):
    df = pd.DataFrame(
        [
            {
                "region": "North",
                "segment": "Enterprise",
                "channel": "Direct",
                "revenue": 82000,
                "cost": 42000,
                "satisfaction": 8.7,
                "converted": True,
            },
            {
                "region": "North",
                "segment": "SMB",
                "channel": "Partner",
                "revenue": 38000,
                "cost": 21000,
                "satisfaction": 7.8,
                "converted": True,
            },
            {
                "region": "South",
                "segment": "Enterprise",
                "channel": "Direct",
                "revenue": 76000,
                "cost": 39000,
                "satisfaction": 8.1,
                "converted": True,
            },
            {
                "region": "South",
                "segment": "SMB",
                "channel": "Online",
                "revenue": 29000,
                "cost": 18000,
                "satisfaction": 6.9,
                "converted": False,
            },
            {
                "region": "East",
                "segment": "Midmarket",
                "channel": "Partner",
                "revenue": 54000,
                "cost": 31000,
                "satisfaction": 7.4,
                "converted": True,
            },
            {
                "region": "East",
                "segment": "SMB",
                "channel": "Online",
                "revenue": 24000,
                "cost": 15000,
                "satisfaction": 6.5,
                "converted": False,
            },
            {
                "region": "West",
                "segment": "Enterprise",
                "channel": "Direct",
                "revenue": 91000,
                "cost": 47000,
                "satisfaction": 9.0,
                "converted": True,
            },
            {
                "region": "West",
                "segment": "Midmarket",
                "channel": "Partner",
                "revenue": 61000,
                "cost": 33000,
                "satisfaction": 8.0,
                "converted": True,
            },
            {
                "region": "Central",
                "segment": "SMB",
                "channel": "Online",
                "revenue": 31000,
                "cost": 19000,
                "satisfaction": 7.1,
                "converted": False,
            },
            {
                "region": "Central",
                "segment": "Midmarket",
                "channel": "Direct",
                "revenue": 59000,
                "cost": 32000,
                "satisfaction": 7.9,
                "converted": True,
            },
        ]
    )
    df["profit"] = df["revenue"] - df["cost"]
    df["margin"] = df["profit"] / df["revenue"]
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1. Generate with AI

    Use the **Generate with AI** button near the bottom of the notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2. Inline autocompletion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. Refactor the current cell

    Use AI refactor on the next repetitive code cell.
    """)
    return


@app.cell
def _(df, pd):
    north_revenue = df.loc[df["region"] == "North", "revenue"].mean()
    south_revenue = df.loc[df["region"] == "South", "revenue"].mean()
    east_revenue = df.loc[df["region"] == "East", "revenue"].mean()
    west_revenue = df.loc[df["region"] == "West", "revenue"].mean()
    central_revenue = df.loc[df["region"] == "Central", "revenue"].mean()

    region_revenue_summary = pd.DataFrame(
        {
            "region": ["North", "South", "East", "West", "Central"],
            "average_revenue": [
                north_revenue,
                south_revenue,
                east_revenue,
                west_revenue,
                central_revenue,
            ],
        }
    )
    region_revenue_summary
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 4. Chat panel with variable context

    The next controls are intentionally named `metric_selector` and
    `segment_selector`. Use them with `@` references in the Chat panel.
    """)
    return


@app.cell
def _(df, mo):
    metric_selector = mo.ui.dropdown(
        options=["revenue", "cost", "profit", "margin", "satisfaction"],
        value="revenue",
        label="Metric",
    )
    segment_selector = mo.ui.multiselect(
        options=sorted(df["segment"].unique()),
        value=sorted(df["segment"].unique()),
        label="Segments",
    )
    mo.vstack([metric_selector, segment_selector])
    return metric_selector, segment_selector


@app.cell
def _(df, metric_selector, segment_selector):
    selected_segments = segment_selector.value
    selected_metric = metric_selector.value
    filtered_df = df[df["segment"].isin(selected_segments)].copy()
    metric_summary = (
        filtered_df.groupby("segment", as_index=False)[selected_metric]
        .mean()
        .sort_values(selected_metric, ascending=False)
    )
    metric_summary
    return metric_summary, selected_metric


@app.cell
def _(metric_summary, plt, selected_metric):
    fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)
    ax.bar(metric_summary["segment"], metric_summary[selected_metric], color="#4C72B0")
    ax.set_title(f"Average {selected_metric} by segment")
    ax.set_xlabel("Segment")
    ax.set_ylabel(selected_metric)
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 5. Generate an entire notebook

    This step happens in the terminal with `marimo new`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 6. Local models and agent workflows

    Use this part of the workshop to compare hosted models, local models, and
    external coding agents.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 7. Check the notebook

    After AI edits, run `marimo check` from the terminal.
    """)
    return


if __name__ == "__main__":
    app.run()
