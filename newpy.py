from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
 
app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "admin"
DB_USER = "proj_admin"
DB_PASS = "password"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
def get_restaurants(name=None, cuisine=None, rating=None):
    #conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()

    query = "SELECT * FROM restaurant WHERE 1=1"
    if name:
        query += f" AND name = '{name}'"
    if cuisine:
        query += f" AND cuisine = '{cuisine}'"
    if rating:
        query += f" AND rating = '{rating}'"

    c.execute(query)
    restaurants = c.fetchall()
    conn.close()
    
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
        print(i) 
    conn.close()

top_5dishes(1)