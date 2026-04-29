## Module 3: Why Interactivity Accelerates AI Discovery

### Opening

Interactivity matters because it shortens the loop between noticing something, testing an idea, and learning from the result. In AI work, that loop often includes data inspection, feature choices, model behavior, and visual feedback. If those pieces live in separate tools or require manual reruns between steps, discovery slows down.

In this module, the goal is to show what happens when those parts become one connected system. Data, controls, models, tables, and plots can all respond to one another in the same notebook.


---

### 3.1 Interactive Computation as a Unified System

Interactive computation becomes powerful when the notebook behaves like one live graph instead of a stack of disconnected steps. In that kind of workflow, user input is not separate from the computation. Tables, widgets, plots, and model outputs all become part of the same system.

That is the main idea behind this notebook. It starts with the data, moves into visual exploration, then carries those choices directly into model training and debugging without breaking the flow.

> 💡 **Try it — `Module_3/module_3.py`**

go terminal - cd Module_3 - 

>
> Open the notebook in sandbox mode:
>
> ```bash
> marimo edit --sandbox Module_3/module_3.py
> ```
>
> As you work through it, notice that the notebook is not divided into isolated phases. The same live state carries forward from data exploration to model comparison to error analysis.

#### What we'll do in the notebook

We'll walk through one end-to-end AI workflow on the **Adult Income** dataset — a classic tabular benchmark from the US Census where the task is to predict whether a person earns more than $50K per year. It's a binary classification problem with a mix of numeric (age, hours-per-week, capital gains) and categorical (occupation, education, marital status) features.

We picked it because it's small enough to model live in a workshop, but messy enough that feature choices and sample sizes actually matter — which is exactly what we want when demonstrating interactivity.

Here's the path we'll take:

1. **Look at the data** — first as a raw dataframe, then as an editable sample.
2. **Explore it visually** — drag columns into a chart, then sort and filter a table.
3. **Pick features and sample size** — using widgets that drive the rest of the pipeline.
4. **Fit and compare two models** — TabICL and Random Forest, side by side.
5. **Debug errors interactively** — move a threshold, inspect misclassified rows, and compare them back to the full test set.

Each stage introduces a marimo widget. The notes below explain *what each concept is* and *how to use each widget*, not just what the notebook shows. 

---

**1. Data — inspecting and editing**

1. The raw dataframe is shown first as a baseline view (just put `df` as the last expression in a cell — marimo renders it as an interactive table). marimo lets you page through, search, sort, and filter dataframes, making it extremely easy to get a feel for your data. You can also export the selection and freeze etc.

2.  **`mo.ui.data_editor(...)`** for editable tabular input:

```python
editor = mo.ui.data_editor(df.head(8), label="Edit a small sample")
editor
```

How to use it:
- Pass a pandas or polars dataframe, a list of dicts, or a dict of lists.
- Click any cell to edit it directly in the table.
- Access the edited data in a *different* cell via `editor.value` — it comes back in the same format you passed in.
- Use `editable_columns=[...]` to restrict which columns are editable.
- Good for small what-if experiments; it is intentionally limited and not meant for bulk editing.

---

**2. Visualization — exploring distributions and relationships**

**`mo.ui.data_explorer(df)`** — chart-first, drag-and-drop exploration:

```python
mo.ui.data_explorer(df)
# or with an initial configuration:
mo.ui.data_explorer(df, x="income", y="age", color="sex"). chart kind =bar
```

How to use it:
- Drag columns into encoding slots: x, y, color, size, shape, row, column.
- Build up a plot incrementally — marimo suggests follow-up charts based on the current config.
- `.value` returns a dict with the current chart spec (useful if you want to persist it).
- Use this *before* you know what you want to plot.

**`mo.ui.dataframe(df)`** — interactive transform builder:

```python
explorer = mo.ui.dataframe(df)
explorer
# in a later cell:
explorer.value   # the transformed dataframe
```

How to use it:
- Click the toolbar to apply one of 13 transforms: filter, sort, group by, aggregate, select columns, rename, sample, unique, pivot, etc.
- The widget also shows the generated Python code for each transform — copy it into a cell to make the transform permanent.
- Use this *after* data_explorer, when you know which subset or shape of the data you want to carry forward.

groupby age / aggrgate on columns - education num, capital gain and hours per week/ -aggregation-count

---

**3. Modeling controls — driving the pipeline with widgets**

