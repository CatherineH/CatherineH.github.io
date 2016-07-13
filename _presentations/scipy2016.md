---
author: Catherine Holloway
company: Qubitekk
twitter: femion
title: 3D drawing in Python Reviving Visual
layout: bright

permalink: scipy2016.html


style: |
    #NoHeaderArduino h2,  #NoHeaderpyOpenGL h2, #NoHeaderpyOpenGL2 h2,
    #NoHeaderpyOpenGL2 h2, #NoHeaderpyOpenGL3 h2, #NoHeaderpyglet h2,
    #NoHeaderpyglet2 h2, #NoHeaderpyglet3 h2, #NoHeaderpyglet4 h2,
    #NoHeaderpythonmultiple h2, #NoHeaderpyOpenGLSmall h2, 
    #NoHeaderphysics h2, #NoHeaderphysics2 h2{
        margin:0px 0 0;
        text-align:center;
        font-size:0px;
        }
            
    .leftcol {
        float: left;
    }
    .rightcol {
        float: right;
    }

    #NoHeaderpyOpenGLSmall code{
        font-size:14px;
    }

    #CodeSmallHeaderiterators h2{
        margin:0px 0 0;
        text-align:center;
        font-size:20px;
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
# 3D drawing in Python: Reviving Visual {#Cover}
{: .slide .cover .w }

Catherine Holloway (@femion, CatherineH)


## ![0](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/College-Freshman.jpg)
{: .slide .cover .w .happyfreshman}


## 3D Drawing Options

1. …Processing + Python

## Processing

 - …created by Ben Fry and Casey Reas in 2001 from the MIT  media lab
 - …integrated language + ide built on Java
 - …targeted at artists and beginners
 - …has a python **mode**


## Processing + Python Code {#NoHeaderArduino}

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

## ![1](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/College-Freshman.jpg)
{: .slide .cover .w }

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/scipy_import_fail.png)
{: .slide .cover .w }

## ![1](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/College-Freshman-sad.jpg)
{: .slide .cover .w }

## 3D Drawing Options

1. Processing + Python
2. …PyOpenGL

## PyOpenGL

