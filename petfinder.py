from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import re
import csv

animal = 'dogs'
city= 'new york city'
state = 'ny'
city = '-'.join(city.split())

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
opts = Options()
opts.add_argument("user-agent=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36']")
driver = webdriver.Chrome()

try:
    with open(f'{animal}_{state}_{city}_urls.txt', 'r') as f:
        pet_urls = [url.strip('\n') for url in f.readlines()] 
except:
    # Go to the page that we want to scrape
    front_url = f"https://www.petfinder.com/search/{animal}-for-adoption/us/{state}/{city}/"

    driver.get(front_url)
    wait_pets = WebDriverWait(driver, 10)
    pets = wait_pets.until(EC.presence_of_all_elements_located((By.XPATH,
					'//a[@class="petCard-link"]')))

    pet_urls = [pet.get_attribute('href') for pet in pets]

    num_pages = driver.find_element_by_xpath('//*[@id="page-select_List_Box_Btn"]/div/div[1]').text
    num_pages = int(num_pages.split('/')[1])

    page_urls = [front_url + f"?page=%{page}" for page in range(2, num_pages + 1)] 

    for page in page_urls:
        driver.get(page)
        time.sleep(2)
        wait_pets = WebDriverWait(driver, 10)
        pets = wait_pets.until(EC.presence_of_all_elements_located((By.XPATH,
					'//a[@class="petCard-link"]')))
        urls_temp = [pet.get_attribute('href') for pet in pets]
        pet_urls.extend(urls_temp)

    with open(f'{animal}_{state}_{city}_urls.txt', 'w') as f:
        for url in pet_urls:
            f.write(url+'\n')

csv_file = open(f'{animal}_{state}_{city}.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

for pet in pet_urls:
    try:
        pet_dict = {}
    
        driver.get(pet)
        time.sleep(random.randint(0,3))
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

        characteristics, adoption_fee, health, coat_length = '', '', '', ''  
        good_in_a_home_with, prefers_a_home_without, house_trained = '', '', ''
        for i, detail in enumerate(dt_texts):
            detail = '_'.join('_'.join(detail.split()).split('-')).lower()  ## var names need to be one word without hyphens
            exec(f'{detail} = dd_texts[i]')
        # print(detail)

         # print(good_in_a_home_with, house_trained, prefers_a_home_without, adoption_fee, health)    
 
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

        try:
            shelter_email = shelter_info.find_elements_by_xpath('//a[starts-with(@href, "mailto")]')[1].get_attribute('href')
            shelter_email = shelter_email.split(':')[1]
        else:
            shelter_email=''
#    emails = [x.get_attribute('href') for x in shelter_email]
#    print(shelter_email)

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
        pet_dict['coat length'] = coat_length
        pet_dict['story'] = story
        pet_dict['shelter name'] = shelter_name
        pet_dict['shelter address'] = shelter_address
        pet_dict['shelter zipcode'] = shelter_zipcode
        pet_dict['shelter email'] = shelter_email

        writer.writerow(pet_dict.values())
  
    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
		break

csv_file.close()
driver.close()



