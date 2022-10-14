import json
from pkgutil import get_data
import sys
import time
from csv import writer
from datetime import datetime
import requests
from fhict_cb_01.CustomPymata4 import CustomPymata4

BUTTON1PIN = 9
BUTTON2PIN = 8
LDRPIN = 2
DHTPIN  = 12

humidity = 0
temperature = 0
t = 0

def Measure(data):
    global humidity, temperature
    if (data[3] == 0):
        humidity = data[4]
        temperature = data[5]

def setup():
    global board
    board = CustomPymata4(com_port = "COM3")
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN)
    board.set_pin_mode_digital_input_pullup(BUTTON2PIN)
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback=Measure)
    time.sleep(2)

def loop():
    global humidity, temperature, orderstarted, t, response
    
    level1, time_stamp1 = board.digital_read(BUTTON1PIN)
    level2, time_stamp2 = board.digital_read(BUTTON2PIN)
    orderdone = True
    if t > 2:
        if level1 == 0:
            timer = input("How much time do you want the pizza to be cooked for? Use s or m for seconds or minutes. ")
            if 'm' in timer:
                timer = timer.replace("m", "")
                orderstarted = int(timer) * 60
            elif 's' in timer:
                timer = timer.replace('s', "")
                orderstarted = int(timer)
            else:
                orderstarted = 60
            print("Timer has begun!")
            
            while orderstarted:
                board.displayShow(orderstarted)
                time.sleep(1)
                print(str(round(temperature)) + "C")
                orderstarted -= 1
                orderdone = False
                array = {'status': 0, 'timer': orderstarted}
                response = requests.post('http://145.93.104.206:5000/status', json = array)
            print("Timer has ended!")
            array["status"] = 1
            response = requests.post('http://145.93.104.206:5000/status', json = array)
        while orderdone == False:
            level2, time_stamp2 = board.digital_read(BUTTON2PIN)
            if level2 == 0:
                orderdone = True
                print("Order is ready!")
                array["status"] = 2
                response = requests.post('http://145.93.104.206:5000/status', json = array)
                time.sleep(0.2)
    t += 1
                


setup()
while True:
    try:
        loop()
    except KeyboardInterrupt: # Shutdown Firmata on Crtl+C.
        print ('shutdown')
        board.shutdown()
        sys.exit(0)  