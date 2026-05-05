# marimo for AI and ML Development
*Enable reactive execution and predictable AI workflows*

*Sponsored by [marimo](https://marimo.io/)*

![Workshop banner](course_img.jpeg)

Workshop materials for the O'Reilly Live course **[marimo for AI and ML Development](https://learning.oreilly.com/live-events/marimo-for-ai-and-ml-development/0642572355555/)**.

The course introduces **marimo**, a next-generation Python programming environment for AI and ML, and shows how to build interactive, reproducible, and reusable workflows that improve on traditional notebook-based development.

## Workshop Modules

### [Module 1: Why Interactive Programming Environments Matter for AI and ML](Module_1/)
This module explores why interactive programming environments are at the very core of modern AI and ML development. We'll look at the shortcomings of traditional notebook systems and discover how modern execution models like marimo help you experiment faster and more reliably.

### [Module 2: Reproducibility as a Baseline for Trustworthy AI](Module_2/)
There's a big difference between just running your code again and reliably getting the same results across different computers and over time. This section will make that distinction clear.

### [Module 3: Why Interactivity Accelerates AI Discovery](Module_3/)
Interactivity is absolutely vital for truly understanding your data and your models in AI development.

### [Module 4: How to Use AI Coding Agents for AI/ML Development](Module_4/)
AI coding agents work best when they're integrated into your environment from the very beginning. This module provides practical advice for using modern AI assistance: when to trust it, what information it needs, and how to choose the best setup for your work.

### [Module 5: From Interactive Work to Reusable Systems](Module_5/)
This module shows you how to move beyond private experimentation and create something that others can easily run, inspect and build upon.

## Setup

marimo can be used **online** through [molab](https://molab.marimo.io), marimo's free cloud-hosted notebook service, or **locally** through the open-source package. molab is the easiest way to follow along — local setup is for those who want to keep working after the workshop.

### Online: molab (no install)

[molab](https://molab.marimo.io/notebooks) is marimo's free cloud-hosted notebook service. It runs entirely in your browser — no Python install, no command line. If you've used Google Colab, the experience is similar.

- **Start fresh:** [marimo.new](https://marimo.new) opens a blank notebook in one click.
- **Preview workshop notebooks from GitHub:** visit [molab.marimo.io/github](https://molab.marimo.io/github) and paste a notebook URL. The preview stays in sync as the notebook changes, and you can fork it into your own workspace.
- **Sharing & export:** molab notebooks are public-by-URL but not discoverable. You can download them as `.py`, `.ipynb`, or PDF.

### Local setup

Clone the repo first:

```bash
git clone <repository-url>
cd "Marimo Workshop"
```

#### Recommended: uv

Install [uv](https://docs.astral.sh/uv/), then install Python:

```bash
uv python install 3.13 --default
```

Run marimo via `uvx` — no virtual environment needed, marimo runs in an isolated environment automatically:

```bash
uvx marimo edit --sandbox Module_1/1_2_marimo_reactive_workflow.py
```

Or open the directory browser:

```bash
uvx marimo edit --sandbox
```

The `--sandbox` flag tells marimo to use the dependencies declared inside each notebook's `# /// script` header, so you don't need to install anything else. This is the cleanest path and is what we use in Module 2.

#### Alternative: pip + virtual environment

If you prefer a traditional setup:

**Mac / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install marimo matplotlib pandas polars
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install marimo matplotlib pandas polars
```

#### VS Code / Cursor

Prefer to stay in your editor? Install the [marimo extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) — works in both VS Code and Cursor.

### First run: the official intro

Before opening the workshop files, take 5 minutes with marimo's built-in tutorial:

```bash
uvx marimo tutorial intro     # or: marimo tutorial intro
```

## How to Run the Notebooks

marimo files are plain Python (`.py`), and the *same file* can run in four modes:

| Mode | Command | When to use |
|------|---------|-------------|
| Edit | `marimo edit Module_1/1_2_marimo_reactive_workflow.py` | The full editor — write and explore |
| App | `marimo run Module_1/1_3_marimo_ui_elements.py` | Run with code hidden, UI only |
| Script | `python Module_1/1_2_marimo_reactive_workflow.py` | Run as plain Python, no notebook |
| Sandbox | `marimo edit --sandbox Module_1/1_2_marimo_reactive_workflow.py` | Isolated env per notebook (Module 2) |

Or open the directory browser:

```bash
marimo edit .
```

The modules are progressive — start with Module 1 and work through them in order. Jupyter notebooks (`.ipynb`) in Modules 1 and 2 are intentionally included as the "before" baseline; the marimo `.py` files alongside them are the "after."

## Prerequisites

- Python 3.10+
- [marimo](https://marimo.io/) (installed via pip or uv as shown above)
- For Module 4: [Ollama](https://ollama.com/) installed locally — see [Module_4/Ollama-Setup.md](Module_4/Ollama-Setup.md)
