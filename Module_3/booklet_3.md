## Module 3: Why Interactivity Accelerates AI Discovery

Interactivity is most valuable when it turns a notebook into a single live system: data, controls, models, visualizations, and selections all working together and updating automatically.


### Hands-on Exercise (guided in marimo)

Open the prepared notebook:

```bash
marimo edit --sandbox Module_3/module_3.py
```
#### Part 1: Start with the data

Start with the Adult Income dataset itself before moving into visual exploration:

- the plain `df` output for a baseline table view
- `mo.ui.data_editor(df)` for editable tabular input- it is a data editor component for editing tabular data.

Use these to inspect columns, scan values, and show that tabular data can
become part of the computation. The notebook includes a reactive summary below
the editable sample so you can see that edits flow into downstream
output immediately.


#### Part 2: Move into visual exploration

The notebook then introduces marimo's visual exploration tools:

- `mo.ui.data_explorer(df)` for chart-based exploration
- `mo.ui.dataframe(df)` for interactive table inspection

Use these to explore distributions, inspect patterns, and decide what is worth
carrying forward into the modelling step.

Presenter cues:

- For `mo.ui.data_explorer(df)`: build a quick chart with `occupation` on the x-axis, `count` on the y-axis, and color by `sex` so participants can see how the explorer helps surface patterns visually without writing plotting code.
- For `mo.ui.dataframe(df)`: use the `workclass` column as an example. Show attendees how to sort that column and then clear the sort again.

#### Part 3: Control the modeling workflow

The notebook includes live controls such as:

- `mo.ui.multiselect(...)` for feature selection
- `mo.ui.slider(...)` for error-table preview settings

As these controls change, the notebook updates automatically. The selected features feed directly into preprocessing, training, and evaluation without requiring a manual rerun sequence. The notebook uses a standard scikit-learn split with a fixed `test_size=0.2`, `random_state=42`, and `stratify=y`.

Presenter cue:

- Point out that the split is intentionally conventional here: `train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)`. The interactive part is the feature selection and downstream analysis, not the split parameter itself.

#### Part 4: Compare models without breaking flow

The notebook trains:

- **TabICL** as the modern tabular foundation model
- **Random Forest** as a familiar baseline

Participants can change features and train split, then immediately see:

- overall model accuracy
- per-class accuracy
- differences between TabICL and Random Forest in the plots
- how the two models react differently to the same feature choices

This keeps the emphasis on how interactivity changes model development: exploration and experimentation happen in one continuous loop.

#### Part 5: Use visual feedback for debugging

The same notebook then shifts from evaluation to debugging:

- `mo.ui.radio(...)` switches the debugging view between TabICL and Random Forest
- an error plot shows where predictions are failing
- `mo.ui.table(...)` lets participants select misclassified rows
- the selected subset is sent back into Python for further summary and inspection

This creates the full interactive cycle:

**explore data → fit models → inspect errors → make a change → observe the result**

That is the main takeaway of Module 3. Interactivity is not a convenience layer on top of notebook work. It changes the way experimentation happens.



