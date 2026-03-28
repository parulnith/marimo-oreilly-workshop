import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    a = 30
    return (a,)


@app.cell
def _():
    b = 20
    return (b,)


@app.cell
def _(a, b):
    c = a + b
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
