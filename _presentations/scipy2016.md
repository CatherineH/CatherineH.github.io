---
author: Catherine Holloway
company: Qubitekk
twitter: femion
title: Resurrecting VPython
layout: bright

permalink: scipy2016.html


style: |
    #CodeSmallArduino h2,  #CodeSmallpyOpenGL h2, #CodeSmallpyOpenGL2 h2,
    #CodeSmallpyOpenGL2 h2, #CodeSmallpyOpenGL3 h2, #CodeSmallpyglet h2,
    #CodeSmallpyglet2 h2, #CodeSmallpyglet3 h2, #CodeSmallpyglet4 h2{
        margin:0px 0 0;
        text-align:center;
        font-size:0px;
        }


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
{: .slide .cover .w }

![](https://raw.githubusercontent.com/CatherineH/pyglet_helper/master/doc/examples/all_objects.gif)


## Outline

1. Drawing options in Python
2. VPython, and why it needed resurrecting
3. Resurrection problems
4. Functionality
5. Conclusion: other resurrections
6. Goofing off


## 3D Drawing Options

1. …Processing + Python

## Processing + Python Code {#CodeSmallArduino}

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

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/processing_animation.gif)
{: .slide .cover .w }


## 3D Drawing Options

1. Processing + Python
2. …PyOpenGL

## pyOpenGL Code

    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *

## pyOpenGL Code  {#CodeSmallpyOpenGL}

    def InitGL(Width, Height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

## pyOpenGL Code {#CodeSmallpyOpenGL2}

    def DrawGLScene():
        global angle
        glLoadIdentity()
        glRotatef(angle, 1.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)
        ...
        glEnd()
        angle += 1

## pyOpenGL Code {#CodeSmall} {#CodeSmallpyOpenGL3}

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(Width, Height)
    glutCreateWindow()
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    InitGL(Width, Height)
    glutMainLoop()

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/pyopenglanimation.gif)
{: .slide .cover .w }


## 3D Drawing Options

1. Processing + Python
2. PyOpenGL
3. …pyglet

## pyglet

    from pyglet.gl import *
    from pyglet import clock, window, image


## pyglet {#CodeSmallpyglet}
    @win.event
    def on_resize(width, height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED

## pyglet {#CodeSmallpyglet2}

    @win.event
    def on_draw():
        global angle
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -6.0)
        glRotatef(angle, 1, 1, 0)
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)
        ...

## pyglet {#CodeSmallpyglet3}

    def update(dt):
        global angle
        angle += 1
    win = window.Window(height=Height, width=Width)

    pyglet.clock.schedule(update)
    clock.set_fps_limit(30)
    pyglet.app.run()

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/pyglet_animation.gif)
{: .slide .cover .w }

## 3D Drawing Options

1. Processing + Python
2. PyOpenGL
3. pyglet
4. …VPython

## VPython code

    from visual import *

    box = box(width=1, height=1, length=1, color=color.red)

    while 1:
        rate(10)
        box.rotate(angle=radians(1), axis=(1, 1, 0))

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/vpython_animation.gif)
{: .slide .cover .w }


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
