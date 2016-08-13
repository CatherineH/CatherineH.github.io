import pyglet
from pyglet.gl import *
from pyglet import clock, window


def vector(type, *args):
    '''
        return a ctype array
        GLfloat
        GLuint
        ...
    '''
    return (type*len(args))(*args)

angle = 0

def update(dt):
    global angle
    angle += 1
    angle %= 360
    print(angle)
    draw()

def draw():
    global angle
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glRotatef(angle, 1, 1, 0)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

    glColorPointer(3, GL_FLOAT, 0, vector(GLfloat, *color))
    glVertexPointer(3, GL_FLOAT, 0, vector(GLfloat, *cube))
    glDrawElements(GL_QUADS, len(indicies), GL_UNSIGNED_INT, vector( GLuint,
        *indicies))

    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)




def setup():
    # look for GL_DEPTH_BUFFER_BIT
    glEnable(GL_DEPTH_TEST)



win = window.Window(fullscreen=False, vsync=True, resizable=True, height=480,
                    width=640)

cube = (
    1, 1, 1, #0
    -1, 1, 1, #1
    -1, -1, 1, #2
    1, -1, 1, #3
    1, 1, -1, #4
    -1, 1, -1, #5
    -1, -1, -1, #6
    1, -1, -1 #7
)


color = (
    1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0
)

indicies = (
    0, 1, 2, 3, # front face
    0, 4, 5, 1, # top face
    4, 0, 3, 7, # right face
    1, 5, 6, 2, # left face
    3, 2, 6, 7, # bottom face
    4, 7, 6, 5  #back face
)


@win.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10, 10, -10, 10, -10, 10)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

@win.event
def on_draw():
    glClearColor(0.2, 0.2, 0.2, 0.8)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw()


pyglet.clock.schedule(update)
clock.set_fps_limit(30)
setup()
pyglet.app.run()