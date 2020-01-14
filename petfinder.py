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

    print(age_group, color, sex, size)

    second_part = driver.find_element_by_xpath('//div[@data-test="Pet_About_Section"]')
    
    ## get every dt tag - which are the labels for the dd tags
    dts = second_part.find_elements_by_xpath('.//dt')
    dt_texts = [dt.text for dt in dts]
    ## the dd tags contain the information for each dt label
    dds = second_part.find_elements_by_xpath('.//dd')
    dd_texts = [dd.text for dd in dds]

    print(dt_texts)
    print(dd_texts)

    good_in_a_home_with, house_trained, prefers_a_home_without, adoption_fee, health = [], [], [], [], []
    for i, detail in enumerate(dt_texts):
        detail = '_'.join('_'.join(detail.split()).split('-')).lower()  ## var names need to be one word without hyphens
        exec(f'{detail} = dd_texts[i]')
        print(detail)

    print(good_in_a_home_with, house_trained, prefers_a_home_without, adoption_fee, health)    
 
    try:
        story = driver.find_element_by_xpath('//div[@data-test="Pet_Story_Section"]//div[@class="u-vr4x"]').text
        story = story.replace('\n\n',' ')
    except:
        story = []
    print(len(story))
    print(story)    
#    break
#about_me
#shelter
#address


#time.sleep(2)


#driver.get(urls[2])

driver.close()



