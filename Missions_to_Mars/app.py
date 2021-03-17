from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars

#Create instance of Flask
app = Flask(__name__)

#Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    #find one record of data from the mongo database
    mars_facts = mongo.db.mars_facts.find_one()

    #return the template
    return render_template("index.html", mars_facts = mars_facts)


@app.route("/scrape")
def scraper():
    #set collection
    mars_facts = mongo.db.mars_facts

    #run the scrape function on scrape_mars.py
    mars_data = scrape_mars.scrape()

    #Update the Mongo database using update and upsert=True
    mars_facts.update({}, mars_data, upsert=True)

    #Return back to the homepage
    return redirect("/")

#complete flask
if __name__ == "__main__":
    app.run(debug=True)


    
