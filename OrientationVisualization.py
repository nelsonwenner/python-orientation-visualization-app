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
