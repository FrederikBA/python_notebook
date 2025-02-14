import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import os
from urllib.parse import urlparse
import re

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)

# Assignment 1
def checkIfFriday():
    browser.get("https://www.erdetfredag.dk")
    browser.implicitly_wait(2)
    browser.maximize_window()

    answer = browser.find_element_by_id("answer").text
    return answer


# Assignment 2
def top_five_recipes():
    browser.get("https://www.nemlig.com/opskrifter/mest-populaere")
    browser.implicitly_wait(2)
    browser.maximize_window()

    recipes = []
    links = []
    for i in range(1, 6):
        # Gets the first 5 recipe-items
        recipes_container = browser.find_elements_by_xpath(
            f'//*[@id="page-content"]/div/leftmenupage/section/div[1]/render-partial/div/recipelist-showall/div/div/div[1]/recipelist-item[{i}]/div/div/div[2]/div[1]'
        )

        for recipe in recipes_container:
            # Finds the href of the <a> tag of the recipe-item
            link = recipe.find_element_by_xpath(
                f'//*[@id="page-content"]/div/leftmenupage/section/div[1]/render-partial/div/recipelist-showall/div/div/div[1]/recipelist-item[{i}]/div/div/div[2]/div[1]/a'
            ).get_attribute("href")
            links.append(link)

    for link in links:
        recipe_full_link = urlparse(link)
        recipe_short_link = os.path.basename(recipe_full_link.path)
        new_recipe_short_link = recipe_short_link.replace("-", " ")
        recipe_name = re.sub("[0123456789]", "", new_recipe_short_link)
        recipes.append(recipe_name)
    print(recipes)
    return recipes


# Assignment 3
def total_price():
    browser.get("https://www.nemlig.com")
    browser.implicitly_wait(2)
    browser.maximize_window()

    items = ["gær", "minimælk", "banan", "tomatpasta"]
    integer_prices = []
    decimal_prices = []

    # Search for each item in the items list
    searchField = browser.find_element_by_xpath(
        '//*[@id="site-header-search-field-main"]'
    )
    searchField.click()
    for item in items:
        searchField.send_keys(item)
        searchField.submit()
        browser.implicitly_wait(2)

        # Get the integer of the price and the decimal of the price and add to seperate lists
        integer_price = float(
            browser.find_element_by_xpath(
                '//*[@id="searchscrollable"]/div/searchresult/div[1]/div[3]/div[1]/div[1]/div[1]/productlist-item[1]/a/div/div[3]/pricecontainer/div/div[2]/span'
            ).text
        )
        integer_prices.append(integer_price)

        decimal_price = (
            float(
                browser.find_element_by_xpath(
                    '//*[@id="searchscrollable"]/div/searchresult/div[1]/div[3]/div[1]/div[1]/div[1]/productlist-item[1]/a/div/div[3]/pricecontainer/div/div[2]/sup'
                ).text
            )
            / 100
        )
        decimal_prices.append(decimal_price)

        searchField.clear()

    # Add the two lists together and print total
    item_prices = np.add(integer_prices, decimal_prices)
    total = 0
    for i in range(0, len(item_prices)):
        total = total + item_prices[i]
    print(str(total) + " kr.")
    return total



# Assignment 4
# Sorter efter pris
def womens_fiction():
    browser.get(
        "http://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html"
    )
    browser.implicitly_wait(2)
    browser.maximize_window()

    titles = []
    prices = []

    # Get all titles and prices in the book list
    booklist_container = browser.find_element_by_xpath(
        '//*[@id="default"]/div/div/div/div/section/div[2]/ol'
    )
    booklist = booklist_container.find_elements_by_tag_name("li")
    browser.implicitly_wait(5)
    for book in booklist:
        currentTitle = book.find_element_by_tag_name("img").get_attribute("alt")
        titles.append(currentTitle)
        browser.implicitly_wait(10)
        price = float(
            book.find_element_by_class_name("price_color").text.replace("£", "")
        )
        prices.append(price)

    book_dict = dict(zip(titles, prices))
    # Sorts the dict based on the value instead of the key, hence 'x: x[1]' instead of 'x: x[0]'
    book_dict_sorted = dict(sorted(book_dict.items(), key=lambda x: x[1]))
    return book_dict_sorted


