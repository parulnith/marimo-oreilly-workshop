# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "openai", "pandas", "altair"]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Module 5: From Interactive Work to Reusable Systems

    ## What this notebook does

    This is a small **LLM evaluation harness** built around a single task:
    classify the sentiment of a **product review** as `positive`, `negative`, or
    `neutral`, with a confidence score and a one-sentence reason.

    It runs the same set of reviews through **two local Ollama models** (default:
    `gemma3:1b` vs. `qwen2.5:0.5b`) so you can compare their behaviour
    side by side, not just whether they agree on the label, but how confident
    each one is and how it justifies the call.


    ## How the eval works

    For every review, each model returns structured JSON: a label, a confidence
    in [0, 1], and a short reason. You then mark each prediction ✓ or ✗ in the
    UI. The notebook aggregates those judgements into a live accuracy dashboard
    so the eval is **human-in-the-loop**, not an automated metric. 

    ## Same file, four modes

    The same `.py` file runs as an interactive notebook, a clean web app, a
    headless CLI script, and an importable Python module — that's the Module 5
    point.

    | Mode | Command |
    |------|---------|
    | Interactive notebook | `marimo edit sentiment_classifier.py` |
    | Clean web app | `marimo run sentiment_classifier.py` |
    | Headless script | `uv run sentiment_classifier.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b --output results.csv` |
    | Importable module | `from sentiment_classifier import get_client, compare_two_models` |
    """)
    return (mo,)


with app.setup:
    import argparse
    import json
    import os

    import altair as alt
    import marimo as mo
    import pandas as pd
    from openai import OpenAI

    SYSTEM_PROMPT = (
        "You are a sentiment classifier. "
        "Classify the sentiment of the product review given by the user. "
        'Respond ONLY with valid JSON: {"label": "<positive|negative|neutral>", '
        '"confidence": <0.0-1.0>, "reason": "<one sentence>"}'
    )


@app.function
def get_client(base_url="http://localhost:11434/v1", api_key="ollama"):
    return OpenAI(base_url=base_url, api_key=api_key or os.getenv("OPENAI_API_KEY", "ollama"))


@app.function
def compare_two_models(client, texts, model_a, model_b):
    """Send each review to both models and return one combined DataFrame."""
    rows = []
    for text in texts:
        for model in (model_a, model_b):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": text},
                    ],
                    temperature=0.0,
                )
                raw = (response.choices[0].message.content or "").strip()
                raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                parsed = json.loads(raw)
                rows.append({
                    "text": text,
                    "model": model,
                    "label": parsed.get("label", "neutral"),
                    "confidence": round(float(parsed.get("confidence", 0.5)), 3),
                    "reason": parsed.get("reason", ""),
                })
            except Exception as exc:
                rows.append({
                    "text": text, "model": model,
                    "label": "error", "confidence": 0.0, "reason": str(exc),
                })
    return pd.DataFrame(rows)


@app.function
def sample_reviews():
    return [
        "Oh wonderful, another charger that lasts a whole three weeks. Just what I needed.",
        "The product itself is fantastic — the courier on the other hand left it in the rain.",
        "Not bad. Not great. I keep using it, which probably says something.",
        "I wanted to hate this but I can't. Annoyingly good.",
        "Five stars for the packaging. The thing inside? Different story.",
        "Does exactly what the listing says. That is neither a compliment nor a complaint.",
        "Returned it. Then bought it again. Make of that what you will.",
        "If you enjoy reading 40-page manuals to brew coffee, this is the product for you.",
        "Customer service was great. Shame I had to call them four times.",
        "Honestly underwhelming for the price, but I can see why some people love it.",
        "Build quality is solid, instructions are a war crime.",
        "It works. My cat is unimpressed. I am cautiously optimistic.",
    ]


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## CLI arguments

    The cell below defines the command-line flags this notebook accepts
    (`--model-a`, `--model-b`, `--base-url`, `--output`). It uses Python's
    standard `argparse`.
    """)
    return


