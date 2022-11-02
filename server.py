import re
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
margaritha = ["Margaritha", 8, "Tomato sauce, Mozzarella", 1]
pepperoni = ["Pepperoni", 10, "Tomato sauce, Mozzarella, Pepperoni", 2]
bbqc = ["Barbeque Chicken", 12, "Tomato sauce, BBQ sauce, Mozzarella, Chicken", 3]
hawaii = ["Hawaii", 11, "Tomato sauce, Mozzarella, Ham, Pineapple", 4]
glutenf = ["Gluten Free", 9, "Gluten free dough, Tomato sauce, Mozzarella", 5]
vegan = ["Vegan", 15, "Vegan dough, Tomato sauce, Vegan cheese", 6]
funghi = ["Funghi", 13, "Tomato sauce, Mozzarella, Mushrooms, Olives", 7]
forange = ["Drink", 2, "Fanta Orange", 8]
ccola = ["Drink", 1.9, "Coca Cola", 9]
grit = ["Drink", 1.7, "Green Ice Tea", 10]
chcola = ["Drink", 1.9, "Coca Cola Cherry", 11]
petea = ["Drink", 1.8, "Peach Ice Tea", 12]
fcasis = ["Drink", 2, "Fanta Cassis", 13]
chcake = ["Dessert", 5, "Cheesecake", 14]
ckie = ["Dessert", 3.5, "Chocolate Cookie", 15]
brownie = ["Dessert", 3.5, "Brownie", 16]
vccake = ["Dessert", 6, "Vanilla Cupcake", 17]
icream = ["Dessert", 3, "Ice Cream", 18]
tsu = ["Dessert", 4, "Tiramisu", 19]
dicktionary = {'margaritha': margaritha, 'pepperoni': pepperoni, 'BBQC': bbqc, 'hawaii' : hawaii, 
'vegan' : vegan, 'funghi' : funghi, 'glutenf' : glutenf, 'forange' : forange, 'ccola' : ccola,
'grit' : grit, 'chcola' : chcola, 'petea' : petea, 'fcasis' : fcasis, 'chcake' : chcake, 'ckie' : ckie,
'brownie' : brownie, 'vccake' : vccake, 'icream' : icream, 'tsu' : tsu}
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
anon = {}
ft = {}
ingredients = ["Normal", "Italian", "Philladelphia", "Tomato sauce", "Pesto", "White Garlic", "Marinara Sauce", 
    "Pepperoni", "Ham", "Mushrooms", "Pineapple", "Olives", "Onions", "Corn", "Sausage", "Bacon", "Chicken", 
    "Spinach", "Basel", "Beef", "Pork"]
prices = [2.00, 4.19, 5.49, 2.00, 3.19, 4.49, 5.49, 1.10, 1.20, 1.30, 1.15, 1.15, 1.30, 1.20, 1.90, 2.00, 2.00, 0.89, 0.89, 3.00, 2.85]
CustomPizza = {}

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

def readOrders():
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

def removeItem(item):
    global order, price
    for index in range(0, len(order[session["name"]])):
        if order[session["name"]][index] == item:
            del order[session["name"]][index]  
            break

def adddelItem():
    global order, price
    if request.method == 'POST':
        pizza = str(request.args.keys()).replace("dict_keys(['", "").replace("'])", "")
        if '2' in pizza:
            delpizza = pizza.replace("2","")
            removeItem(delpizza)
            price[session["name"]] -= dicktionary[delpizza][1]
        else:
            order[session["name"]].append(pizza)
            price[session["name"]] += dicktionary[pizza][1]
            print(price)

readinfo()
readOrders()

@app.route('/')
def index():
    global order, anon, ft
    if not session.get("name"):
        session["name"] = randrange(1000)
        anon[session["name"]] = 1
        order[session["name"]] = []
        price[session["name"]] = 0
        CustomPizza[session["name"]] = {"crust": ingredients[0], "sauce": ingredients[3], "toppings": [], "price": 4}
        if session["name"] not in ft:
            ft[session["name"]] = 0
        print(order)
    elif session["name"] in usernames:
        if session["name"] in order:
            None
        elif session["name"] == "Pizza":
            return redirect('/cookorders')
        else:
            anon[session["name"]] = 2
            order[session["name"]] = []
            price[session["name"]] = 0
            CustomPizza[session["name"]] = {"crust": ingredients[0], "sauce": ingredients[3], "toppings": [], "price": 4}
            if session["name"] not in ft:
                ft[session["name"]] = 0
            print(order)
    elif session.get("name"):
        if session["name"] in order:
            None
        else:
            anon[session["name"]] = 1
            order[session["name"]] = []
            price[session["name"]] = 0
            CustomPizza[session["name"]] = {"crust": ingredients[0], "sauce": ingredients[3], "toppings": [], "price": 4}
            print(order)
    return render_template('index.html', Order = order, Timer = timer, Status = status, anon = anon, ft = ft)

