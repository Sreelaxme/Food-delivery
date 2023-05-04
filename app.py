from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from PIL import Image 
 
app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "admin"
DB_USER = "proj_admin"
DB_PASS = "password"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
@app.route('/')
def home():
  
    return render_template('index.html')
@app.route('/', methods=['GET','POST'])
def get_restaurants():
    #conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()

    query = "select r.r_name,r.r_image_link,d.dish_image_link from restaurants as r join Restaurant_Items as i on i.r_id=r.r_id join Restaurant_Dish as d on d.dish_id=i.dish_id "
    
    query += f" where r_name = 'Saffron Spice'"
    

    c.execute(query)
    restaurants = c.fetchall()
    conn.close()
    for i in restaurants:
        print (i)
    return render_template('rest.html',restaurant=restaurants)
# with app.app_context():
#     get_restaurants('Saffron Spice')
@app.route('/dishes', methods=['GET','POST'])
def top_5dishes(name,veg = None, cuisine = None ):
    c=conn.cursor()
    query1= "SELECT r_id from restaurants"
    query1 += f" where r_name = '{name}'"
    c.execute(query1)
    id = c.fetchone()
    # print(type(id[0]))

    query="SELECT d.dish_name, i.rating,d.dish_image_link FROM Restaurant_Dish AS d JOIN Restaurant_Items AS i ON d.dish_id = i.dish_id "
    query+=f" where i.r_id='{id[0]}'"
    if veg:
        query+=f" and d.vegetarian='t'"
    if cuisine:
        query+=f" and d.cousine ='{cuisine}'"

    c.execute(query)

    dishes = c.fetchall()
    sorted_list = sorted(dishes, key=lambda x: x[1], reverse=True)[:5]
    # sort(dishes)
    for i in sorted_list:
        # Open the image file
        image = Image.open(i[2])
        image.show()
 
    conn.close()
    return render_template('dishes.html',top5dishes=sorted_list)

# def top_5drestaurants():
#     c=conn.cursor()
   

#     query="SELECT * FROM Restaurants order by rating DESC limit 5"
   
#     c.execute(query)
#     rest=c.fetchall()
    
#     # sort(dishes)
#     for i in rest:
#         # Open the image file
#         # image = Image.open(i[4    ])
#         # image.show()
#         print(i)
 
#     conn.close()
# def restaurants(pin=None,status = None):
#     c=conn.cursor()
   

#     query="SELECT r.r_name,r.rating FROM Restaurants as r join restaurant_address as a on a.r_id=r.r_id where 1=1"
#     if pin :
#         query+=f" and a.pin_code='{pin}' "
#     if status:
#         query+=f"and r.status='t'"
#     query+=f" order by r.rating "
#     c.execute(query)
#     rest=c.fetchall()
    
#     # sort(dishes)
#     for i in rest:
#         # Open the image file
#         # image = Image.open(i[4    ])
#         # image.show()
#         print(i)
 
#     conn.close()

# # top_5drestaurants()
# # get_restaurants('Saffron Spice')

# #top5 dishes of a restaurant and all dishes
# restaurants()

# #do route
# @app.route()
# def loginCustomer():

   
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
    
 
#         # Check if account exists using pSQL
#         cursor.execute('SELECT loginCustomer(%s, %d)',(username,password))

    
#         accountUser = cursor.fetchone()
#         if accountUser:
#             return redirect(url_for('restaurants'))
#         else:
#             return redirect(url_for('loginCustomer'))
#         #give proper url


# @app.route()
# def loginRestaurants():

   
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
    
 
#         # Check if account exists using pSQL
#         cursor.execute('SELECT loginRest(%s, %d)',(username,password))

    
#         accountUser = cursor.fetchone()
#         if accountUser:
#             return redirect(url_for('restaurants'))
#         else:
#             return redirect(url_for('loginRestaurants'))
#         #give proper url

# @app.route()
# def loginDeliverBoy():

   
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
    
 
#         # Check if account exists using pSQL
#         cursor.execute('SELECT loginDelivery(%s, %d)',(username,password))

    
#         accountUser = cursor.fetchone()
#         if accountUser:
#             return redirect(url_for('restaurants'))
#         else:
#             return redirect(url_for('loginRestaurants'))
# @app.route()
# def loginCustomers():

   
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
    
 
#         # Check if account exists using pSQL
#         cursor.execute('SELECT loginCustomer(%s, %d)',(username,password))

    
#         accountUser = cursor.fetchone()
#         if accountUser:
#             return redirect(url_for('restaurants'))
#         else:
#             return redirect(url_for('loginRestaurants'))

# @app.route()
# def RegisterCustomers():

   
    
#   if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         phone = request.form['phone']
#         who = request.form['Type']
    
 
#         # Check if account exists using pSQL
#         cursor.execute('SELECT loginCustomer(%s, %d)',(username,password))

    
#         accountUser = cursor.fetchone()
#         if accountUser:
#             return redirect(url_for('restaurants'))
#         else:
#             return redirect(url_for('loginRestaurants'))


# Define a Flask route that inserts a new row into the Customer_cartlist table
@app.route('/add_to_cartlist')
def add_to_cartlist():
    # Retrieve the ID of the currently logged in user from the Flask session
    customer_id = session.get('customer_id')

    # Retrieve the item ID and quantity from the request
    item_id = request.args.get('item_id')
    quantity = request.args.get('quantity')

    # Insert a new row into the Customer_cartlist table with the retrieved customer ID
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Customer_cartlist ( item_id, customer_id, number) VALUES ( %s, %s, %s)", (item_id, customer_id, quantity))
    conn.commit()

    return "Item added to cartlist!"




if __name__ == "__main__":
    app.run(debug=True)