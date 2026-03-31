# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "pandas",
#     "numpy",
#     "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")

with app.setup:
    import pandas as pd
    import numpy as np
    import json
    import time
    from typing import Literal


@app.function
def build_eval_dataset(n_samples: int = 200, random_state: int = 42) -> pd.DataFrame:
    """Generate a synthetic LLM evaluation dataset.

    Simulates the kind of data you get when running prompts through
    multiple models and scoring the outputs — the core loop of
    prompt engineering and model comparison.

    Each row represents one (prompt, model, response) evaluation.
    """
    rng = np.random.default_rng(random_state)

    models = ["gpt-5-mini", "claude-haiku-4.5", "gemini-2.5-flash", "qwen3-coder-local"]
    task_types = ["code_generation", "summarization", "classification", "reasoning"]
    prompt_templates = {
        "code_generation": [
            "Write a function that {task}",
            "Refactor this code to {task}",
            "Debug the following and {task}",
        ],
        "summarization": [
            "Summarize the following document about {topic}",
            "Give a 3-sentence summary of {topic}",
            "Extract key findings from {topic}",
        ],
        "classification": [
            "Classify this text as positive/negative: {text}",
            "Is this customer feedback about {category}?",
            "Label the intent of: {text}",
        ],
        "reasoning": [
            "Explain step by step how to {task}",
            "Compare the tradeoffs between {option_a} and {option_b}",
            "What would happen if {scenario}?",
        ],
    }

    rows = []
    for i in range(n_samples):
        model = rng.choice(models)
        task_type = rng.choice(task_types)
        prompt = rng.choice(prompt_templates[task_type])

        # Simulate realistic model characteristics
        is_local = model == "qwen3-coder-local"
        is_reasoning = task_type == "reasoning"

        # Quality: cloud models score higher, local models lower on complex tasks
        base_quality = {
            "gpt-5-mini": 82,
            "claude-haiku-4.5": 80,
            "gemini-2.5-flash": 78,
            "qwen3-coder-local": 65,
        }[model]

        # Local models do better on code, worse on reasoning
        if is_local and task_type == "code_generation":
            base_quality += 8
        if is_local and is_reasoning:
            base_quality -= 10

        quality_score = np.clip(
            base_quality + rng.normal(0, 8), 0, 100
        ).round(1)

        # Latency: local models slower, reasoning tasks slower
        base_latency = 0.8 if is_local else 0.3
        if is_reasoning:
            base_latency *= 2.5
        latency_ms = max(50, int(base_latency * 1000 + rng.normal(0, 200)))

        # Cost: local is free, cloud varies
        cost_per_1k = {
            "gpt-5-mini": 0.69,
            "claude-haiku-4.5": 4.00,
            "gemini-2.5-flash": 2.38,
            "qwen3-coder-local": 0.0,
        }[model]

        # Token counts
        input_tokens = int(rng.normal(150, 50))
        output_tokens = int(rng.normal(300, 100))
        total_tokens = input_tokens + output_tokens
        cost_usd = (total_tokens / 1000) * cost_per_1k

        # Pass/fail based on quality threshold
        passed = quality_score >= 70

        rows.append(
            {
                "eval_id": f"eval_{i:04d}",
                "model": model,
                "task_type": task_type,
                "prompt_template": prompt,
                "quality_score": quality_score,
                "latency_ms": latency_ms,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "cost_usd": round(cost_usd, 4),
                "passed": passed,
                "timestamp": pd.Timestamp("2026-03-01")
                + pd.Timedelta(minutes=int(i * 2.5 + rng.integers(0, 10))),
            }
        )

    return pd.DataFrame(rows)


@app.function
def filter_evals(
    df: pd.DataFrame,
    model: str = "All",
    task_type: str = "All",
    min_quality: float = 0.0,
) -> pd.DataFrame:
    """Filter evaluation results by model, task type, and quality threshold."""
    filtered = df.copy()
    if model != "All":
        filtered = filtered[filtered["model"] == model]
    if task_type != "All":
        filtered = filtered[filtered["task_type"] == task_type]
    filtered = filtered[filtered["quality_score"] >= min_quality]
    return filtered


