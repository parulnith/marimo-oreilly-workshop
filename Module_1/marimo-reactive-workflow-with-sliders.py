import marimo

app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    x = mo.ui.number(label="First number", value=10)
    y = mo.ui.number(label="Second number", value=20)
    return mo.vstack([x, y]), x, y


@app.cell
def _(mo, x, y):
    mo.md(f"## Sum = {x.value + y.value}")
    return


if __name__ == "__main__":
    app.run()
