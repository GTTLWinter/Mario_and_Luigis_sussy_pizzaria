import time
from flask import Flask, render_template, request, redirect, flash, session, Response
import csv
import pandas as pd
from random import randrange
from flask_session import Session

order = {}
price = {}
usernames = []
passwords = []
pizzas = []
margaritha = ["Margaritha", 8, "Tomato sauce, Mozzarella"]
pepperoni = ["Pepperoni", 10, "Tomato sauce, Mozzarella, Pepperoni"]
bbqc = ["Barbeque Chicken", 12, "Tomato sauce, Mozzarella, Chicken"]
hawaii = ["Hawaii", 11, "Tomato sauce, Mozzarella, Ham, Pineapple"]
glutenf = ["Gluten Free", 9, "Gluten free dough, Tomato sauce, Mozzarella"]
vegan = ["Vegan", 15, "Tomato sauce, Vegan cheese"]
veggie = ["Vegeterian", 13, "Tomato sauce, Mozzarella, Other healthy shit idk"]
dicktionary = {'margaritha': margaritha, 'pepperoni': pepperoni, 'BBQC': bbqc, 'hawaii' : hawaii, 'vegan' : vegan, 'veggie' : veggie}
total = 0
timer = 0
status = 0
loggedIn = 0
ordernumber = {}
one = 1
counter = 0
username = ""
tracked = []
user = 0
anon = 0

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
Flask.secret_key = 'lmaosus'

def readinfo():
    with open("userinfo.csv") as readdata:
        reader = csv.reader(readdata)
        for row in reader:
            usernames.append(row[0])
            passwords.append(row[1])
            print(usernames)
            print(passwords)

def removeItem(item):
    global order, price
    for index in range(0, len(order[session["name"]])):
        if order[session["name"]][index] == item:
            del order[session["name"]][index]
            del price[session["name"]][index]
            break

readinfo()

@app.route('/')
def index():
    global order, anon
    if not session.get("name"):
        session["name"] = randrange(1000)
        anon = 1
        order[session["name"]] = []
        price[session["name"]] = []
        print(order)
    elif session["name"] in usernames:
        anon = 0
        order[session["name"]] = []
        price[session["name"]] = []
        print(order)
    else:
        session["name"] = randrange(1000)
        anon = 1
        order[session["name"]] = []
        price[session["name"]] = []
        print(order)
    
    return render_template('index.html', Order = order, Timer = timer, Status = status, anon = anon)

@app.route('/payment')
def payment():
    return render_template("payment.html")

@app.route('/cart')
def cart():
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

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
    return render_template("index.html", Order = order, Timer = timer, Status = status)

@app.route('/register', methods=["POST", "GET"])
def register():
    global anon
    logn = 1
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("pass")
        if username in usernames:
            flash("This username has already been taken")
            return redirect('/register')
        else:
            session["name"] = username
            userpass = [str(username), str(password)]
            print(userpass)
            anon = 0
            order[session["name"]] = []
            price[session["name"]] = []
            with open('userinfo.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(userpass)
            readinfo()
            return redirect('/')
    return render_template("login.html", logn = logn)

@app.route("/login", methods=["POST", "GET"])
def login(): 
    global anon
    logn = 0
    if request.method == "POST":  
        username = request.form.get("name")
        password = request.form.get("pass")
        if username in usernames:
            if password == passwords[usernames.index(username)]:
                session["name"] = request.form.get("name")
                anon = 0
                order[session["name"]] = []
                price[session["name"]] = []
                print(order)
                return redirect('/')
            else:
                flash("Wrong password!")
                return redirect("/login")
        else:
            flash("No such user exists!")
            return redirect("/login")
    return render_template("login.html", logn = logn)

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/orderstatus')
def orderstatus():
    global ordernumber, username, order, total, price
    print(order)
    username = session["name"]
    ordernumber[session["name"]] = randrange(99999999)
    print(ordernumber)
    with open("orders.csv", "a")as writeorder:
        writeorder.write("," + str(username) + "," + str(ordernumber[session["name"]]) + ",")
        for index in range(0, len(order[session["name"]])):
            writeorder.write(order[session["name"]][index] + ",")
        writeorder.write(str(total) + "," + "\n")
    order[session["name"]] = []
    price[session["name"]] = []
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
    price[session["name"]].append(8)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/Pep', methods = ['GET'])
def pepperoni():
    order[session["name"]].append("pepperoni")
    price[session["name"]].append(10)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/BBQC', methods = ['GET'])
def BBQC():
    order[session["name"]].append("BBQC")
    price[session["name"]].append(12)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/hawaii', methods = ['GET'])
def hawaii():
    order[session["name"]].append("hawaii")
    price[session["name"]].append(11)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/vegan', methods = ['GET'])
def vegann():
    order[session["name"]].append("vegan")
    price[session["name"]].append(15)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/veggie', methods = ['GET'])
def veggiee():
    order[session["name"]].append("veggie")
    price[session["name"]].append(13)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/rmargaritha', methods = ['GET'])
def rmar():
    item = "margaritha"
    removeItem(item)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/rPep', methods = ['GET'])
def rpep():
    item = "pepperoni"
    removeItem(item)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/rBBQC', methods = ['GET'])
def rbbqc():
    item = "BBQC"
    removeItem(item)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/rhawaii', methods = ['GET'])
def rhawaii():
    item = "hawaii"
    removeItem(item)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/rvegan', methods = ['GET'])
def rvegan():
    item = "vegan"
    removeItem(item)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

@app.route('/rveggie', methods = ['GET'])
def rVeggie():
    item = "veggie"
    removeItem(item)
    global total
    total = 0
    for index in range(0, len(price[session["name"]])):
        total = total + int(price[session["name"]][index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)


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

    return render_template('cookorders.html', Length = len(order[session["name"]]), AllOrders = allOrders, order = order[session["name"]], Dicktionary = dicktionary, Pizzas = pizzas)

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

@app.route('/account', methods=['GET'])
def acc():
    return render_template('account.html', anon = anon)