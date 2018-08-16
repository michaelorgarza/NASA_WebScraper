# dependencies 
from bs4 import BeautifulSoup as bs
from requests import get 
import requests as req
from pprint import pprint
import pandas as pd
import splinter
from splinter import Browser
import time


def index_broswer():
    executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    """" Scrapes info from desired websites"""

    Browser = index_broswer()
    mars_data = {}

    # NASA headline scraper
    url = "https://mars.nasa.gov/news/" 
    response = req.get(url)
    html_soup = bs(response.text, 'html.parser')
    news_title = html_soup.find('div', class_='content_title').text.strip()
    news_p = html_soup.find('div', class_="rollover_description_inner").text.strip()
    # updating dictionary into mongodb
    mars_data["nasa_headline"] = news_title
    mars_data["nasa_text"] = news_p

    # JPL Images scraper
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    Browser.visit(url_2)
    time.sleep(1)
    Browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    expand = Browser.find_by_css('a.fancybox-expand')
    expand.click()
    time.sleep(1)
    jpl_html = Browser.html
    jpl_soup = bs(jpl_html, 'html.parser')
    img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
    image_path = f'https://www.jpl.nasa.gov{img_relative}'
    #updating dictionary into mongo 
    mars_data["jpl_image"] = image_path


    # Mars weather scraper from Twitter 
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    Browser.visit(weather_url)
    time.sleep(1)
    weather_html = Browser.html
    weather_soup = bs(weather_html, 'html.parser')
    tweets = weather_soup.find('ol', class_='stream-items')
    tw_weather = tweets.find('p', class_="tweet-text").text
    # update collection in mongodb 
    mars_data["Mars_Weather"] = tw_weather


    # Mars Facts scraper
    url_4 = req.get("https://space-facts.com/mars/")
    facts_table = pd.read_html(url_4.text)
    facts_table
    df = facts_table[0]

    mars_html_tablestring = df.to_html()
    mars_html_tablestring.replace('\n', '')

    # Martian hemisphere scraper
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}
    
        Browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hemispheres_html = Browser.html
        hemispheres_soup = bs(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
        detail_links = Browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        Browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        Browser.windows.current = Browser.windows[-1]
        hemi_img_html = Browser.html
        Browser.windows.current = Browser.windows[0]
        Browser.windows[-1].close()
        hemi_img_soup = bs(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']
        hemi_dict['title'] = hemi_name.strip()
        hemi_dict['img_url'] = hemi_img_path
        hemi_dicts.append(hemi_dict)

    mars_data["Hemisphere_Images"] = hemi_dicts
    Browser.quit()
    return mars_data

    


