"""#Enter module description here.

Created on 2022-08-18

@author: samuel.letellier-duc
"""

import logging
import os
import re

import nbformat

logger = logging.getLogger(__name__)
# use logger instead of print

NOTEBOOK_DIR = os.path.join(os.path.dirname(__file__), "..", "notebooks")

CHAPTERS = {"00": "Preface", "01": "Design Spaces", "02": "archetypal"}

REG = re.compile(r"(\d\d)\.(\d\d)-(.*)\.ipynb")


def iter_notebooks():
    """Iterate over the notebooks."""
    return sorted(nb for nb in os.listdir(NOTEBOOK_DIR) if REG.match(nb))


def get_notebook_title(nb_file):
    """Get the title of the notebook."""
    nb = nbformat.read(os.path.join(NOTEBOOK_DIR, nb_file), as_version=4)
    for cell in nb.cells:
        if cell.source.startswith("#"):
            return cell.source[1:].splitlines()[0].strip()


def gen_contents(directory=None):
    """Generate the contents of the notebooks."""
    for nb in iter_notebooks():
        nb_url = os.path.join(directory, nb) if directory else nb
        chapter, section, title = REG.match(nb).groups()
        title = get_notebook_title(nb)
        if section == "00":
            if chapter in ["00", "06"]:
                yield f"\n### [{title}]({nb_url})"
            else:
                yield f"\n### [{int(chapter)}. {title}]({nb_url})"
        else:
            yield f"- [{title}]({nb_url})"


def print_contents(directory=None):
    """Print the contents of the notebooks."""
    print("\n".join(gen_contents(directory)))


if __name__ == "__main__":
    print_contents()
    print("\n", 70 * "#", "\n")
    print_contents(
        "https://nbviewer.org/github/Elementa-Engineering/DesignAnalytics.Tutorials/tree/main/notebooks/"
    )
