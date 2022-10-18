import time
from flask import Flask, render_template, request, redirect, flash, session
import csv
from random import randrange
from flask_session import Session

order = []
price = []
usernames = []
passwords = []
allOrders = []
margaritha = ["Margaritha", 8, "Pizza Sauce, Cheese"]
pepperoni = ["Pepperoni", 10, "Pizza Sauce, Cheese, Pepperoni"]
bbqc = ["Barbeque Chicken", 12, "Pizza Sauce, Cheese, Chicken"]
dicktionary = {'margaritha': margaritha, 'pepperoni': pepperoni, 'BBQC': bbqc}
total = 0
timer = 0
status = 0
loggedIn = 0
one = 1
username = ""
tracked = []
user = 0

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = b'sussybakalmaohaha'
Flask.secret_key = 'lmaosus'

with open("userinfo.csv") as readdata:
    reader = csv.reader(readdata)
    for row in reader:
        usernames.append(row[0])
        passwords.append(row[1])
        print(usernames)

def removeItem(item):
    global order, price
    for index in range(0, len(order)):
        if order[index] == item:
            del order[index]
            del price[index]
            break

@app.route('/')
def index():
    global order, session
    return render_template('index.html', Order = order, Timer = timer, Status = status, LoggedIn = loggedIn, One = one, username = username)

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
    return render_template("index.html", Order = globals()[ordernumber], Timer = timer, Status = status, LoggedIn = loggedIn, One = one)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/logout')
def logout():
    global loggedIn
    session["username"] = None
    loggedIn = 0
    return redirect("/")

@app.route('/registerdata', methods = ['POST'])
def registerdata():
    global loggedIn, username, usernames, passwords
    if request.method == "POST":
        username = request.args['username']
        password = request.args['password']
    for index in range(0, len(usernames)):
        if username == usernames[index]:
            flash('Username already has a account')
            return redirect('/register')
        else:
            session["username"] = request.form.get("username")
            usernames.append(username)
            passwords.append(password)
            with open("userinfo.csv", "a") as writedata:
                writedata.write("\n" + username + "," + password)
            loggedIn = 1
            return redirect('/')


@app.route('/logindata')
def logindata():
    global loggedIn, username, session
    username = request.args['username']
    password = request.args['password']
    for index in range(0, len(usernames)):
        if username == usernames[index]:
            if password == passwords[index]:
                loggedIn = 1
                session["username"] = request.form.get("username")
                return redirect('/')
            else:
                return redirect('login')
                break
        else:
            flash('No account found with that username')
    return redirect('login')

@app.route('/orderstatus')
def orderstatus():
    global ordernumber, username, order
    ordernumber = randrange(99999999)
    print(ordernumber)
    globals()[ordernumber] = order
    allOrders.append(globals()[ordernumber])
    print(globals()[ordernumber])
    order = []
    with open("orders.csv", "a")as writeorder:
        writeorder.write(username + "," + str(ordernumber) + ",")
        for index in range(0, (len(globals()[ordernumber]) - 1)):
            writeorder.write(globals()[ordernumber][index] + ",")
        writeorder.write(globals()[ordernumber][-1] + "," + str(total) + "\n")
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
            if orderask == row[1]:
                for index in range(2, (len(row) - 1)):
                    tracked.append(row[index])
                total = row[-1]
                return render_template("tracked.html", Dicktionary = dicktionary, Ordernumber = orderask, Order = tracked, Price = total)
        if len(tracked) == 0:
            flash("No order found.")
    return redirect('/ordertracker')

@app.route('/margaritha', methods = ['GET'])
def margaritha():
    order.append("margaritha")
    price.append(8)
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary, LoggedIn = loggedIn, One = one)

@app.route('/Pep', methods = ['GET'])
def pepperoni():
    order.append("pepperoni")
    price.append(10)
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary, LoggedIn = loggedIn, One = one)

@app.route('/BBQC', methods = ['GET'])
def BBQC():
    order.append("BBQC")
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
    global ordernumber
    return render_template('cookorders.html', Length = len(globals()[ordernumber]), AllOrders = allOrders, Dicktionary = dicktionary, ON = ordernumber)

@app.route('/anon', methods = ['GET'])
def anon():
    global user
    return user