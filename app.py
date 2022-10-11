from flask import Flask, render_template, json, redirect, request, url_for
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)
# DB connection info
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_calhounn'
app.config['MYSQL_PASSWORD'] = '3792' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_calhounn'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)

# Routes
# home page
@app.route('/')
def home():
    return redirect('/Merchants')   # render_template("Merchants.j2")

@app.route('/Merchants', methods=['POST', 'GET'])
def merchants():
    """Displays and updates Merchants table."""
    # add a merchant
    if request.method == 'POST':
        if request.form.get('Add_Merchant'):
            merchant_name = request.form['merchant_name']
            race = request.form['race']
            shop_name = request.form['shop_name']
            gold = request.form['gold']
            Locations_locationID = request.form['location']    

            query = 'INSERT INTO Merchants (merchant_name, race, shop_name, gold, Locations_locationID) VALUES (%s, %s, %s, %s, %s);'    
            cur = mysql.connection.cursor()
            cur.execute(query, (merchant_name, race, shop_name, gold, Locations_locationID))
            mysql.connection.commit()
        
        return redirect('/Merchants')

    # display merchants
    if request.method == 'GET':
        query = 'SELECT merchantID, merchant_name, race, shop_name, gold, Locations.location_name AS location FROM Merchants INNER JOIN Locations ON Merchants.Locations_locationID = Locations.locationID;'
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        query2 = 'SELECT locationID, location_name FROM Locations;'
        cur = mysql.connection.cursor()
        cur.execute(query2)
        location_data = cur.fetchall()
        
        return render_template('Merchants.j2', data=data, location_data=location_data)

@app.route('/Merchants_delete/<int:id>')
def delete_merchant(id):
    """Receives merchant id, deletes a merchant from the Merchant table"""
    query = "DELETE FROM Merchants WHERE merchantID= '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    # Return to merchants page after removing merchant
    return redirect("/Merchants")

@app.route('/Items', methods = ['POST', 'GET'])
def items():
    """Display and add an item to Items table."""
    # add an item
    if request.method == 'POST':
        if request.form.get('Add_Item'):
            item_name = request.form['item_name']
            item_class = request.form['class']
            damage = request.form['damage']
            weight = request.form['weight']
            value = request.form['value']
            category = request.form['Categories_categoryID']
            enchantment = request.form['Enchantments_enchantmentID']

            # if enchantment is Null
            if enchantment == '0':
                query = 'INSERT INTO Items (item_name, class, damage, weight, value, Categories_categoryID) VALUES (%s, %s, %s, %s, %s, %s);'
                cur = mysql.connection.cursor()
                cur.execute(query, (item_name, item_class, damage, weight, value, category))
                mysql.connection.commit()

            # enchantment not null
            else:
                query = 'INSERT INTO Items (item_name, class, damage, weight, value, Categories_categoryID, Enchantments_enchantmentID) VALUES (%s, %s, %s, %s, %s, %s, %s);'
                cur = mysql.connection.cursor()
                cur.execute(query, (item_name, item_class, damage, weight, value, category, enchantment))
                mysql.connection.commit()

            return redirect('/Items')

    # display items
    if request.method == 'GET':
        query = 'SELECT itemID, item_name, class, damage, weight, value, Categories.category_name AS category, Enchantments.enchantment_name AS enchantment FROM Items INNER JOIN Categories ON Items.Categories_categoryID = Categories.categoryID LEFT JOIN Enchantments ON Items.Enchantments_enchantmentID = Enchantments.enchantmentID;'
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = 'SELECT * FROM Categories;'
        cur = mysql.connection.cursor()
        cur.execute(query2)
        categories = cur.fetchall()

        query3 = 'SELECT enchantmentID, enchantment_name FROM Enchantments;'
        cur = mysql.connection.cursor()
        cur.execute(query3)
        enchantments = cur.fetchall()

    return render_template('Items.j2', data=data, categories=categories, enchantments=enchantments)

@app.route('/Items_delete/<int:id>')
def delete_item(id):
    """Receives items ID and deletes the item."""
    query = "DELETE FROM Items WHERE itemID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/Items")

