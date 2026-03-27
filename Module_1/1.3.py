# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.8",
#     "pandas==3.0.1",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The Same Workflow, Reactively

    We start with the same **plain compound-interest workflow** from Section 1.2:
    fixed parameters, a helper function, a computed result, a plot, a table.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    import time

    return mo, pd, plt


@app.function
def compound_interest(principal, rate, years):
    values = [principal]
    for _year in range(1, years + 1):
        values.append(values[-1] * (1 + rate))
    return values


@app.cell
def _():
    principal = 10000
    rate = 0.07
    years = 20

    growth = compound_interest(principal, rate, years)
    return growth, principal, rate, years


@app.cell(hide_code=True)
def _(growth, mo, rate, years):
    mo.md(
        f"""
        After **{years} years** at **{rate:.0%}**, the account grows to
        **${growth[-1]:,.2f}**.
        """
    )
    return


@app.cell
def _(growth, plt, years):
    fig, ax = plt.subplots()
    ax.plot(range(years + 1), growth, marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("Balance ($)")
    ax.set_title(f"Compound Interest Growth ({years} years)")
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Compare multiple interest rates

    Same idea as before, but the table stays aligned automatically with the current inputs.
    """)
    return


@app.cell
def _():
    rates = [0.03, 0.05, 0.07, 0.10]
    return (rates,)


@app.cell
def _(pd, principal, rates, years):
    rows = []
    for comparison_rate in rates:
        scenario_growth = compound_interest(principal, comparison_rate, years)
        rows.append(
            {
                "rate": f"{comparison_rate:.0%}",
                "years_used": years,
                "final_value": scenario_growth[-1],
            }
        )
    summary_df = pd.DataFrame(rows)
    summary_df
    return


if __name__ == "__main__":
    app.run()
