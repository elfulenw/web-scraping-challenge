# Dependencies
from bs4 import BeautifulSoup
import pymongo
import pandas as pd
from splinter import Browser
import time

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mission_to_mars_db
collection = db.mars_information


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()


    # # NASA Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    # Create BeautifulSoup object; parse with html.parser
    news_soup = BeautifulSoup(browser.html, 'lxml')

    # Examine the results, then determine delement that contains sought info
    # print(news_soup.prettify())

    news_p = news_soup.find('div', class_='article_teaser_body').text
    news_title = news_soup.select_one('div.content_title a').text

    # # JPL Mars Space Images - Featured Image
    # featured_image_url
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # response = requests.get(featured_image_url)
    browser.visit(featured_image_url)
    time.sleep(3)

    browser.is_element_present_by_id('full_image')

    img_btn = browser.find_by_id('full_image', wait_time=1)
    img_btn.click()

    browser.is_text_present('more info')
    more_btn = browser.find_link_by_partial_text('more info')

    more_btn.click()
    html_image = browser.html
    image_soup = BeautifulSoup(html_image, 'lxml')

    featured_image_url = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_url}'

    # # Mars Facts
    # Read Mars Facts into Pandas
    mars_df = pd.read_html('https://space-facts.com/mars/')[0]
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    time.sleep(3)

    # Pandas to html
    mars_facts = mars_df.to_html(classes='table table-stripped thread-dark')


    # # Mars Hemispheres
    #  Visit the USGS Astrogeology site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(3)

    html_hem = browser.html
    hem_soup = BeautifulSoup(html_image, 'lxml')

    hemisphere_image_urls = []

    # Generate list of all the hemispheres
    links = browser.find_by_css('a.product-item h3')
    for item in range(len(links)):
        hemisphere_info = {}
        
        browser.find_by_css('a.product-item h3')[item].click()
        
        sample_image = browser.find_link_by_text('Sample').first
        hemisphere_info['image_url'] = sample_image['href']
        
        hemisphere_info['title'] = browser.find_by_css('h2.title').text
        
        hemisphere_image_urls.append(hemisphere_info)
        
        browser.back()

    hemisphere_image_urls

    mars_data = {
        'title': news_title,
        'paragraph': news_p,
        'featured_image':featured_image_url,
        'facts': mars_facts,
        'hemi': hemisphere_image_urls
    }

    return mars_data
