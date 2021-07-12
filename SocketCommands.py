from websocket_server import WebsocketServer

class SocketCommands:
  def __init__(self, host = '0.0.0.0', port = 8080):
    self.host = host
    self.port = port
    self.server = None
    self.data = None
    self.clients = []

  def connect(self):
    self.server = WebsocketServer(self.port, self.host)
    self.server.set_fn_new_client(self.new_client)
    self.server.set_fn_client_left(self.client_left)
    self.server.set_fn_message_received(self.message_received)
    self.server.serve_forever()

  def new_client(self, client, server):
    current_client = str(client['id'])
    message = '[X] A new client connected of id: {}'.format(current_client)
    self.clients.append(message)

  def client_left(self, client, server):
    current_client = str(client['id'])
    message = '[X] Client disconnected of id: {}'.format(current_client)
    self.clients.append(message)

  def message_received(self, client, server, message):
    self.data = message

  def is_connect(self):
    return self.server is not None

  def get_data(self):
    if not self.data: 
      return None
    else:
      return self.data.split(',')

  def disconnect(self):
    if self.server is None: return
    self.server.server_close()
    self.server = None
    self.data = None
    self.clients = []