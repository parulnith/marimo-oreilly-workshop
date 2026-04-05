import marimo

app = marimo.App()


@app.cell
def _():
    x = 10
    y = 20
    print("Sum =", x + y)
    return x, y


if __name__ == "__main__":
    app.run()
