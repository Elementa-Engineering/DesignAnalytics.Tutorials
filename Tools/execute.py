"""#Enter module description here.

Created on 2022-08-19

@author: samuel.letellier-duc 
"""

import logging
import os
import sys

from path import Path

logger = logging.getLogger(__name__)
# use logger instead of print

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOK_DIR = os.path.join(os.path.dirname(__file__), "..", "notebooks")


def run_notebooks():
    for url in Path(NOTEBOOK_DIR).files("*.ipynb"):
        with open(url) as f:
            nb = nbformat.read(f, as_version=4)
            ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
            ep.preprocess(nb, {"metadata": {"path": "../notebooks/"}})


if __name__ == "__main__":
    run_notebooks()