![](http://www.pygame.org/shots/443.gif)
PyOpenGL is to OpenGL as PyQt is to Qt

## pyOpenGL Code

    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *

## pyOpenGL Code  {#NoHeaderpyOpenGL}

    def InitGL(Width, Height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, Width / Height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

## pyOpenGL Code {#NoHeaderpyOpenGL2}

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

## pyOpenGL Code 
{: .double #NoHeaderpyOpenGLSmall}

<div class="leftcol"> <pre><code>def DrawGLScene():</code><code>    global angle</code><code>    glLoadIdentity()</code><code>    glRotatef(angle, 1.0, 1.0, 0.0)</code><code>    glBegin(GL_QUADS)</code><code>    </code><code>    glColor3f(1.0, 0.0, 0.0)</code><code>    glVertex3f(1.0, 1.0, -1.0)</code><code>    glVertex3f(-1.0, 1.0, -1.0)</code><code>    glVertex3f(-1.0, 1.0, 1.0)</code><code>    glVertex3f(1.0, 1.0, 1.0)</code><code>    </code><code>    glColor3f(1.0, 0.0, 0.0)</code><code>    glVertex3f(1.0, -1.0, 1.0)</code><code>    glVertex3f(-1.0, -1.0, 1.0)</code><code>    glVertex3f(-1.0, -1.0, -1.0)</code><code>    glVertex3f(1.0, -1.0, -1.0)</code><code> </code><code>    glColor3f(0.0, 1.0, 0.0)</code><code>    glVertex3f(1.0, 1.0, 1.0)</code><code>    glVertex3f(-1.0, 1.0, 1.0)</code><code>    glVertex3f(-1.0, -1.0, 1.0)</code><code>    glVertex3f(1.0, -1.0, 1.0)</code><code> </code></pre> </div>  
<div class="rightcol"><pre><code>    glColor3f(1.0, 1.0, 0.0)</code><code>    glVertex3f(1.0, -1.0, -1.0)</code><code>    glVertex3f(-1.0, -1.0, -1.0)</code><code>    glVertex3f(-1.0, 1.0, -1.0)</code><code>    glVertex3f(1.0, 1.0, -1.0)</code><code> </code><code>    glColor3f(0.0, 0.0, 1.0)</code><code>    glVertex3f(-1.0, 1.0, 1.0)</code><code>    glVertex3f(-1.0, 1.0, -1.0)</code><code>    glVertex3f(-1.0, -1.0, -1.0)</code><code>    glVertex3f(-1.0, -1.0, 1.0)</code><code> </code><code>    glColor3f(1.0, 0.0, 1.0)</code><code>    glVertex3f(1.0, 1.0, -1.0)</code><code>    glVertex3f(1.0, 1.0, 1.0)</code><code>    glVertex3f(1.0, -1.0, 1.0)</code><code>    glVertex3f(1.0, -1.0, -1.0)</code><code> </code><code>    glEnd()</code><code>    angle += 1</code></pre></div>

## pyOpenGL Code {#NoHeaderpyOpenGL3}

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(Width, Height)
    glutCreateWindow()
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    InitGL(Width, Height)
    glutMainLoop()

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/pyopenglanimation.gif)
{: .slide .cover .w }

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/opengl.png)
{: .slide .cover .w }

## ![2](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/College-Freshman-sad.jpg)
{:.slide .cover .w }

## 3D Drawing Options

1. Processing + Python
2. PyOpenGL
3. …pyglet

## pyglet


![](http://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/_static/logo.png)

Also a python OpenGL binding, but simplifies windowing and multimedia

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/pyglet_animation.gif)
{: .slide .cover .w }

## pyglet

    from pyglet.gl import *
    from pyglet import clock, window

## pyglet {#NoHeaderpyglet3}

    def update(dt):
        global angle
        angle += 1
    win = window.Window(height=Height, width=Width)

    pyglet.clock.schedule(update)
    clock.set_fps_limit(30)
    pyglet.app.run()

## ![3](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/College-Freshman.jpg)
{: .slide .cover .w }

## pyglet {#NoHeaderpyglet}
    @win.event
    def on_resize(width, height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, Width / Height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED

## pyglet {#NoHeaderpyglet2}

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


## ![3](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/College-Freshman-sad.jpg)
{: .slide .cover .w }

## 3D Drawing Options

1. Processing + Python
2. PyOpenGL
3. pyglet
4. …VPython


## VPython

 - …Created by **David Scherer** in **2000** to replace **cT**, a simple graphics library
 used in CMU's computational physics classes
 - …Further development led by **Bruce Sherwood**, a developer of **cT**
 - …Developed to aid understanding of physics through computing
 - …C++ calls OpenGL, compiled to a module called cvisual
 - …depends on wxPython and boost

## physics example: projectile motion {#NoHeaderphysics}

    ball = sphere(pos=vector(-10, 0, 0), radius=0.1, 
                  color=color.red, make_trail=True)
    ball.velocity = vector(10, 10, 0)
    time = 0.0; time_final = 2; dt = 0.01; m = 0.15
    while time <= time_final and ball.pos.y > -0.1:
        rate(100)
        f = - m * vector(0, 9.8, 0)
        
        ball.pos += ball.velocity * dt
        ball.velocity += f * dt / m
        time += dt

## physics example: projectile motion with air resistance {#NoHeaderphysics2}

    ball = sphere(pos=vector(-10, 0, 0), radius=0.1, 
                  color=color.red, make_trail=True)
    ball.velocity = vector(10, 10, 0)
    time = 0.0; time_final = 2; dt = 0.01; m = 0.15
    while time <= time_final and ball.pos.y > -0.1:
        rate(100)
        f = - m * vector(0, 9.8, 0) 
             <mark>-0.006 * ball.velocity * ball.velocity.mag</mark>
        ball.pos += ball.velocity * dt
        ball.velocity += f * dt / m
        time += dt

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/projectile.gif)
{: .slide .cover .h }


## VPython code

    from visual import *
    a_box = box(width=1, height=1, length=1, color=color.red)
    while True:
        rate(10)
        a_box.rotate(angle=radians(1), axis=vector(1, 1, 0))

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/vpython_animation.gif)
{: .slide .cover .h }

## ![4](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/College-Freshman.jpg)
{: .slide .cover .w }

## "There is no debian package for wxPython3"
{: .slide .shout .up }

## ![4](https://imgflip.com/s/meme/Engineering-Professor.jpg)
{: .slide .cover .w }

## ![4](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/College-Freshman-sad.jpg)
{: .slide .cover .w }



## Writing simple graphics libraries is hard.
{: .slide .shout .down }

## An OpenGL *Helper*

- …Use the C++ code from VPython as a guide
- …Let a python OpenGL binding do the heavy lifting
- …Obscure the windowing


## PyOpenGL vs. pyglet

|  Feature       | PyOpenGL | pyglet |
+----------------|----------|--------+
|* GLUT         *| yes      | no     |
|* GLext        *| yes      | no (experimental)  |
|* 3.5 support  *| yes (not official)     | no     |

