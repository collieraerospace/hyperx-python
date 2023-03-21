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

from .library import ReferenceLibrary
ReferenceLibrary()

from .api import Open
