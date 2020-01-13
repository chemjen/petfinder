from selenium import webdriver
import time
import re

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
driver = webdriver.Chrome()
# Go to the page that we want to scrape
driver.get("https://www.petfinder.com/search/dogs-for-adoption/us/ny/new-york-city/")

time.sleep(2)
# find dog urls
dogs = driver.find_elements_by_xpath('//a[@class="petCard-link"]')

print(dogs[0].get_attribute('href'))

driver.close()



