from selenium import webdriver
import time
import re

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
driver = webdriver.Chrome()
# Go to the page that we want to scrape
front_url = "https://www.petfinder.com/search/dogs-for-adoption/us/ny/new-york-city/"

driver.get(front_url)

time.sleep(2)
# find dog urls
pets = driver.find_elements_by_xpath('//a[@class="petCard-link"]')

pet_urls = [pet.get_attribute('href') for pet in pets]
print(len(pet_urls))

num_pages = driver.find_element_by_xpath('//*[@id="page-select_List_Box_Btn"]/div/div[1]').text
num_pages = int(num_pages.split('/')[1])
#print(num_pages.split('/')[1])

page_urls = [front_url + f"?page=%{page}" for page in range(2, num_pages + 1)] 

#for page in page_urls:
#    driver.get(page)
#    time.sleep(10)
#    pets = driver.find_elements_by_xpath('//a[@class="petCard-link"]')
#    urls_temp = [pet.get_attribute('href') for pet in pets]
#    pet_urls.extend(urls_temp)
#    print(len(pet_urls))
#    break

i = 0
for pet in pet_urls[:10]:
    driver.get(pet)
    time.sleep(5)
    
    first_part = driver.find_element_by_xpath('//div[@class="card-section-inner"]')
    name = first_part.find_element_by_xpath('.//span[@data-test="Pet_Name"]').text
    print(name)
    breeds = first_part.find_element_by_xpath('.//span[@data-test="Pet_Breeds"]').text

    print(breeds)
    try:
        urlbreed =  first_part.find_elements_by_xpath('//span[@data-test="Pet_Breeds"]/a')
        print(len(urlbreed))
        for a in urlbreed:
            breed_text = a.text
            if breed_text not in breeds:
                breeds = breeds + breed_text
    except:
        print('no urls')

    try:
        age_group = first_part.find_element_by_xpath('./ul[@aria-label="Pet physical characteristics"]//span[@data-test="Pet_Age"]').text
    except:
        print('no age group')
        age_group = []
    try:
        color = first_part.find_element_by_xpath('./ul[@aria-label="Pet physical characteristics"]//span[@data-test="Pet_Primary_Color"]').text
    except:
        print('no color')
        color = []

    print(age_group, color)

    try:
        sex = first_part.find_element_by_xpath('./ul[@aria-label="Pet physical characteristics"]//span[@data-test="Pet_Sex"]').text
        print(sex)
    except:
        print('no sex')
        sex = []

    try:
        size = first_part.find_element_by_xpath('./ul[@aria-label="Pet physical characteristics"]//span[@data-test="Pet_Full_Grown_Size"]').text
        print(size)
    except:
        print('no size')
        size = []


#    break

#location
#house_trained
#health
#good_in_a_home_with
#prefers_a_home_without
#adoption_fee
#about_me
#shelter
#address


#time.sleep(2)


#driver.get(urls[2])

driver.close()



