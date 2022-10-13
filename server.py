from flask import Flask, render_template, request, redirect, flash
import csv
from random import randrange
from turbo_flask import Turbo


order = []
price = []
usernames = []
passwords = []
margaritha = ["Margaritha", 8, "Pizza Sauce, Cheese"]
pepperoni = ["Pepperoni", 10, "Pizza Sauce, Cheese, Pepperoni"]
bbqc = ["Barbeque Chicken", 12, "Pizza Sauce, Cheese, Chicken"]
dicktionary = {'margaritha': margaritha, 'pepperoni': pepperoni, 'BBQC': bbqc}
total = 0
timer = 0
status = 0
loggedIn = 0
username = ""
tracked = []

app = Flask(__name__)
turbo = Turbo(app)
app.secret_key = b'sussybakalmaohaha'

#Reads login data
with open("userinfo.csv") as readdata:
    reader = csv.reader(readdata)
    for row in reader:
        usernames.append(row[0])
        passwords.append(row[1])
        print(usernames)

#Function to remove items from order
def removeItem(item):
    global order, price
    for index in range(0, len(order)):
        if order[index] == item:
            del order[index]
            del price[index]
            break

#Load Main page
@app.route('/')
def index():
    global order                        
    return render_template('index.html', Timer = timer, Status = status, LoggedIn = loggedIn) #Logged in check to see if the user is logged in, and One is a variable for the number one

#Fake payment
@app.route('/payment')
def payment():
    global order
    if len(order) != 0:
        return render_template("payment.html")
    else:
        flash("Cart empty!")
        return redirect('/cart')

#Load Cart page
@app.route('/cart')
def cart():
    #Calculates total price
    global total
    total = 0
    for index in range(0, len(price)):
        total = total + int(price[index])
    return render_template('cart.html', Order = order, Price = total, Dicktionary = dicktionary)

#Recieves timer and pizza status from "Smart Oven"
@app.route('/status', methods = ['POST'])
def statusupdate():
    global timer, status
    list = request.get_json()
    timer = list["timer"]
    status = list["status"]
    print(list)
    return redirect('/')

#Loads Login page 
@app.route('/login')
def login():
    return render_template("login.html")

#Loads Regster page
@app.route('/register')
def register():
    return render_template("register.html")

#Logs User out
@app.route('/logout')
def logout():
    global loggedIn
    loggedIn = 0
    return redirect("/")

#The Login process
@app.route('/registerdata')
def registerdata():
    global loggedIn, username, usernames, passwords
    #Takes data from form on register.html
    username = request.args['username']
    password = request.args['password']
    #Checks in userdata if username exists
    for index in range(0, len(usernames)):
        if username == usernames[index]:
            #If found, gives register error
            flash('Username already has a account')
            return redirect('/register')
    usernames.append(username)
    passwords.append(password)
    print(usernames)
    with open("userinfo.csv", "a") as writedata:
        writedata.write("\n" + username + "," + password)
    loggedIn = 1
    return redirect('/')


@app.route('/logindata')
def logindata():
    global loggedIn, username, usernames, passwords
    username = request.args['username']
    password = request.args['password']
    for index in range(0, len(usernames)):
        if username == usernames[index]:
            if password == passwords[index]:
                loggedIn = 1
                return redirect('/')
            else:
                flash('Incorrect Password')
                return redirect('/login')
    flash('No account found with that username')
    return redirect('/login')

@app.route('/orderstatus')
def orderstatus():
    global ordernumber, username, status, timer
    ordernumber = randrange(99999999)
    print(ordernumber)
    with open("orders.csv", "a")as writeorder:
        writeorder.write(username + "," + str(ordernumber) + ",")
        for index in range(0, (len(order) - 1)):
            writeorder.write(order[index] + ",")
        writeorder.write(order[-1] + "," + str(total) + "\n")
    return redirect('/orderupdates') 

@app.route('/orderupdates')
def updates():
    global ordernumber, username, status, timer
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

@app.route('/orders')
def showorder():
    currentorders = []
    current
    return render_template('cookorders.html')

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