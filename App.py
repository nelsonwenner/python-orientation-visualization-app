from OrientationVisualization import OrientationVisualization
from SerialCommands import SerialCommands
from SocketCommands import SocketCommands
import PySimpleGUI as sg
import threading

class App:

  header_font = ('Courier', 14, 'bold')
  large_font = ('Courier', 12)
  medium_font = ('Courier', 10)
  small_font = ('Courier', 8)

  sg.SetOptions(
    background_color='#2C2C2C',
    text_element_background_color='#2C2C2C',
    element_background_color='#2C2C2C',
    scrollbar_color=None,
    input_elements_background_color='#FAFAFA',
    progress_meter_color=('#32D957', '#EEEEEE'),
    button_color=('#FAFAFA', '#222222')
  )

  layout = [
    [
      sg.Text('Orientation Visualization', justification='center', 
      pad=((28, 0), (10, 15)), font=header_font)
    ],
    [
      sg.Checkbox('Wifi', key='_WIFI_', change_submits=True, 
      font=large_font, pad=((72, 5), (0, 0))), 
      sg.VerticalSeparator(), 
      sg.Checkbox('Serial', key='_SERIAL_', change_submits=True,
      default=True, font=large_font, pad=((0, 0), (0, 0)))
    ],
    [
      sg.Text('Select your serial port', pad=((68, 0), (20, 10)), 
      key='_DEVICE_TITLE_', font=medium_font)
    ],
    [
      sg.Listbox(values=[x[0] for x in SerialCommands.get_ports()],
      size=(40, 6), key='_DEVICE_LIST_', font=medium_font, enable_events=True)
    ],
    [
      sg.Text('', key='_SERIAL_PORT_CONFIRM_', size=(40, 1), font=small_font)
    ],
    [
      sg.HorizontalSeparator(pad=((0, 0), (0, 15)))
    ],
    [
      sg.Checkbox('Quaternion', key='_QUATERNION_', change_submits=True, 
      font=large_font, pad=((20, 5), (0, 0))), 
      sg.VerticalSeparator(), 
      sg.Checkbox('EulerAngle', key='_EULERANGLE_', change_submits=True,
      default=True, font=large_font, pad=((0, 0), (0, 0)))
    ],
    [
      sg.Button('Start',  key='_ACT_BUTTON_', font=medium_font, size=(40, 1), 
      pad=((0, 0), (24, 0)))
    ],
    [
      sg.Text('NelsonWenner - Version: 0.1', justification='right', size=(60, 1), 
      pad=((0, 0), (10, 0)), font=small_font) 
    ]
  ]

  def __init__(self):
    self.baud_rate = 115200
    self.current_device = '_SERIAL_'
    self.current_type_data = '_EULERANGLE_'
    self.stop_thread_trigger = False
    self.orientation_visualization = OrientationVisualization()
    self.serial_commands = SerialCommands(self.baud_rate)
    self.socket_commands = SocketCommands()
    self.window = sg.Window('', self.layout, size=(360, 400), keep_on_top=True)

    while True:
      event, values = self.window.Read(timeout=100)

      if event == sg.WIN_CLOSED: break

      if event == '_SERIAL_':
        self.window['_DEVICE_TITLE_'].update('Select your serial port')
        self.window['_SERIAL_'].update(True)
        self.window['_WIFI_'].update(False)
        self.current_device = '_SERIAL_'
        self.add_serial_port()
        self.socket_commands.disconnect()

      if event == '_WIFI_':
        self.window['_DEVICE_TITLE_'].update('Waiting for connections')
        self.window['_WIFI_'].update(True)
        self.window['_SERIAL_'].update(False)
        self.window['_DEVICE_LIST_'].update(values=['[X] Server listening in port 8080'])
        self.window['_SERIAL_PORT_CONFIRM_'].update(value='')
        self.current_device = '_WIFI_'
        self.thread_socket = threading.Thread(
          target=self.socket_commands.connect, 
          daemon=True
        )
        self.thread_socket.start()

      if event == '_QUATERNION_':
        self.window['_QUATERNION_'].update(True)
        self.window['_EULERANGLE_'].update(False)
        self.current_type_data = '_QUATERNION_'

      if event == '_EULERANGLE_':
        self.window['_EULERANGLE_'].update(True)
        self.window['_QUATERNION_'].update(False)
        self.current_type_data = '_EULERANGLE_'
        
      if self.current_device == '_WIFI_':
        if len(self.socket_commands.clients) != (len(self.window['_DEVICE_LIST_'].get()) - 1):
          info = ['[X] Server listening in port 8080'] + self.socket_commands.clients
          self.window['_DEVICE_LIST_'].update(values=info)

      if event == '_DEVICE_LIST_':
        current_values = self.window['_DEVICE_LIST_'].get()[0]
        self.window['_SERIAL_PORT_CONFIRM_'].update(value="[X] {}".format(current_values))

      if event == '_ACT_BUTTON_':
        if self.window[event].get_text() == 'Start':
          if self.current_device == '_SERIAL_':
            if len(self.window['_DEVICE_LIST_'].get()) == 0:
              self.popup_dialog('Serial Port is not selected yet!', 'Serial Port', self.medium_font)
            elif self.serial_commands.get_data() is None:
              self.popup_dialog('The app is not receiving any data', 'Data Transmission', self.medium_font)
            elif self.current_type_data == '_QUATERNION_' and len(self.serial_commands.get_data()) != 4:
              self.popup_dialog('Invalid data type, quaternion requires 4 values (w, x, y, z)', 'Data Type', self.medium_font)
            elif self.current_type_data == '_EULERANGLE_' and len(self.serial_commands.get_data()) != 3:
              self.popup_dialog('Invalid data type, euler angle requires 3 values (x, y, z)', 'Data Type', self.medium_font)
            else:
              self.stop_thread_trigger = False
              self.thread_device = threading.Thread(
                target=self.start_orientation_visualization, 
                args=(
                  self.orientation_visualization, self.serial_commands, self,
                  self.window['_DEVICE_LIST_'].get()[0]
                ),
                daemon=True
              )
              self.thread_device.start()
              self.window['_ACT_BUTTON_'].update('Stop')

          elif self.current_device == '_WIFI_':
            if not self.socket_commands.clients:
              self.popup_dialog('Not have any device connected', 'Device Connection', self.medium_font)
            elif not ('new client' in self.socket_commands.clients[-1]):
              self.popup_dialog('Not have client connected', 'Client Connection', self.medium_font)
            elif self.socket_commands.get_data() is None:
              self.popup_dialog('The app is not receiving any data', 'Data Transmission', self.medium_font)
            elif self.current_type_data == '_QUATERNION_' and len(self.socket_commands.get_data()) != 4:
              self.popup_dialog('Invalid data type, quaternion requires 4 values (w, x, y, z)', 'Data Type', self.medium_font)
            elif self.current_type_data == '_EULERANGLE_' and len(self.socket_commands.get_data()) != 3:
              self.popup_dialog('Invalid data type, euler angle requires 3 values (x, y, z)', 'Data Type', self.medium_font)
            else:
              self.stop_thread_trigger = False
              self.thread_device = threading.Thread(
                target=self.start_orientation_visualization, 
                args=(
                  self.orientation_visualization, 
                  self.socket_commands, self, -1
                ),
                daemon=True
              )
              self.thread_device.start()
              self.window['_ACT_BUTTON_'].update('Stop')
        else:
          self.stop_thread_trigger = True
          self.thread_device.join()
          self.window['_ACT_BUTTON_'].update('Start')

    self.window.close()

  def start_orientation_visualization(self, orientation_visualization, device, app, serialport):
    if self.current_device == '_SERIAL_':
      device.connect(serialport)
    if device.is_connect():
      orientation_visualization.start(device, app)

  def add_serial_port(self):
    self.window['_DEVICE_LIST_'].update(values=[x[0] for x in SerialCommands.get_ports()])

  def popup_dialog(self, contents, title, font):
    sg.Popup(contents, title=title, keep_on_top=True, font=font)

if __name__ == '__main__':
  App()