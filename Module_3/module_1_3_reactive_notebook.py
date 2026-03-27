import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # Classifying 2D Data — Interactively

    Let's explore a classification problem. We'll generate data, train a model,
    and see what happens when we change things.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split
    from sklearn.datasets import make_moons, make_circles
    from sklearn.metrics import roc_auc_score, accuracy_score
    from sklearn.ensemble import RandomForestClassifier

    return (
        RandomForestClassifier,
        accuracy_score,
        make_circles,
        make_moons,
        mo,
        plt,
        roc_auc_score,
        train_test_split,
    )


@app.cell
def _(mo):
    noise_slider = mo.ui.slider(
        start=0.05,
        stop=0.60,
        step=0.05,
        value=0.25,
        label="Noise level",
    )
    sample_slider = mo.ui.slider(
        start=200,
        stop=1500,
        step=100,
        value=800,
        label="Number of samples",
    )
    dataset_picker = mo.ui.dropdown(
        options=["Moons", "Circles"],
        value="Moons",
        label="Dataset shape",
    )
    mo.md(
        f"""
        ## Step 1: Configure the dataset

        {dataset_picker}

        {noise_slider}

        {sample_slider}
        """
    )
    return dataset_picker, noise_slider, sample_slider


@app.cell
def _(
    dataset_picker,
    make_circles,
    make_moons,
    noise_slider,
    plt,
    sample_slider,
    train_test_split,
):
    # Generate data based on UI selections
    if dataset_picker.value == "Moons":
        X, y = make_moons(
            n_samples=sample_slider.value,
            noise=noise_slider.value,
            random_state=0,
        )
    else:
        X, y = make_circles(
            n_samples=sample_slider.value,
            noise=noise_slider.value,
            factor=0.5,
            random_state=0,
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    _, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(
        X_train[:, 0], X_train[:, 1],
        c=y_train, cmap="RdYlBu_r",
        edgecolors="k", s=40, alpha=0.7,
    )
    ax.set(xlabel="Feature 1", ylabel="Feature 2")
    ax.set_title(
        f"{dataset_picker.value} — "
        f"n={sample_slider.value}, noise={noise_slider.value:.2f}"
    )
    plt.tight_layout()
    plt.show()
    return X_test, X_train, y_test, y_train


@app.cell
def _(mo):
    mo.md(r"""
    ## Step 2: Train TabICL

    TabICL is a foundation model for tabular classification —
    it works out of the box with no hyperparameter tuning.
    """)
    return


@app.cell
def _(X_test, X_train, accuracy_score, roc_auc_score, y_test, y_train):
    from tabicl import TabICLClassifier

    model = TabICLClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)

    acc = accuracy_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_proba[:, 1])
    return acc, roc


@app.cell
def _(acc, dataset_picker, mo, noise_slider, roc, sample_slider):
    mo.md(
        f"""
        ### Results

        | Metric | Value |
        |--------|-------|
        | **Accuracy** | {acc:.3f} |
        | **ROC AUC** | {roc:.3f} |
        | Dataset | {dataset_picker.value} |
        | Noise | {noise_slider.value:.2f} |
        | Samples | {sample_slider.value} |

        *Try changing the sliders above — these results update automatically.*
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Step 3: Compare with Random Forest

    Let's see how TabICL compares to a traditional classifier on the same data.
    """)
    return


@app.cell
def _(
    RandomForestClassifier,
    X_test,
    X_train,
    acc,
    accuracy_score,
    mo,
    roc,
    roc_auc_score,
    y_test,
    y_train,
):
    rf = RandomForestClassifier(n_estimators=100, random_state=0)
    rf.fit(X_train, y_train)

    rf_pred = rf.predict(X_test)
    rf_proba = rf.predict_proba(X_test)
    rf_acc = accuracy_score(y_test, rf_pred)
    rf_roc = roc_auc_score(y_test, rf_proba[:, 1])

    mo.md(
        f"""
        | Model | Accuracy | ROC AUC |
        |-------|----------|---------|
        | **TabICL** | {acc:.3f} | {roc:.3f} |
        | **Random Forest** | {rf_acc:.3f} | {rf_roc:.3f} |

        *Change the noise or dataset above — both models re-train automatically.*
        """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
