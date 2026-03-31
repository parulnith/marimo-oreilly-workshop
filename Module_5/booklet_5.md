## Module 5: From Interactive Work to Reusable Systems

Everything you've built across this course — the reactive notebook, the reproducible environment, the interactive ML pipeline, the AI-assisted workflow — has lived in a single `.py` file. This module shows you how to take that file and do four things with it that are impossible with a traditional Jupyter notebook: run it as a script, serve it as a web app, publish it as a shareable artifact, and import from it as a Python module.

Each section uses `module_5.py` as the working example. By the end of this module, the same file will be running in four different modes — no duplication, no reformatting, no export step.

---

### 5.1 Turning Your Work Into Executable Scripts

#### The concept: one file, two modes

Every marimo notebook is a valid Python program. The `if __name__ == "__main__": app.run()` block at the bottom means you can execute it directly from the command line, just like any other Python script. The reactive graph runs top to bottom, cells execute in dependency order, and outputs print to stdout.

This matters for ML pipelines because it means your interactive exploration and your production pipeline are the same file. You don't maintain a notebook for exploration and a separate script for automation. You have one file that does both.

#### Hands-on: run as a script

**Step 1 — Run the notebook directly:**

```bash
python module_5.py
```

The notebook executes as a plain Python script and prints a small report to stdout.

**Step 2 — Run with arguments:**

```bash
python module_5.py --region North --min-units 70 --output north_report.csv
```

The same file that runs interactively in marimo now also accepts CLI arguments for automation. In this example:

- `--region` filters the data by region
- `--min-units` keeps only rows at or above a threshold
- `--output` saves the filtered table to CSV

**Step 5 — Schedule it.** Because it's a plain Python script, you can run it on a schedule with cron:

```bash
# Run every day at 6am, log output
0 6 * * * python /path/to/module_5.py --region West --min-units 80 >> /logs/daily_run.log 2>&1
```

Or in a GitHub Action:

```yaml
- name: Run notebook as script
  run: python module_5.py --region South --min-units 60
```

