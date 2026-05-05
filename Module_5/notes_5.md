# Module 5: From Interactive Work to Reusable Systems


### 5.1 Turning Your Work Into Executable Scripts

Every marimo notebook is a valid Python program. The `if __name__ == "__main__"` block at the bottom means you can run it directly from the terminal — no UI, no browser.


**Step 1 — Run and print results:**

```bash
cd "/Users/parulpandey/Desktop/Marimo Workshop/Module_5"
python sentiment_classifier.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b
```

**Step 2 — Save results to CSV:**

```bash
python sentiment_classifier.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b --output results.csv
```


### 5.2 Publishing Flexible, Interactive Data Apps


**Step 1 — Launch app (code hidden, UI only):**

```bash
marimo run sentiment_classifier.py
```

**Step 2 — Share on your local network:**

```bash
marimo run sentiment_classifier.py --host 0.0.0.0 --port 8080
```

Others on the same WiFi open: `http://<your-ip>:8080`

Find your IP:

```bash
ipconfig getifaddr en0
```
> In the app, click the layout switcher (bottom-right) → **Slides** for a presentation view.


> **App layouts:** marimo supports vertical (default), grid (drag-and-drop), and slides layouts. For a presentation-style walkthrough of your results, slides layout lets you step through one chart at a time.


### 5.3 From Outputs to Published Artifacts

**Artifacts** turn your results into shareable documents. The notebook where you compared models becomes an HTML report or an interactive page anyone can view without Python installed.

#### Hands-on

**Step 1 — Static HTML** (share as file, no server needed):

```bash
marimo export html sentiment_classifier.py -o report.html
open report.html
```

Share as an email attachment, add to a documentation site, or commit to a repo.

**Step 2 — PDF:**

```bash
marimo export pdf sentiment_classifier.py -o report.pdf
```

**Step 3 — Publish to molab:**

```
https://molab.marimo.io/github/<your-username>/<your-repo>/blob/main/sentiment_classifier.py
```

Anyone can fork it, connect their own Ollama instance, and run the classifier.

**Step 4 — Interactive WASM** (runs in browser):

```bash
marimo export html-wasm sentiment_classifier.py -o wasm_output --mode run
cd wasm_output && python -m http.server 8080
```

Open: `http://localhost:8080`

> **⚠️ WASM + Ollama limitation:** WASM cannot reach Ollama (`localhost:11434`) due to browser security. You will see `TypeError: Failed to fetch` — this is expected. WASM export works best for notebooks that do not make external API calls.

> **Fix `layout_file` error during export:** If you see `layouts/sentiment_classifier.slides.json not found`, open `sentiment_classifier.py` line 9 and change:
> ```python
> app = marimo.App(width="medium", layout_file="layouts/sentiment_classifier.slides.json")
> ```
> to:
> ```python
> app = marimo.App(width="medium")
> ```

---

### 5.4 From Interactive Code to Importable Modules

**Modules** turn your functions into reusable code. The `classify_text()` function you wrote while exploring becomes importable by your evaluation pipeline, your test suite, and your colleague's notebook.

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

**Step 1 — Import into a pipeline script.** Create `5_3_eval_pipeline.py` in the `Module_5` folder:

**Step 2 — Test with pytest:**

```bash
pytest test_classifier.py -v -s   # -v verbose, -s show prints
```

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

