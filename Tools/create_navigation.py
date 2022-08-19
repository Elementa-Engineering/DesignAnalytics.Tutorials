"""#Enter module description here.

Created on 2022-08-18

@author: samuel.letellier-duc 
"""

import logging
import sys


import itertools
import os

import nbformat
from generate_contents import NOTEBOOK_DIR, REG, get_notebook_title, iter_notebooks
from ipykernel import kernelspec as ks
from nbformat.v4.nbbase import new_markdown_cell

logger = logging.getLogger(__name__)
# use logger instead of print


def prev_this_next(it):
    a, b, c = itertools.tee(it, 3)
    next(c)
    return zip(itertools.chain([None], a), b, itertools.chain(c, [None]))


PREV_TEMPLATE = "< [{title}]({url}) "
CONTENTS = "| [Contents](Index.ipynb) |"
NEXT_TEMPLATE = " [{title}]({url}) >"
NAV_COMMENT = "<!--NAVIGATION-->\n"

# COLAB_LINK = """
#
# <a href="https://colab.research.google.com/github/jakevdp/PythonDataScienceHandbook
# /blob/master/notebooks/{notebook_filename}"><img align="left"
# src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"
# title="Open and Execute in Google Colaboratory"></a>
# """

COLAB_LINK = """"""


def iter_navbars():
    for prev_nb, nb, next_nb in prev_this_next(iter_notebooks()):
        navbar = NAV_COMMENT
        if prev_nb:
            navbar += PREV_TEMPLATE.format(
                title=get_notebook_title(prev_nb), url=prev_nb
            )
        navbar += CONTENTS
        if next_nb:
            navbar += NEXT_TEMPLATE.format(
                title=get_notebook_title(next_nb), url=next_nb
            )

        navbar += COLAB_LINK.format(notebook_filename=os.path.basename(nb))

        yield os.path.join(NOTEBOOK_DIR, nb), navbar


def write_navbars():
    for nb_name, navbar in iter_navbars():
        nb = nbformat.read(nb_name, as_version=4)
        nb_file = os.path.basename(nb_name)
        is_comment = lambda cell: cell.source.startswith(NAV_COMMENT)

        if is_comment(nb.cells[0]):
            print("- amending navbar for {0}".format(nb_file))
            nb.cells[0].source = navbar
        else:
            print("- inserting navbar for {0}".format(nb_file))
            nb.cells.insert(1, new_markdown_cell(source=navbar))

        if is_comment(nb.cells[-1]):
            nb.cells[-1].source = navbar
        else:
            nb.cells.append(new_markdown_cell(source=navbar))
        nbformat.write(nb, nb_name)


if __name__ == "__main__":
    write_navbars()
