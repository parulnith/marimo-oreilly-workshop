# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.7",
#     "pandas==2.3.3",
#     "scikit-learn==1.8.0",
#     "tabicl",
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # Adult Income Explorer

        This notebook shows the full interactive loop for AI work:
        explore data, shape features, fit models, inspect errors, and adjust the
        setup without breaking flow.
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    from sklearn.datasets import fetch_openml
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from tabicl import TabICLClassifier

    return (
        LabelEncoder,
        RandomForestClassifier,
        TabICLClassifier,
        accuracy_score,
        fetch_openml,
        mo,
        plt,
        train_test_split,
    )


@app.cell
def _(fetch_openml):
    data = fetch_openml("adult", version=2, as_frame=True)
    df = data.frame.copy()
    df["income"] = (df["class"].str.strip() == ">50K").astype(int)
    df = df.drop(columns=["class"]).dropna()
    feature_options = [
        "age",
        "education-num",
        "hours-per-week",
        "capital-gain",
        "capital-loss",
        "occupation",
        "marital-status",
    ]
    return df, feature_options


@app.cell(hide_code=True)
def _(df, mo):
    mo.md(
        f"""
        ## Interactive Data Exploration

        The Adult Income dataset has **{len(df):,} rows**. Start by exploring it
        directly in the notebook.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("### Raw dataframe")
    return


@app.cell
def _(df):
    df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("### `mo.ui.dataframe(df)`")
    return


@app.cell
def _(df, mo):
    explorer = mo.ui.dataframe(df)
    explorer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        `mo.ui.dataframe()` is useful for direct table inspection. If you want a
        chart-first exploration workflow, use `mo.ui.data_explorer()` in the same
        notebook.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("### `mo.ui.data_explorer(df)`")
    return


@app.cell
def _(df, mo):
    data_explorer = mo.ui.data_explorer(df)
    data_explorer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("### `mo.ui.data_editor(df)`")
    return


@app.cell
def _(df, mo):
    editable_sample = mo.ui.data_editor(
        df[["age", "education-num", "hours-per-week", "capital-gain"]].head(8),
        label="Optional: edit a small sample to test what-if scenarios",
    )
    editable_sample
    return (editable_sample,)


@app.cell
def _(editable_sample, mo):
    edited = editable_sample.value
    numeric_cols = [
        col
        for col in ["age", "education-num", "hours-per-week", "capital-gain"]
        if col in edited.columns
    ]
    summary_rows = "\n".join(
        f"| {col} | {edited[col].mean():.1f} |" for col in numeric_cols
    )
    mo.md(
        f"""
        The edited sample below stays reactive. You can change a few values and
        immediately see the updated summary.

        | Column | Mean in edited sample |
        |---|---|
        {summary_rows}
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## Interactive Modeling

        The controls below drive preprocessing, model fitting, and error analysis
        automatically.
        """
    )
    return


@app.cell
def _(feature_options, mo):
    selected_features_ui = mo.ui.multiselect(
        options=feature_options,
        value=["age", "education-num", "hours-per-week", "capital-gain"],
        label="Features to include in the model",
    )
    train_size_slider = mo.ui.slider(
        start=0.2,
        stop=0.9,
        step=0.1,
        value=0.7,
        label="Training set size",
    )
    preview_rows = mo.ui.slider(
        start=5,
        stop=25,
        step=5,
        value=10,
        label="Rows to preview in the error table",
    )
    mo.vstack([selected_features_ui, train_size_slider, preview_rows])
    return preview_rows, selected_features_ui, train_size_slider


@app.cell
def _(df, mo, selected_features_ui, train_size_slider):
    selected_features = selected_features_ui.value
    train_size = train_size_slider.value
    test_rows = len(df) - int(len(df) * train_size)
    mo.md(
        f"""
        **Active configuration**
        - Features: `{selected_features}`
        - Training split: `{int(train_size * 100)}% / {int((1 - train_size) * 100)}%`
        - Training rows: `{int(len(df) * train_size):,}`
        - Test rows: `{test_rows:,}`
        """
    )
    return selected_features, train_size


@app.cell
def _(LabelEncoder, df, selected_features, train_size, train_test_split):
    X = df[selected_features].copy()
    encoder_map = {}
    for col in X.select_dtypes(include="object").columns:
        encoder = LabelEncoder()
        X[col] = encoder.fit_transform(X[col].astype(str))
        encoder_map[col] = encoder

    y = df["income"].astype(int).values
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        train_size=train_size,
        random_state=42,
        stratify=y,
    )
    return X_test, X_train, encoder_map, y_test, y_train


@app.cell
def _(X_test, X_train, encoder_map, mo, selected_features, y_test):
    mo.md(
        f"""
        **Dataset ready**
        - Encoded categorical columns: `{list(encoder_map)}`
        - Training matrix: `{X_train.shape[0]:,} rows x {X_train.shape[1]} columns`
        - Test matrix: `{X_test.shape[0]:,} rows`
        - Positive class share in test set: `{y_test.mean():.1%}`
        - Selected features: `{selected_features}`
        """
    )
    return


@app.cell
def _(
    RandomForestClassifier,
    TabICLClassifier,
    X_test,
    X_train,
    accuracy_score,
    mo,
    y_test,
    y_train,
):
    tabicl = TabICLClassifier()
    tabicl.fit(X_train, y_train)
    tabicl_preds = tabicl.predict(X_test)
    tabicl_acc = accuracy_score(y_test, tabicl_preds)

    rf = RandomForestClassifier(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_preds)

    mo.md(
        f"""
        ### Model comparison

        - TabICL accuracy: `{tabicl_acc:.1%}`
        - Random Forest accuracy: `{rf_acc:.1%}`
        """
    )
    return rf_acc, rf_preds, tabicl_acc, tabicl_preds


@app.cell
def _(
    accuracy_score,
    mo,
    plt,
    rf_acc,
    rf_preds,
    selected_features,
    tabicl_acc,
    tabicl_preds,
    train_size,
    y_test,
):
    classes = ["<=50K", ">50K"]
    tabicl_per_class = [
        accuracy_score(y_test[y_test == i], tabicl_preds[y_test == i]) for i in [0, 1]
    ]
    rf_per_class = [
        accuracy_score(y_test[y_test == i], rf_preds[y_test == i]) for i in [0, 1]
    ]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8), sharey=True)
    plot_data = [
        ("TabICL", tabicl_per_class, "#4C72B0"),
        ("Random Forest", rf_per_class, "#55A868"),
    ]
    for ax, (title, values, color) in zip(axes, plot_data):
        bars = ax.bar(classes, values, color=[color, "#DD8452"])
        ax.set_ylim(0, 1)
        ax.set_title(title)
        ax.set_ylabel("Accuracy")
        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.02,
                f"{value:.1%}",
                ha="center",
                fontsize=10,
            )

    fig.suptitle(
        "Per-class accuracy by model\n"
        f"train size={int(train_size * 100)}%, features={len(selected_features)}"
    )
    plt.tight_layout()

    mo.vstack(
        [
            mo.md(
                f"""
                | Model | Overall accuracy |
                |---|---|
                | TabICL | {tabicl_acc:.1%} |
                | Random Forest | {rf_acc:.1%} |

                Compare the overall scores and then check whether one model is more
                stable across the two income groups.
                """
            ),
            fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## Visual Feedback for Analysis and Debugging

        Switch between models, inspect where the errors cluster, and select rows
        for a closer look.
        """
    )
    return


