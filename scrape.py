import json
from time import sleep
from random import randint , uniform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

xpaths = {
'catalog': "//div[@role='group']",
'book' : '//div[@id="gridItemRoot"]',
'title' : 'div/div/div[2]/div/a[2]/span/div',
'author' : 'div/div/div[2]/div/div/span/div',
'rating' : 'div/div/div[2]/div/div[2]/div/a',
'price' : 'div/div/div[2]/div//a/span/span',
'img' : 'div/div/div[2]/div/a/div/img'
}

def get_book_details(book):
    try:
        title = book.find_element(By.XPATH, xpaths['title']).text
    except :
        title = 'N/A'

    try:
        author = book.find_element(By.XPATH, xpaths['author']).text
    except:
        author = 'N/A'
        
    try:
        price = book.find_element(By.XPATH, xpaths['price']).text
    except:
        price = 'N/A'
        
    try:
        img = book.find_element(By.XPATH, xpaths['img']).get_attribute('src')
    except:
        img = 'N/A'

    try:
        rating = float(book.find_element(By.XPATH, xpaths['rating']).get_attribute('title').split()[0])
    except:
        rating = 'N/A'

    return {"title": title, "author": author, "rating": rating, "price": price, "img": img}

def write_to_json(data : dict, file_name = 'books.json'):
    with open(file_name, 'w') as f:
        json.dump(data, f)

def x_get(driver, link, xpath="//div[@role='group']" , wait = 7):
    if driver.current_url != link:
        driver.get(link)
    # Wait until the div with role=group is visible
    wait = WebDriverWait(driver, wait)  
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except:
        driver.refresh()
        x_get(driver, link, xpath, wait = 7)

def load_all_books(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    height = driver.execute_script("return document.body.scrollHeight")
    currentY = driver.execute_script("return window.scrollY")
    sleep(3)
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight*0.2)")
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(1)
    if currentY < height*0.9:
        load_all_books(driver)
    # books = len(driver.find_elements(By.XPATH, xpaths['book']))
    # print(f"Total {books} books loaded")

def next_page(driver):
    xpath = "//li[contains(@class, 'a-last')]/a"
    try:
        next_btn = driver.find_element(By.XPATH, xpath)
        # check if btn has class a-disabled
        if 'a-disabled' in next_btn.get_attribute('class'):
            return False
        else:
            link = next_btn.get_attribute('href')
            next_btn.click()
            x_get(driver, link)
            return True
    except:
        return False

def scrape_the_link(link, driver = None):
    if driver is None:
        driver = webdriver.Chrome()


    x_get(driver, link, xpaths['catalog'])
    load_all_books(driver)
    books = driver.find_elements(By.XPATH, xpaths['book'])

    scrapedbooks = []

    for i, book in enumerate(books):
        try:
            scrapedbooks.append(get_book_details(book))
        except Exception as e:
            print(f"Error at book {i+1}:\n\t{e}")

    if next_page(driver):
        scrapedbooks += scrape_the_link(driver.current_url, driver)
    return scrapedbooks







