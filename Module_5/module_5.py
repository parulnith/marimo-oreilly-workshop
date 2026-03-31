# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "altair",
#     "scikit-learn",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Wine Classifier — An Interactive ML Pipeline

    This notebook trains a **Random Forest** on the
    [UCI Wine dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#wine-dataset)
    (178 samples · 13 chemical features · 3 wine classes).

    Use the sliders to tune the model and watch accuracy, feature importance,
    and the confusion matrix update reactively.

    | Mode | Command |
    |------|---------|
    | Interactive notebook | `marimo edit module_5.py` |
    | Clean web app | `marimo run module_5.py` |
    | Headless script | `python module_5.py --n-estimators 200 --max-depth 5` |
    | Importable module | `from module_5 import load_wine_data, train_classifier` |
    """)
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import altair as alt

    return alt, mo, pl


@app.cell
def _(load_wine_data):
    wine_df, feature_names, class_names = load_wine_data()
    return class_names, feature_names, wine_df


@app.cell(hide_code=True)
def _(mo, wine_df):
    mo.md(f"""
    #### Dataset

    **{wine_df.shape[0]} samples · {wine_df.shape[1] - 1} features · 3 classes**
    (Barolo, Grignolino, Barbera)
    """)
    return


@app.cell
def _(mo, wine_df):
    mo.ui.dataframe(wine_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Model Configuration
    """)
    return


@app.cell
def _(mo):
    n_estimators_ui = mo.ui.slider(10, 300, value=100, step=10, label="Number of trees")
    max_depth_ui = mo.ui.slider(0, 20, value=0, step=1, label="Max depth (0 = unlimited)")
    test_size_ui = mo.ui.slider(0.1, 0.4, value=0.2, step=0.05, label="Test size")
    mo.vstack([n_estimators_ui, max_depth_ui, test_size_ui])
    return max_depth_ui, n_estimators_ui, test_size_ui


@app.cell
def _(
    feature_names,
    max_depth_ui,
    n_estimators_ui,
    test_size_ui,
    train_classifier,
    wine_df,
):
    model, X_test, y_test = train_classifier(
        wine_df,
        feature_names,
        n_estimators=n_estimators_ui.value,
        max_depth=max_depth_ui.value,
        test_size=test_size_ui.value,
    )
    return X_test, model, y_test


@app.cell
def _(X_test, evaluate_model, model, y_test):
    metrics = evaluate_model(model, X_test, y_test)
    return (metrics,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Model Performance
    """)
    return


@app.cell(hide_code=True)
def _(metrics, mo):
    mo.hstack([
        mo.stat(value=f"{metrics['accuracy']:.1%}", label="Accuracy"),
        mo.stat(value=f"{metrics['f1_macro']:.1%}", label="Macro F1"),
        mo.stat(value=str(len(metrics["y_test"])), label="Test samples"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Feature Importance
    """)
    return


@app.cell
def _(alt, feature_names, model, pl):
    _fi_df = pl.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_.tolist(),
    }).sort("Importance", descending=True)

    alt.Chart(_fi_df).mark_bar(color="#4C72B0").encode(
        x=alt.X("Importance:Q", title="Mean decrease in impurity"),
        y=alt.Y("Feature:N", sort="-x", title=None),
        tooltip=["Feature:N", alt.Tooltip("Importance:Q", format=".3f")],
    ).properties(title="Feature Importance (Random Forest)", width=550, height=320)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Confusion Matrix
    """)
    return


@app.cell
def _(alt, class_names, metrics, pl):
    from sklearn.metrics import confusion_matrix as _cm_fn

    _cm = _cm_fn(metrics["y_test"], metrics["y_pred"])
    _rows = [
        {"Actual": class_names[i], "Predicted": class_names[j], "Count": int(_cm[i][j])}
        for i in range(3)
        for j in range(3)
    ]
    _cm_df = pl.DataFrame(_rows)

    _base = alt.Chart(_cm_df)
    (
        _base.mark_rect().encode(
            x=alt.X("Predicted:N", title="Predicted label"),
            y=alt.Y("Actual:N", title="True label"),
            color=alt.Color("Count:Q", scale=alt.Scale(scheme="blues"), legend=None),
            tooltip=["Actual:N", "Predicted:N", "Count:Q"],
        )
        + _base.mark_text(fontSize=16, fontWeight="bold").encode(
            x="Predicted:N",
            y="Actual:N",
            text="Count:Q",
            color=alt.condition(
                alt.datum.Count > int(_cm.max() / 2),
                alt.value("white"),
                alt.value("black"),
            ),
        )
    ).properties(title="Confusion Matrix", width=280, height=240)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Reuse as a Module

    Because `module_5.py` is plain Python, you can import its functions
    directly from another script — no conversion, no copy-paste:

    ```python
    # pipeline.py
    from module_5 import load_wine_data, train_classifier, evaluate_model

    df, features, classes = load_wine_data()
    model, X_test, y_test = train_classifier(df, features, n_estimators=200)
    metrics = evaluate_model(model, X_test, y_test)
    print(f"Accuracy: {metrics['accuracy']:.1%}")
    ```

    The interactive notebook and the production pipeline share the **same
    source of truth** — edit once, run everywhere.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Run as a Script

    Pass hyperparameters from the command line for headless automation:

    ```bash
    python module_5.py --n-estimators 200 --max-depth 5 --test-size 0.25
    ```

    Schedule with cron or a GitHub Action — the same notebook that runs
    interactively here becomes a reproducible pipeline step with no changes.
    """)
    return


if __name__ == "__main__":
    app.run()
