---
layout: post
title: "Troubleshooting Windows dll imports in Python"
description: "Some obvious stuff for next time"
category: programming
tags: [python, windows, troubleshooting]
---
{% include JB/setup %}

I stumbled over some fairly obvious things when importing a Windows dll in python this
 morning. I'm writing this post to shorten the amount of time I spend reading Stack
 Overflow next time.

The code I will be using for this post is:

```python
from ctypes import cdll
lib = cdll.LoadLibrary("mydll.dll")
```

Are you using the static version of the library instead of the dynamic version?
===============================================================================

ctypes can only import dynamic libraries. If you attempt to load a static library, you
 will get the error:

```
  File "Python35\Lib\ctypes\__init__.py", line 425, in LoadLibrary
    return self._dlltype(name)
  File "Python35\Lib\ctypes\__init__.py", line 347, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: [WinError 193] %1 is not a valid Win32 application
```

Make sure the dynamic *.dll* file is loaded, not the static *.lib* file. If only
static libraries are provided, it might be possible to recompile as a dynamic library,
but I did not try this.

Are you using 32 bit python with a 64 bit library?
==================================================

Using a 64-bit dll with 32 bit python results in the error:

```
   File "Python35\lib\ctypes\__init__.py", line 429, in LoadLibrary
    return self._dlltype(name)
  File "Python35\lib\ctypes\__init__.py", line 351, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: [WinError 193] %1 is not a valid Win32 application
```

To solve this, download the [Windows x86-64](https://www.python.org/downloads) version
 of python, and configure your IDE to use this python interpreter.

Are you using the 32 bit version of ctypes with a 64 bit version of python?
===========================================================================

If you install the 64 bit version of python alongside the 32 bit version, it is likely
 that your environment variables will still be set up to point the PYTHONPATH to the
 32 bit versions of the python libraries.

This will result in the error:

```
   File "example.py", line 1, in <module>
    from ctypes import cdll
  File "Python35\lib\ctypes\__init__.py", line 7, in <module>
    from _ctypes import Union, Structure, Array
ImportError: DLL load failed: %1 is not a valid Win32 application.
```

To fix this, I set the PYTHONPATH in my IDE to be *Python35\Lib\;Python35\libs;
Python35\DLLs*

On Windows, with python > 3.5, it is important to add the DLL folder; the *_ctypes*
module lives in there now.



