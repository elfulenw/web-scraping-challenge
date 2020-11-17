# Mission to Mars Web Scraping

The Mission to Mars web application scrapes images and information from the mars.nasa.gov website including the the latest headline and paragraph, featured image, facts about Mars and the hemisphere images.  

The initial scraping is located in the 'mission_to_mars.ipynb'.  Items scraped include: the latest news title and paragraph text, the JPL featured space image, Mars facts (diameter, mass, etc), and the high resolution images for each of Mars's hemispheres.  

All of this infomation is housed in a Mongo database with a Flask template application to create a new website using HTML to display all of the scraped information.  The '/scrape' route imports the 'scrape_mars_py' script and stores the return value in Mongo as a Python dictionary.  The '/' route queries the Mongo database and passes the scraped data into the HTML template to display on the website.  
