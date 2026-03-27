# Install and Run marimo

This is the simplest way to get ready for the workshop.

## Easiest option: use marimo in the browser

If you do not want to install anything locally, open:

[https://molab.marimo.io](https://molab.marimo.io)

You can also start a fresh notebook directly from:

[https://marimo.new](https://marimo.new)

This opens marimo in the browser using Molab.

## Recommended local setup: install with `pip`

If you want to work locally, this is the easiest option for most participants.

### Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install marimo
marimo tutorial intro
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install marimo
marimo tutorial intro
```

If that works, marimo is installed correctly.

## Clone the workshop repository

Once marimo is installed, clone the workshop repository and move into it.

```bash
git clone https://github.com/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop.git
cd marimo-for-ai-and-ml-development-oreilly-workshop
```

If you want the virtual environment inside the repo folder, you can create and activate it there before installing marimo.

### Mac / Linux

```bash
git clone https://github.com/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop.git
cd marimo-for-ai-and-ml-development-oreilly-workshop
python3 -m venv .venv
source .venv/bin/activate
pip install marimo
```

### Windows PowerShell

```powershell
git clone https://github.com/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop.git
cd marimo-for-ai-and-ml-development-oreilly-workshop
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install marimo
```

## Optional: install with `uv`

`uv` is a faster Python environment and package tool. If you already use it, you can install marimo this way instead.

### Mac / Linux

```bash
uv venv
source .venv/bin/activate
uv pip install marimo
marimo tutorial intro
```

### Windows PowerShell

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install marimo
marimo tutorial intro
```

You may also see `uvx` in the marimo docs. `uvx` is for quickly running a tool without installing it into your project. For this workshop, `pip` or `uv pip install` is easier.

## Open the workshop notebooks

### Edit mode

Use edit mode when you want the full marimo editor:

```bash
marimo edit Module_1/marimo-reactive-workflow.py
```

### App mode

Use app mode when you want to run a notebook with the code hidden:

```bash
marimo run Module_1/marimo-reactive-workflow-with-sliders.py
```

### Script mode

Use script mode when you want to execute a notebook as normal Python:

```bash
python Module_1/marimo-reactive-workflow.py
```

## Sandbox mode

Later in the workshop, we will use sandbox mode for reproducibility:

```bash
marimo edit --sandbox notebook.py
```

This gives a notebook its own isolated environment.

## Workshop files in Module 1

- `jupyter-notebook-failure-modes.ipynb`
- `marimo-reactive-workflow.py`
- `marimo-reactive-workflow-with-sliders.py`

## One thing to remember

In marimo, notebooks are plain Python files ending in `.py`.  
The same file can be:

- edited interactively
- run as an app
- executed as a script
