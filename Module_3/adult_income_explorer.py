import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from sklearn.datasets import fetch_openml
    import pandas as pd

    data = fetch_openml("adult", version=2, as_frame=True)
    df = data.frame
    df["income"] = (df["class"].str.strip() == ">50K").astype(int)
    df = df.drop(columns=["class"]).dropna()
    df
    return (df,)


@app.cell
def _(df, mo):
    mo.ui.dataframe(df)
    return


@app.cell
def _(mo):
    feature_selector = mo.ui.multiselect(
        options=["age", "education-num", "hours-per-week",
                 "capital-gain", "capital-loss"],
        value=["age", "education-num", "hours-per-week"],
        label="Features to include"
    )

    train_size_slider = mo.ui.slider(
        start=0.1, stop=0.9, step=0.1, value=0.7,
        label="Training set size"
    )

    mo.vstack([feature_selector, train_size_slider])
    return feature_selector, train_size_slider


@app.cell
def _(df, feature_selector, mo, train_size_slider):
    selected_features = feature_selector.value
    train_size = train_size_slider.value

    mo.md(f"""
    **Active configuration:**
    - Features: `{selected_features}`
    - Training split: `{int(train_size * 100)}% / {int((1 - train_size) * 100)}%`
    - Training rows: `{int(len(df) * train_size):,}`
    """)
    return


if __name__ == "__main__":
    app.run()