@app.cell
def _(mo):
    model_view = mo.ui.radio(
        options=["TabICL", "Random Forest"],
        value="TabICL",
        label="Model to inspect in the error analysis",
    )
    model_view
    return (model_view,)


@app.cell
def _(X_test, model_view, rf_preds, tabicl_preds, y_test):
    active_preds = tabicl_preds if model_view.value == "TabICL" else rf_preds
    results_df = X_test.copy()
    results_df["true_label"] = y_test
    results_df["predicted"] = active_preds
    results_df["correct"] = (
        results_df["true_label"] == results_df["predicted"]
    ).astype(int)
    results_df["income_label"] = results_df["true_label"].map({0: "<=50K", 1: ">50K"})
    errors = results_df[results_df["correct"] == 0].copy()
    return errors, results_df


@app.cell
def _(errors, model_view, mo):
    mo.md(
        f"""
        **Inspecting:** `{model_view.value}`

        **Current error count:** `{len(errors):,}`
        """
    )
    return


@app.cell
def _(errors, mo, plt, selected_features):
    required_cols = {"age", "hours-per-week"}
    if not required_cols.issubset(errors.columns):
        mo.callout(
            mo.md(
                "Add both `age` and `hours-per-week` to the feature selector to "
                "render the error map."
            ),
            kind="warn",
        )
        return

    fig, ax = plt.subplots(figsize=(7, 4.8))
    ax.scatter(
        errors["age"],
        errors["hours-per-week"],
        c="#C44E52",
        alpha=0.65,
        s=24,
        label="Misclassified rows",
    )
    ax.set_xlabel("Age")
    ax.set_ylabel("Hours per week")
    ax.set_title(
        "Where the model makes mistakes\n"
        f"features={selected_features}"
    )
    ax.legend()
    plt.tight_layout()
    fig
    return


@app.cell
def _(errors, mo, preview_rows):
    display_cols = [
        col
        for col in [
            "age",
            "education-num",
            "hours-per-week",
            "capital-gain",
            "income_label",
            "predicted",
        ]
        if col in errors.columns
    ]
    error_table = mo.ui.table(
        errors[display_cols].head(preview_rows.value),
        label="Select misclassified rows to inspect",
    )
    error_table
    return (error_table,)


@app.cell
def _(error_table, mo, results_df):
    selected = error_table.value
    if len(selected) == 0:
        mo.callout(
            mo.md("Select one or more rows in the error table to inspect them."),
            kind="info",
        )
        return

    stats_cols = [
        col
        for col in ["age", "hours-per-week", "education-num", "capital-gain"]
        if col in selected.columns and col in results_df.columns
    ]
    rows = "\n".join(
        f"| {col} | {selected[col].mean():.1f} | {results_df[col].mean():.1f} |"
        for col in stats_cols
    )
    mo.vstack(
        [
            mo.md(f"**{len(selected)} error rows selected**"),
            mo.md(
                f"""
                | Feature | Selected mean | Full test mean |
                |---|---|---|
                {rows}
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ### Close the loop

        Try removing `capital-gain`, shrinking the training split, or adding
        `occupation`. Watch the model metrics, plots, and error table update
        together.
        """
    )
    return


if __name__ == "__main__":
    app.run()