@app.function
def compare_models(df: pd.DataFrame) -> pd.DataFrame:
    """Compare models across quality, latency, cost, and pass rate.

    Returns a summary table with one row per model — the kind of
    comparison table you build when deciding which model to use
    for a production pipeline.
    """
    summary = (
        df.groupby("model")
        .agg(
            avg_quality=("quality_score", "mean"),
            median_latency_ms=("latency_ms", "median"),
            avg_cost_usd=("cost_usd", "mean"),
            pass_rate=("passed", "mean"),
            total_evals=("eval_id", "count"),
        )
        .round(3)
    )
    summary["pass_rate"] = (summary["pass_rate"] * 100).round(1)
    summary = summary.sort_values("avg_quality", ascending=False)
    return summary.reset_index()


@app.function
def score_cost_efficiency(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate a quality-per-dollar efficiency score for each model.

    This answers the practical question: for every dollar I spend,
    how much quality do I get? Higher is better. Local models get
    infinite efficiency (free), so they are scored separately.
    """
    comparison = compare_models(df)
    comparison["quality_per_dollar"] = np.where(
        comparison["avg_cost_usd"] > 0,
        (comparison["avg_quality"] / comparison["avg_cost_usd"]).round(1),
        np.inf,  # Local models are free
    )
    return comparison[
        ["model", "avg_quality", "avg_cost_usd", "quality_per_dollar", "pass_rate"]
    ]


@app.function
def generate_report(df: pd.DataFrame, model_filter: str, task_filter: str) -> dict:
    """Generate a summary report dict — used by both app mode and CLI mode."""
    comparison = compare_models(df)
    best_model = comparison.iloc[0]
    cheapest = comparison.loc[comparison["avg_cost_usd"].idxmin()]

    return {
        "total_evals": len(df),
        "models_tested": df["model"].nunique(),
        "task_types_tested": df["task_type"].nunique(),
        "avg_quality": df["quality_score"].mean().round(1),
        "overall_pass_rate": (df["passed"].mean() * 100).round(1),
        "best_model": best_model["model"],
        "best_quality": best_model["avg_quality"].round(1),
        "cheapest_model": cheapest["model"],
        "cheapest_cost": cheapest["avg_cost_usd"].round(4),
        "filter_model": model_filter,
        "filter_task": task_filter,
    }


@app.cell
def _(mo):
    mo.md("""
    # LLM Evaluation Dashboard

    Compare model quality, latency, and cost across tasks and providers.
    Use the controls below to filter results and explore tradeoffs.

    **Run modes:**
    - `marimo edit module_5.py` — interactive notebook
    - `marimo run module_5.py` — dashboard (code hidden)
    - `python module_5.py -- --model claude-haiku-4.5 --task reasoning` — CLI report
    - `from module_5 import compare_models, score_cost_efficiency` — reusable in pipelines
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    eval_df = build_eval_dataset(n_samples=200)
    eval_df
    return (eval_df,)


@app.cell
def _(mo):
    model_ui = mo.ui.dropdown(
        options=[
            "All",
            "gpt-5-mini",
            "claude-haiku-4.5",
            "gemini-2.5-flash",
            "qwen3-coder-local",
        ],
        value="All",
        label="Model",
    )
    task_ui = mo.ui.dropdown(
        options=["All", "code_generation", "summarization", "classification", "reasoning"],
        value="All",
        label="Task type",
    )
    quality_ui = mo.ui.slider(
        start=0, stop=90, value=0, step=5, label="Min quality score"
    )

    mo.hstack([model_ui, task_ui, quality_ui], gap=2)
    return model_ui, quality_ui, task_ui


@app.cell
def _(eval_df, model_ui, quality_ui, task_ui):
    filtered = filter_evals(
        eval_df,
        model=model_ui.value,
        task_type=task_ui.value,
        min_quality=quality_ui.value,
    )
    return (filtered,)


@app.cell
def _(filtered, mo, model_ui, task_ui):
    report = generate_report(filtered, model_ui.value, task_ui.value)
    mo.md(
        f"""
    ### Summary

    | Metric | Value |
    |--------|-------|
    | Evaluations | **{report['total_evals']}** |
    | Models tested | **{report['models_tested']}** |
    | Avg quality | **{report['avg_quality']}** |
    | Pass rate (≥70) | **{report['overall_pass_rate']}%** |
    | Best model | **{report['best_model']}** ({report['best_quality']} avg) |
    | Cheapest model | **{report['cheapest_model']}** (${report['cheapest_cost']}/call) |
    """
    )
    return


@app.cell
def _(filtered, mo):
    comparison = compare_models(filtered)
    mo.md("### Model Comparison")
    mo.ui.table(comparison)
    return


@app.cell
def _(filtered, mo):
    efficiency = score_cost_efficiency(filtered)
    mo.md("### Cost Efficiency (quality per dollar)")
    mo.ui.table(efficiency)
    return


@app.cell
def _(filtered, mo):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # 1. Quality by model
    models_in_data = filtered["model"].unique()
    quality_by_model = filtered.groupby("model")["quality_score"].mean()
    colors = ["#4A90D9", "#E8913A", "#50B88C", "#9B6EC5"]
    axes[0].barh(
        quality_by_model.index,
        quality_by_model.values,
        color=colors[: len(quality_by_model)],
    )
    axes[0].set_title("Avg Quality by Model")
    axes[0].set_xlabel("Quality Score")
    axes[0].set_xlim(0, 100)

    # 2. Quality vs Cost scatter
    model_stats = filtered.groupby("model").agg(
        quality=("quality_score", "mean"),
        cost=("cost_usd", "mean"),
    )
    for idx, (model_name, row) in enumerate(model_stats.iterrows()):
        axes[1].scatter(
            row["cost"],
            row["quality"],
            s=120,
            color=colors[idx % len(colors)],
            label=model_name,
            zorder=5,
        )
    axes[1].set_title("Quality vs Cost")
    axes[1].set_xlabel("Avg Cost (USD/call)")
    axes[1].set_ylabel("Avg Quality")
    axes[1].legend(fontsize=7, loc="lower right")

    # 3. Quality by task type
    quality_by_task = filtered.groupby("task_type")["quality_score"].mean()
    axes[2].bar(
        range(len(quality_by_task)),
        quality_by_task.values,
        color="#4A90D9",
    )
    axes[2].set_xticks(range(len(quality_by_task)))
    axes[2].set_xticklabels(quality_by_task.index, rotation=30, ha="right", fontsize=8)
    axes[2].set_title("Avg Quality by Task")
    axes[2].set_ylabel("Quality Score")
    axes[2].set_ylim(0, 100)

    plt.tight_layout()
    mo.as_html(fig)
    return


@app.cell
def _(filtered, mo):
    mo.md("### Evaluation Details")
    mo.ui.table(
        filtered[
            [
                "eval_id",
                "model",
                "task_type",
                "quality_score",
                "latency_ms",
                "cost_usd",
                "passed",
            ]
        ].sort_values("quality_score", ascending=False)
    )
    return


@app.cell
def _():
    import marimo as _mo

    _cli_args = _mo.cli_args()

    cli_model = _cli_args.get("model", None)
    cli_task = _cli_args.get("task", None)
    cli_min_quality = _cli_args.get("min-quality", None)
    cli_output = _cli_args.get("output", None)

    if cli_model or cli_task or cli_min_quality or cli_output:
        _df = build_eval_dataset(n_samples=200)

        _model = cli_model or "All"
        _task = cli_task or "All"
        _min_q = float(cli_min_quality) if cli_min_quality else 0.0

        _filtered = filter_evals(_df, model=_model, task_type=_task, min_quality=_min_q)
        _report = generate_report(_filtered, _model, _task)
        _comparison = compare_models(_filtered)
        _efficiency = score_cost_efficiency(_filtered)

        print("=== LLM Evaluation Report ===")
        print(f"Filter: model={_model}, task={_task}, min_quality={_min_q}")
        print(f"Evaluations: {_report['total_evals']}")
        print(f"Avg quality: {_report['avg_quality']}")
        print(f"Pass rate: {_report['overall_pass_rate']}%")
        print(f"Best model: {_report['best_model']} ({_report['best_quality']} avg)")
        print(f"Cheapest: {_report['cheapest_model']} (${_report['cheapest_cost']}/call)")
        print()
        print("--- Model Comparison ---")
        print(_comparison.to_string(index=False))
        print()
        print("--- Cost Efficiency ---")
        print(_efficiency.to_string(index=False))

        if cli_output:
            _filtered.to_csv(cli_output, index=False)
            print(f"\nSaved {len(_filtered)} rows to {cli_output}")
    return


if __name__ == "__main__":
    app.run()
