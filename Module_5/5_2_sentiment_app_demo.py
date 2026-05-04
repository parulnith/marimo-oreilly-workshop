import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Sentiment Analysis Dashboard
    Set up dependencies and imports for the interactive sentiment analysis app.
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Try it: Interactive Sentiment App

    This is the **same app** you just ran with `marimo run`. Interact with it:
    filter results, sort the table, pick a label — all reactive, no page reloads.
    """)
    return


@app.cell(hide_code=True)
def _():
    import polars as pl
    import altair as alt

    # Mock pre-classified results (no Ollama needed — works in browser)
    _data = [
        {"text": "Absolutely love this product! Fast shipping and works perfectly.",    "label": "positive", "confidence": 0.97, "model": "gemma3:1b"},
        {"text": "Terrible experience. Broke after two days and support was unhelpful.", "label": "negative", "confidence": 0.95, "model": "gemma3:1b"},
        {"text": "It's okay. Does what it says but nothing special.",                    "label": "neutral",  "confidence": 0.82, "model": "gemma3:1b"},
        {"text": "Exceeded my expectations. Highly recommend to anyone.",               "label": "positive", "confidence": 0.93, "model": "gemma3:1b"},
        {"text": "Packaging was damaged, product inside seemed fine but I'm not happy.", "label": "negative", "confidence": 0.79, "model": "gemma3:1b"},
        {"text": "Great value for money. Using it daily for three months.",              "label": "positive", "confidence": 0.91, "model": "gemma3:1b"},
        {"text": "Instructions were confusing and setup took way too long.",             "label": "negative", "confidence": 0.88, "model": "gemma3:1b"},
        {"text": "Customer service responded quickly and resolved my issue same day.",   "label": "positive", "confidence": 0.90, "model": "gemma3:1b"},
        {"text": "Average product. Works but feels a bit cheap.",                       "label": "neutral",  "confidence": 0.76, "model": "gemma3:1b"},
        {"text": "Would not buy again. Stopped working after a week.",                  "label": "negative", "confidence": 0.94, "model": "gemma3:1b"},
        {"text": "Absolutely love this product! Fast shipping and works perfectly.",    "label": "positive", "confidence": 0.92, "model": "qwen2.5:0.5b"},
        {"text": "Terrible experience. Broke after two days and support was unhelpful.", "label": "negative", "confidence": 0.89, "model": "qwen2.5:0.5b"},
        {"text": "It's okay. Does what it says but nothing special.",                    "label": "neutral",  "confidence": 0.71, "model": "qwen2.5:0.5b"},
        {"text": "Exceeded my expectations. Highly recommend to anyone.",               "label": "positive", "confidence": 0.88, "model": "qwen2.5:0.5b"},
        {"text": "Packaging was damaged, product inside seemed fine but I'm not happy.", "label": "neutral",  "confidence": 0.65, "model": "qwen2.5:0.5b"},
        {"text": "Great value for money. Using it daily for three months.",              "label": "positive", "confidence": 0.87, "model": "qwen2.5:0.5b"},
        {"text": "Instructions were confusing and setup took way too long.",             "label": "negative", "confidence": 0.84, "model": "qwen2.5:0.5b"},
        {"text": "Customer service responded quickly and resolved my issue same day.",   "label": "positive", "confidence": 0.85, "model": "qwen2.5:0.5b"},
        {"text": "Average product. Works but feels a bit cheap.",                       "label": "neutral",  "confidence": 0.70, "model": "qwen2.5:0.5b"},
        {"text": "Would not buy again. Stopped working after a week.",                  "label": "negative", "confidence": 0.91, "model": "qwen2.5:0.5b"},
    ]

    results_df = pl.DataFrame(_data)
    return alt, pl, results_df


@app.cell
def _(mo, results_df):
    label_filter = mo.ui.dropdown(
        options=["All", "positive", "neutral", "negative"],
        value="All",
        label="Filter by label",
    )
    model_filter = mo.ui.dropdown(
        options=["All"] + results_df["model"].unique().to_list(),
        value="All",
        label="Filter by model",
    )
    mo.hstack([label_filter, model_filter], justify="start")
    return label_filter, model_filter


@app.cell(hide_code=True)
def _(alt, label_filter, mo, model_filter, pl, results_df):
    import math

    _filtered = results_df
    if label_filter.value != "All":
        _filtered = _filtered.filter(pl.col("label") == label_filter.value)
    if model_filter.value != "All":
        _filtered = _filtered.filter(pl.col("model") == model_filter.value)

    _color_map = {"positive": "#22c55e", "neutral": "#f59e0b", "negative": "#ef4444"}

    _total = len(_filtered)
    _avg_conf = _filtered["confidence"].mean() if _total else 0.0

    _label_counts = _filtered.group_by("label").len()
    _positive = int(_label_counts.filter(pl.col("label") == "positive")["len"].sum()) if "positive" in _filtered["label"].to_list() else 0
    _negative = int(_label_counts.filter(pl.col("label") == "negative")["len"].sum()) if "negative" in _filtered["label"].to_list() else 0
    _neutral  = int(_label_counts.filter(pl.col("label") == "neutral")["len"].sum())  if "neutral"  in _filtered["label"].to_list() else 0

    _stats = mo.hstack([
        mo.stat(value=str(_total),      label="Reviews shown"),
        mo.stat(value=f"{_avg_conf:.0%}", label="Avg confidence"),
        mo.stat(value=str(_positive),   label="Positive"),
        mo.stat(value=str(_negative),   label="Negative"),
        mo.stat(value=str(_neutral),    label="Neutral"),
    ])

    _chart = (
        alt.Chart(_filtered)
        .mark_bar()
        .encode(
            x=alt.X("model:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("count():Q", title="Reviews"),
            color=alt.Color(
                "label:N",
                scale=alt.Scale(
                    domain=["positive", "neutral", "negative"],
                    range=["#22c55e", "#f59e0b", "#ef4444"],
                ),
            ),
            tooltip=["model:N", "label:N", "count():Q"],
        )
        .properties(title="Label distribution by model", width=300, height=220)
    )

    mo.vstack([
        _stats,
        mo.hstack([
            mo.ui.table(_filtered.select(["model", "text", "label", "confidence"])),
            _chart,
        ], align="start"),
    ])
    return


if __name__ == "__main__":
    app.run()
