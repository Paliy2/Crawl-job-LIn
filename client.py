from __future__ import print_function
from selenium import webdriver
from selenium.common.exceptions import JavascriptException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from settings import print_scraped_data, scroll_job_panel
import time
from bs4 import BeautifulSoup
from scrape import JobScraper

RESULT_FILE = 'result.csv'


def get_job_link(url):
    job_id = url.split('/')[6].strip()
    if not job_id.isdigit():
        parts = url.split('/')
        for i in range(len(parts)):
            if i != len(parts) - 1 and parts[i] == 'views':
                job_id = parts[i + 1]
                break

    if job_id:
        return 'https://www.linkedin.com/jobs/search/?currentJobId=' + job_id


def dump(data):
    """
    Data is a dictionary
    """
    row = ''
    for key in data.keys():
        row += data[key] + ';'
    row = row[:-1] + '\n'

    with open(RESULT_FILE, 'a', encoding='utf-8-sig') as f:
        f.write(row)


def scroll_job_panel(driver):
    """
    Scroll the left panel containing the job offers by sending PAGE_DOWN
    key until the very end has been reached
    :param driver: selenium chrome driver object
    :return: None
    """
    panel = driver.find_element_by_class_name("jobs-search-results")
    last_height = driver.execute_script(
        "return document.getElementsByClassName(" +
        "'jobs-search-results')[0].scrollHeight")
    while True:
        time.sleep(.2)
        for i in range(5):
            panel.send_keys(Keys.PAGE_DOWN)
            time.sleep(.2)
        new_height = driver.execute_script(
            "return document.getElementsByClassName(" +
            "'jobs-search-results')[0].scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height
    javascript = (
            "var x = document.getElementsByClassName(" +
            "'jobs-search-results')[0]; x.scrollTo(0, x.scrollHeight)"
    )
    driver.execute_script(javascript)


def scroll_data_panel(driver, banned=False):
    """
    Scroll the left panel containing the job offers by sending PAGE_DOWN
    key until the very end has been reached
    :param driver: selenium chrome driver object
    :return: None
    """
    x = 15
    if banned:
        # additional time to load pages
        time.sleep(.2)
        x = 35
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # panel = driver.find_element_by_class_name('job-view-layout jobs-details ember-view')
    xpath_1 = '/html/body/div[8]/div[3]/div[2]/div[2]/div/div/div'
    xpath_2 = '/html/body/div[7]/div[3]/div[2]/div[2]/div/div/div'
    xpath = '//*[@id="ember213"]'
    x_path_3 = '/html/body/div[7]/div[3]/div[2]/div[2]/div/div/div/div/div[1]'
    x_path_4 = '/html/body/div[8]/div[3]/div[2]/div[3]/div/div/div'
    x_path_5 = '/html/body/div[7]/div[3]/div[2]/div[3]/div/div/div'
    # x_path_6 = ''

    pathes = [xpath_2, xpath_1, x_path_4, x_path_3, x_path_5, xpath]
    last_height = driver.execute_script(
        "return document.getElementsByClassName(" +
        "'jobs-search-results')[0].scrollHeight")

    for path in pathes:
        try:
            panel = driver.find_element_by_xpath(path)
            if panel:
                print('[INFO] XPath founf')
                break
        except:
            print('Choosing another Xpath')

    while True:
        print('started scrolling')
        time.sleep(.1)
        for i in range(x):
            panel.send_keys(Keys.PAGE_DOWN)
            time.sleep(.1)

        print('Done scroling')
        new_height = driver.execute_script(
            "return document.getElementsByClassName(" +
            "'jobs-search-results')[0].scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height
    javascript = (
            "var x = document.getElementsByClassName(" +
            "'jobs-search-results')[0]; x.scrollTo(0, x.scrollHeight)"
    )
    driver.execute_script(javascript)


class LIClient(object):
    def __init__(self, driver, username, password, **kwargs):
        self.username = username
        self.password = password
        self.driver = driver
        self.results_page = 'https://www.linkedin.com/jobs/search/?start={}'  # kwargs["results_page"]

    def set_results_page(self, url):
        task = url.split('?')
        test_2 = task[1].split('&')
        for i in test_2:
            if 'currentJobId' in i:
                url.replace(i, '').replace('&&', '&').replace('?&', '?')
        self.results_page = url + '&start={}'

    def driver_quit(self):
        self.driver.quit()

    def login(self):
        """login to linkedin then wait 3 seconds for page to load"""
        time.sleep(6)
        # input login

        if self.username == 'eixt' or self.password == 'exit':
            return

        elem = self.driver.find_element_by_id('username')
        elem.send_keys(self.username)
        # input password

        elem = self.driver.find_element_by_id("password")
        elem.send_keys(self.password)

        # submit login
        btn = '//div[@class="login__form_action_container "]'
        elem = self.driver.find_element_by_xpath(btn)
        elem.click()

        # Wait a few seconds for the page to load
        time.sleep(3)
        print('logged successfully')

    def navigate_to_jobs_page(self, url):
        """
        navigate to the 'Jobs' page
        """
        self.set_results_page(url)

        try:
            self.driver.get(url)
        except Exception as e:
            print("  jobs page not detected")
        else:
            print("**************************************************")
            print("\nSuccessfully navigated to {} page\n".format(url))

    def navigate_search_results(self):
        """
        scrape postings for all pages in search results
        """
        driver = self.driver
        results_page = self.results_page
        # delay = 60
        x = 0
        all_links = []
        while True:
            try:
                # print(results_page)
                self.navigate_to_jobs_page(results_page.format(x))
                # wait to load page
                time.sleep(3)

                scroll_job_panel(self.driver)
                time.sleep(3)

                # print(self.driver.page_source)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                urls = soup.find_all('a', class_='disabled ember-view job-card-container__link job-card-list__title')
                urls2 = soup.find_all('a', class_='disabled ember-view job-card-container__link job-card-list__title ')

                urls = [i['href'] for i in urls] + [i['href'] for i in urls2]
                all_links += urls
                # data = scrape_page(self.driver)
                print('\n', urls, '\n', len(urls))

                print("\n**************************************************")
                print("\n\n\nNavigating to results page  {}" \
                      "\n\n\n".format(results_page.format(x)))
                x += 25
                if len(urls) == 0:
                    print('Got all links')
                    break
                if len(all_links) > 1000:
                    print('Got more than 40 pages')
                    break

                with open('links.txt', 'a', encoding='utf-8') as f:
                    for i in urls:
                        f.write(i + '\n')
            except ValueError:
                print("**************************************************")
                print("\n\n\n\n\nSearch results exhausted\n\n\n\n\n")
                break
            else:
                print('Done')

    def parse_all_jobs(self, write_headers=True):
        file = 'links.txt'

        with open(file, 'r', encoding='utf-8') as f:
            links = f.read().split('\n')
            links = [i for i in links if i != '']
            print(links)

        if write_headers:
            with open(RESULT_FILE, 'a', encoding='utf-8') as f:
                f.write(
                    'job_url;job_name;company;company_url;full_field;location;posted_on;views;num_of_applicants;seniority;num_of_employees;job_location;job_description;employment_type;job_functions;industry;past_day_applicants;applicants_seniority;applicants_education;applicants_location;company_growth;followers')

        # loop through each link
        while links:
            url = links[0]
            try:
                # if True:
                a = url
                start = time.time()
                new_url = 'https://www.linkedin.com/' + url
                # change the link a bit to parse in general way
                url = get_job_link(new_url)
                self.navigate_to_jobs_page(url)
                time.sleep(.3)

                # if got page then scroll it to load
                try:
                    scroll_data_panel(self.driver, True)
                except JavascriptException:
                    # page is already loaded
                    pass
                except ElementNotInteractableException:
                    pass
                except UnboundLocalError:
                    print('Unbound Local Error, cannot locate scrolling element')

                # wait to load
                time.sleep(1.2)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                soup = soup.find('div', role='main')
                if not soup:
                    # just wait to load
                    time.sleep(4)
                    soup = BeautifulSoup(self.driver.page_source, 'lxml')
                    soup = soup.find('div', role='main')

                if not soup:
                    print("Can't scrape page", url, "wrong html")
                    with open(file, 'w', encoding='utf-8') as f:
                        for i in links:
                            f.write(i + '\n')
                    print('Saved backup')
                    input('Press enter after you resolved the captcha')
                    print('Done')
                    time.sleep(3)
                    # if False:

                    if 'sign in' in self.driver.page_source:
                        self.driver.navigate(
                            'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
                        self.login()
                        # todo also resolve the captcha
                        try:
                            checkbox = self.driver.find_element_by_id('recaptcha-anchor')
                            checkbox.click()
                        except:
                            print('unable to locate box')
                            time.sleep(15)

                            self.parse_all_jobs(write_headers=False)

                    if len(links) > 3:
                        links[0], links[-1] = links[-1], links[0]
                    else:
                        break
                    continue

                # exctract job data
                js = JobScraper(soup, url)
                job_data = js.get_job_data()
                print_scraped_data(job_data)
                # save into csv
                dump(job_data)
                # delet ejob from a list
                links.remove(a)
                print('Time taken:', time.time() - start)
            except:
                print('skipping', url, 'Unknown error occured. Please, wait a minute.')
                with open(file, 'w', encoding='utf-8') as f:
                    for i in links:
                        f.write(i + '\n')
                print('Saved backup')
        # clear file for future
        with open(file, 'w', encoding='utf-8') as f:
            f.write('')


if __name__ == '__main__':
    # path to webdriver
    driver = webdriver.Chrome('C:/Program Files/Mozilla/chromedriver.exe')
    driver.get("https://www.linkedin.com/uas/login")

    username = input('--username: ')
    password = input('--password: ')
    liclient = LIClient(driver, username, password)
    liclient.login()
    liclient.parse_all_jobs()
