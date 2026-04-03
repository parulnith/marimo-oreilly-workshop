# Module 5: From Interactive Work to Reusable Systems


> **Model defaults:** Model A = `gemma3:1b` · Model B = `qwen2.5:0.5b`
> **Ollama URL:** `http://localhost:11434/v1`
> Before starting: `ollama serve`

---

## Preface

Everything you have built across this workshop including the reactive notebook, the reproducible environment, the interactive ML pipeline, the AI-assisted workflow, all lives in a single `.py` file. 

However, in most AI/ML workflows, there is a gap between exploration and production:
- You explore in a notebook, then rewrite as a script. 
- You build an interactive analysis, then rebuild it as a dashboard. 
- You define useful functions, then copy-paste them into a separate module. 

This module closes that gap. It shows you how to take the same `.py` file you have been working in and do four things with it: run it as a script, serve it as a web app, publish it as a shareable artifact, and import from it as a Python module.

### Example
The working example is an **LLM text classifier** — a notebook that sends texts to two local models via Ollama, compares their sentiment labels, and lets you explore the results. It connects directly to Module 4's setup: you already have Ollama running, you already have models pulled — now you will see that same notebook deployed four different ways.


---

## Presentation: Moving Beyond Private Experimentation

### The problem: ML work dies in notebooks

Most ML work ends where it started — in a notebook on someone's laptop. The LLM evaluation looks good, the model comparison is convincing, the classification results make sense. But then what?

- Your colleague cannot run your classifier without your exact environment
- Your CI pipeline cannot call your scoring functions as part of an automated test
- Your team lead cannot see your results without asking you to re-run it
- Your classification logic is trapped inside notebook cells — you cannot import it into the evaluation harness you are building

The traditional answer is to rewrite. Convert the notebook to a script for automation. Rebuild the analysis as a  app for stakeholders. Copy-paste the useful functions into a separate module. 

### The solution: one file, four modes

marimo notebooks are stored as plain `.py` files. That single fact changes everything, because it means the file you explore in is already a valid Python program. There is no conversion step. The notebook is the script, the app, the artifact, and the module — all at once.

---

## Hands-on Exercise: Four Modes From One File


### 5.1 Turning Your Work Into Executable Scripts
**Scripts** turn your exploration into automation. The notebook where you compared two models becomes the script that classifies a batch of texts nightly. Same prompt, same parsing logic — but now parameterized with CLI arguments for different models. You do not maintain two files.

Take your interactive classifier and run it from the command line. Pass arguments to switch models or save results.

#### How it works

Every marimo notebook is a valid Python program. The `if __name__ == "__main__"` block at the bottom means you can run it directly from the terminal — no UI, no browser.

When Python runs a file directly, `__name__` is `"__main__"`. When it is imported by another script, `__name__` is the module name. So the block only fires when you do `python module_5.py`, not when marimo imports it.

The `--` separator tells Python to stop processing its own flags and pass everything after it to your script:

```bash
python module_5.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b --output results.csv
```

`argparse` then reads `--model-a`, `--model-b`, and `--output` as `args.model_a`, `args.model_b`, `args.output`. The same `classify_text()` function used interactively in the notebook runs here — no duplication.

#### Hands-on

**Step 1 — Run and print results:**

```bash
cd "/Users/parulpandey/Desktop/Marimo Workshop/Module_5"
python module_5.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b
```

This classifies the sample texts using both models and prints each result with label, confidence, and the text.

**Step 2 — Save results to CSV:**

```bash
python module_5.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b --output results.csv
```

Same classifier, same prompt — but now the results are saved to a file. This is what a batch pipeline looks like.

**Step 3 — Schedule with cron.**

Because it is a plain Python script, you can schedule it. Set the time 2 minutes from now to test:

```bash
crontab -e
```

Add this line (adjust `MM HH` to your current time + 2 minutes):

```
39 1 * * * cd "/Users/parulpandey/Desktop/Marimo Workshop/Module_5" && python module_5.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b --output results.csv >> /tmp/classify.log 2>&1
```

Save and exit vim: `Esc` → `:wq` → `Enter`

Check the log after it runs:

```bash
cat /tmp/classify.log
```

Change to `0 20 * * *` for a nightly 8pm run.

> **macOS gotcha:** cron needs Full Disk Access.
> System Settings → Privacy & Security → Full Disk Access → `+` → `/usr/sbin/cron`

Or use a GitHub Action:

```yaml
- name: Run LLM classifier
  run: python module_5.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b --output results.csv
```

---

### 5.2 Publishing Flexible, Interactive Data Apps

**Apps** turn your analysis into a tool for others. The notebook where you built a classifier becomes a dashboard your team can use. They see results, charts, and comparisons. They do not see the prompt engineering or JSON parsing.


#### Hands-on

**Step 1 — Launch app (code hidden, UI only):**

```bash
marimo run module_5.py
```

Open the URL in your browser. You see the model selector, the classify button, the results table, the summary, and the charts — all working reactively. The prompt engineering and JSON parsing are hidden.

**Step 2 — Share on your local network:**

```bash
marimo run module_5.py --host 0.0.0.0 --port 8080
```

Others on the same WiFi open: `http://<your-ip>:8080`

Find your IP:

```bash
ipconfig getifaddr en0
```

Your teammate gets the full interactive classifier. No Python, no marimo, no setup required on their end.

> In the app, click the layout switcher (bottom-right) → **Slides** for a presentation view.


> **App layouts:** marimo supports vertical (default), grid (drag-and-drop), and slides layouts. For a presentation-style walkthrough of your results, slides layout lets you step through one chart at a time.


