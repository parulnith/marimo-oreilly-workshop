import marimo

__generated_with = "0.23.1"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    return np, plt


@app.cell
def _(np, plt):
    x = np.linspace(-3, 3, 200)
    y = x**2

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("y = x^2")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
