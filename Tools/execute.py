"""#Enter module description here.

Created on 2022-08-19

@author: samuel.letellier-duc
"""

import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from tqdm import tqdm

logger = logging.getLogger(__name__)
# use logger instead of print

NOTEBOOK_DIR = os.path.join(os.path.dirname(__file__), "..", "notebooks")
IGNORED_NOTEBOOKS = [
    "Brampton-Parametric.ipynb",
    "1.Sensitivity-Analysis.ipynb",
    "2.Exploring-Results-Debugging.ipynb",
]


def execute_notebook(url, pbar: tqdm):
    """Execute a single notebook."""
    if any(url.name.endswith(n) for n in IGNORED_NOTEBOOKS):
        logger.warning(f"Ignoring notebook: {url}")
        return
    with open(url) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        ep.preprocess(nb, {"metadata": {"path": NOTEBOOK_DIR}})

    # Save the executed notebook
    with open(url, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    pbar.write(f"Completed notebook: {url}")


def run_notebooks():
    """Run all the notebooks in parallel."""
    notebooks = list(Path(NOTEBOOK_DIR).rglob("*.ipynb"))
    with ThreadPoolExecutor() as executor, tqdm(
        total=len(notebooks), desc="Executing notebooks"
    ) as pbar:
        futures = [executor.submit(execute_notebook, url, pbar) for url in notebooks]
        for _ in as_completed(futures):
            pbar.update(1)


if __name__ == "__main__":
    run_notebooks()
