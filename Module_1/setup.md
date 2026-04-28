# Install and Run marimo

This is the simplest way to get ready for the workshop.

## Easiest option: use marimo in the browser

If you do not want to install anything locally, open:

[https://molab.marimo.io](https://molab.marimo.io)

You can also start a fresh notebook directly from:

[https://marimo.new](https://marimo.new)

This opens marimo in the browser using Molab.

## Local setup

If you want to work locally, start by cloning the workshop repository and creating the virtual environment inside it.

## Clone the workshop repository

```bash
git clone https://github.com/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop.git
cd marimo-for-ai-and-ml-development-oreilly-workshop
```

## Install marimo with `pip`

This is the easiest local option for most participants.

### Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install marimo matplotlib pandas polars
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install marimo matplotlib pandas polars
```

If that works, marimo and the packages used in Module 1 are installed correctly.

Before opening the workshop files, start with the official intro notebook:

```bash
marimo tutorial intro
```

This is a good way to quickly see the main parts of the marimo interface before moving into the course materials.

## Optional: install with `uv`

`uv` is a faster Python environment and package tool. If you already use it, you can install marimo this way instead.

### Mac / Linux

```bash
uv venv
source .venv/bin/activate
uv pip install marimo matplotlib pandas polars
marimo tutorial intro
```

### Windows PowerShell

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install marimo matplotlib pandas polars
marimo tutorial intro
```

You may also see `uvx` in the marimo docs. `uvx` is for quickly running a tool without installing it into your project. For this workshop, `pip` or `uv pip install` is easier.

## Open the workshop notebooks

### Edit mode

Use edit mode when you want the full marimo editor:

```bash
marimo edit Module_1/1_2_marimo_reactive_workflow.py
```

### App mode

Use app mode when you want to run a notebook with the code hidden:

```bash
marimo run Module_1/1_3_marimo_ui_elements.py
```

### Script mode

Use script mode when you want to execute a notebook as normal Python:

```bash
python Module_1/1_2_marimo_reactive_workflow.py
```

### Sandbox mode

Later in the workshop, we will use sandbox mode for reproducibility:

```bash
marimo edit --sandbox Module_1/1_2_marimo_reactive_workflow.py
```

This gives a notebook its own isolated environment.
