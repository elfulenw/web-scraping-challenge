# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app,uri = 'mongodb://localhost:27017/mission_to_mars_db')

@app.route('/')
def index():
    mars_data = mongo.db.mars_information.find_one()
    return render_template('index.html', data=mars_information)

@app.route('/scrape')
def scrape():
    scrape_mars = scrape_mars.scrape()
    print(scrape_mars)
    mongo.db.mars_information.update({}, scrape_mars, upsert=True)
    return redirect ('/', code=302)

if __name__ == '__main__'
    app.run(debug=True)