from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import time
import re
import csv

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
driver = webdriver.Chrome()
# Go to the page that we want to scrape
front_url = "https://www.petfinder.com/search/dogs-for-adoption/us/ny/new-york-city/"

driver.get(front_url)
wait_pets = WebDriverWait(driver, 10)
pets = wait_pets.until(EC.presence_of_all_elements_located((By.XPATH,
					'//a[@class="petCard-link"]')))

pet_urls = [pet.get_attribute('href') for pet in pets]

num_pages = driver.find_element_by_xpath('//*[@id="page-select_List_Box_Btn"]/div/div[1]').text
num_pages = int(num_pages.split('/')[1])
#print(num_pages.split('/')[1])

page_urls = [front_url + f"?page=%{page}" for page in range(2, num_pages + 1)] 

for page in page_urls:
    driver.get(page)
    wait_pets = WebDriverWait(driver, 10)
    pets = wait_pets.until(EC.presence_of_all_elements_located((By.XPATH,
					'//a[@class="petCard-link"]')))
    urls_temp = [pet.get_attribute('href') for pet in pets]
    pet_urls.extend(urls_temp)
    break

csv_file = open('dogs_nyc.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

for pet in pet_urls:
    pet_dict = {}
    
    driver.get(pet)
    
    wait_first_part = WebDriverWait(driver, 10)
    first_part = wait_first_part.until(EC.presence_of_all_elements_located((By.XPATH,
        '//div[@class="card-section-inner"]')))[0]
    
    name = first_part.find_element_by_xpath('.//span[@data-test="Pet_Name"]').text

    breeds = first_part.find_element_by_xpath('.//span[@data-test="Pet_Breeds"]').text

    try:
        urlbreed =  first_part.find_elements_by_xpath('//span[@data-test="Pet_Breeds"]/a')
        for a in urlbreed:
            breed_text = a.text
            if breed_text not in breeds:
                breeds = breeds + breed_text
    except:
        breeds = []

    try:
        age_group = first_part.find_element_by_xpath('./ul[@aria-label="Pet physical characteristics"]//span[@data-test="Pet_Age"]').text
    except:
        age_group = ''
    try:
        color = first_part.find_element_by_xpath('./ul[@aria-label="Pet physical characteristics"]//span[@data-test="Pet_Primary_Color"]').text
    except:
        color = ''

    try:
        sex = first_part.find_element_by_xpath('./ul[@aria-label="Pet physical characteristics"]//span[@data-test="Pet_Sex"]').text
    except:
        sex = ''

    try:
        size = first_part.find_element_by_xpath('./ul[@aria-label="Pet physical characteristics"]//span[@data-test="Pet_Full_Grown_Size"]').text
    except:
        size = ''

    second_part = driver.find_element_by_xpath('//div[@data-test="Pet_About_Section"]')
    
    ## get every dt tag - which are the labels for the dd tags
    dts = second_part.find_elements_by_xpath('.//dt')
    dt_texts = [dt.text for dt in dts]
    ## the dd tags contain the information for each dt label
    dds = second_part.find_elements_by_xpath('.//dd')
    dd_texts = [dd.text for dd in dds]

    good_in_a_home_with, house_trained, coat_length, prefers_a_home_without, adoption_fee, health = '', '', '', '', '', ''
    for i, detail in enumerate(dt_texts):
        detail = '_'.join('_'.join(detail.split()).split('-')).lower()  ## var names need to be one word without hyphens
        exec(f'{detail} = dd_texts[i]')
#        print(detail)

#    print(good_in_a_home_with, house_trained, prefers_a_home_without, adoption_fee, health)    
 
    try:
        story = driver.find_element_by_xpath('//div[@data-test="Pet_Story_Section"]//div[@class="u-vr4x"]').text
        story = story.replace('\n\n',' ')
    except:
        story = ''

    try:
        shelter_info = driver.find_element_by_xpath('//div[@class="card card_org"]')
        shelter_name = shelter_info.find_element_by_xpath('//pf-truncate/div').text
    except:
        shelter_name=''

    try:
        shelter_address = shelter_info.find_element_by_xpath('//div[@itemprop="address"]').text
        shelter_zipcode = re.search('\d\d\d\d\d$', shelter_address)
        if shelter_zipcode:
            shelter_zipcode = shelter_zipcode.group(0)
        else:
            shelter_zipcode = ''
    except: 
        shelter_address, shelter_zipcode = '', ''

    pet_dict['name'] = name
    pet_dict['breeds'] = breeds
    pet_dict['age group'] = age_group
    pet_dict['color'] = color
    pet_dict['sex'] = sex
    pet_dict['size'] = size
    pet_dict['good in a home with'] = good_in_a_home_with
    pet_dict['house trained'] = house_trained
    pet_dict['prefers a home without'] = prefers_a_home_without
    pet_dict['adoption fee'] = adoption_fee
    pet_dict['health'] = health
    pet_dict['story'] = story
    pet_dict['shelter name'] = shelter_name
    pet_dict['shelter address'] = shelter_address
    pet_dict['shelter zipcode'] = shelter_zipcode
    pet_dict['coat length'] = coat_length

    writer.writerow(pet_dict.values())

driver.close()



