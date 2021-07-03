from websocket_server import WebsocketServer
from threading import Thread
from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GL import *
import pygame
import json
import math
import sys

class OrientationVisualization:

  HOST = '0.0.0.0'
  PORT = 8080

  data = [0.0, 0.0, 0.0, 0.0]

  verticeA = [1.0, 0.2, 1.0]
  verticeB = [-1.0, 0.2, 1.0]
  verticeC = [-1.0, -0.2, 1.0]
  verticeD = [1.0, -0.2, 1.0]
  verticeE = [1.0, 0.2, -1.0]
  verticeF = [-1.0, 0.2, -1.0]
  verticeG = [-1.0, -0.2, -1.0]
  verticeH = [1.0, -0.2, -1.0]

  def __init__(self, useSerial, useQuat):
    self.useSerial = useSerial
    self.useQuat = useQuat
    if self.useSerial:
      import serial
      self.serial = serial.Serial('/dev/ttyUSB0', 38400)
    else:
      self.thread_socket_server()
  def thread_socket_server(self):
    server = WebsocketServer(self.PORT, self.HOST)
    server.set_fn_new_client(self.new_client)
    server.set_fn_client_left(self.client_left)
    server.set_fn_message_received(self.message_received)
    threadSocketServer = Thread(target=server.run_forever, daemon=True)
    threadSocketServer.start()
    print('[x] Running Thread WebSocket: ', threadSocketServer.getName())
    print('[x] Server started with successfully!')
  def new_client(self, client, server):
    print("[x] New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")
  def client_left(self, client, server):
    print("[x] Client(%d) disconnected" % client['id'])

  def message_received(self, client, server, message):
    data_serialized = json.loads(message)
    if self.useQuat:
      [w, x, y, z] = data_serialized
      self.data = [w, x, y, z]
    else:
      [pitch, roll, yaw] = data_serialized
      self.data = [pitch, roll, yaw]

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
  def draw(self, w, x, y, z):
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
