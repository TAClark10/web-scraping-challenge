from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#  create route that renders index.html template

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# scrape
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_info = scrape_mars.scrape_info()
   mars.update({}, mars_info, upsert=True)
   return redirect("/")

if __name__ == "__main__":
   app.run(port=5001)