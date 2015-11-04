
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
from urlparse import urljoin
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
import contextlib
import lxml.html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import textrazor
import json


textrazor.api_key = "Put API Key Here"

def get_locations(name):
    #SET DRIVER
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.delete_all_cookies()

    #GO TO LINK
    #...........
   #Application is under development and parsing code is hidden!
   #.............

    entities = list(response.entities())
    entities.sort(key=lambda x: x.relevance_score, reverse=True)
    seen = set()
    entity_list =[]

    for entity in entities:
        if entity.id not in seen:
            entity_list.append(entity.id)
            seen.add(entity.id)
    driver.quit()
    return entity_list

from flask import Flask, request
app = Flask(__name__, static_url_path='/static')

@app.route('/movie')
def movie_locations():
    name = request.args.get("name")
    return json.dumps(get_locations(name)), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/')
def index():
    with open("frontend/index.html") as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True)


