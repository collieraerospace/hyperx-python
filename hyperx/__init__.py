#  /_/       _  _  ( /
# / / (/ /) (- /  / )
#     / /

"""
HyperX Scripting Library
~~~~~~~~~~~~~~~~~~~~~~~~

The HyperX python package is a library, written in python, for python developers.

Basic usage:

    >>> import hyperx
    >>> with hyperx.open('mydatabase.hdb3') as hdb:
    >>>     print(f'Active project = {hdb.ActiveProject}')
"""

from .api import Open

from .library import SetLibrary

# TODO remove this once everything is wrapped.
from .library import ReferenceLibrary