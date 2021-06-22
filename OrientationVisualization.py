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

  def client_left(self, client, server):
    print("[x] Client(%d) disconnected" % client['id'])
