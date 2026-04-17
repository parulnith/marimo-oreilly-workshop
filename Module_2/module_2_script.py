import marimo

__generated_with = "0.23.1"
app = marimo.App()


@app.cell
def _():
    x = 10

    return (x,)


@app.cell
def _():
    y = 40

    return (y,)


@app.cell
def _(x, y):
    print("Sum =", x + y)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
