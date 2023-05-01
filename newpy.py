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
def get_restaurants(name):
    #conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()

    query = "select r.r_name,r.r_image_link,d.dish_image_link from restaurants as r join Restaurant_Items as i on i.r_id=r.r_id join Restaurant_Dish as d on d.dish_id=i.dish_id "
    if name:
        query += f" where r_name = '{name}'"
    

    c.execute(query)
    restaurants = c.fetchall()
    conn.close()
    for i in restaurants:
        print (i)
    return restaurants
def top_5dishes(id):
    c=conn.cursor()
    query="SELECT d.dish_name, i.rating,d.dish_image_link FROM Restaurant_Dish AS d JOIN Restaurant_Items AS i ON d.dish_id = i.dish_id "
    query+=f" where i.r_id='{id}'"
    c.execute(query)

    dishes = c.fetchall()
    sorted_list = sorted(dishes, key=lambda x: x[1], reverse=True)[:5]
    # sort(dishes)
    for i in sorted_list:
        # Open the image file
        image = Image.open(i[2])
        image.show()
 
    conn.close()

# top_5dishes(2)
get_restaurants('Saffron Spice')
