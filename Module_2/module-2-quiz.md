# Module 2 Quiz

## 1. What marimo feature helps keep a notebook's environment isolated and reproducible?

- A. `--sandbox`
- B. `marimo export`
- C. `git diff`
- D. `mo.ui.slider`

**Answer:** A. `--sandbox`

**Explanation:** `--sandbox` creates an isolated environment for a notebook, which helps keep execution more reproducible across runs.

---

## 2. Why are marimo notebooks usually easier to review in Git than `.ipynb` notebooks?

- A. They are stored as plain Python files
- B. They never contain outputs
- C. They cannot use external libraries
- D. They automatically resolve merge conflicts

**Answer:** A. They are stored as plain Python files

**Explanation:** marimo notebooks are plain `.py` files, so diffs focus on readable code changes instead of large notebook JSON blobs.

---

## 3. Which command opens a marimo notebook as an interactive notebook in the browser?

- A. `marimo edit notebook.py`
- B. `python notebook.py`
- C. `marimo export html notebook.py`
- D. `git status notebook.py`

**Answer:** A. `marimo edit notebook.py`

**Explanation:** `marimo edit notebook.py` opens the notebook editor, where the file runs as an interactive notebook.

---

## 4. What does `marimo run notebook.py` do differently from `marimo edit notebook.py`?

- A. It serves the notebook as an app with code hidden
- B. It converts the notebook into a Jupyter file
- C. It deletes all outputs before running
- D. It disables the notebook's dependencies

**Answer:** A. It serves the notebook as an app with code hidden

**Explanation:** `marimo run` serves the notebook like an app, while `marimo edit` opens the editable notebook interface.

---

## 5. Why does storing a marimo notebook as `.py` help with version control?

- A. Code changes are easier to diff without notebook JSON noise
- B. Git can only track Python files
- C. Python files cannot contain outputs or markdown
- D. It prevents all merge conflicts

**Answer:** A. Code changes are easier to diff without notebook JSON noise

**Explanation:** Because the notebook is plain Python, the diff is centered on code changes instead of notebook metadata and structural wrappers.