---

### 5.3 From Outputs to Published Artifacts

**Artifacts** turn your results into shareable documents. The notebook where you compared models becomes an HTML report or an interactive page anyone can view without Python installed.

#### Hands-on

**Step 1 — Static HTML** (share as file, no server needed):

```bash
marimo export html module_5.py -o report.html
open report.html
```

Share as an email attachment, add to a documentation site, or commit to a repo.

**Step 2 — PDF:**

```bash
marimo export pdf module_5.py -o report.pdf
```

**Step 3 — Publish to molab:**

```
https://molab.marimo.io/github/<your-username>/<your-repo>/blob/main/module_5.py
```

Anyone can fork it, connect their own Ollama instance, and run the classifier.

**Step 4 — Interactive WASM** (runs in browser):

```bash
marimo export html-wasm module_5.py -o wasm_output --mode run
cd wasm_output && python -m http.server 8080
```

Open: `http://localhost:8080`

> **⚠️ WASM + Ollama limitation:** WASM cannot reach Ollama (`localhost:11434`) due to browser security. You will see `TypeError: Failed to fetch` — this is expected. WASM export works best for notebooks that do not make external API calls.

> **Fix `layout_file` error during export:** If you see `layouts/module_5.slides.json not found`, open `module_5.py` line 9 and change:
> ```python
> app = marimo.App(width="medium", layout_file="layouts/module_5.slides.json")
> ```
> to:
> ```python
> app = marimo.App(width="medium")
> ```

**Step 5 — Publish to GitHub Pages** with a GitHub Action:

```yaml
name: Publish LLM classifier
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

**Why this matters for AI/ML work:**

Your classification results become a shareable link, not a "can you re-run this and send me a screenshot" conversation. For research, this means reproducible artifacts. For teams, this means results anyone can access without running code.

> **Docs:** [docs.marimo.io/guides/exporting](https://docs.marimo.io/guides/exporting/) and [docs.marimo.io/guides/publishing/github](https://docs.marimo.io/guides/publishing/github/)

---

### 5.4 From Interactive Code to Importable Modules

**Modules** turn your functions into reusable code. The `classify_text()` function you wrote while exploring becomes importable by your evaluation pipeline, your test suite, and your colleague's notebook. One source of truth, not three copies.

#### How it works: setup cells and `@app.function`

For a function to be importable from a marimo notebook, it must:

1. Be defined in a cell by itself
2. Only reference symbols from the **setup cell** or other top-level functions

Under the hood, marimo decorates these with `@app.function`. In the marimo editor, you do not write the decorators manually — marimo adds them when a cell defines a single function that meets the criteria.

To add a setup cell: notebook menu → "Add setup cell." The setup cell is where you put imports and constants that your reusable functions depend on.

> **Key rules:**
> - Functions can only reference symbols from the setup cell or other top-level functions
> - Functions cannot depend on variables from regular cells
> - Cyclic dependencies between functions are not allowed
> - Local variables (names starting with `_`) cannot be made reusable

> **Docs:** [docs.marimo.io/guides/reusing_functions](https://docs.marimo.io/guides/reusing_functions/)

#### Hands-on

**Step 1 — Import into a pipeline script.** Create `eval_pipeline.py` in the `Module_5` folder:

```python
from module_5 import get_client, classify_batch, summarize_results

client = get_client(base_url="http://localhost:11434/v1")

texts = [
    "The new model is significantly faster and more accurate.",
    "Latency increased after the update. Very disappointed.",
    "Works about the same as before. No complaints.",
]

results = classify_batch(client, texts, model="gemma3:1b")
summary = summarize_results(results)

print(results[["model", "text", "label", "confidence"]].to_string(index=False))
print(f"Avg confidence: {summary['avg_confidence']:.0%}")
```

Run it:

```bash
python eval_pipeline.py
```

The classification functions from your interactive notebook run in a plain Python script. The notebook is still fully editable and interactive in marimo. There is no duplication — `eval_pipeline.py` imports from the notebook, it does not copy from it.

**Step 2 — Test with pytest:**

```bash
pytest test_classifier.py -v
```


---

## Key Takeaways

1. **One file, four modes.** The same `.py` file runs as a script, serves as an app, exports as an artifact, and imports as a module. No conversion, no duplication.

2. **Scripts close the exploration-production gap.** Your interactive classifier becomes a parameterized batch pipeline, schedulable with cron or GitHub Actions.

3. **Apps make your work accessible.** Non-technical collaborators classify texts through a button and a dropdown, not code cells.

4. **Artifacts make your results portable.** HTML, PDF, WASM, and molab links let you share classification results without requiring anyone to install Python.

5. **Modules make your code reusable.** Functions defined in your notebook become importable, testable Python — the same code your exploration used and your pipeline calls.

---

## Quick Reference

| Goal | Command |
|------|---------|
| Edit notebook | `marimo edit notebook.py` |
| Run as app | `marimo run notebook.py` |
| Share on network | `marimo run notebook.py --host 0.0.0.0 --port 8080` |
| Export HTML | `marimo export html notebook.py -o report.html` |
| Export PDF | `marimo export pdf notebook.py -o report.pdf` |
| Export WASM | `marimo export html-wasm notebook.py -o output_dir --mode run` |
| Run as script | `python notebook.py -- --arg1 value1 --arg2 value2` |
| Save to CSV | `python notebook.py -- --output results.csv` |
| Import functions | `from notebook import my_function` |

---