## Why pyglet?

 - Better documentation
 - Extra app, window, sound, image and video libraries

## A Helper for Pyglet

- …Submodule "*objects*" has geometric shape primitives 
- …Submodule "*utils*" has mathematical primitives (vector, vertex, etc) 
- …Let pyglet.gl interact with OpenGL
- …Let pyglet.window and pyglet.app handle display

## Implementation
{: .slide .shout .up }

<!--
## Replacing Iterators {#CodeSmallHeaderiterators}

    std::vector<point_coord> points;
    typedef std::vector<point_coord>::iterator ip;
    for (ip i = points.begin(); i != points.end(); ++i) {
        // render point

Becomes:

    for curr_point in range(0, points.count):
        # render point

-->

## Multiple Method Declarations

    explicit vector( double a = 0.0, double b = 0.0,
                     double c = 0.0) throw()
		: x(a), y(b), z(c) {}
	inline explicit vector( const double* v)
		: x(v[0]), y(v[1]), z(v[2]) {}

## Python version {#NoHeaderpythonmultiple}

    def __init__(self, in_vector=None):
        if in_vector is None:
            self.zero()
        elif len(in_vector) > 2:
            for i in range(len(self)):
                self[i] = in_vector[i]
        else:
            raise ValueError("in_vector must contain "
                             "at least three numbers!")

## PEP
{:.no-numbers}
    box() became Box()
    vector.x became Vector.x_component, or Vector[0]

## How do we make sure API changes don't break everything?
{: .slide .shout .up }

## Use Continuous Integration!

<img src="https://cdn.travis-ci.com/images/logos/Tessa-4-05d037b0d8b10e8b921ac1e24ee10606.svg" alt="Drawing"
style="width: 150px;"/>

- Runs setup.py install for python 2.7 - 3.4
- Runs pylint to check for PEP8
- Runs unit tests

## Continous integration with no display

OpenGL requires a display to draw to, but Travis-CI runs on a headless server!

## Rendering to a still image

- Xdummy appears to require the Nvidia X driver.
- Nvidia X driver does not work on headless systems.
- If you know a solution, let me know!


## Alternative - Mocking GL

    @patch('pyglet_helper.objects.box.<mark>gl</mark>',
           new=pyglet_helper.test.<mark>fake_gl</mark>)
    def test_box_generate_model():
        from pyglet_helper.objects import Box
        box = Box()
        box.generate_model()

## fake_gl module

    def glVertex3f(x_component, y_component, z_component):
        pass



## pyglet_helper Functionality

1. Objects
2. Lights and scenes
4. Default scene

## ![](https://raw.githubusercontent.com/CatherineH/pyglet_helper/master/doc/examples/all_objects.gif)
{: .slide .cover .w }


## Lights and Scenes

 - The *Scene* object contains information on the camera position
 - Lights are non-renderable objects
 - Objects can either be drawn in a scene by passing the scene as an argument, or by
 adding the object to a scene and rendering a scene

## Drawing options

    my_box = Box()
    my_scene = View()
    my_box.render(my_scene)

or 

    my_scene.objects.append(my_box)
    my_scene.setup()    
 
## Default Scene

    from pyglet_helper import *
    <mark>vsetup()</mark>
    box = objects.Box(size=(1, 1, 1), color=util.RED)
    def update(dt):
        box.rotate(angle=radians(1),
                   axis=util.Vector([1, 1, 0]))
    <mark>vrun(update, render_images=True, max_frames=180)</mark>

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/default_scene.gif)
{: .slide .cover .w }

## What about jupyter?
{: .slide .shout .up }

## vpython ecosystem

1. Sherwood and others switched efforts from OpenGL to WebGL
    1. wxPython has no python 3 version
    2. few people familiar with C++ code base
2. GlowScript JavaScript library written in 2012
3. Two python routes to GlowScript

## glowscript.org

1. completely online, no local installs
2. Python-to-JavaScript transpiler provides python interface
3. no access to full scientific Python stack

## vpython-jupyter

1. Originally developed by Coady as ivisual
2. Updated to use GlowScipt Python API and released on PyPI as vpython
3. Runs in Jupyter notebook, typically in a local installation
4. Rendering handled through a custom kernel that calls GlowScript

## ![](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/vjupyter_animation.gif)
{: .slide .cover .h }

## Future Work on pyglet_helper

1. … Rename pyglet_helper to vpython-pyglet?
3. … 3D Text
2. … Make vpython-jupyter  compatible with pyglet_helper

## Thank you!
{: .slide .shout .up }