> **Docs:** [docs.marimo.io/guides/scripts](https://docs.marimo.io/guides/scripts/) — covers `argparse` and `simple-parsing` integration and scheduled execution patterns.

---

### 5.2 Publishing Flexible, Interactive Data Apps

#### The concept: code hidden, interactivity kept

App mode is the other side of the same file. Run `marimo run` instead of `marimo edit` and the notebook becomes a web app: all code is hidden, only outputs and UI elements are visible. The reactive graph still runs — sliders still update the model, tables still reflect selections — but your collaborator sees a clean interface, not a notebook.

There is no conversion step, no framework to learn, no separate deployment file. The notebook you built is already the app.

#### Hands-on: serve as a web app

**Step 1 — Launch in app mode:**

```bash
marimo run module_5.py
```

Open the URL in your browser. You see the region dropdown, the units slider, the summary block, the interactive table, and the plot — all working reactively. The helper functions and plotting code are hidden, so it behaves like a small data app instead of a notebook.

**Step 2 — Clean up for non-technical users.** Add a Markdown header cell at the top of your notebook (it will appear at the top of the app):

```python
mo.md("""
# Sales Explorer

Use the controls below to filter the data and update the summary,
table, and chart.

**No coding required** — just change the controls and inspect the outputs.
""")
```

**Step 3 — Control layout.** By default, app mode stacks outputs vertically. For a more polished layout, arrange outputs side by side using `mo.hstack`:

```python
mo.hstack([
    mo.vstack([region_ui, min_units_ui]),
    mo.md(f"### Revenue: `${summary['revenue']:,.0f}`")
])
```

**Step 4 — Preview without leaving edit mode.** In the marimo editor, click the **Preview** button (bottom-right) to see exactly what the app looks like without switching modes.

**Step 5 — Share with a teammate.** If you're both on the same network:

```bash
marimo run module_5.py --host 0.0.0.0 --port 8080
```

Your teammate opens `http://your-ip:8080` and gets the full interactive app. No Python, no marimo, no setup required on their end.

> **App layouts:** marimo supports vertical (default), grid (drag-and-drop), and slides layouts. Switch between them in the app preview dropdown. For a presentation-style walkthrough of your results, slides layout lets you step through cells one at a time.

> **Docs:** [docs.marimo.io/guides/apps](https://docs.marimo.io/guides/apps/)

---

### 5.3 From Outputs to Published Artifacts

#### The concept: static snapshots and live previews

Not everyone needs the live app. Sometimes you want to send a link to a static report, embed results in documentation, or publish a notebook that others can view — or fork and run themselves. marimo supports all of these through export and publishing.

#### Hands-on: export and publish

**Step 1 — Export to static HTML.** This captures your current notebook state — code, outputs, plots — as a single self-contained HTML file:

```bash
marimo export html module_5.py -o report.html
```

Open `report.html` in any browser. No Python, no server. Share it as an email attachment, add it to a documentation site, or commit it to a repo. The plots, tables, and Markdown are all there.

To include pre-rendered outputs (so the HTML shows results immediately without running anything):

```bash
marimo export html module_5.py -o report.html --include-outputs
```

**Step 2 — Export to PDF:**

```bash
marimo export pdf module_5.py -o report.pdf
```

**Step 3 — Publish to molab.** Push your notebook to a GitHub repository, then generate a shareable molab preview URL:

```
https://molab.marimo.io/github/<your-username>/<your-repo>/blob/main/module_5.py
```

Anyone with this URL sees a live preview of your notebook. They can fork it into their own molab workspace and run it — with the same sandbox environment, the same inline dependencies — without installing anything. This is the sharing story for research: one URL, fully reproducible.

**Step 4 — Generate a WASM-powered interactive HTML.** This exports your notebook as a self-contained HTML file that runs entirely in the browser via WebAssembly — no server needed, fully interactive:

```bash
marimo export html-wasm module_5.py -o interactive_report.html
```

Open `interactive_report.html`. The sliders work. The model runs. Everything is live — powered by Python compiled to WebAssembly, running in the browser tab. You can host this on GitHub Pages, embed it in a documentation site, or send it directly.

**Step 5 — Publish to GitHub Pages** with a GitHub Action. Create `.github/workflows/publish.yml`:

```yaml
name: Publish notebook to GitHub Pages
on:
  push:
    branches: [main]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install marimo
      - run: marimo export html-wasm module_5.py -o docs/index.html
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs/
      - uses: actions/deploy-pages@v4
```

Every push to `main` rebuilds and republishes your notebook as a live interactive page on `https://<your-username>.github.io/<your-repo>`.

> **Docs:** [docs.marimo.io/guides/exporting](https://docs.marimo.io/guides/exporting/) and [docs.marimo.io/guides/publishing/github](https://docs.marimo.io/guides/publishing/github/)

---

### 5.4 From Interactive Code to Importable Modules

#### The concept: the notebook is the module

In Jupyter, when you want to reuse code from a notebook in another file, your options are: copy-paste, convert to a `.py` script manually, or import the notebook with a hack that executes the entire file. None of these are good.

In marimo, the notebook *is already* a Python module. Because it's stored as a `.py` file with proper function definitions, you can import from it directly — the same way you'd import from any other Python module. No conversion, no copy-paste, no hacks.

The only requirement is the **setup cell**: a special cell that runs before the reactive graph, designed specifically for top-level definitions that should be importable. Functions and classes defined in the setup cell become the notebook's public interface.

#### Hands-on: make your notebook importable

**Step 1 — Identify the reusable logic.** In `module_5.py`, the reusable logic already lives at the top of the file as standard Python functions:

```python
def build_sales_data():
    ...


def filter_sales_data(df, region="All", min_units=0):
    ...


def summarize_sales(df):
    ...
```

**Step 3 — Import from another file.** Create `pipeline.py` in the same directory:

```python
# pipeline.py
from module_5 import build_sales_data, filter_sales_data, summarize_sales

df = build_sales_data()
filtered = filter_sales_data(df, region="North", min_units=70)
summary = summarize_sales(filtered)

print(summary)
```

Run it:

```bash
python pipeline.py
```

The functions from your interactive notebook run in a plain Python script. The notebook is still fully editable and interactive in marimo. There is no duplication — `pipeline.py` imports from the notebook, it doesn't copy from it.

**Step 4 — Test your functions with pytest.** Because the functions are proper Python, you can test them directly:

```python
# test_pipeline.py
from module_5 import build_sales_data, filter_sales_data, summarize_sales


def test_filter_sales_data_region():
    df = build_sales_data()
    filtered = filter_sales_data(df, region="North", min_units=0)
    assert set(filtered["region"]) == {"North"}


def test_summarize_sales_counts_rows():
    df = build_sales_data()
    filtered = filter_sales_data(df, region="All", min_units=80)
    summary = summarize_sales(filtered)
    assert summary["rows"] == len(filtered)
```

```bash
pytest test_pipeline.py -v
```

Your interactive notebook is now part of a tested, importable codebase. This is what "from interactive work to reusable systems" actually means — not a metaphor, but a concrete workflow where the notebook, the pipeline script, and the test suite all point to the same source of truth.

> **Docs:** [docs.marimo.io/guides/reusing_functions](https://docs.marimo.io/guides/reusing_functions/)

---

The four sections of this module represent the four ways a single marimo notebook can be deployed: as a script for automation, as an app for non-technical collaborators, as a published artifact for sharing, and as a module for larger codebases. In every case, the file is the same. The work you did interactively doesn't need to be translated into something else to be useful. It already is something else — it was the whole time.
