{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Dependencies\n",
    "from bs4 import BeautifulSoup\n",
    "import pymongo\n",
    "import pandas as pd\n",
    "from splinter import Browser"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Initialize PyMongo to work with MongoDBs\n",
    "conn = 'mongodb://localhost:27017'\n",
    "client = pymongo.MongoClient(conn)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Define database and collection\n",
    "db = client.mission_to_mars_db\n",
    "collection = db.mars_information"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "def init_browser():\n",
    "    executable_path = {\"executable_path\": \"/usr/local/bin/chromedriver\"}\n",
    "    return Browser(\"chrome\", **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "browser = init_browser()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# NASA Mars News"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# URL of page to be scraped\n",
    "url = 'https://mars.nasa.gov/news/'\n",
    "browser.visit(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create BeautifulSoup object; parse with html.parser\n",
    "news_soup = BeautifulSoup(browser.html, 'lxml')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Examine the results, then determine delement that contains sought info\n",
    "# print(news_soup.prettify())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "\"NASA Readies Perseverance Mars Rover's Earthly Twin \""
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "news_title = news_soup.select_one('div.content_title a').text\n",
    "news_title"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "\"Did you know NASA's next Mars rover has a nearly identical sibling on Earth for testing? Even better, it's about to roll for the first time through a replica Martian landscape.\""
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "news_p = news_soup.find('div', class_='article_teaser_body').text\n",
    "news_p"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# JPL Mars Space Images - Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "# featured_image_url\n",
    "featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "# response = requests.get(featured_image_url)\n",
    "browser.visit(featured_image_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "browser.is_element_present_by_id('full_image')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "img_btn = browser.find_by_id('full_image', wait_time=1)\n",
    "img_btn.click()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "browser.is_text_present('more info')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/allred/anaconda3/envs/PythonData/lib/python3.8/site-packages/splinter/driver/webdriver/__init__.py:490: FutureWarning: browser.find_link_by_partial_text is deprecated. Use browser.links.find_by_partial_text instead.\n",
      "  warnings.warn(\n"
     ]
    }
   ],
   "source": [
    "more_btn = browser.find_link_by_partial_text('more info')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "more_btn.click()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "html_image = browser.html"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA17761_hires.jpg\n"
     ]
    }
   ],
   "source": [
    "image_soup = BeautifulSoup(html_image, 'lxml')\n",
    "\n",
    "featured_image_url = image_soup.find('figure', class_='lede').a['href']\n",
    "featured_image_url = f'https://www.jpl.nasa.gov{featured_image_url}'\n",
    "print(featured_image_url)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "                      0                              1\n",
      "0  Equatorial Diameter:                       6,792 km\n",
      "1       Polar Diameter:                       6,752 km\n",
      "2                 Mass:  6.39 × 10^23 kg (0.11 Earths)\n",
      "3                Moons:            2 (Phobos & Deimos)\n",
      "4       Orbit Distance:       227,943,824 km (1.38 AU)\n",
      "5         Orbit Period:           687 days (1.9 years)\n",
      "6  Surface Temperature:                   -87 to -5 °C\n",
      "7         First Record:              2nd millennium BC\n",
      "8          Recorded By:           Egyptian astronomers\n"
     ]
    }
   ],
   "source": [
    "# Read Mars Facts into Pandas\n",
    "mars_df = pd.read_html('https://space-facts.com/mars/')[0]\n",
    "print(mars_df)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Value</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Description</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Equatorial Diameter:</th>\n",
       "      <td>6,792 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Polar Diameter:</th>\n",
       "      <td>6,752 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Mass:</th>\n",
       "      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Moons:</th>\n",
       "      <td>2 (Phobos &amp; Deimos)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Orbit Distance:</th>\n",
       "      <td>227,943,824 km (1.38 AU)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Orbit Period:</th>\n",
       "      <td>687 days (1.9 years)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Surface Temperature:</th>\n",
       "      <td>-87 to -5 °C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>First Record:</th>\n",
       "      <td>2nd millennium BC</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Recorded By:</th>\n",
       "      <td>Egyptian astronomers</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                              Value\n",
       "Description                                        \n",
       "Equatorial Diameter:                       6,792 km\n",
       "Polar Diameter:                            6,752 km\n",
       "Mass:                 6.39 × 10^23 kg (0.11 Earths)\n",
       "Moons:                          2 (Phobos & Deimos)\n",
       "Orbit Distance:            227,943,824 km (1.38 AU)\n",
       "Orbit Period:                  687 days (1.9 years)\n",
       "Surface Temperature:                   -87 to -5 °C\n",
       "First Record:                     2nd millennium BC\n",
       "Recorded By:                   Egyptian astronomers"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mars_df.columns=[\"Description\", \"Value\"]\n",
    "mars_df.set_index(\"Description\", inplace=True)\n",
    "mars_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Pandas to html\n",
    "mars_df.to_html('table.html')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Mars Hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "#  Visit the USGS Astrogeology site\n",
    "executable_path = {\"executable_path\": \"/usr/local/bin/chromedriver\"}\n",
    "browser = Browser(\"chrome\", **executable_path, headless=False)\n",
    "url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "browser.visit(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [],
   "source": [
    "html_hem = browser.html\n",
    "hem_soup = BeautifulSoup(html_image, 'lxml')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [],
   "source": [
    "hemisphere_image_urls = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/allred/anaconda3/envs/PythonData/lib/python3.8/site-packages/splinter/driver/webdriver/__init__.py:498: FutureWarning: browser.find_link_by_text is deprecated. Use browser.links.find_by_text instead.\n",
      "  warnings.warn(\n"
     ]
    }
   ],
   "source": [
    "# Generate list of all the hemispheres\n",
    "links = browser.find_by_css('a.product-item h3')\n",
    "for item in range(len(links)):\n",
    "    hemisphere_info = {}\n",
    "    \n",
    "    browser.find_by_css('a.product-item h3')[item].click()\n",
    "    \n",
    "    sample_image = browser.find_link_by_text('Sample').first\n",
    "    hemisphere_info['image_url'] = sample_image['href']\n",
    "    \n",
    "    hemisphere_info['title'] = browser.find_by_css('h2.title').text\n",
    "    \n",
    "    hemisphere_image_urls.append(hemisphere_info)\n",
    "    \n",
    "    browser.back()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[{'image_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',\n",
       "  'title': 'Cerberus Hemisphere Enhanced'},\n",
       " {'image_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',\n",
       "  'title': 'Schiaparelli Hemisphere Enhanced'},\n",
       " {'image_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',\n",
       "  'title': 'Syrtis Major Hemisphere Enhanced'},\n",
       " {'image_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg',\n",
       "  'title': 'Valles Marineris Hemisphere Enhanced'}]"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "hemisphere_image_urls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  },
  "varInspector": {
   "cols": {
    "lenName": 16,
    "lenType": 16,
    "lenVar": 40
   },
   "kernels_config": {
    "python": {
     "delete_cmd_postfix": "",
     "delete_cmd_prefix": "del ",
     "library": "var_list.py",
     "varRefreshCmd": "print(var_dic_list())"
    },
    "r": {
     "delete_cmd_postfix": ") ",
     "delete_cmd_prefix": "rm(",
     "library": "var_list.r",
     "varRefreshCmd": "cat(var_dic_list()) "
    }
   },
   "types_to_exclude": [
    "module",
    "function",
    "builtin_function_or_method",
    "instance",
    "_Feature"
   ],
   "window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
