## Module 3: Why Interactivity Accelerates AI Discovery

This notebook uses that idea for an end-to-end AI workflow. It starts with data inspection, moves into visual exploration, connects those choices to model training, and then uses model errors as the next input for analysis.

> 💡 **Try it — `Module_3/3_1_interactive_ml_workflow.py`**

>
> From the repo root, open the notebook in sandbox mode:
>
> ```bash
> marimo edit --sandbox Module_3/3_1_interactive_ml_workflow.py
> ```
>


#### What we'll do in the notebook

We'll walk through one end-to-end AI workflow on the **Adult Income** dataset — a classic tabular benchmark from the US Census where the task is to predict whether a person earns more than $50K per year. It's a binary classification problem with a mix of numeric (age, hours-per-week, capital gains) and categorical (occupation, education, marital status) features.


Here's the path we'll take:

1. **Look at the data** — first as a raw dataframe, then as an editable sample.
2. **Explore it visually** — drag columns into a chart, then sort and filter a table.
3. **Pick features and sample size** — using widgets that drive the rest of the pipeline.
4. **Fit and compare two models** — TabICL and Random Forest, side by side.
5. **Debug errors interactively** — move a threshold, inspect misclassified rows

Each stage introduces a marimo widget. 
---

**1. Data — inspecting and editing**

1. The raw dataframe is shown first as a baseline view (just put `df` as the last expression in a cell — marimo renders it as an interactive table). marimo lets you page through, search, sort, and filter dataframes, making it extremely easy to get a feel for your data. You can also export the selection and freeze etc.

2.  **`mo.ui.data_editor(...)`** for editable tabular input:


- Click any cell to edit it directly in the table.
- Access the edited data in a *different* cell via `editor.value` — it comes back in the same format you passed in.
- Use `editable_columns=[...]` to restrict which columns are editable.
- Good for small what-if experiments; it is intentionally limited and not meant for bulk editing.


---

**2. Visualization — exploring distributions and relationships**

**`mo.ui.data_explorer(df)`** — chart-first, drag-and-drop exploration:


How to use it:
- Drag columns into encoding slots: x, y, color, size, shape, row, column.
- Build up a plot incrementally — marimo suggests follow-up charts based on the current config.
- `.value` returns a dict with the current chart spec (useful if you want to persist it).
- Use this *before* you know what you want to plot.

> - In `mo.ui.data_explorer(...)`, build a quick chart such as `occupation` on the x-axis and `count` on the y-axis, colored by `sex`.

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

> - In `mo.ui.dataframe(...)`, try grouping by `age` and aggregating `education-num`, `capital-gain`, and `hours-per-week`.




---

**3. Modeling controls — driving the pipeline with widgets**


How to use these:
- Define the widget in one cell, display it, then read `.value` in a *different* cell. Reading `.value` in the same cell that defines the widget will not work.
- Any downstream cell that reads `selected_features_ui.value` re-runs automatically whenever the user changes the multiselect. No callbacks needed.


> **Presenter cues**
>
> - In the feature selector, remove a few columns and show that the selected features feed directly into preprocessing and training.
> - Lower the modelling sample size if TabICL feels slow during a live session.

---

**4. Model comparison — two models on the same live inputs**

We fit two very different models on the same `X_train`, `y_train`:

- **TabICL** — a *tabular foundation model*. Like large language models pre-trained on text, TabICL is pre-trained on many synthetic tabular datasets, so it can make predictions on a new table through in-context learning without traditional gradient-based training on your data. Think of it as "GPT for tables." Fast to use, no hyperparameter tuning, strong out-of-the-box performance on small/medium tabular tasks. [Docs](https://github.com/soda-inria/tabicl).
- **Random Forest** — the classic baseline. An ensemble of decision trees where each tree sees a random subset of rows and features, and predictions are averaged. Reliable, interpretable, and a reasonable reference point for any tabular problem.

We compare them two ways:

- **ROC AUC** (Receiver Operating Characteristic – Area Under the Curve). A single number between 0 and 1 that measures how well the model *ranks* positive cases above negative ones, across every possible classification threshold. 1.0 is perfect, 0.5 is random guessing. Unlike accuracy, it doesn't get fooled by class imbalance — which matters here because most people in the dataset earn ≤ 50K.
- **Predicted-probability histograms** split by the actual income label. Each chart shows the probabilities a model assigns to "income > 50K." Ideally, rows that really are `>50K` should appear more on the right side of the chart, and rows that are `≤50K` should appear more on the left. If the two groups overlap a lot, the model is unsure and will make more mistakes.




> **Presenter cue**
>
> - Change one feature or sample-size control, then show how both model outputs update from the same live inputs.

---

**5. Error analysis — `mo.ui.table` closes the loop**

A classifier first produces a *probability* for each row, such as "73% chance this person earns >50K." The notebook uses a **classification threshold** slider to turn that probability into a yes/no prediction. At the default threshold of 0.5, a row with probability 0.73 is predicted as `>50K`; a row with probability 0.32 is predicted as `≤50K`.

In the notebook, the error-analysis controls do three things:

- **Model to inspect** switches between TabICL and Random Forest.
- **Classification threshold** changes how strict the model is before predicting `>50K`.
- **Error type to inspect** filters the table to all errors, false positives, or false negatives.

The summary table updates immediately and shows the number of correct predictions, total errors, false positives, and false negatives. The row table below it previews the misclassified examples with columns such as `age`, `education-num`, `hours-per-week`, `capital-gain`, `proba_positive`, `income_label`, and `predicted`.

The two error types mean:

- **False positives** — model said > 50K, actual label was ≤ 50K.
- **False negatives** — model said ≤ 50K, actual label was > 50K.

This makes the model behavior easier to explain: move the threshold, watch the error counts change, then inspect the actual rows behind those mistakes.