@app.route('/payment')
def payment():
    return render_template("payment.html")

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == "POST":
        order[session["name"]] = []
        price[session["name"]] = 0
    return render_template('cart.html', Order = order, Price = price[session["name"]], Dicktionary = dicktionary)

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

@app.route('/changep', methods=['POST', 'GET'])
def ChangeP():
    if request.method == "POST":
        password = request.form.get("pass")
        passwords[usernames.index(session["name"])] = password
        f = open("userinfo.csv", "w")
        f.truncate()
        f.close()
        with open('userinfo.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                print(len(usernames))
                for row in range(len(usernames)):
                    userpass = [str(usernames[row]), str(passwords[row])]
                    print(userpass)
                    writer.writerow(userpass)
        return redirect('/')
    return render_template("changep.html")

@app.route('/register', methods=["POST", "GET"])
def register():
    global anon
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("pass")
        if username in usernames:
            flash("This username has already been taken")
            return render_template("register.html")
        else:
            session["name"] = username
            userpass = [str(username), str(password)]
            print(userpass)
            anon[session["name"]] = 0
            order[session["name"]] = []
            price[session["name"]] = []
            with open('userinfo.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(userpass)
            readinfo()
            return redirect('/rel')
    return render_template("register.html")

@app.route("/rel", methods=['GET'])
def Rel():
    return render_template('rel.html')

@app.route("/login", methods=["POST", "GET"])
def login(): 
    global anon
    if request.method == "POST":  
        username = request.form.get("name")
        password = request.form.get("pass")
        if username in usernames:
            if password == passwords[usernames.index(username)]:
                session["name"] = request.form.get("name")
                anon[session["name"]] = 0
                order[session["name"]] = []
                price[session["name"]] = 0
                print(order)
                return redirect('/rel')
            else:
                flash("Wrong password!")
                return redirect("/login")
        else:
            flash("No such user exists!")
            return redirect("/login")
    return render_template("login.html")

@app.route("/logout")
def logout():
    global anon
    session["name"] = None
    return redirect("/")

@app.route('/orderstatus')
def orderstatus():
    global ordernumber, username, order, price
    print(order)
    username = session["name"]
    ordernumber[session["name"]] = randrange(99999999)
    print(ordernumber)
    with open("orders.csv", "a")as writeorder:
        writeorder.write("," + str(username) + "," + str(ordernumber[session["name"]]) + ",")
        for index in range(0, len(order[session["name"]])):
            if order[session["name"]][index][0] == "Custom":
                for item in order[session["name"]][index]:
                    writeorder.write(str(item).replace(" ","") + ",")
            else:
                writeorder.write(order[session["name"]][index] + ",")
        writeorder.write(str(price[session["name"]]) + "," + "\n")
    order[session["name"]] = []
    price[session["name"]] = 0
    return render_template("status.html", Status = status, Timer = timer, Ordernumber = ordernumber)


@app.route('/ordertracker')
def ordertracker():
    return render_template("ordertracker.html")

@app.route('/ordertrack', methods=['POST'])
def ordertrack():
    global ordernumber
    tracked = {session["name"] : []}
    if request.method == "POST":
        orderask = request.form.get('ordernumber')
        with open("orders.csv", 'r') as orders:
            reader = csv.reader(orders)
            for row in reader:
                if orderask == row[2] or (str(orderask) + str(.0)) == row[2]:
                    for index in range(3, (len(row) - 2)):
                        tracked[session["name"]].append(row[index])
                    print(tracked)
                    total = {session["name"] : row[len(row)-2]}
                    return render_template("tracked.html", Dicktionary = dicktionary, Ordernumber = orderask, Order = tracked[session["name"]], Price = total[session["name"]])
    return redirect('/ordertracker')

@app.route('/cookorders')
def cook():
    readOrders()

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

@app.route('/account', methods=['GET', 'POST'])
def acc():
    pastorders = {}
    pastorders[session["name"]] = []
    with open("orders.csv") as readdata:
        reader = csv.reader(readdata)
        for row in reversed(list(reader)):
            if len(pastorders[session["name"]]) == 5:
                continue
            else:
                if row[1] == session["name"]:
                    pastorders[session["name"]].append(row)
    print(pastorders)
    if request.method == "POST":
        k = int(str(request.args.keys()).replace("dict_keys(['", "").replace("'])", ""))
        print(pastorders[session["name"]][k])
        if "Custom" in pastorders[session["name"]][k]:
                c = pastorders[session["name"]][k].index("Custom")
                CustomPizza[session["name"]] = {"crust": pastorders[session["name"]][k][c+2], "sauce": pastorders[session["name"]][k][c+3], "toppings": pastorders[session["name"]][k][c+4:c+int(pastorders[session["name"]][k][c+1])+1], "price": pastorders[session["name"]][k][c+int(pastorders[session["name"]][k][c+1])+1]}
                Custom = ["Custom", 3 + len(CustomPizza[session["name"]]["toppings"]), CustomPizza[session["name"]]["crust"], CustomPizza[session["name"]]["sauce"], str(CustomPizza[session["name"]]["toppings"]).replace("[", "").replace("]", "").replace("'",""), round(float(CustomPizza[session["name"]]["price"]), 2)]
                print(Custom)
                order[session["name"]].append(Custom)
                price[session["name"]] += Custom[len(Custom) - 1]
                CustomPizza[session["name"]] = {"crust": ingredients[0], "sauce": ingredients[3], "toppings": [], "price": 4}
        for item in pastorders[session["name"]][k]:
            if item in ingredients:
                continue
            elif item == '':
                continue
            elif item.isdigit():
                continue
            elif "." in item:
                continue
            elif item == session["name"]:
                continue
            elif item == "Custom":
                continue
            elif item == "Done":
                continue
            elif item == "Tomatosauce":
                continue
            elif item == pastorders[session["name"]][k][-1]:
                continue
            else:
                order[session["name"]].append(item)
                price[session["name"]] += dicktionary[item][1]
        return redirect('/cart')
    return render_template('account.html', anon = anon, porder = pastorders[session["name"]], Dictionary = dicktionary)

@app.route('/hpage', methods=['GET'])
def homepage():
    global ft
    ft[session["name"]] = 1
    return render_template('homepage.html')

@app.route('/pizza', methods=['POST', 'GET'])
def Pizza():
    if request.method == "POST":
        k = str(request.args.keys()).replace("dict_keys(['", "").replace("'])", "")
        if "cu" in k:
            k = k.replace("cu","")
            price[session["name"]] -= order[session["name"]][int(k)][5]
            del order[session["name"]][int(k)]
        else:    
            adddelItem()
        return redirect('/cart')
    return render_template('pizzas.html')
    
@app.route('/drinks', methods=['GET', 'POST'])
def Drinks():
    return render_template('drinks.html')

@app.route('/desserts', methods=['GET', 'POST'])
def Desserts():
    return render_template('desserts.html')

@app.route('/custpizza', methods=['GET', 'POST'])
def Custpizza():
    global CustomPizza, ingredients, prices, price, order
    if request.method == "POST":
        if request.args.keys():
            ingr = int(str(request.args.keys()).replace("dict_keys(['", "").replace("'])", ""))
        else:
            ingr = int(request.form.get('stuff'))
        print(ingr)
        if ingr <= 2: 
            CustomPizza[session["name"]]["price"] -= prices[ingredients.index(CustomPizza[session["name"]]["crust"])]
            CustomPizza[session["name"]]["crust"] = ingredients[ingr]
            CustomPizza[session["name"]]["price"] += prices[ingr]
            print(CustomPizza[session["name"]])
            return render_template('custprice.html', Price = round(float(CustomPizza[session["name"]]["price"]), 2))
        elif ingr == 21:
            Custom = ["Custom", 3 + len(CustomPizza[session["name"]]["toppings"]), CustomPizza[session["name"]]["crust"], CustomPizza[session["name"]]["sauce"], str(CustomPizza[session["name"]]["toppings"]).replace("[", "").replace("]", "").replace("'",""), round(float(CustomPizza[session["name"]]["price"]), 2)]
            order[session["name"]].append(Custom)
            price[session["name"]] += Custom[len(Custom) - 1]
            print(Custom)
            CustomPizza[session["name"]] = {"crust": ingredients[0], "sauce": ingredients[3], "toppings": [], "price": 4}
            print(CustomPizza)
            print(order)
            return redirect('/custpizza')
        elif ingr > 6:
            if ingredients[ingr] in CustomPizza[session["name"]]["toppings"]:
                CustomPizza[session["name"]]["toppings"].remove(ingredients[ingr])
                CustomPizza[session["name"]]["price"] -= prices[ingr]
                return render_template('custprice.html', Price = round(float(CustomPizza[session["name"]]["price"]), 2))
            else:
                CustomPizza[session["name"]]["toppings"].append(ingredients[ingr])
                CustomPizza[session["name"]]["price"] += prices[ingr]
                return render_template('custprice.html', Price = round(float(CustomPizza[session["name"]]["price"]), 2))
        elif ingr > 2:
            CustomPizza[session["name"]]["price"] -= prices[ingredients.index(CustomPizza[session["name"]]["sauce"])]
            CustomPizza[session["name"]]["sauce"] = ingredients[ingr]
            CustomPizza[session["name"]]["price"] += prices[ingr]
            return render_template('custprice.html', Price = CustomPizza[session["name"]]["price"])
    CustomPizza[session["name"]] = {"crust": ingredients[0], "sauce": ingredients[3], "toppings": [], "price": 4}
    return render_template('custpizza.html', Price = round(float(CustomPizza[session["name"]]["price"]), 2))

@app.route('/testinGet', methods=['GET'])
def getting():
    return pizzas
