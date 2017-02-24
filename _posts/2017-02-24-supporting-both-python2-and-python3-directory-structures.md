---
layout: post
title: "Supporting both Python2 and Python3 directory Structures"
description: "A hacky solution to a common problem"
category: programming
tags: [python]
---
{% include JB/setup %}

Consider a python project with the directory structure:

```
├── inone
│   └── myfuncs.py
└── test.py
```

where **myfuncs.py** is:

```python
def hello_world():
    print("hello world")
```

and **test.py** is:

```python
from inone.myfuncs import hello_world

hello_world()
```

Running test.py with python 3.+ works as expected, but running in python 2 results in the error:

```
$ python2 test.py 
Traceback (most recent call last):
  File "test.py", line 1, in <module>
    from inone.myfuncs import hello_world
ImportError: No module named inone.myfuncs
```

The solution is to add the file **__init__.py** to the **inone** directory with the code:

```python
import myfuncs
```

However, this causes the error when running with python 3.+:

```python
$ python3 test.py 
Traceback (most recent call last):
  File "test.py", line 1, in <module>
    from inone.myfuncs import hello_world
  File "/home/catherine/python_projects/import_test/inone/__init__.py", line 1, in <module>
    import myfuncs
ImportError: No module named 'myfuncs'
```

The proposed solutions to this on the [Stack Overflow question](http://stackoverflow.com/questions/23952074/import-structure-that-works-both-in-packages-and-out-in-both-python-2-and-3) are unsatisfactory; they are either to add this compatibility to the setup script, which is useless for running code in the directory, or using importlib or appending to the PYTHONPATH, which seems unnecessarily complicated.

My own solution is to simply check for python3 in **__init__.py**:

```python
import sys
if sys.version_info[0] < 3:
    import myfuncs
```

Of course, this is also a bit hacky and annoying, because these two lines need to be added to each directory's **__init__.py**. Are there any better solutions out there?


