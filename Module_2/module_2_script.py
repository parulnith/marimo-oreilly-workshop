import marimo

__generated_with = "0.23.1"
app = marimo.App()


@app.cell
def _():
    x = 10
    y = 40
    print("Sum =", x + y)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
