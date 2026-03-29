#### Running marimo everywhere

One of marimo's practical advantages is that a notebook is just a Python file. That means you do not need to convert it into a different format to use it in different settings. The same `.py` notebook can be edited, shared, reviewed, and executed across multiple environments.

You can use a marimo notebook in several ways:

| Environment | How it works |
|---|---|
| **Terminal / Notebook mode** | `marimo edit notebook.py` opens the notebook as an interactive notebook interface. |
| **App mode** | `marimo run notebook.py` serves the notebook as a web app, with code hidden from view. |
| **Sandbox mode** | `marimo edit --sandbox notebook.py` runs the notebook in an isolated environment for cleaner dependency management. |
| **VS Code** | Open the `.py` file directly in VS Code, or use the official [marimo VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) for a more integrated notebook experience. |
| **molab** | [molab.marimo.io](https://molab.marimo.io) lets you use marimo in the cloud without a local installation. |
| **JupyterLab** | marimo notebooks can also be used through the [marimo JupyterLab extension](https://github.com/marimo-team/marimo-jupyter-extension). |
| **Script execution** | `python notebook.py` runs the notebook directly as a Python script. |

The key idea is simple: one notebook, many ways to run it. Because marimo notebooks are stored as plain Python files, they fit naturally into normal development workflows while still supporting interactive notebook use.
