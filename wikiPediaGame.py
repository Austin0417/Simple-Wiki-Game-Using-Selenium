import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import random

ser = Service('C:\Program Files (x86)\chromedriver.exe')
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

# Asks user for the starting and end links to find end condition of the game
startingLink = input("Enter your starting Wikipedia link: ")
endingLink = input("Enter you ending Wikipedia link: ")


def selectRandom(links):
    # Chooses a random element from the array of links
    checker = ''
    randomChoice = ''

    # Checks if '/wiki/ is missing in the href of the random chosen element (redirects away from Wikipedia)
    # Also checks for '[' because these are not real links, but instead clickables that refer to the same page
    while "/wiki/" not in checker or "[" in randomChoice.text:
        randomChoice = random.choice(links)
        checker = randomChoice.get_attribute('href')
    randomChoice.click()
    time.sleep(3)

def startGame(startLink, endingLink):
    # Go to the end link page initially to grab the title of the end page, and store the title into a set 'goal'
    driver.get(endingLink)
    time.sleep(3)
    goal = set(driver.find_element(By.XPATH, value='//span[@class="mw-page-title-main"]').text.split())
    time.sleep(3)

    # Game begins here essentially
    driver.get(startLink)
    time.sleep(3)
    currentTitle = set(driver.find_element(By.XPATH, value='//span[@class="mw-page-title-main"]').text.split())
    #currentTitle = set(driver.find_element(By.XPATH, value='//h1[@id="firstHeading"]').text.split())

    while currentTitle != goal:
        # Grabbing all the links/href elements present on the Wiki page
        links = driver.find_elements(By.TAG_NAME, value='a')

        #Looping through all the links in the array
        for i in range(len(links)):
            # Checks that the text attribute is not None and if text is a subset of the goal set
            if links[i].text and set(links[i].text.split()).issubset(goal):
                try:
                    # ElementNotInteractableException could occur here
                    links[i].click()
                    time.sleep(3)

                    # NoSuchElementException could occur here
                    currentTitle = set(driver.find_element(By.XPATH, value='//span[@class="mw-page-title-main"]').text.split())
                    break
                except selenium.common.exceptions.ElementNotInteractableException:
                    # If the element is not clickable, move on to the next element in the array
                    continue
                except selenium.common.exceptions.NoSuchElementException:
                    # Some wiki pages' titles are under a different tag, so we account for this as well
                    currentTitle = set(driver.find_element(By.XPATH, value='//h1[@id="firstHeading"]').text.split())

            # Last element of the array, this means that we have not found a single link that is a subset of 'goal'
            # Therefore, we use the defined selectRandom method to instead simply choose a random link
            elif links[i] == links[-1]:
                while True:
                    try:
                        # Potential ElementNotInteractableException can occur. If so, we except by continuing and trying to select another random link
                        selectRandom(links)
                        break
                    except selenium.common.exceptions.ElementNotInteractableException:
                        continue
                try:
                    prevTitle = currentTitle
                    currentTitle = set(driver.find_element(By.XPATH, value='//span[@class="mw-page-title-main"]').text.split())
                except selenium.common.exceptions.ElementNotInteractableException:
                    currentTitle = set(driver.find_element(By.XPATH, value='//h1[@id="firstHeading"]').text.split())

                # This check is for 'fake' Wikipedia pages that are more for support and help, not ones that refer to concepts of the real world
                # If any of these key words are found in the title of the page, we need to go back to the previous page and repeat
                if str(currentTitle).find('Help') > 0 or str(currentTitle).find('Wikipedia:') > 0 or str(currentTitle).find('Category:') > 0:
                    currentTitle = prevTitle
                    driver.back()
                    time.sleep(3)

    while True:
        time.sleep(1)


startGame(startingLink, endingLink)