@app.cell
def _(argparse):
    parser = argparse.ArgumentParser(
        description="Compare two Ollama models on a set of reviews.",
    )
    parser.add_argument("--model-a", default="gemma3:1b")
    parser.add_argument("--model-b", default="qwen2.5:0.5b")
    parser.add_argument("--base-url", default="http://localhost:11434/v1")
    parser.add_argument("--output", default=None, help="Optional CSV path for results")
    args, _ = parser.parse_known_args()
    return (args,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## LLM Comparison

    Run the same reviews through **two Ollama models** side by side.
    Mark each classification correct ✓ or incorrect ✗ to build a live accuracy dashboard.

    Make sure Ollama is running first: `ollama serve`
    """)
    return


@app.cell
def _(args, mo):
    base_url_input = mo.ui.text(
        value=args.base_url,
        label="Ollama base URL",
        full_width=True,
    )
    model_a_input = mo.ui.text(
        value=args.model_a,
        label="Model A",
        placeholder="e.g. gemma3:1b",
    )
    model_b_input = mo.ui.text(
        value=args.model_b,
        label="Model B",
        placeholder="e.g. qwen2.5:0.5b",
    )
    reviews_input = mo.ui.text_area(
        value="\n".join(sample_reviews()),
        label="Reviews to classify (one per line — edit, add or replace)",
        full_width=True,
        rows=10,
    )
    run_btn = mo.ui.run_button(label="Classify with both models", kind="success")
    mo.vstack([
        base_url_input,
        mo.hstack([model_a_input, model_b_input], justify="start"),
        reviews_input,
        run_btn,
    ])
    return base_url_input, model_a_input, model_b_input, reviews_input, run_btn


@app.cell
def _(
    args,
    base_url_input,
    compare_two_models,
    get_client,
    mo,
    model_a_input,
    model_b_input,
    reviews_input,
    run_btn,
):
    mo.stop(
        not run_btn.value,
        mo.md("_Click **Classify with both models** to start._"),
    )
    _texts = [r.strip() for r in reviews_input.value.splitlines() if r.strip()]
    mo.stop(not _texts, mo.md("_No reviews to classify._"))

    _client = get_client(base_url=base_url_input.value)
    results_df = compare_two_models(
        _client,
        _texts,
        model_a_input.value.strip(),
        model_b_input.value.strip(),
    )
    results_df
    return (results_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Mark each classification correct or incorrect
    """)
    return


