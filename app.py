# imports/dependencies
from flask import Flask, render_template, redirect
import scrape
import pymongo

app = Flask(__name__)

# Initialize PyMongo to work with MongoDBs
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data_entries


@app.route("/")     
def index():
    mars_data = list(db.collection.find())
    return render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def scraper():
    db.collection.remove({})
    mars_data = scrape.scrape()
    db.collection.insert(mars_data)
    return render_template('scrape.html')

if __name__ == "__main__":
    app.run(debug=True)