import configparser
import random
import subprocess
import time
from itertools import cycle

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from utils import find_ads, run_alpha

# elements xpath
search_line = '//*[@id="lst-ib"]'
# DO NOT MIDIFY
confirm_link = '/html/body/div[2]/a[1]'


def confirm_redirect(driver):
    # Sometimes Google Chrome asks for confirmation of redirection
    try:
        driver.find_element_by_xpath(confirm_link).click()
    except NoSuchElementException:
        pass


def open_url(url, driver, delay_time):
    current_url = url.a['href']
    if not current_url.startswith('http'):
        current_url = f'https://www.google.com/{current_url}'
    driver.get(current_url)
    confirm_redirect(driver)
    time.sleep(delay_time)
    driver.quit()


def run_browser(search_query, user_agent, chrome_options, delay, mode):
    # set User-Agent
    if mode == 2:
        run_alpha()
    chrome_options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://www.google.com/')
    try:
        # error page loading
        search_field = driver.find_element_by_xpath(search_line)
    except NoSuchElementException:
        return driver.quit()
    search_field.send_keys(search_query)
    try:
        search_field.send_keys(Keys.ENTER)
    except StaleElementReferenceException:
        pass
    # search ad link
    ad = find_ads(driver.page_source)
    return open_url(ad, driver, delay) if ad else driver.quit()
    

def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return {
        'delay': config.getint('TIME', 'delay_time'),
        'chromium_path': config.get('PATHWAYS', 'chromium_path'),
        'alpha_mode': config.getint('OPTIONS', 'alpha_mode')
    }


def main():
    params = read_config('config.ini')
    if params['alpha_mode'] == 1:
        run_alpha()
    chrome_options = webdriver.ChromeOptions()
    # disable javascript
    prefs = {"webkit.webprefs.javascript_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.binary_location = params['chromium_path']
    with open('Search-Query.txt') as queries, open('User-Agent.txt') as user_agents:
        data = queries.readlines()
        agents = user_agents.readlines()
        for query in cycle(data):
            run_browser(query, random.choice(agents),
                        chrome_options, params['delay'], mode=params['alpha_mode'])


if __name__ == '__main__':
    main()
