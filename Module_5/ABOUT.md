# Module 5: From Interactive Work to Reusable Systems

A small LLM evaluation harness, used to show that one marimo notebook can run as a notebook, an app, a CLI script, and an importable module.

## Files

| File | What it is |
|------|------------|
| `sentiment_classifier.py` | The main notebook. Classifies product reviews with two Ollama models side-by-side. |
| `eval_pipeline.py` | A marimo notebook that imports helpers from `sentiment_classifier.py`. |
| `eval_script.py` | A plain Python script that imports the same helpers. |
| `test_classifier.py` | pytest tests against the notebook's helpers (run from outside). |
| `inline_test_demo.py` | A marimo notebook with `test_*` cells that run inline via marimo's built-in pytest support. |


## Quick Reference

| Goal | Command |
|------|---------|
| Edit notebook | `marimo edit sentiment_classifier.py` |
| Run as app | `marimo run sentiment_classifier.py` |
| Share on network | `marimo run sentiment_classifier.py --host 0.0.0.0 --port 8080` |
| Run as script | `python sentiment_classifier.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b --output results.csv` |
| Run a plain script that imports it | `python eval_script.py` |
| Run tests (external) | `pytest test_classifier.py -v -s` (`-v` verbose, `-s` show prints) |
| Run tests (inline) | `marimo edit inline_test_demo.py`. Tests run next to each cell |
| Export HTML | `marimo export html sentiment_classifier.py -o report.html` |
| Export PDF | `marimo export pdf sentiment_classifier.py -o report.pdf` |
| Export WASM | `marimo export html-wasm sentiment_classifier.py -o wasm_output --mode run` |
