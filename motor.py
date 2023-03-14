import pigpio
import time

DEVICE_ADDRESS = 0x20
REG_IODIRA = 0x00 # GPA I/O direction register
REG_IODIRB = 0x01 # GPB I/O direction register
REG_OLATA = 0x14 # GPA output latch register
REG_OLATB = 0x15 # GPB output latch register

# pigpio library : https://abyz.me.uk/rpi/pigpio/python.html

class Motor(object):
    def __init__(self):
        Motor.pi = pigpio.pi()
        Motor._device = Motor.pi.i2c_open(1, DEVICE_ADDRESS) 
        # SDA = 2, SCL = 3 => channel = 1
        Motor.pi.i2c_write_byte_data(Motor._device, REG_IODIRA, 0x00)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_IODIRB, 0x00)
        # stop
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x00)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x00)
    
    def forward(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x30)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x06)
        print("forward")
        
    def back(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x06)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x30)
        print("back")
    
    def stop(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x00)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x00)
        print("stop")
        
    def turn_right(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x36)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x00)
        print("turn right")
    
    def turn_left(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x00)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x36)
        print("turn left")
        
    def stuck(self):
        Motor.back(self)
        time.sleep(3)
        Motor.turn_right(self)
        time.sleep(1)
        Motor.forward(self)
        time.sleep(3)
        Motor.stop(self)
        print('Finish stuck processing')
        
    def sepa_mecha(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x00)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x08)
        print("Separation mechanism activated")
        
    def attach_para(self):
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATA, 0x08)
        Motor.pi.i2c_write_byte_data(Motor._device, REG_OLATB, 0x00)
        

if __name__ == '__main__':
    drive = Motor()
    while True:
        c = input('Enter char : ')
        if c == 'w':
            drive.forward()
        elif c == 'a':
            drive.turn_left()
        elif c == 'd':
            drive.turn_right()
        elif c == 's':
            drive.back()
        elif c == 'q':
            drive.stop()
        elif c == 'st':
            drive.stuck()
        elif c == 'sep':
            drive.sepa_mecha()
        elif c == 'para':
            drive.attach_para()
        elif c == 'quit':
            break
        else:
            print('Invalid input')
