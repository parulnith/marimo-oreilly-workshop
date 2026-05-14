import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop/blob/main/Module_1/1_3_marimo_ui_elements.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # marimo UI Elements

    marimo ships with a built-in UI component library — sliders, dropdowns,
    tables, forms, selectable plots so you can explore **what-if questions**
    about your data and models without writing any callbacks.

    Every widget is **reactive**: change a value and dependent cells update
    instantly. Custom widgets work too via the [AnyWidget](https://anywidget.dev)
    standard, so domain-specific UIs slot in cleanly.

    The cells below tour the most common elements.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl

    return mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### `mo.ui.text` and `mo.ui.text_area`
    """)
    return


@app.cell
def _(mo):
    text_input = mo.ui.text(value="Hello, Marimo!", label="Text")
    textarea_input = mo.ui.text_area(value="Multiline text here...", label="Text Area")
    mo.vstack([text_input, textarea_input])
    return text_input, textarea_input


@app.cell(hide_code=True)
def _(mo, text_input, textarea_input):
    mo.md(f"""
    **Text value:** `{text_input.value}`

    **Text area value:** `{textarea_input.value}`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### `mo.ui.number`, `mo.ui.slider`, and `mo.ui.range_slider`
    """)
    return


@app.cell
def _(mo):
    number_input = mo.ui.number(value=42, label="Number")
    slider_input = mo.ui.slider(0, 100, value=50, label="Slider", step=1)
    range_input = mo.ui.range_slider(0, 100, value=[20, 80], label="Range Slider", step=5)
    mo.vstack([number_input, slider_input, range_input])
    return number_input, range_input, slider_input


@app.cell(hide_code=True)
def _(mo, number_input, range_input, slider_input):
    mo.md(f"""
    **Number:** {number_input.value}

    **Slider:** {slider_input.value}

    **Range:** {range_input.value[0]} – {range_input.value[1]}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### `mo.ui.checkbox`, `mo.ui.radio`, and `mo.ui.dropdown`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    checkbox_input = mo.ui.checkbox(label="Enable feature", value=True)
    radio_input = mo.ui.radio(
        options=["Option A", "Option B", "Option C"],
        value="Option A",
        label="Radio",
    )
    dropdown_input = mo.ui.dropdown(
        options=["Python", "R", "Julia", "Rust"],
        value="Python",
        label="Dropdown",
    )
    mo.hstack([checkbox_input, radio_input, dropdown_input])
    return checkbox_input, dropdown_input, radio_input


@app.cell(hide_code=True)
def _(checkbox_input, dropdown_input, mo, radio_input):
    mo.md(f"""
    **Checkbox:** {checkbox_input.value}

    **Radio:** {radio_input.value}

    **Dropdown:** {dropdown_input.value}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### `mo.ui.date`
    """)
    return


@app.cell
def _(mo):
    date_input = mo.ui.date(label="Date Picker")
    date_input
    return (date_input,)


@app.cell(hide_code=True)
def _(date_input, mo):
    date_str = str(date_input.value) if date_input.value else "No date selected"
    mo.md(f"**Selected date:** {date_str}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    #### `mo.ui.run_button`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    run_btn = mo.ui.run_button(label="Run Analysis", kind="neutral")
    run_btn
    return (run_btn,)


@app.cell(hide_code=True)
def _(mo, run_btn):
    _msg = "**Analysis complete!** The run button was clicked." if run_btn.value else "_Click the button to trigger an action._"
    mo.md(_msg)
    return


@app.cell
def _(mo):
    mo.md("""
    #### `mo.ui.table`
    """)
    return


@app.cell
def _(mo, pl):
    table_data = pl.DataFrame({
        "Name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
        "Score": [92, 85, 78, 95, 88],
        "Grade": ["A", "B", "C", "A", "B"],
    })
    table_input = mo.ui.table(table_data)
    table_input
    return (table_input,)


@app.cell
def _(mo, table_input):
    mo.md(f"""
    **{len(table_input.value)} row(s) selected**
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    #### `mo.ui.array`
    """)
    return


@app.cell
def _(mo):
    checkbox_array = mo.ui.array([
        mo.ui.checkbox(label="Task 1"),
        mo.ui.checkbox(label="Task 2"),
        mo.ui.checkbox(label="Task 3"),
        mo.ui.checkbox(label="Task 4"),
    ])
    checkbox_array
    return (checkbox_array,)


@app.cell
def _(checkbox_array, mo):
    completed = sum(checkbox_array.value)
    total = len(checkbox_array.value)
    mo.md(f"**Progress:** {completed}/{total} tasks completed")
    return


@app.cell
def _(mo):
    mo.md("""
    #### `mo.ui.form`

    Values are only committed when the user clicks Submit.
    """)
    return


@app.cell
def _(mo):
    form = mo.ui.form(
        mo.ui.array([
            mo.ui.text(label="Name"),
            mo.ui.number(value=25, label="Age"),
            mo.ui.dropdown(
                options=["Beginner", "Intermediate", "Advanced"],
                value="Beginner",
                label="Level",
            ),
        ]),
        label="Submit your info",
    )
    form
    return (form,)


@app.cell
def _(form, mo):
    _msg = (
        f"**Submitted:** Name=`{form.value[0]}`, Age=`{form.value[1]}`, Level=`{form.value[2]}`"
        if form.value is not None
        else "_Fill out the form and click Submit._"
    )
    mo.md(_msg)
    return


@app.cell
def _(mo):
    mo.md("""
    #### `mo.ui.tabs`
    """)
    return


@app.cell
def _(mo):
    summary_tabs = mo.ui.tabs({
        "What is Marimo?": mo.md("""
        Marimo is a **reactive** Python notebook where:
        - Cells re-run automatically when their dependencies change
        - Variables are unique across cells
        - UI elements update the notebook without callbacks
        """),
        "UI Element Tips": mo.md("""
        - Access values with `.value` (e.g. `slider.value`)
        - Define elements in one cell, read `.value` in the next
        - Use `mo.hstack` / `mo.vstack` for layout
        - `mo.ui.array` groups elements and returns a list of values
        - `mo.ui.form` defers value changes until the user clicks Submit
        """),
    })
    summary_tabs
    return


if __name__ == "__main__":
    app.run()
