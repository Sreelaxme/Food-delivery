
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

@app.route('/')
def top_5_restaurants():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    c = conn.cursor()
    query = "SELECT * FROM Restaurants ORDER BY rating DESC LIMIT 5"
    c.execute(query)
    restaurants = c.fetchall()
    session['top_restaurants'] = restaurants
    session['loggedInCustomers'] = False
    session['veg'] =False
    # conn.close()
    return render_template('index.html', results=restaurants,loggedIn = False)
@app.route('/')
def logout():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    session['loggedInCustomers'] = False
    return render_template('index.html',loggedIn=False)

@app.route('/login_check', methods = ['POST','GET'])
def login_check():
    user_type = request.form['user_type']
    session['user_type']=user_type
    if user_type == '0':
        return render_template('login-customer.html')
    elif user_type == '1':
        return render_template('login-restaurant.html')
    elif user_type == '2':
        return render_template('login-delivery.html')


@app.route('/login',methods=['POST','GET'])
def login():
    name = request.form['name']
    session['name']=name

    password = request.form['password']
    session['password'] = password
    user_type = session['user_type']
    # try:
    conn=psycopg2.connect(dbname=DB_NAME, user=name+password, password=password, host=DB_HOST)
    if user_type == '0':
        session['loggedInCustomers'] = True
        return render_template('index.html',results = session['top_restaurants'] ,loggedIn=True,name=name)
    if user_type =='1':
        return render_template('rest.html',loggedIn=True,name=name)
    if user_type =='2':
        # return render_template('deliveryhome.html',loggedIn=True,name=name)
        return deliveryview()

    # except:
    #     flash('Invalid Login')
    #     if user_type == '0':
    #         return render_template('login-customer.html')
    #     elif user_type == '1':
    #         return render_template('login-restaurant.html')
    #     elif user_type == '2':
    #         return render_template('login-delivery.html')

@app.route('/',methods = ['POST'])
def fillcomplaint():
    name = request.form['name']
    email = request.form['email-id']
    message = request.form['message']
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute('INSERT INTO complaints (name,email,message) values(%s,%s,%s)',(name,email,message))
        conn.commit()
    except:
        flash('DIDnt enter')
    if session['loggedInCustomers']==True:
        return render_template('index.html',loggedIn=session['loggedInCustomers'],results= session['top_restaurants'],name = session['name'])
    else :
        return render_template('index.html',loggedIn=session['loggedInCustomers'],results= session['top_restaurants'])
    
    
