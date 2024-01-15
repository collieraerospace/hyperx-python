"""
Utilities for finding HyperX files.
"""

from __future__ import annotations
import os
import winreg

def _TryGetEnvInstallFolder() -> str | None:
    '''Looks for the HyperX installation folder in the environment variables.'''
    value = os.environ.get('HyperXInstall', '')
    return value if value != '' else None


def _TryGetRegistryInstallFolder(keyType: int) -> str | None:
    '''
    Attempts to find the HyperX install folder in either the current user
    or local machine registry.
    '''
    try:
        hyperXKey = winreg.OpenKey(keyType, r"SOFTWARE\Collier Aerospace\HyperX", 0, winreg.KEY_READ)
        installFolder, _ = winreg.QueryValueEx(hyperXKey, 'InstallFolder')
    except:
        return None
    else:
        return installFolder


def AutoDetectInstallFolder() -> str:
    '''
    Gets the installation directory of the most recently installed HyperX.
    The order of locations searched is:
     - environment variable
     - current user registry (if installed 'for this user only')
     - local machine registry (if installed 'for all users')
    '''
    folder = _TryGetEnvInstallFolder()
    if folder is None:
        folder = _TryGetRegistryInstallFolder(winreg.HKEY_CURRENT_USER)
    if folder is None:
        folder = _TryGetRegistryInstallFolder(winreg.HKEY_LOCAL_MACHINE)
    if folder is None:
        raise RuntimeError(
            'Cannot find HyperX install directory.'
            ' Try setting the "HyperXInstall" environment variable with'
            ' a path to your HyperX installation directory.')
    return folder
