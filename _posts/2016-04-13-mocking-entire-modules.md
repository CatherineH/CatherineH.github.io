---
layout: post
title: "Mocking Entire Modules"
description: "or Mock-ception"
category: programming
tags: [python, testing]
---
{% include JB/setup %}

I'm increasing the code coverage on my [pyglet_helper](https://github.com/CatherineH/pyglet_helper)
project prior to adding new functionality.
As of right now it is:


[![Coverage Status](https://coveralls.io/repos/github/CatherineH/pyglet_helper/badge.svg?branch=master)](https://coveralls.io/github/CatherineH/pyglet_helper?branch=master)

If this is green, I have succeeded in my task. Go me!

Before I got this spiffy number, I had to tackle an issue: pyglet_helper project is built on top of OpenGL, but OpenGL needs a display to draw to. The continuous integration system I am using (Travis) does not
have a display.

After embarking on a fool's errand to get [Xdummy](http://xpra
.org/trac/wiki/Xdummy) working in a docker container, my friend [Steven](http://scasagrande.github.io/) pointed to an easier solution: simply create
 a fakeGL module and then run the tests using that instead of OpenGL. This
 is not an ideal solution, as my unit tests will only check to make sure
 that the math is correct, and not that things are being drawn to the screen
  without glitching, but at the moment I'm okay with that. I'm not trying to
   test the functionality of OpenGL; I want to test that my math and the
   inheritance of the objects in pyglet_helper works out. My own math
   mistakes, and not OpenGL, are responsible for 99% of the weird visual
   glitches in pyglet_helper.

This post details how to replace an entire module in python unit tests,
since I didn't find it in my initial reading of the mock documentation.

As an example, suppose we have some math to be tested on a 
Windows AMD machine[^1]. Thus, we would like to mock out numpy.

The function to be tested is in the file **one_deep.py**:

```python
import numpy

def sum_array(lower, upper):
    return sum(numpy.arange(lower, upper))
```

This module uses the arange function in numpy, so the file **fake_numpy.py**
 contains the code:

```python
def arange(lower, upper):
    return range(lower, upper)
```

Essentially, the range is now a list instead of a numpy array.

The unit test, which replaces **numpy** with **fake_numpy** is:

```python
from mock import patch
import fake_numpy


@patch('one_deep.numpy', new=fake_numpy)
def test_sum_to_hundred():
    from one_deep import sum_array
    result = sum_array(4, 16)
    assert result == 114
```

Now, suppose we need to go deeper. A second function is in the file
**two_deep.py**:

```python
from one_deep import sum_array
import numpy


def sum_array_again(lower, upper):
    return sum(numpy.arange(lower, sum_array(lower, upper)))
```

In our unit tests, if only **two_deep** is patched, when **sum_array** is
called, it will still use **numpy.arange** instead of **fake_numpy.arange**.
 This can produce some interesting errors if **numpy** is expecting to
 operate on **numpy** types.

Thus, the module must be patched all the way down:

```python
from mock import patch
import fake_numpy


@patch('one_deep.numpy', new=fake_numpy)
@patch('two_deep.numpy', new=fake_numpy)
def test_sum_to_hundred():
    from two_deep import sum_array_again
    result = sum_array_again(4, 16)
    assert result == 6435
```

Unfortunately, I haven't figured out a good way of making sure that numpy
gets patched all in every place where it is invoked yet, leading to a lot of
 failed Travis builds as I encover another layer of a pyglet_helper object's
  dependencies which rely on OpenGL.

[^1]: Numpy does not support Windows running on AMD chips, as I recently learned. 
