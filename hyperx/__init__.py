#  /_/       _  _  ( /
# / / (/ /) (- /  / )
#     / /

"""
HyperX Scripting Library
~~~~~~~~~~~~~~~~~~~~~~~~

The HyperX python package is a library, written in python, for python developers.

Basic usage:

    >>> import hyperx
    >>> with hyperx.Open('mydatabase.hdb3') as hdb:
    >>>     print(f'Active project = {hdb.ActiveProject}')

The HyperX installation folder is found automatically if the installer was run.
Otherwise, the installation folder can be specified by setting the environment
variable `HyperXInstall`

    >>> import os
    >>> os.environ['HyperXInstall'] = 'C:/path/to/hyperx/installation'
    >>> import hyperx
"""

# TODO remove once encapsulated
from .library import _api, _types

from .api import Db
from .utils import Open, OpenWithDefault, WriteCsv
