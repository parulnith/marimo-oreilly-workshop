# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "pytest"]
# ///

import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell
def imports():
    import marimo as mo
    import pytest

    return mo, pytest


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Inline pytest in a marimo notebook

    marimo has built-in pytest support. Two ways to write tests:

    1. **A cell whose function name starts with `test_`** — that cell *is*
       the test. marimo runs it and shows pass/fail next to the cell.
    2. **A cell containing a collection of `test_*` functions** —
       marimo runs each of them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## The function

    `sample_reviews()` should return a non-empty list of non-empty review strings.
    """)
    return


@app.function
def sample_reviews():
    """Return a list of product reviews to classify."""
    return [
        "Battery dies in three weeks. Disappointing.",
        "Solid build, instructions are a war crime.",
        "Works fine. No complaints, no excitement.",
        "Returned it. Then bought it again.",
        "Five stars for packaging, the thing inside is fine.",
        "I wanted to hate this but I can't. Annoyingly good.",
        "Not bad, not great. I keep using it though.",
        "Customer service was great. Shame I had to call four times.",
        "Underwhelming for the price.",
        "It works. My cat is unimpressed.",
    ]


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## The tests

    Each cell below is a test that runs inline.
    """)
    return


@app.cell
def test_not_empty():
    assert len(sample_reviews()) > 0, "sample_reviews should not be empty"
    return


@app.cell
def test_are_strings():
    assert all(isinstance(r, str) for r in sample_reviews()), (
        "every review must be a string"
    )
    return


@app.cell
def test_no_blanks():
    assert all(r.strip() for r in sample_reviews()), "no blank reviews allowed"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### A collection of parametrized tests

    One cell, multiple parametrized cases — pytest runs each one.
    """)
    return


@app.cell
def collection_of_tests(pytest):
    @pytest.mark.parametrize("min_count", [1, 5, 10])
    def test_has_at_least(min_count):
        assert len(sample_reviews()) >= min_count, f"need at least {min_count} reviews"

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Try it

    Break a test on purpose to see what failure looks like for example,
    add `"\"` to the list above and the `test_no_blanks` cell turns red.

    Same file also runs as plain pytest:

    ```bash
    pytest inline_test_demo.py -v
    ```
    """)
    return


if __name__ == "__main__":
    app.run()
