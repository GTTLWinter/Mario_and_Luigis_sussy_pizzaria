from flask import Flask, render_template, request, redirect, flash
import csv

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
one = 1

app = Flask(__name__)
app.secret_key = b'sussybakalmaohaha'

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
    global order
    return render_template('index.html', Timer = timer, Status = status, LoggedIn = loggedIn, One = one)

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

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/logout')
def logout():
    global loggedIn
    loggedIn = 0
    return redirect("/")

@app.route('/registerdata')
def registerdata():
    global loggedIn, usernames, passwords
    username = request.args['username']
    password = request.args['password']
    for index in range(0, len(usernames)):
        if username == usernames[index]:
            flash('Username already has a account')
            return redirect('/register')
        else:
            usernames.append(username)
            passwords.append(password)
            with open("userinfo.csv", "a") as writedata:
                writedata.write("\n" + username + "," + password)
            loggedIn = 1
            return redirect('/')


@app.route('/logindata')
def logindata():
    global loggedIn
    username = request.args['username']
    password = request.args['password']
    for index in range(0, len(usernames)):
        if username == usernames[index]:
            if password == passwords[index]:
                loggedIn = 1
                return redirect('/')
            else:
                return redirect('login')
                break
        else:
            flash('No account found with that username')
            return redirect('login')


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