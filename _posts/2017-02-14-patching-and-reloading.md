---
layout: post
title: "Patching and Reloading"
description: "Always reload patched modules"
category: programming
tags: [python, testing, nose, mock, importlib]
---
{% include JB/setup %}

Modules that are patched with *mock*'s *patch* decorator must be re-imported. This is a simple thing but I wasted a couple of hours this morning on it, so I'm documenting this for future reference.

Suppose you have two files:

**parent.py**

```python
class MyParent(object):
    parent_name = "me"
```

**child.py:**

```python
from parent import MyParent


class MyChild(MyParent):
    pass
```

And you would like to run some tests, one where the **MyParent** object is patched, and one where it is not. If you use this code for your tests:

```python
from mock import patch


class MockParent(object):
    parent_name = "someone else"


def test_child():
    import child
    assert child.MyChild().parent_name == "me"


@patch("parent.MyParent", new=MockParent)
def test_mock():
    import child
    assert child.MyChild().parent_name == "someone else"
```

If you run these tests, only one test will work, depending on the order. I had assumed that imports were local to the scope of the function, but it appears that they aren't. They aren't even local to the file - if you split these tests up, only one will work, and it will be the one in the alphabetically first named file.

To run the tests as expected, you will need to re-import the child module. First, in order for this to work with both python2 and python3, import either **imp** or **importlib**

```python
if sys.version_info >= (3, 0):
    import importlib
else:
    import imp as importlib
```

Then, after patching your code, re-import the patched library:

```python
@patch("parent.MyParent", new=MockParent)
def test_mock():
    import child
    importlib.reload(child)
    assert child.MyChild().parent_name == "someone else"
```

