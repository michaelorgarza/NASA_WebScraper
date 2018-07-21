# dependencies 
from bs4 import BeautifulSoup as bs
from requests import get 
import requests as req
import pandas as pd
from splinter import Browser
import pymongo
import time

def _browser():
    executable_path = {'executable_path' : '/Users/michaelorgarza/chromedriver'}
    return browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    """A function that scrapes websites for data and returns it in a dict"""
    browser = _browser()
    data = {}

    url_1 = "https://mars.nasa.gov/news/"
    broswer.visit(url_1)

    url_1_html = browser.html
    soup = bs(url_1_html, "html.parser")

    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div', class_="rollover_description_inner").text.strip()

    data["News Title"] = news_title
    data["Teaser Text"] = news_p

###########
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)


    html = browser.html
    soup = bs(html, "html.parser")

    # feature image scrapedd
    browser.click_link_by_partial_text('FULL IMAGE')
   

    # bs object
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    # extract info 
    jpl_img = jpl_soup.find('img', class_='fancybox-image')
    jpl_img_path = jpl_img.get('src')

    # append img pathway to jpl url 
    recent_mars_img_url = "https://www.jpl.nasa.gov" + jpl_img_path

    data["Featured Image"] = recent_mars_img_url
   
###########
    url_3 = ("https://twitter.com/marswxreport?lang=en")
    browser.visit(url_3)
    html = browser.html

    tw_soup = bs(html.text, 'html.parser')

    # extract info 
    tw_weather = tw_soup.find_all('div', class_="js-tweet-text-container")

    data["Martian Weather from Twitter"] = tw_weather

############

    url_4 = req.get("https://space-facts.com/mars/")
    browser.visit(url_4)
    facts_table = pd.read_html(url_4.text)
    facts_table = pd.DataFrame(facts_table[0])
    facts_table.columns = ["Description", "Value"]
    facts_table = facts_table.set_index("Description")
    facts_html = facts_table.to_html(index = True, header = True)
    facts_html.replace('\n', '')

    data["Martian Data Table"] = facts_html

############

    # use USGS astrogeology url to scrape images of martian hemispheres
    url_5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_5)
    html = browser.html
    # bs object
    soup = bs(html, "html.parser")
    # empty list to hold image urls
    hemisphere_image_urls =[]

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    # loop over all each link and append hrefs 
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        link = "https://astrogeology.usgs.gov" + a['href']
        browser.visit(link)
    
        img_page = browser.html
        soup = bs(img_page, 'html.parser')
        img_link = soup.find('div', class_='downloads').find('li').a['href']
    
        image_dict = {}
        image_dict['title'] = title
        image_dict['url'] = img_link
    
        hemisphere_image_urls.append(image_dict)

    data["Hemisphere Images"] = hemisphere_image_urls

    return data

