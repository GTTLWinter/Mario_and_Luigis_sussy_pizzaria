from flask import Flask, render_template, request, redirect
import csv

order = []
price = []
margaritha = ["Margaritha", 8, "Pizza Sauce, Cheese"]
pepperoni = ["Pepperoni", 10, "Pizza Sauce, Cheese, Pepperoni"]
bbqc = ["Barbeque Chicken", 12, "Pizza Sauce, Cheese, Chicken"]
dicktionary = {'margaritha': margaritha, 'pepperoni': pepperoni, 'BBQC': bbqc}
total = 0
timer = 0
status = 0

app = Flask(__name__)

def removeItem(item):
    global order, price
    for index in range(0, len(order)):
        if order[index] == item:
            del order[index]
            del price[index]
            break

@app.route('/')
def index():
    global order
    return render_template('index.html', Timer = timer, Status = status)

@app.route('/payment')
def payment():
    return render_template("payment.html")

@app.route('/cart')
def cart():
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/status', methods = ['POST'])
def statusupdate():
    global timer, status
    poopybutthole = request.get_json()
    timer = poopybutthole["timer"]
    status = poopybutthole["status"]
    print(poopybutthole)
    return redirect('/')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logindata')
def logindata():
        username = request.args['username']
        password = request.args['password']
        return redirect('/')

@app.route('/orderstatus')
def orderstatus():
    return render_template("status.html")

@app.route('/margaritha')
def margaritha():
    order.append("margaritha")
    price.append(8)
    return redirect('/')

@app.route('/Pep')
def pepperoni():
    order.append("pepperoni")
    price.append(10)
    return redirect('/')

@app.route('/BBQC')
def BBQC():
    order.append("BBQC")
    price.append(12)
    return redirect('/')

@app.route('/rmargaritha')
def rmar():
    item = "margaritha"
    removeItem(item)
    return redirect('/')

@app.route('/rPep')
def rpep():
    item = "pepperoni"
    removeItem(item)
    return redirect('/')

@app.route('/rBBQC')
def rbbqc():
    item = "BBQC"
    removeItem(item)
    return redirect('/')