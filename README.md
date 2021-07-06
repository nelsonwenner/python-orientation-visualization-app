<h2 align="center">
  ORIENTATION VISUALIZATION
</h2>

## :bulb: About
The module that allows observing orientations through a 3D object from Euler angles or quaternion transmitted with WebSocket via wi-fi or serial port.

## :movie_camera: Preview

<div align="center">
  <img src="preview.gif" />
</div>

## :rocket: Technologies

* [Python3](https://www.python.org/)
* [OpenGL](https://pypi.org/project/PyOpenGL/)

## :raised_hand: Warning
To use this module, remember that data must be transmitted via serial port or wifi in string in the following format:
* Quaternion
  ```json
  "
    [
      w,
      x,
      y,
      z
    ]
  "
  ``` 

* Euler angles
  ```json
  "
    [
      pitch,
      roll,
      yaw
    ]
  "
  ``` 

## :information_source: Getting Started

1. Fork this repository and clone it on your machine.
2. Change the directory to `orientation-visualization` where you cloned it.

## :zap: Module Getting Started

1. Install requirements.
```shell
$ pip install -r requirements.txt
```
2. Startup
```shell
$ python3 OrientationVisualization.py
```
* If you are going to use data transmission via Wifi, when connecting, keep in mind that the WebSocket server `IP` will be your machine's `IP` and port `8080`.
---
Made with :hearts: by Nelson Wenner :wave: [Get in touch!](https://www.linkedin.com/in/nelsonwenner/)