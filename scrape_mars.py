#!/usr/bin/env python
# coding: utf-8

# Dependencies
from builtins import AttributeError

from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time


def scrape_info():
    
    browser = Browser('chrome')
    mars = {}
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(5)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

    results = soup.find_all('div', class_="slide")
    title=[]
    description=[]
    for result in results:
        try:
            title.append(result.find('div',class_="content_title").a.text)

            description.append(result.find('div',class_="rollover_description_inner").text)

            print("title and descriptions")
            if(title and description):
                print(title)
                print(description)

        except AttributeError as e:
            print(e)

    news_title=title[0]
    news_p=description[0]
    mars["news_title"] = news_title
    mars["news_p"] = news_p

    url="https://spaceimages-mars.com/"
    browser.visit(url)
    time.sleep(5)
    soup = BeautifulSoup(browser.html, 'html.parser')
    images = soup.find_all('img', class_="headerimage")
    image = images[0]

    featured_image_url=image["src"]
    mars["featured_image"]= url + featured_image_url

    # Mars Facts

    url=r'http://space-facts.com/mars'

    tables = pd.read_html(url)

    df=tables[0]
    df.columns=['Attributes','Values']
    html_table = df.to_html()
    html_table=html_table.replace('\n', '')
    mars['facts'] = html_table

    df.to_html('table.html')

    # # Mars Hemispheres
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    time.sleep(5)
    usgs_soup = BeautifulSoup(browser.html, 'html.parser')
    headers = []
    titles = usgs_soup.find_all('h3')
    time.sleep(5)

    for title in titles:
      headers.append(title.text)

    images = []
    count = 0
    for thumb in headers:
        browser.find_by_css('img.thumb')[count].click()
        images.append(browser.find_by_text('Sample')['href'])
        browser.back()
        count = count+1

    hemisphere_image_urls = []  #initialize empty list to collect titles
    counter = 0
    for item in images:
        hemisphere_image_urls.append({"title":headers[counter],"img_url":images[counter]})
        counter = counter+1
    # closeBrowser(browser)
    browser.back()
    time.sleep(1)
    mars["hemispheres"] = hemisphere_image_urls

    return mars
if __name__ == "__main__":
    print(scrape_info())