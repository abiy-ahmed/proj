'''
Copyright (C) 2023 https://github.com/haile-selassie

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

while True:
    try:
        import pandas as pd
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys
        import progress
    except:
        choice = input("One or more dependencies are not installed. Would you like to install them? [Y/n]\n> ").lower()
        if choice != "y" and choice != "yes":
            exit()
        pipmain(["install","selenium"])
        pipmain(["install","pandas"])
        pipmain(["install","progress"])
    else:
        break

from time import sleep as wait
import datetime
import logging

REVIEWS_PER_LOCATION = 1 # -1 for no limits (laggy)
HEADLESS = False
OPTIONS = FirefoxOptions()
LOGGING = True
SORT_BY = "Most relevant" # Most relevant, Newest, Highest, Lowest
LOCATION = "San Antonio"
OUTFILE_NAME = "<city>-reviews.csv"
COLUMNS = ("search term","place name","address","username","stars","timestamp","review","pfp url") #Review is text only

place_types = (
    "businesses",
    "stores",
    "restaurants",
    "services",
    "restaurants",
    "public services",
    "bars",
    "landmarks",
    "parks",
    "churches",
    "schools"
)

positions = (
    "north side <location>",
    "northeast side <location>",
    "east side <location>",
    "southeast side <location>",
    "south side <location>",
    "southwest side <location>",
    "west side <location>",
    "northwest side <location>",
    "central <location>",
    "downtown <location>",
    "<location> outskirts",
    "<location>"
)

def wait_for_element(driver,byvar,byval,timeout=2):
    element = None
    t = 0
    while True:
        if t == timeout:
            return None
        try:
            element = driver.find_element(byvar,byval)
        except:
            t+=1
            wait(1)
            continue
        else:
            break
    return element

def banner():
    print("Review scraper has been started.")

def main():
    global LOCATION
    global REVIEWS_PER_LOCATION
    banner()

    known_places = set()
    reviews_data = list()

    if not LOCATION or len(LOCATION) == 0:
        LOCATION = input("Enter a city/region...\n> ")
    if HEADLESS:
        OPTIONS.add_argument("-headless")
    
    driver = webdriver.Firefox(options=OPTIONS)
    driver.get('https://google.com')
    search_bar = wait_for_element(driver,By.CLASS_NAME,'gLFyf',-1)
    search_bar.send_keys("stores near me")
    search_bar.submit()

    more_places_button = wait_for_element(driver,By.XPATH,"//a[@class='CHn7Qb pYouzb']",-1)
    more_places_button.click()
    wait_for_element(driver,By.CLASS_NAME,"axGQJc",-1)

    for position in positions:
        for place_type in place_types:
            search_term = f"{place_type} in {position}".replace("<location>",LOCATION)
            places_search_bar = wait_for_element(driver,By.CLASS_NAME,"gLFyf",-1)
            places_search_bar.send_keys(search_term)
            places_search_bar.submit()

            n_places = len(driver.find_elements(By.CLASS_NAME,"VkpGBb"))
            driver.refresh()
            for i in range(n_places):
                #place_link = wait_for_element(driver,By.XPATH,f"//div[@class='VkpGBb'][{i+1}]/div[@class='cXedhc']/a[2]")
                #place_link = wait_for_element(driver,By.XPATH,f"//div[@class='cXedhc'][{i+1}]/a[1]")
                #place_link = wait_for_element(driver,By.XPATH,f"//div[@jscontroller='EfJGEe']/div[{(i+1)*2}]//div[@class='cXedhc']/a[1]")
                # place_link = WebDriverWait(driver, 2,ignored_exceptions=(NoSuchElementException,StaleElementReferenceException))\
                #                         .until(expected_conditions.presence_of_element_located((By.XPATH, f"//div[@class='VkpGBb'][{i+1}]/div[@class='cXedhc']/a[1]")))
                
                #place_link.click()
                

                popup = wait_for_element(driver,By.CLASS_NAME,"xpdopen")

                title = wait_for_element(driver,By.XPATH,"//div[@class='xpdopen']//div[@class='SPZz6b']/h2/span").text
                if title in known_places: continue
                address = wait_for_element(driver,By.XPATH,"//div[@class='xpdopen']//span[@class='LrzXr']").text
                reviews_button = wait_for_element(driver,By.XPATH,"//div[@class='xpdopen']//a[@class='KYeOtb rWAMad']")
                reviews_button.click()
                if not REVIEWS_PER_LOCATION or REVIEWS_PER_LOCATION <= 0:
                    REVIEWS_PER_LOCATION = wait_for_element(driver,By.XPATH,"//div[@class='xpdopen']//span[@class='z5jxId']").text
                    REVIEWS_PER_LOCATION = int(REVIEWS_PER_LOCATION.split()[0].strip())
                REVIEWS_DIV_CLASS_NAME = "RMCqNd"
                REVIEW_DIV_CLASS_NAME = "jxjCjc"
                for j in range(REVIEWS_PER_LOCATION):
                    actions = ActionChains(driver)
                    actions.move_to_element(popup)
                    actions.send_keys(Keys.PAGE_DOWN)
                    actions.perform()
                    username = wait_for_element(driver,By.XPATH,f"//div[@class='xpdopen']//div[@class='{REVIEWS_DIV_CLASS_NAME}']//div[@class='{REVIEW_DIV_CLASS_NAME}'][{j+1}]//div[@class='TSUbDb']/a").text
                    stars = wait_for_element(driver,By.XPATH,f"//div[@class='xpdopen']//div[@class='{REVIEWS_DIV_CLASS_NAME}']//div[@class='{REVIEW_DIV_CLASS_NAME}'][{j+1}]//div[@class='PuaHbe']/g-review-stars[@class='lTi8oc']/span").get_attribute("aria-label")
                    stars = stars.split()[1]
                    timestamp = wait_for_element(driver,By.XPATH,f"//div[@class='xpdopen']//div[@class='{REVIEWS_DIV_CLASS_NAME}']//div[@class='{REVIEW_DIV_CLASS_NAME}'][{j+1}]//div[@class='PuaHbe']/span[1]").text
                    review = wait_for_element(driver,By.XPATH,f"//div[@class='xpdopen']//div[@class='{REVIEWS_DIV_CLASS_NAME}']//div[@class='{REVIEW_DIV_CLASS_NAME}'][{j+1}]//span[@class='review-full-text']").text
                    pfp_url = wait_for_element(driver,By.XPATH,f"//div[@class='xpdopen']//div[@class='{REVIEWS_DIV_CLASS_NAME}']//div[@class='{REVIEW_DIV_CLASS_NAME}'][{j+1}]/../a[1]").get_attribute("href")

                    known_places.add(address)
                    review_data = [search_term,title,address,username,stars,timestamp,review,pfp_url]
                    reviews_data.append(review_data)
                

if __name__ == "__main__":
    main()