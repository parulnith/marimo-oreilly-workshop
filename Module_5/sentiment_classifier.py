# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "openai", "pandas", "altair"]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import pandas as pd
    import altair as alt
    import json
    import os
    from openai import OpenAI

    SYSTEM_PROMPT = (
        "You are a sentiment classifier. "
        "Classify the sentiment of the product review given by the user. "
        'Respond ONLY with valid JSON: {"label": "<positive|negative|neutral>", "confidence": <0.0-1.0>, "reason": "<one sentence>"}'
    )


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Module 5: From Interactive Work to Reusable Systems

    Everything you have built across this workshop lives in a single `.py` file.

    This module closes that gap. The working example is an **LLM sentiment
    classifier** — a notebook that sends product reviews to a local Ollama model
    and returns labels with confidence scores.

    By the end, the same file will run in four modes

    | Mode | Command |
    |------|---------|
    | Interactive notebook | `marimo edit module_5.py` |
    | Clean web app | `marimo run module_5.py` |
    | Headless script | `python module_5.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b` |
    | Importable module | `from module_5 import get_client, classify_batch` |
    """)
    return


@app.function
def get_client(base_url="http://localhost:11434/v1", api_key="ollama"):
    return OpenAI(base_url=base_url, api_key=api_key or os.getenv("OPENAI_API_KEY", "ollama"))


@app.function
def classify_text(client, text, model="gemma3:1b"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0.0,
        )
        raw = (response.choices[0].message.content or "").strip().strip("```json").strip("```").strip()
        parsed = json.loads(raw)
        return {
            "text": text,
            "label": parsed.get("label", "neutral"),
            "confidence": round(float(parsed.get("confidence", 0.5)), 3),
            "reason": parsed.get("reason", ""),
            "model": model,
            "error": None,
        }
    except Exception as exc:
        return {"text": text, "label": "error", "confidence": 0.0, "reason": str(exc), "model": model, "error": str(exc)}


@app.function
def classify_batch(client, texts, model="gemma3:1b"):
    return pd.DataFrame([classify_text(client, t, model) for t in texts])


@app.function
def summarize_results(df):
    ok = df[df["label"] != "error"]
    return {
        "total": len(df),
        "successful": len(ok),
        "label_counts": ok["label"].value_counts().to_dict() if len(ok) else {},
        "avg_confidence": round(float(ok["confidence"].mean()), 3) if len(ok) else 0.0,
    }


@app.function
def filter_by_label(df, label="All"):
    if label == "All":
        return df
    return df[df["label"] == label].reset_index(drop=True)


@app.function
def sample_reviews():
    return [
        "Absolutely love this product! Fast shipping and works perfectly.",
        "Terrible experience. Broke after two days and support was unhelpful.",
        "It's okay. Does what it says but nothing special.",
        "Exceeded my expectations. Highly recommend to anyone looking for quality.",
        "Packaging was damaged, product inside seemed fine but I'm not happy.",
        "Great value for money. Using it daily for three months with no issues.",
        "Instructions were confusing and setup took way too long.",
        "Customer service responded quickly and resolved my issue same day.",
        "Average product. Works but feels a bit cheap.",
        "Would not buy again. Stopped working after a week.",
    ]


@app.cell(hide_code=True)
def _():
    mo.md("""
    ## LLM Model Comparison

    Run the same reviews through **two Ollama models** side by side.
    Mark each classification correct ✓ or incorrect ✗ to build a live accuracy dashboard.

    Make sure Ollama is running first: `ollama serve`
    """)
    return


@app.cell
def _():
    base_url_input = mo.ui.text(
        value="http://localhost:11434/v1",
        label="Ollama base URL",
        full_width=True,
    )
    model_a_input = mo.ui.text(
        value="gemma3:1b",
        label="Model A",
        placeholder="e.g. gemma3:1b",
    )
    model_b_input = mo.ui.text(
        value="qwen2.5:0.5b",
        label="Model B",
        placeholder="e.g. qwen2.5:0.5b",
    )
    reviews_input = mo.ui.text_area(
        value="\n".join([
            "Absolutely love this product! Fast shipping and works perfectly.",
            "Terrible experience. Broke after two days and support was unhelpful.",
            "It's okay. Does what it says but nothing special.",
            "Exceeded my expectations. Highly recommend to anyone looking for quality.",
            "Packaging was damaged, product inside seemed fine but I'm not happy.",
            "Great value for money. Using it daily for three months with no issues.",
            "Instructions were confusing and setup took way too long.",
            "Customer service responded quickly and resolved my issue same day.",
            "Average product. Works but feels a bit cheap.",
            "Would not buy again. Stopped working after a week.",
        ]),
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
def _(base_url_input, model_a_input, model_b_input, reviews_input, run_btn):
    mo.stop(
        not run_btn.value,
        mo.md("_Fill in both models and click **Classify with both models** to start._"),
    )
    _texts = [r.strip() for r in reviews_input.value.splitlines() if r.strip()]
    mo.stop(not _texts, mo.md("_No reviews to classify._"))
    mo.stop(not model_a_input.value.strip(), mo.md("_Enter Model A._"))
    mo.stop(not model_b_input.value.strip(), mo.md("_Enter Model B._"))

    _client = get_client(base_url=base_url_input.value)
    _df_a = classify_batch(_client, _texts, model=model_a_input.value.strip())
    _df_b = classify_batch(_client, _texts, model=model_b_input.value.strip())
    results_df = pd.concat([_df_a, _df_b], ignore_index=True)
    results_df
    return (results_df,)


@app.cell(hide_code=True)
def _():
    mo.md("""
    ### Mark each classification correct or incorrect
    """)
    return


@app.cell(hide_code=True)
def _(model_a_input, model_b_input, results_df):
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
def _():
    mo.md("""
    ### Accuracy Dashboard
    """)
    return


@app.cell(hide_code=True)
def _(model_a_input, model_b_input, verdicts_a, verdicts_b):
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
def _(model_a_input, model_b_input, verdicts_a, verdicts_b):
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


if __name__ == "__main__":
    app.run()