```python
selected_features_ui = mo.ui.multiselect(options=feature_options, value=feature_options, label="Features")
sample_size_ui = mo.ui.slider(500, 3000, step=500, value=1000, label="Rows to sample")
preview_rows = mo.ui.slider(5, 25, step=5, value=10, label="Error rows to preview")
mo.vstack([selected_features_ui, sample_size_ui, preview_rows])
```

How to use these:
- Define the widget in one cell, display it, then read `.value` in a *different* cell. Reading `.value` in the same cell that defines the widget will not work.
- Any downstream cell that reads `selected_features_ui.value` re-runs automatically whenever the user changes the multiselect. No callbacks needed.
- Group related widgets with `mo.vstack([...])` or `mo.hstack([...])` for a tidy layout.

---

**4. Model comparison — two models on the same live inputs**

We fit two very different models on the same `X_train`, `y_train`:

- **TabICL** — a *tabular foundation model*. Like large language models pre-trained on text, TabICL is pre-trained on many synthetic tabular datasets, so it can make predictions on a new table through in-context learning without traditional gradient-based training on your data. Think of it as "GPT for tables." Fast to use, no hyperparameter tuning, strong out-of-the-box performance on small/medium tabular tasks. [Docs](https://github.com/soda-inria/tabicl).
- **Random Forest** — the classic baseline. An ensemble of decision trees where each tree sees a random subset of rows and features, and predictions are averaged. Reliable, interpretable, and a reasonable reference point for any tabular problem.

We compare them two ways:

- **ROC AUC** (Receiver Operating Characteristic – Area Under the Curve). A single number between 0 and 1 that measures how well the model *ranks* positive cases above negative ones, across every possible classification threshold. 1.0 is perfect, 0.5 is random guessing. Unlike accuracy, it doesn't get fooled by class imbalance — which matters here because most people in the dataset earn ≤ 50K.
- **Predicted-probability histograms** split by true label. These show *how confident* each model is, not just whether it's right. A well-calibrated model puts high probabilities on true positives and low probabilities on true negatives — if the two histograms overlap heavily, the model is struggling to separate the classes.

Because both models depend on the same widget-driven inputs, the bar chart and histograms recompute whenever features or sample size change — no rerun needed.

Pattern to remember: put the expensive step (fitting) in a cell that depends only on the widget values, and let the plot cells depend on the fitted models. Marimo's DAG handles the rest.

---

**5. Error analysis — `mo.ui.table` closes the loop**

A quick concept first: a classifier produces a *probability* for each row (e.g. "73% chance this person earns > 50K"). To turn that into a hard yes/no prediction, you pick a **threshold** — typically 0.5. Lowering the threshold (say, to 0.3) makes the model more eager to predict "positive," which catches more true positives but also produces more false positives. Moving the threshold live is one of the fastest ways to build intuition about a classifier's behavior.

From there, errors fall into two types:

- **False positives** — model said > 50K, actual label was ≤ 50K.
- **False negatives** — model said ≤ 50K, actual label was > 50K.

Which of these matters more depends on the downstream use case; the notebook lets you look at either.

```python
threshold_slider = mo.ui.slider(0.1, 0.9, step=0.05, value=0.5, label="Threshold", show_value=True)
model_source = mo.ui.radio(options=["TabICL", "Random Forest"], value="TabICL")
model_view = mo.ui.radio(options=["All errors", "False positives", "False negatives"], value="All errors")
```

Then:

```python
error_table = mo.ui.table(display_errors, label="Select rows to inspect")
error_table
# in a later cell:
selected = error_table.value   # a dataframe of the selected rows
```

How to use `mo.ui.table`:
- Pass a list of dicts or a dataframe.
- `selection="multi"` by default — use `"single"`, `"single-cell"`, `"multi-cell"`, or `None` to change.
- `initial_selection=[0, 2]` pre-selects rows.
- `.value` returns the selected rows in the same format as the input. This is what makes it the *closing widget* of the loop — user selections become Python data again.

The selected rows feed a comparison of feature means vs. the full test set, connecting a model failure back to concrete rows.

---

**The loop in one line:** explore data → change inputs → fit models → inspect errors → test another idea — all without rerunning cells.


---

### 3.2 Interactive Data in Model Development

One of the most useful parts of an interactive notebook is that data exploration does not have to stop when modelling begins. You can inspect rows, edit small samples, explore distributions, and then feed those choices directly into the next modelling step.

This notebook shows that progression in three layers:

- the raw dataframe for a baseline table view
- `mo.ui.data_editor(...)` for editable tabular input
- `mo.ui.data_explorer(...)` and `mo.ui.dataframe(...)` for interactive exploration

Those interfaces are not just for presentation. They support model development by helping you decide what to inspect, what to change, and what to carry into the next step.

The notebook then adds live controls for the modelling workflow:

- `mo.ui.multiselect(...)` for feature selection
- `mo.ui.slider(...)` for modelling sample size
- `mo.ui.slider(...)` for error-table preview size

As those controls change, downstream preprocessing, training, and evaluation update automatically. That keeps the modelling loop continuous instead of forcing a stop-and-rerun workflow.

> **Presenter cues**
>
> - Start by showing the plain dataframe so attendees see the raw dataset first.
> - In `mo.ui.data_editor(...)`, edit one or two values in the small sample and show that downstream output responds immediately.
> - In `mo.ui.data_explorer(...)`, build a quick chart such as `occupation` on the x-axis and `count` on the y-axis, colored by `sex`.
> - In `mo.ui.dataframe(...)`, sort a column such as `workclass`, then clear the sort again.
> - In the feature selector, remove a few columns and show that the selected features feed directly into preprocessing and training.

**Script cue:**  
The important point is continuity. Exploration does not end when modelling begins. The same notebook lets you move straight from inspecting data to changing the model inputs.

---

### 3.3 Visual Feedback for Analysis and Debugging

Interactivity becomes especially valuable when model outputs can immediately drive the next round of analysis. Instead of treating evaluation as a final report, you can use it as a live debugging surface.

In this notebook, two models are trained on the same selected features:

- **TabICL** as the tabular foundation model
- **Random Forest** as the baseline

That comparison is useful because participants can make one change, then immediately inspect how both models respond. The notebook surfaces:

- overall model quality
- differences in predicted probabilities
- plots that reveal model behavior
- error views that connect failures back to concrete rows

The debugging section closes the loop:

- `mo.ui.radio(...)` switches the error view between the two models
- a plot shows where predictions are failing
- `mo.ui.table(...)` exposes misclassified rows
- the selected subset is sent back into Python for further summary and inspection

This creates a much faster cycle of experimentation:

**explore data -> change inputs -> fit models -> inspect errors -> test another idea**

That is why interactivity accelerates discovery. It reduces the friction between an interesting observation and the next concrete test.

> **Presenter cues**
>
> - Lower the modelling sample size if TabICL feels slow during a live session.
> - Switch between TabICL and Random Forest in the debugging view and show how the same data can produce different failure patterns.
> - Select a few misclassified rows and point out that the selected subset becomes live input for the next analysis step.

**Script cue:**  
Visual feedback is not just for display. It helps you decide what to check next, which model behavior matters, and where to intervene.

---

### Closing

Interactivity speeds up AI work because it keeps exploration, modelling, and debugging in one continuous loop. Instead of repeatedly stopping to rerun cells, rewrite plots, or move data into another tool, you can keep the notebook live and let each observation feed the next step.

In this module, the key takeaway is that interactivity is not an extra layer on top of AI development. It changes how quickly you can discover patterns, test ideas, and debug model behavior.

### 3 Takeaways to Remember

1. **Interactivity turns the notebook into one live system.**  
   Data, controls, models, and visualizations can all update together instead of living in separate steps.

2. **Interactive exploration improves model development.**  
   You can inspect data, adjust inputs, and feed those choices directly into modelling without breaking your flow.

3. **Visual feedback speeds up debugging.**  
   When plots, tables, and selections respond immediately, it becomes easier to connect model failures to the next experiment.

### Code to Remember

```bash
marimo edit --sandbox Module_3/module_3.py
```

Use this to open the full interactive workflow in an isolated environment.

```python
selected_features_ui = mo.ui.multiselect(
    options=feature_options,
    value=feature_options,
    label="Features to include in the model",
)
```

Use this to show that user input can directly control modelling choices.

```python
data_explorer = mo.ui.data_explorer(df)
```

Use this to show that visual exploration can become part of the computation instead of staying separate from it.

**Script cue:**  
Interactive notebooks help you explore, model, and debug in one place. That faster feedback loop is what makes discovery happen sooner.