@app.route('/register',methods=['POST','GET'])
def register():
    user_type = session['user_type']
    name = (request.form['name'])
    building_name = request.form['Bname']
    city = request.form['city']
    pin = request.form['pin']
    ph = request.form['phno']
    # return render_template("tral.html",name = '"'+name+'"')
    user_name=session['name']+session['password']
    conn = psycopg2.connect(dbname=DB_NAME, user=user_name, password=session['password'], host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if user_type == '0':
        email = request.form['email-id']
        c=cursor.execute(f'INSERT INTO CUSTOMER (c_name,phone_no,email_id) values(%s,{ph},%s)',(name,email))
        conn.commit()
        name = "'"+(name)+"'"
        c2=cursor.execute(f'SELECT customer_id from customer where c_name = {name}')
        c_id=cursor.fetchone()[0]
        c1 = cursor.execute(f'INSERT INTO CUSTOMER_Address (customer_id,building_name,city,pin_code) values({c_id},%s,%s,{pin})',(building_name,city))
        flash(f'Ur password is {c_id}')
        conn.commit()
        return render_template('login-customer.html')
    elif user_type == '1':
        gstno = request.form['gst_no']
        image_url = request.form['img_link']
        c=cursor.execute(f'INSERT INTO restaurants (r_name,r_phone_no,r_image_link,gst_no) values(%s,{ph},%s,{gst_no})',(name,image_url))
        conn.commit()
        name = "'"+(name)+"'"
        c2=cursor.execute(f'SELECT r_id from restaurants where r_name={name}')
        r_id=cursor.fetchone()[0]
        c1 = cursor.execute(f'INSERT INTO restaurant_Address (r_id,building_name,city,pin_code) values({r_id},%s,%s,{pin})',(building_name,city))
        flash(f'Ur password is {r_id}')
        return render_template('login-restaurant.html')
    elif user_type == '2':
        c=cursor.execute(f'INSERT INTO deliveryboy (name,ph_no) values(%s,%s)',(name,ph))
        conn.commit()
        name = "'"+(name)+"'"
        c2=cursor.execute(f'SELECT id from deliveryboy where name={name}')
        d_id=cursor.fetchone()[0]
        city = "'"+city+"'"
        c1 = cursor.execute(f'INSERT INTO delivery_Address (deliveryboy_id,city,pin_code) values({d_id},{city},{pin})')
        flash(f'Ur password is {d_id}')
        conn.commit()
        return render_template('login-delivery.html')

@app.route('/deliveryview')
def deliveryview():
    id = session['password']
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c = cursor.execute(f'SELECT * from order_Address_view where deliveryboy_id= {id}')
    c1 = cursor.fetchone()
    return render_template('deliveryhome.html',results = c1)
@app.route('/dish')
def restaurant_dish():
    user_name=session['name']+session['password']
    conn = psycopg2.connect(dbname=DB_NAME, user=user_name, password=session['password'], host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c = cursor.execute(f'SELECT dish_id,dish_name,dish_image_link from restaurant_dish')
    dishes = cursor.fetchall()
    return render_template('rest.html',results = dishes)

@app.route('/items')
def restaurant_items():
    id = session['password']
    user_name=session['name']+session['password']
    conn = psycopg2.connect(dbname=DB_NAME, user=user_name, password=session['password'], host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c = cursor.execute(f'SELECT d.dish_name,i.item_cost,i.available from restaurant_dish as d join restaurant_items as i on d.dish_id=i.dish_id where i.r_id = {id}')
    items = cursor.fetchall()
    return render_template('restmenu.html',results = items)

@app.route('/restaurants',methods = ['POST'])
def all_restaurants():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    c = conn.cursor()
    query = "SELECT r_id,r_name FROM Restaurants ORDER BY rating "
    c.execute(query)
    restaurants = c.fetchall()
    session['top_restaurants'] = restaurants
    session['loggedInCustomers'] = False
    session['veg'] =False
    # conn.close()
    return render_template('restaurant_list.html', results=restaurants,loggedIn = True)

@app.route('/dishes', methods=['POST'])
def all_dishes():
    # user_name=session['name']+session['password']
    restaurant_id = request.form['restaurant_id']
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    c = conn.cursor()
    query = f"SELECT d.dish_name,d.cousine,d.dish_image_link,d.vegetarian,d.dish_id FROM Restaurant_dish as d join restaurant_items as i on d.dish_id=i.dish_id where i.r_id = {restaurant_id}"
    if request.form.get('cuisine'):
        query +=f"and d.cousine = {cuisine}"
    else:
        pass
    if request.form.get('veg'):
        query+=f"and d.vegetarian = 't'"
    else:
        pass
    c.execute(query)
    dishes = c.fetchall()
    return render_template('restaurant_ordering.html',results = dishes)

@app.route('/cart',methods = ['POST'])
def cart():
    user_name=session['name']+session['password']
    restaurant_id = request.form['restaurant_id']
    dish_id = request.form['dish_id']
    conn = psycopg2.connect(dbname=DB_NAME, user=user_name, password=session['password'], host=DB_HOST)
    c = conn.cursor()

    query = f"select item_id from restaurant_items where dish_id = {dish_id } and r_id = {restaurant_id}"
    c.execute(query)
    item_id = c.fetchone()[0]

#update time
#display

# def home():

  
#     return render_template('index.html')
# @app.route('/', methods=['GET','POST'])
# def get_restaurants():
#     #conn = sqlite3.connect('restaurant.db')
#     c = conn.cursor()

#     query = "select r.r_name,r.r_image_link,d.dish_image_link from restaurants as r join Restaurant_Items as i on i.r_id=r.r_id join Restaurant_Dish as d on d.dish_id=i.dish_id "
    
#     query += f" where r_name = 'Saffron Spice'"
    

#     c.execute(query)
#     restaurants = c.fetchall()
#     conn.close()
#     for i in restaurants:
#         print (i)
#     return render_template('rest.html',restaurant=restaurants)
# # with app.app_context():
# #     get_restaurants('Saffron Spice')
# @app.route('/dishes', methods=['GET','POST'])
# def top_5dishes(name,veg = None, cuisine = None ):
#     c=conn.cursor()
#     query1= "SELECT r_id from restaurants"
#     query1 += f" where r_name = '{name}'"
#     c.execute(query1)
#     id = c.fetchone()
#     # print(type(id[0]))

#     query="SELECT d.dish_name, i.rating,d.dish_image_link FROM Restaurant_Dish AS d JOIN Restaurant_Items AS i ON d.dish_id = i.dish_id "
#     query+=f" where i.r_id='{id[0]}'"
#     if veg:
#         query+=f" and d.vegetarian='t'"
#     if cuisine:
#         query+=f" and d.cousine ='{cuisine}'"

#     c.execute(query)

#     dishes = c.fetchall()
#     sorted_list = sorted(dishes, key=lambda x: x[1], reverse=True)[:5]
#     # sort(dishes)
#     for i in sorted_list:
#         # Open the image file
#         image = Image.open(i[2])
#         image.show()
 
#     conn.close()
#     return render_template('dishes.html',top5dishes=sorted_list)





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
# @app.route('/add_to_cartlist')
# def add_to_cartlist():
#     # Retrieve the ID of the currently logged in user from the Flask session
#     customer_id = session.get('customer_id')

#     # Retrieve the item ID and quantity from the request
#     item_id = request.args.get('item_id')
#     quantity = request.args.get('quantity')

#     # Insert a new row into the Customer_cartlist table with the retrieved customer ID
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO Customer_cartlist ( item_id, customer_id, number) VALUES ( %s, %s, %s)", (item_id, customer_id, quantity))
#     conn.commit()

#     return "Item added to cartlist!"




if __name__ == "__main__":
    app.run(debug=True)