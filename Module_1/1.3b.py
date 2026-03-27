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


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return mo, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Section 1.3b — The Same Workflow, Now With Sliders

    This notebook takes the exact same compound-interest workflow and connects the inputs to UI controls.

    The important idea is still **reactive execution**:
    move a slider and every dependent result updates automatically.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose the inputs interactively

    These sliders replace the fixed variables from `1.3.py`.
    """)
    return


@app.cell
def _(mo):
    principal_slider = mo.ui.slider(
        start=500,
        stop=10000,
        step=500,
        value=1000,
        label="Starting amount ($)",
    )
    rate_slider = mo.ui.slider(
        start=0.01,
        stop=0.15,
        step=0.01,
        value=0.07,
        label="Annual interest rate",
    )
    years_slider = mo.ui.slider(
        start=5,
        stop=50,
        step=5,
        value=20,
        label="Years",
    )
    return principal_slider, rate_slider, years_slider


@app.cell
def _(mo, principal_slider, rate_slider, years_slider):
    mo.vstack(
        [
            principal_slider,
            rate_slider,
            years_slider,
        ],
        gap=1.0,
    )

    return


@app.cell
def _(principal_slider, rate_slider, years_slider):
    principal = principal_slider.value
    rate = rate_slider.value
    years = years_slider.value
    return principal, rate, years


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Use the same helper function
    """)
    return


@app.function
def compound_interest(principal, rate, years):
    values = [principal]
    for _year in range(1, years + 1):
        values.append(values[-1] * (1 + rate))
    return values


@app.cell
def _(principal, rate, years):
    growth = compound_interest(principal, rate, years)
    return (growth,)


@app.cell(hide_code=True)
def _(growth, mo, rate, years):
    mo.md(
        f"""
        ## Compute one scenario

        After **{years} years** at **{rate:.0%}**, the account grows to
        **${growth[-1]:,.2f}**.

        """
    )
    return


@app.cell
def _(growth, plt, years):
    fig, ax = plt.subplots()
    ax.plot(range(years + 1), growth, marker="o", color="#d95f02")
    ax.set_xlabel("Year")
    ax.set_ylabel("Balance ($)")
    ax.set_title(f"Reactive Growth View ({years} years)")
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Keep the comparison table in sync
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
 
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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---

    In Jupyter, changing an input means remembering which cells to rerun.

    Here, the sliders are just the visible part of the system. The real improvement is that marimo keeps the whole dependency graph synchronized automatically.
    """)
    return


if __name__ == "__main__":
    app.run()
