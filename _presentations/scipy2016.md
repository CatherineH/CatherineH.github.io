---
author: Catherine Holloway
company: Qubitekk
twitter: femion
title: Resurrecting VPython
layout: bright

permalink: scipy2016.html


style: |

    #Cover h2 {
        margin:30px 0 0;
        color:#FFF;
        text-align:center;
        font-size:70px;
        }
    #Cover p {
        margin:10px 0 0;
        text-align:center;
        color:#FFF;
        font-style:italic;
        font-size:20px;
        }
        #Cover p a {
            color:#FFF;
            }

---
# Resurrecting VPython {#Cover}


![](https://raw.githubusercontent.com/CatherineH/pyglet_helper/master/doc/examples/all_objects.gif)


## Outline

1. Drawing options in Python
2. VPython, and why it needed resurrecting
3. Resurrection problems
4. Functionality
5. Conclusion: other resurrections
6. Goofing off


## Drawing Options

1. …Processing + Python

## Processing + Python

```python
angle = 0
def setup():
    size(640, 480, P3D)
def draw():
    global angle
    clear()
    translate(320, 240)
    rotate(angle, 1, 1, 0)
    fill(255, 0, 0)
    box(100)
    angle += PI/100.0
```

## Drawing Options

1. Processing + Python
2. …pyglet and PyOpenGL

## pyglet and pyOpenGL

## Drawing Options

1. Processing + Python
2. pyglet and PyOpenGL
3. …pyGame
4. …svgwrite

## pyGame

## Drawing Options

1. Processing + Python
2. pyglet and PyOpenGL
3. pyGame
4. …svgwrite

## svgwrite

## VPython, and why it needed resurrecting

1. introduce creators
2. teaching uses
3. implementation

## Resurrection problems

1. converting C++ to python
1.a. inheritance, data types, iterators
1.b. removing indirect links
1.c. multiple declarations
2. Continuous integration with no display
3. to pep or not to pep?

## VPython Functionality

1. objects
2. lights and scenes
3. trails
4. default scene

## Other Resurrections

## Goofing off
