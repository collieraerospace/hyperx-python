"""
Utility methods.
"""

from contextlib import contextmanager
import os
import subprocess
import csv
from pathlib import Path
from typing import Any, Generator
import errno

from ..api import Application
from ..library import _api

def Open(hdbPath: os.PathLike) -> Application:
    '''Opens a HyperX database for script access.'''
    hdbPath = os.fspath(hdbPath)
    if not os.path.isabs(hdbPath):
        hdbPath = os.path.abspath(hdbPath)
    
    if not os.path.exists(hdbPath):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), hdbPath)

    _api.Environment.Initialize()
    database = _api.Application()
    database.OpenDatabase(hdbPath)
    return Application(database)


@contextmanager
def OpenManagedDatabase(hdbPath: os.PathLike) -> Generator[Application, None, None]:
    '''Opens a HyperX database for script access in with statement context managers.'''
    app = Open(hdbPath)
    try:
        yield app
    finally:
        app.CloseDatabase()


def OpenWithDefault(filepath: str):
    '''Opens a file in the default application for its file extension.'''
    cmd = f'explorer.exe "{Path(filepath)}"'
    CallExternalProcess(cmd)


def CallExternalProcess(cmd) -> str:
    '''Calls an external process and returns stdout as a string.'''
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout_value = proc.communicate()[0].decode('utf-8').rstrip()

    return stdout_value


def WriteCsv(data: list[list[Any]], headers: list[str], title: str, outputDir: str) -> str:
    '''
    Write tabular data to a csv file.
    Returns the path that the file was written to.
    '''
    filename = ScrubFileName(title) + '.csv'  
    path = Path(outputDir) / filename

    # Excel will lock a file when it is opened but we still need to write out our data
    stem = path.stem
    n = 0
    while True:
        try:
            # Note: newline='' required to not add `\r\r\r`` as newline on windows.
            f = open(path, 'w', newline='')
        except PermissionError:
            n += 1
            path = path.with_stem(f'{stem}_{n}')
            continue
        else:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
            f.close()
            break

    return str(path)


def ScrubFileName(filename: str) -> str:
    '''Removes invalid characters from a windows file name.'''
    filename = filename.strip()
    filename = RemoveCharacters(filename, '\\/:*?"<>|') # ref explorer.exe
    return filename


def RemoveCharacters(s: str, chars: str) -> str:
    '''Removes a set of characters from a string.'''
    for c in chars:
        s = s.replace(c, '')
    return s
