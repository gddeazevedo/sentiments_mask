import pyfirmata
import time


usb_port = '/dev/ttyACM0'
board = pyfirmata.Arduino(usb_port)

led = board.get_pin('d:11:o')

# board.digital[12].mode = pyfirmata.OUTPUT

while True:
    led.write(1)
    time.sleep(1)
    led.write(0)
    time.sleep(1)
  
