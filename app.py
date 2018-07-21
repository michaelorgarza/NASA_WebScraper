# imports/dependencies
from flask import Flask, render_template, redirect
from pymongo import MongoClient
import scrape


# mongo connection
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mars_db'
app.config['MONGO_URI'] = 'mongodb://micahelorgarza:Sanders2016@ds147451.mlab.com:47451/mars_db' 

client = pymongo.MongoClient('mongodb://micahelorgarza:Sanders2016@ds147451.mlab.com:47451/mars_db')
db = client.mars_db
collection = db.mars_data_scrape

@app.route("/")     
def index():
    mars = list(db.collection.find())[0]
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    db.collection.remove({})
    mars = scrape.scrape()
    db.collection.insert_one(mars)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)