@app.cell(hide_code=True)
def _(mo, model_a_input, model_b_input, results_df):
    _model_a = model_a_input.value.strip()
    _model_b = model_b_input.value.strip()
    _df_a = results_df[results_df["model"] == _model_a].reset_index(drop=True)
    _df_b = results_df[results_df["model"] == _model_b].reset_index(drop=True)
    _n = len(_df_a)
    _label_color = {"positive": "🟢", "negative": "🔴", "neutral": "🟡", "error": "⚠️"}

    verdicts_a = mo.ui.array(
        [mo.ui.checkbox(label="correct") for _ in range(_n)],
        label=f"{_model_a} verdicts",
    )
    verdicts_b = mo.ui.array(
        [mo.ui.checkbox(label="correct") for _ in range(_n)],
        label=f"{_model_b} verdicts",
    )

    _header = mo.hstack([
        mo.md("**Review**"),
        mo.md(f"**{_model_a}**"),
        mo.md(f"**{_model_b}**"),
    ], justify="start", widths=[4, 2, 2])

    _rows = [_header]
    for _i in range(_n):
        _a = _df_a.iloc[_i]
        _b = _df_b.iloc[_i]
        _rows.append(mo.hstack([
            mo.md(f"*{_a['text'][:80]}{'…' if len(_a['text']) > 80 else ''}*"),
            mo.vstack([
                mo.md(f"{_label_color.get(_a['label'], '')} **{_a['label']}** ({_a['confidence']:.0%})"),
                verdicts_a.elements[_i],
            ]),
            mo.vstack([
                mo.md(f"{_label_color.get(_b['label'], '')} **{_b['label']}** ({_b['confidence']:.0%})"),
                verdicts_b.elements[_i],
            ]),
        ], justify="start", widths=[4, 2, 2]))

    mo.vstack(_rows)
    return verdicts_a, verdicts_b


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Accuracy Dashboard
    """)
    return


@app.cell(hide_code=True)
def _(mo, model_a_input, model_b_input, verdicts_a, verdicts_b):
    _model_a = model_a_input.value.strip()
    _model_b = model_b_input.value.strip()
    _n = len(verdicts_a.value)
    _correct_a = sum(verdicts_a.value)
    _correct_b = sum(verdicts_b.value)
    _acc_a = _correct_a / _n if _n else 0
    _acc_b = _correct_b / _n if _n else 0
    _winner = _model_a if _acc_a > _acc_b else (_model_b if _acc_b > _acc_a else "Tie")

    mo.hstack([
        mo.stat(value=f"{_acc_a:.0%}", label=f"{_model_a} accuracy", caption=f"{_correct_a}/{_n} correct"),
        mo.stat(value=f"{_acc_b:.0%}", label=f"{_model_b} accuracy", caption=f"{_correct_b}/{_n} correct"),
        mo.stat(value=_winner, label="Better model"),
    ])
    return


@app.cell(hide_code=True)
def _(alt, mo, model_a_input, model_b_input, pd, verdicts_a, verdicts_b):
    _model_a = model_a_input.value.strip()
    _model_b = model_b_input.value.strip()
    _n = len(verdicts_a.value)
    _summary_df = pd.DataFrame({
        "Model": [_model_a, _model_b],
        "Correct": [sum(verdicts_a.value), sum(verdicts_b.value)],
        "Incorrect": [_n - sum(verdicts_a.value), _n - sum(verdicts_b.value)],
        "Accuracy": [
            sum(verdicts_a.value) / _n if _n else 0,
            sum(verdicts_b.value) / _n if _n else 0,
        ],
    })
    _melted = _summary_df.melt(id_vars="Model", value_vars=["Correct", "Incorrect"], var_name="Verdict", value_name="Count")
    _chart = (
        alt.Chart(_melted).mark_bar()
        .encode(
            x=alt.X("Model:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Count:Q", title="Reviews"),
            color=alt.Color("Verdict:N", scale=alt.Scale(domain=["Correct", "Incorrect"], range=["#55A868", "#C44E52"])),
            tooltip=["Model:N", "Verdict:N", "Count:Q"],
        )
        .properties(title="Correct vs Incorrect by Model", width=300, height=240)
    )
    _acc_chart = (
        alt.Chart(_summary_df).mark_bar()
        .encode(
            x=alt.X("Model:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Accuracy:Q", title="Accuracy", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format=".0%")),
            color=alt.Color("Model:N", legend=None),
            tooltip=["Model:N", alt.Tooltip("Accuracy:Q", format=".0%")],
        )
        .properties(title="Accuracy by Model", width=300, height=240)
    )
    mo.hstack([_chart, _acc_chart])
    return


@app.cell
def _():
    return


def _run_headless(argv):
    """Headless CLI entry point: parse args, run both models, write CSV."""
    import argparse as _argparse
    import json as _json
    import os as _os

    import pandas as _pd
    from openai import OpenAI as _OpenAI

    _SYSTEM_PROMPT = (
        "You are a sentiment classifier. "
        "Classify the sentiment of the product review given by the user. "
        'Respond ONLY with valid JSON: {"label": "<positive|negative|neutral>", '
        '"confidence": <0.0-1.0>, "reason": "<one sentence>"}'
    )

    parser = _argparse.ArgumentParser(description="Compare two Ollama models on a set of reviews.")
    parser.add_argument("--model-a", default="gemma3:1b")
    parser.add_argument("--model-b", default="qwen2.5:0.5b")
    parser.add_argument("--base-url", default="http://localhost:11434/v1")
    parser.add_argument("--output", required=True, help="CSV path for results")
    cli = parser.parse_args(argv)

    client = _OpenAI(base_url=cli.base_url, api_key=_os.getenv("OPENAI_API_KEY", "ollama"))
    texts = sample_reviews()
    rows = []
    for text in texts:
        for model in (cli.model_a, cli.model_b):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": _SYSTEM_PROMPT},
                        {"role": "user", "content": text},
                    ],
                    temperature=0.0,
                )
                raw = (response.choices[0].message.content or "").strip()
                raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                parsed = _json.loads(raw)
                rows.append({
                    "text": text, "model": model,
                    "label": parsed.get("label", "neutral"),
                    "confidence": round(float(parsed.get("confidence", 0.5)), 3),
                    "reason": parsed.get("reason", ""),
                })
            except Exception as exc:
                rows.append({"text": text, "model": model, "label": "error", "confidence": 0.0, "reason": str(exc)})

    df = _pd.DataFrame(rows)
    df.to_csv(cli.output, index=False)
    print(f"Wrote {len(df)} rows to {cli.output}")


if __name__ == "__main__":
    import sys
    if "--" in sys.argv:
        sep = sys.argv.index("--")
        _run_headless(sys.argv[sep + 1:])
    else:
        app.run()
