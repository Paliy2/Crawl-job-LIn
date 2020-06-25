from selenium import webdriver
from client import LIClient
import time


if __name__ == "__main__":
    # initialize selenium webdriver - pass latest chromedriver path to webdriver.Chrome()
    driver = webdriver.Chrome('C:/Program Files/Mozilla/chromedriver.exe')
    driver.get("https://www.linkedin.com/uas/login")

    username = input('Login: ')
    password = input('Password: ')

    # initialize LinkedIn web client
    liclient = LIClient(driver, username, password)

    liclient.login()

    # wait for page load
    time.sleep(3)

    # url = 'https://www.linkedin.com/jobs/search/?keywords=remote'

    # 'https://www.linkedin.com/jobs/search/?alertAction=viewjobs&geoId=102264497&keywords=python%20developer&location=Ukraine'
    url = input('Enter url to scrape: ').strip()
    liclient.navigate_to_jobs_page(url)
    liclient.navigate_search_results()
    liclient.parse_all_jobs()
    liclient.driver_quit()