@app.route('/Items_edit/<int:id>', methods=['POST', 'GET'])
def edit_item(id):
    """Edits an item already in the Items table."""
    # get item to edit
    if request.method == 'GET':
        query = "SELECT * FROM Items WHERE itemID = %s;" %(id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        item = cur.fetchall()

        query2 = "SELECT enchantmentID, enchantment_name FROM Enchantments"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        enchantments = cur.fetchall()

        query3 = "SELECT * FROM Categories"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        categories = cur.fetchall()

        return render_template("Edit_Item.j2", item=item, enchantments=enchantments, categories=categories)

    # update item
    if request.method == "POST":
        if request.form.get("Edit_Item"):
            id = request.form["itemID"]
            name = request.form["item_name"]
            item_class = request.form["class"]
            damage = request.form["damage"]
            weight = request.form["weight"]
            value = request.form["value"]
            category = request.form["Categories_categoryID"]
            enchantment = request.form["Enchantments_enchantmentID"]

            # null enchantment
            if enchantment == "0":
                query = "UPDATE Items SET Items.item_name = %s, Items.class = %s, Items.damage = %s, Items.weight = %s, Items.value = %s, Items.Categories_categoryID = %s, Items.Enchantments_enchantmentID = NULL WHERE Items.itemID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, item_class, damage, weight, value, category, id))
                mysql.connection.commit()

            else:
                query = "UPDATE Items SET Items.item_name = %s, Items.class = %s, Items.damage = %s, Items.weight = %s, Items.value = %s, Items.Categories_categoryID = %s, Items.Enchantments_enchantmentID = %s WHERE Items.itemID = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, item_class, damage, weight, value, category, enchantment, id))
                mysql.connection.commit()

            return redirect("/Items")

@app.route('/Merchants_Items/', defaults={'id': 0})
@app.route('/Merchants_Items/<int:id>', methods=['GET', 'POST'])
def merchants_items(id):
    """Display items a merchant has and add item to merchant."""
    # display merchants items
    if request.method == 'GET':
        # a request query to select the merchant
        if request.args:
            id = int(request.args.get('merchantID'))

        # no merchant selected, displays only select a merchant
        if id == 0:
            query = 'SELECT merchantID, merchant_name FROM Merchants;'
            cur = mysql.connection.cursor()
            cur.execute(query)
            merchants_list = cur.fetchall()

            return render_template('Merchants_Items.j2', merchants_list=merchants_list, id=id)

        # displays selected merchants items
        else:
            query = "SELECT itemID, item_name, class, damage, weight, value, Categories.category_name AS category, Enchantments.enchantment_name AS enchantment FROM Merchants_Items INNER JOIN Items on Merchants_Items.Items_itemID = Items.itemID LEFT JOIN Categories ON Items.Categories_categoryID = Categories.categoryID LEFT JOIN Enchantments ON Items.Enchantments_enchantmentID = Enchantments.enchantmentID WHERE Merchants_Items.Merchants_merchantID = '%s';"
            cur = mysql.connection.cursor()
            cur.execute(query, (id,))
            merchants_items = cur.fetchall()

            query = 'SELECT merchantID, merchant_name FROM Merchants;'
            cur = mysql.connection.cursor()
            cur.execute(query)
            merchants_list = cur.fetchall()

            query = "SELECT * FROM Merchants WHERE merchantID = '%s';"
            cur = mysql.connection.cursor()
            cur.execute(query, (id,))
            merchant = cur.fetchall()

            query = 'SELECT itemID, item_name FROM Items;'
            cur = mysql.connection.cursor()
            cur.execute(query)
            item_list = cur.fetchall()

            return render_template('Merchants_Items.j2', merchants_items = merchants_items, merchants_list = merchants_list, merchant=merchant, item_list=item_list)

    # add item to merchant
    if request.method == 'POST':
        if request.form.get('Add_Inventory'):
            merchantID = request.form['merchantID']
            itemID = request.form['itemID']

            query = 'INSERT INTO Merchants_Items (Merchants_merchantID, Items_itemID) VALUES (%s, %s);'
            cur = mysql.connection.cursor()
            cur.execute(query, (merchantID, itemID))
            mysql.connection.commit()

            return redirect(url_for('merchants_items', id=merchantID))


@app.route('/Merchants_Items_Delete/<int:merch_id>/<int:item_id>')
def delete_merchant_item(merch_id, item_id):
    """Deletes an item from Merchants_Items."""
    query = 'DELETE FROM Merchants_Items WHERE Merchants_merchantID = %s AND Items_itemID = %s;'
    cur = mysql.connection.cursor()
    cur.execute(query, (merch_id, item_id))
    mysql.connection.commit()

    return redirect(url_for('merchants_items', id=merch_id))


@app.route('/Categories', methods = ['POST', 'GET'])
def categories():
    """Displays categories and adds a category."""
    # display categories
    if request.method == "GET":
        query = "SELECT * FROM Categories;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template('Categories.j2', data=data)

    # add a category
    if request.method =="POST":
        if request.form.get('Add_Category'):
            category_name = request.form['category_name']

            query = 'INSERT INTO Categories (category_name) VALUES (%s);'    
            cur = mysql.connection.cursor()
            cur.execute(query, (category_name,))
            mysql.connection.commit()

            return redirect('/Categories')

@app.route('/Categories_delete/<int:id>')
def categoriesDelete(id):
    """Delete a category from Categories table."""
    query = "DELETE FROM Categories WHERE categoryID= '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect("/Categories")

@app.route('/Merchants_Categories/', defaults={'id': 0})
@app.route('/Merchants_Categories/<int:id>', methods=['GET', 'POST'])
def merchants_categories(id):
    """Displays all merchants in a category."""
    # displays merchants
    if request.method == 'GET':
        # request query for category to display
        if request.args:
            id = int(request.args.get('categoryID'))

        if id == 0: # list categories
            query = 'SELECT categoryID, category_name FROM Categories;'
            cur = mysql.connection.cursor()
            cur.execute(query)
            category_list = cur.fetchall()

            return render_template('Merchants_Categories.j2', category_list=category_list, id=id)

        # list merchants in selected category
        else: 

            query = "SELECT merchantID, merchant_name, race, shop_name, gold, Locations.location_name as Location FROM Merchants_Categories INNER JOIN Merchants on Merchants_Categories.Merchants_merchantID = Merchants.merchantID LEFT JOIN Locations ON Merchants.Locations_locationID = Locations.locationID WHERE Merchants_Categories.Categories_categoryID = '%s';"
            cur = mysql.connection.cursor()
            cur.execute(query, (id,))
            merchants_categories = cur.fetchall()

            query = 'SELECT merchantID, merchant_name FROM Merchants;'
            cur = mysql.connection.cursor()
            cur.execute(query)
            merchants_list = cur.fetchall()

            query = "SELECT * FROM Categories WHERE categoryID = '%s';"
            cur = mysql.connection.cursor()
            cur.execute(query, (id,))
            category = cur.fetchall()

            query = 'SELECT categoryID, category_name FROM Categories;'
            cur = mysql.connection.cursor()
            cur.execute(query)
            category_list = cur.fetchall()

            return render_template('Merchants_Categories.j2', merchants_categories = merchants_categories, merchants_list = merchants_list, category=category, category_list=category_list)
    
    # add a merchant to specific category
    if request.method == 'POST':
        if request.form.get('Add_Cat_Merch'):
            merchantID = request.form['merchantID']
            categoryID = request.form['categoryID']

            query = 'INSERT INTO Merchants_Categories (Merchants_merchantID, Categories_categoryID) VALUES (%s, %s);'
            cur = mysql.connection.cursor()
            cur.execute(query, (merchantID, categoryID))
            mysql.connection.commit()

            return redirect(url_for('merchants_categories', id=categoryID))

@app.route('/Merchants_Categories_Delete/<int:merchant_id>/<int:category_id>')
def delete_merchant_category(merchant_id, category_id):
    """Delete a merchant from a category."""
    query = 'DELETE FROM Merchants_Categories WHERE Merchants_merchantID = %s AND Categories_categoryID = %s;'
    cur = mysql.connection.cursor()
    cur.execute(query, (merchant_id, category_id))
    mysql.connection.commit()

    return redirect(url_for('merchants_categories', id=category_id))

@app.route('/Enchantments', methods = ['POST', 'GET'])
def enchantments():
    """Displays and adds enchantments."""
    # display enchantments
    if request.method == "GET":
        query = "SELECT * FROM Enchantments;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template('Enchantments.j2', data=data)

    # add enchantment
    if request.method =="POST":
        if request.form.get('Add_Enchantment'):
            enchantment_name = request.form['enchantment_name']
            school = request.form['school']
            if school == "":
                school = 'None'

            query = 'INSERT INTO Enchantments (enchantment_name, school) VALUES (%s, %s);'    
            cur = mysql.connection.cursor()
            cur.execute(query, (enchantment_name, school))
            mysql.connection.commit()

            return redirect('/Enchantments')

@app.route('/Enchantments_delete/<int:id>')
def delete_enchantment(id):
    """Delete an enchantment."""
    query = "DELETE FROM Enchantments WHERE enchantmentID= '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/Enchantments")

@app.route('/Locations', methods = ['POST', 'GET'])
def location():
    """Display and add a location."""
    # display locations
    if request.method == "GET":
        query = "SELECT * FROM Locations;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template('Locations.j2', data=data)
    
    # add location
    if request.method =="POST":
        if request.form.get('Add_Location'):
            hold = request.form['hold']
            location_name = request.form['location_name']
            location_type = request.form['location_type']

            query = 'INSERT INTO Locations (location_name, hold, type) VALUES (%s, %s, %s);'    
            cur = mysql.connection.cursor()
            cur.execute(query, (location_name, hold, location_type))
            mysql.connection.commit()

            return redirect('/Locations')

@app.route('/Locations_delete/<int:id>')
def delete_location(id):
    """Delete a location."""
    query = "DELETE FROM Locations WHERE locationID= '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    
    return redirect("/Locations")

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(host='http://flip2.engr.oregonstate.edu', port=55122, debug=True)