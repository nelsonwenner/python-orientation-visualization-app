import serial.tools.list_ports
import serial

class SerialCommands:
  def __init__(self, serial_speed):
    self.baud_rate = serial_speed
    self.serial = None

  @staticmethod
  def get_ports():
    return list(serial.tools.list_ports.comports())

  def connect(self, port):
    self.serial = serial.Serial(port, self.baud_rate)
    self.serial.flushInput()

  def is_connect(self):
    return self.serial.isOpen()

  def get_data(self):
    if not self.serial.isOpen():
      return None
    else:
      return self.serial.readline().decode('utf-8').split(',')

  def disconnect(self):
    if self.serial is None:
      return
    self.serial.close()