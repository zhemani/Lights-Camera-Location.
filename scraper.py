
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
    driver.get("http://www.movie-locations.com/films.html")
    #ENTER INPUT
    submit_box = driver.find_element_by_name("q")
    submit_box.send_keys(name) 


    def find_by_xpath(locator):
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, locator))
        )

        return element

    find_by_xpath('//input[@value = "or search the site"]').click()


    for handle in driver.window_handles:
        driver.switch_to_window(handle)


    html_doc = driver.page_source
    soup = BeautifulSoup(html_doc)
    soup.prettify()
    get_link = soup.find('div', {'class' : "gsc-url-bottom"}).text
    
    newlink = get_link.replace("www.movie-locations.comw", "")
    w = 'http://w'
    newlink = w + newlink

    client = textrazor.TextRazor(extractors=["entities"])
    client.set_entity_freebase_type_filters(["/architecture/building", "/business/shopping_center", "/architecture/building", "/architecture/house", "/architecture/lighthouse", "/architecture/landscape_project", "/architecture/museum", "/architecture/skyscraper", "/architecture/structure", "/architecture/tower", "/architecture/venue", "/geography/lake", "/geography/waterfall", "/geography/mountain", "/geography/river", "/transportation/bridge", "/transportation/road", "/zoos/zoo", "/amusement_parks/park"])
    client.set_entity_dbpedia_type_filters(["ArchitecturalStructure", "Bridge", "Building", "CollegeOrUniversity", "EducationalInstitution", "HistoricBuilding", "HistoricPlace", "Hotel", "Infrastructure", "LandmarksOrHistoricalBuildings", "Library", "Lighthouse", "Museum", "Mountain", "Restaurant", "School", "ShoppingCenter", "ShoppingMall", "StadiumOrArena", "Station", "University", "College"])
    client.set_cleanup_mode("cleanHTML")
    response = client.analyze_url(newlink)


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


