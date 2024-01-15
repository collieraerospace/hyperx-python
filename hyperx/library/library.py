"""
References the HyperX scripting library.
"""

import os
import errno
from pathlib import Path

from .find import AutoDetectInstallFolder


def ReferenceLibrary():
    '''
    Adds references to the C# HyperX scripting library.
    '''
    installFolder = AutoDetectInstallFolder()
    libFolder = Path(installFolder) / 'Executable'

    scriptingDll = libFolder / 'HyperX.Scripting.dll'
    typesDll = libFolder / 'HyperX.Types.dll'
    runtimeConfig = libFolder / 'HyperX.Scripting.runtimeconfig.json'

    if not scriptingDll.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), scriptingDll)
        
    if not typesDll.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), typesDll)
        
    if not runtimeConfig.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), runtimeConfig)

    from clr_loader import get_coreclr
    from pythonnet import set_runtime

    runtime = get_coreclr(runtime_config=str(runtimeConfig))
    set_runtime(runtime)

    import clr

    # Allow importing `HyperX.Scripting`
    # import HyperX.Scripting as hxapi
    clr.AddReference(str(scriptingDll))
    clr.AddReference(str(typesDll))

    # Allow C#-compatible types.
    # from System.Collections.Generic import List
    clr.AddReference('System.Collections')
    
    # Enable dashboard features
    clr.AddReference('System.Security.Cryptography.ProtectedData')
