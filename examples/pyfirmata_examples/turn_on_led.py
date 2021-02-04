import pyfirmata


usb_port = '/dev/ttyACM0'

board = pyfirmata.Arduino(usb_port)

led = board.get_pin('d:10:o')

while True:
    led.write(1)