from glob import glob
import time
from flask import Flask, render_template, request, redirect, flash, session
import csv
import pandas as pd
from random import randrange
from flask_session import Session

order = {}
price = []
usernames = []
passwords = []
pizzas = []
margaritha = ["Margaritha", 8, "Pizza Sauce, Cheese"]  # type: ignore
pepperoni = ["Pepperoni", 10, "Pizza Sauce, Cheese, Pepperoni"]  # type: ignore
bbqc = ["Barbeque Chicken", 12, "Pizza Sauce, Cheese, Chicken"]
dicktionary = {'margaritha': margaritha, 'pepperoni': pepperoni, 'BBQC': bbqc}  # type: ignore
total = 0
timer = 0
status = 0
loggedIn = 0
ordernumber = 0
one = 1
counter = 0
username = ""
tracked = []
user = 0
anon = 0

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
Flask.secret_key = 'lmaosus'

with open("userinfo.csv") as readdata:
    reader = csv.reader(readdata)
    for row in reader:
        usernames.append(row[0])
        passwords.append(row[1])
        print(usernames)

def removeItem(item):
    global order, price
    for index in range(0, len(order[session["name"]])):
        if order[session["name"]][index] == item:
            del order[session["name"]][index]
            del price[index]
            break

@app.route('/')
def index():
    global order, anon
    if not session.get("name"):
        session["name"] = randrange(350)
        anon = 1
        order[session["name"]] = []
        print(order)
    return render_template('index.html', Order = order, Timer = timer, Status = status, LoggedIn = loggedIn, One = one, anon = anon)

@app.route('/payment')
def payment():
    return render_template("payment.html")

@app.route('/cart')
def cart():
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary, loggedIn = loggedIn, One = one)

@app.route('/status', methods = ['POST'])
def statusupdate():
    global timer, status
    poopybutthole = request.get_json()
    timer = poopybutthole["timer"]
    status = poopybutthole["status"]
    print(poopybutthole)
    return redirect("/")

@app.route('/timerupdate', methods = ['GET'])
def timerupdate():
    return render_template("status.html", Status = status, Timer = timer, Ordernumber = ordernumber)

@app.route('/indexupdate')
def indexupdates():
    time.sleep(0.1)
    return render_template("index.html", Order = order, Timer = timer, Status = status, LoggedIn = loggedIn, One = one)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login(): 
    global anon
  # if form is submited
    if request.method == "POST":
        # record the user name
        session["name"] = request.form.get("name")
        # redirect to the main page
        anon = 0
        order[session["name"]] = []
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/orderstatus')
def orderstatus():
    global ordernumber, username, order, total, price
    ordernumber = randrange(99999999)
    print(ordernumber)
    with open("orders.csv", "a")as writeorder:
        writeorder.write("," + username + "," + str(ordernumber) + ",")
        for index in range(0, len(order)):
            writeorder.write(order[index] + ",")
        writeorder.write(str(total) + "," + "\n")
    order = []
    price = []
    return render_template("status.html", Status = status, Timer = timer, Ordernumber = ordernumber)


@app.route('/ordertracker')
def ordertracker():
    return render_template("ordertracker.html")

@app.route('/ordertrack')
def ordertrack():
    global ordernumber
    tracked = []
    orderask = request.args['ordernumber']
    with open("orders.csv") as orders:
        reader = csv.reader(orders)
        for row in reader:
            if orderask == row[2] or (str(orderask) + str(.0)) == row[2]:
                for index in range(3, (len(row) - 2)):
                    tracked.append(row[index])
                    print(tracked)
                total = row[-1]
                return render_template("tracked.html", Dicktionary = dicktionary, Ordernumber = orderask, Order = tracked, Price = total)
        if len(tracked) == 0:
            flash("No order found.")
    return redirect('/ordertracker')

@app.route('/margaritha', methods = ['GET'])
def margaritha():
    order[session["name"]].append("margaritha")
    price.append(8)
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary, LoggedIn = loggedIn, One = one)

@app.route('/Pep', methods = ['GET'])
def pepperoni():
    order[session["name"]].append("pepperoni")
    price.append(10)
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary, LoggedIn = loggedIn, One = one)

@app.route('/BBQC', methods = ['GET'])
def BBQC():
    order[session["name"]].append("BBQC")
    print(order)
    price.append(12)
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary, LoggedIn = loggedIn, One = one)

@app.route('/rmargaritha', methods = ['GET'])
def rmar():
    item = "margaritha"
    removeItem(item)
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary, LoggedIn = loggedIn, One = one)

@app.route('/rPep', methods = ['GET'])
def rpep():
    item = "pepperoni"
    removeItem(item)
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary, LoggedIn = loggedIn, One = one)

@app.route('/rBBQC', methods = ['GET'])
def rbbqc():
    item = "BBQC"
    removeItem(item)
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary, LoggedIn = loggedIn, One = one)

@app.route('/cookorders')
def cook():
    global order, allOrders, pizzas, pizzas2
    pizzas = []
    allOrders = []
    with open("orders.csv") as orders:
        reader = csv.reader(orders)
        for row in reader:
            if row[0] != "Done":
                pizzas2 = []
                allOrders.append(row)
                for index in range(2, len(row)):
                    if row[index] != "":
                        pizzas2.append(row[index])
                pizzas.append(pizzas2)
        for index in range(0, len(pizzas)):
            pizzas[index].pop()
        print(allOrders)
        print(pizzas)

    return render_template('cookorders.html', Length = len(order), AllOrders = allOrders, Order = order, Dicktionary = dicktionary, Pizzas = pizzas)

@app.route('/cooking')
def testing():
    global counter
    counter = 0
    df = pd.read_csv("orders.csv")
    tempordernumber = request.args['ON']
    print(tempordernumber)
    with open("orders.csv", "r") as datafile:
        reader = csv.reader(datafile)
        for row in reader:
            if row[2] == tempordernumber:
                df.loc[(counter - 1), 'Done'] = "Done"
                df.to_csv("orders.csv", index=False)
            counter += 1
    return redirect('cookorders')
