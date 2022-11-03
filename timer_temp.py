from dis import code_info
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
REDLEDPIN = 4
DHTPIN  = 12

humidity = 0
temperature = 0
t = 0
countdown = 0
timer = 15
count = 0
status = 0
timersStarted = []
orders = []
array = {}


def Measure(data):
    global humidity, temperature
    if (data[3] == 0):
        humidity = data[4]
        temperature = data[5]

def Buttonchange(data):
    global count, status, orders
    if data[2] == 0:
        if globals()["status" + orders[count][0]] == 0:
            globals()["status" + orders[count][0]] += 1
            timersStarted.append(orders[count][0])
            board.digital_pin_write(REDLEDPIN, 1)
        elif globals()["status" + orders[count][0]] == 2:
            globals()["status" + orders[count][0]] += 1
            orders.pop(count)
        board.displayShow(orders[(count)][0])
        print(orders[count][0])
        print(globals()["status" + orders[count][0]])


def Buttonchange2(data):
    global count, orders
    if data[2] == 0:
        if count == (len(orders)-1):
            count = 0
        else:
            count += 1
        board.displayShow(orders[count][0])
        if globals()["timer" + orders[count][0]] == 10 or globals()["timer" + orders[count][0]] == 0:
            board.digital_pin_write(REDLEDPIN, 0) 
        else:
            board.digital_pin_write(REDLEDPIN, 1) 
    print(data)

def setup():
    global board
    board = CustomPymata4(com_port = "COM7")
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN, callback=Buttonchange)
    board.set_pin_mode_digital_input_pullup(BUTTON2PIN, callback=Buttonchange2)
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback=Measure)
    board.set_pin_mode_digital_output(REDLEDPIN)
    time.sleep(2)

def updateOrders():
    global orders, array
    array = {}
    resp = requests.get('http://192.168.2.4:5000/testinGet')
    pizzas = resp.content
    orders = json.loads(pizzas)
    for order in orders:
        if ("status" + order[0]) in globals():
            array["Status" + order[0]] = globals()["status" + order[0]]
            array.update({"Timer" + order[0]: globals()["timer" + order[0]]})
        else:
            globals()["status" + order[0]] = 0
            globals()["timer" + order[0]] = 10
        print(array)
    print(orders)

def loop():
    global timer, countdown, array, response
    countdown += 1
    if countdown == 10:
        countdown = 0
        for timer in timersStarted:
            if globals()["timer" + timer] != 0:
                globals()["timer" + timer] -= 1
                print(globals()["timer" + timer])
            else:
                globals()["status" + timer] = 2
                timersStarted.remove(timer)
                board.digital_pin_write(REDLEDPIN, 0)
                print(globals()["status" + timer])
        response = requests.post('http://192.168.2.4:5000/status', json = array)
        updateOrders() 
    time.sleep(0.1)



setup()
updateOrders()
if orders != []:
    board.displayShow(orders[0][0])
while True:
    try:
        loop()
    except KeyboardInterrupt: # Shutdown Firmata on Crtl+C.
        print ('shutdown')
        board.shutdown()
        sys.exit(0)