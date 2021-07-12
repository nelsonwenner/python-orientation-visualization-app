from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GL import * 
import pygame
import math
class OrientationVisualization:

  verticeA = [1.0, 0.2, 1.0]
  verticeB = [-1.0, 0.2, 1.0]
  verticeC = [-1.0, -0.2, 1.0]
  verticeD = [1.0, -0.2, 1.0]
  verticeE = [1.0, 0.2, -1.0]
  verticeF = [-1.0, 0.2, -1.0]
  verticeG = [-1.0, -0.2, -1.0]
  verticeH = [1.0, -0.2, -1.0]

  def start(self, device, app):
    pygame.init()
    flags = OPENGL | DOUBLEBUF
    screen = pygame.display.set_mode((1280, 720), flags)
    pygame.display.set_caption("Orientation Visualization")
    clock = pygame.time.Clock()
    self.screen(1280, 720)
    self.init()

    while True:
      if app.stop_thread_trigger: break
      data = device.get_data()
      self.display(data, app.current_type_data)
      pygame.display.flip()
      clock.tick(50)
    pygame.quit()

  def init(self):
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

  def screen(self, width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
 
  def display(self, data, current_type_data):
    # Clear the image
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Reset previous transforms
    glLoadIdentity()
    # Transform to perspective view
    glTranslatef(0, 0.0, -7.0)

    # Draw
    if current_type_data == '_QUATERNION_':
      w = float(data[0])
      x = float(data[1])
      y = float(data[2])
      z = float(data[3])
      self.draw(w, x, y, z, current_type_data)
    elif current_type_data == '_EULERANGLE_':
      yaw = float(data[0])
      pitch = float(data[1])
      roll = float(data[2])
      self.draw(1, pitch, roll, yaw, current_type_data)

    self.draw_axes()

    # Flush and swap
    glFlush()
    
  def draw(self, w, x, y, z, current_type_data):
  
    if current_type_data == '_QUATERNION_':
      info = "Quaternion w: %.4f, x: %.4f, y: %.4f z: %.4f" %(w, x, y, z)
      self.draw_text((-2.6, -1.8, 2), info, 20)
      # W and the angle of rotation around the axis of the quaternion.
      # Specifies the angle of rotation, in degrees.
      angle = 2 * math.acos(w) * 180.00 / math.pi 
      glRotatef(angle, x, z, y)

    elif current_type_data == '_EULERANGLE_':
      yaw, pitch, roll = x, y, z
      info = "Angle Euler Pitch: %f, Roll: %f, Yaw: %f" %(pitch, roll, yaw)
      self.draw_text((-2.6, -1.8, 2), info, 20)
      glRotatef(-roll, 0.00, 0.00, 1.00)
      glRotatef(pitch, 1.00, 0.00, 0.00)
      glRotatef(yaw, 0.00, 1.00, 0.00)

    glBegin(GL_QUADS)

    # FRONT: ABCD - GREEN
    glColor3f(0.0, 1.0, 0.0)
    glVertex3fv(self.verticeA)
    glVertex3fv(self.verticeB)
    glVertex3fv(self.verticeC)
    glVertex3fv(self.verticeD)

    # BACK: FEHG - GREEN
    glColor3f(0.0, 1.0, 0.0)
    glVertex3fv(self.verticeF)
    glVertex3fv(self.verticeE)
    glVertex3fv(self.verticeH)
    glVertex3fv(self.verticeG)

    # RIGHT: EADH - RED
    glColor3f(1.0, 0.0, 0.0)
    glVertex3fv(self.verticeE)
    glVertex3fv(self.verticeA)
    glVertex3fv(self.verticeD)
    glVertex3fv(self.verticeH)

    # LEFT: BFGC - RED
    glColor3f(1.0, 0.0, 0.0)
    glVertex3fv(self.verticeB)
    glVertex3fv(self.verticeF)
    glVertex3fv(self.verticeG)
    glVertex3fv(self.verticeC)

    # TOP: EFBA - BLUE
    glColor3f(0.0, 0.0, 1.0)
    glVertex3fv(self.verticeE)
    glVertex3fv(self.verticeF)
    glVertex3fv(self.verticeB)
    glVertex3fv(self.verticeA)

    # BOTTOM: DCGH - BLUE
    glColor3f(0.0, 0.0, 1.0)
    glVertex3fv(self.verticeD)
    glVertex3fv(self.verticeC)
    glVertex3fv(self.verticeG)
    glVertex3fv(self.verticeH)

    glEnd()

  def draw_axes(self, len = 2.0):
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(4.0)

    glBegin(GL_LINE_LOOP)
    glVertex3d(0, 0, 0)
    glVertex3d(len, 0, 0)
    glVertex3d(0, 0, 0)
    glVertex3d(0, len, 0)
    glVertex3d(0, 0, 0)
    glVertex3d(0, 0, len)
    glEnd()

    glVertex3d(len, 0, 0)
    self.draw_text((len, 0, 0), "X", 20)
    glVertex3d(0, len, 0)
    self.draw_text((0, len, 0), "Y", 20)
    glVertex3d(0, 0, len)
    self.draw_text((0, 0, len), "Z", 20)

  def draw_text(self, position, text, size):
    font = pygame.font.SysFont("Courier", size, True)
    textSurface = font.render(text, True, 
    (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), 
      GL_RGBA, GL_UNSIGNED_BYTE, textData
    )