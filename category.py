
# import basic selenium and go to the link
import json
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



t = "Request was throttled"



def write_to_json(data : dict, file_name = 'categories.json'):

    with open(file_name, 'w') as f:
        json.dump(data, f)

def get_cats_pc():
    main_link = "https://www.amazon.com/Best-Sellers-Audible-Books-Originals/zgbs/audible/"
    driver = webdriver.Chrome()
    driver.get(main_link)

    # Wait until the div with role=group is visible
    wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds
    try:
        catalog = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='group']")))
    except:
        driver.refresh()
        catalog = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='group']")))



    # get the category links

    categories = catalog.find_elements(By.TAG_NAME, 'a')
    sorted_categories = []

    for category in categories:
        cat = {"name": category.text, "link": category.get_attribute('href'), "subcats": {}}
        sorted_categories.append(cat)

    return sorted_categories

def get_subcats_pc(cat, name, level = 1):
    
    main_link = cat['link']
    driver = webdriver.Chrome()
    driver.get(main_link)

    # Wait until the div with role=group is visible
    wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds
    try:
        catalog = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='group']")))
    except:
        driver.refresh()
        catalog = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='group']")))
    
    # check if an element exist in catalog
    try:
        exists = driver.find_element(By.XPATH, f"//div[@role='group']/div/span")
        if exists:
            print("\t"*level+f"{name} has no subcategories")
            return cat
    except:
        pass

    # get the category links
    categories = catalog.find_elements(By.TAG_NAME, 'a')

    for category in categories:
        cat['subcats'][category.text ] = {"link": category.get_attribute('href'), "subcats": {}}
        print("\t"*level+f"{category.text}")

    return cat

def get_all_subcats_pc(subcats, level = 1):
    for name in subcats.keys():
        print("\t"*level+f"{name}")
        if subcats[name]['subcats']:
            get_all_subcats_pc(subcats[name]['subcats'], level+1)
        else:
            subcats[name] = get_subcats_pc(subcats[name], name, level+1)
            print("\t"*(level+1)+f"---------")

def get_catalog():

    cats = get_cats_pc()
    write_to_json(cats)
    
    with open('categories.json') as f:
        cats = json.load(f)

    for cat in cats:
        print(cat['name'])
        get_all_subcats_pc(cat['subcats'])
        write_to_json(cats, 'categories.json')

       

