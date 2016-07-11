from pyglet.gl import *
from pyglet.gl.glu import *
from pyglet.window import *
from pyglet.app import *
from pyglet.clock import *
from pyglet.image import *

Width = 640
Height = 480

window = Window(Width, Height)

ESCAPE = '\033'


# rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0

DIRECTION = 1
frame_num = 0

def InitGL():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    gluLookAt(
        0, 6, 12,
        0, 0, 0,
        0, 1, 0
    )
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene(dt):
    global X_AXIS, Y_AXIS, Z_AXIS
    global DIRECTION
    global frame_num

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6.0)

    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)

    # Draw Cube (multiple quads)
    glBegin(GL_QUADS)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glEnd()

    X_AXIS = X_AXIS - 1.0
    Z_AXIS = Z_AXIS - 1.0

    if abs(X_AXIS) < 18.0:
        filename = "b%03d.png" % frame_num
        get_buffer_manager().get_color_buffer().save(filename)
        frame_num += 1

if __name__ == "__main__":
    InitGL()
    schedule(DrawGLScene)

    run()
