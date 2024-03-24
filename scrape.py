import json
from time import sleep
from random import randint , uniform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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
    sleep(2)
    if currentY < height*0.9:
        load_all_books(driver)

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
    xpaths = {
    'catalog': "//div[@role='group']",
    'book' : '//div[@id="gridItemRoot"]',
    'title' : 'div/div/div[2]/div/a[2]/span/div',
    'author' : 'div/div/div[2]/div/div/span/div',
    'rating' : 'div/div/div[2]/div/div[2]/div/a',
    'price' : 'div/div/div[2]/div/div[4]/a/span/span/span',
    'img' : 'div/div/div[2]/div/a/div/img'
    }

    x_get(driver, link, xpaths['catalog'])
    load_all_books(driver)
    books = driver.find_elements(By.XPATH, xpaths['book'])

    scrapedbooks = []

    for book in books:
        try:
            title = book.find_element(By.XPATH, xpaths['title']).text
            author = book.find_element(By.XPATH, xpaths['author']).text
            rating = float(book.find_element(By.XPATH, xpaths['rating']).get_attribute('title').split()[0])
            price = book.find_element(By.XPATH, xpaths['price']).text
            img = book.find_element(By.XPATH, xpaths['img']).get_attribute('src')
            scrapedbooks.append({"title": title, "author": author, "rating": rating, "price": price, "img": img})
        except:
            pass

    if next_page(driver):
        scrapedbooks += scrape_the_link(driver.current_url, driver)
    return scrapedbooks


link =  "https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Art/zgbs/audible/18571913011/ref=zg_bs_nav_audible_2_18571910011"

data = scrape_the_link(link)
write_to_json(data)




