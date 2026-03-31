import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas

    return


@app.cell
def _():
    import pandas as pd

    df_transactions = pd.DataFrame({'transaction_id': [1, 2, 3], 'amount': [100, 200, 150]})
    return (df_transactions,)


@app.cell
def _(df_transactions):
    df_transactions
    return


@app.cell
def _():
    import seaborn as sns

    df_penguins = sns.load_dataset('penguins')
    df_penguins
    return


app._unparsable_cell(
    r"""
    import pandas as 
    """,
    name="_"
)


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    def generate_fibonacci(n):
        """Returns the first n numbers in the Fibonacci sequence."""
        if n <= 0:
            return []
        elif n == 1:
            return [0]
    
        sequence = [0, 1]
        for _ in range(2, n):
            sequence.append(sequence[-1] + sequence[-2])
        return sequence[:n]

    # Generate the first 15 terms
    fib_sequence = generate_fibonacci(15)

    # Display the result nicely using markdown
    mo.md(f"**Fibonacci sequence (first 15 terms):** {fib_sequence}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    **Morning dew glistens**

    On spider silk stretched between
    Flower petals sway
    """)
    return


app._unparsable_cell(
    r"""
    import pandas as 
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
