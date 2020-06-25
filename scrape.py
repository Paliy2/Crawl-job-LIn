"""
A class to define the methods to scrape LinkedIn job web pages
"""


class JobScraper(object):
    def __init__(self, soup, url):
        """
        Initialize the class
        :param soup: BeautifulSoup instance
        :param url: str job URL to scrape
        :param query: str query to perform
        """
        self.soup = soup
        self.url = url

    def get_job_skills(self):
        """
        Get the skills required by the job offer being scraped.
        :return: list of skills
        """
        requested_skills = [rq.get_text() for rq in self.soup.find_all(
            class_="jobs-ppc-criteria__value")]
        if type(requested_skills) is str:
            requested_skills = requested_skills.replace('\n', '').replace('\t', '').replace('\r', '').strip()
        elif type(requested_skills) is list or type(requested_skills) is tuple or type(requested_skills) is set:
            # list
            requested_skills = [i.replace('\n', '').replace('\t', '').replace('\r', '').strip() for i in
                                requested_skills]
        return requested_skills

    def get_job_title(self):
        """
        Get the job title of the job page is being scraped.
        Return a string containing the job title
        :return: str job title
        """
        try:
            job_title = self.soup.find_all(
                class_='jobs-details-top-card__job-title t-20 t-black t-normal')[0].get_text()
        except IndexError:
            job_title = ""
        return job_title

    def get_job_location(self):
        """
        Get the location of the job offer being scraped.
        Return a string containing the location.
        """

        def validate_location(loc):
            """
            Validate the location by checking that the string extracted
            by the preferred "jobs-top-card__exact-location" HTML class
            is not empty, otherwise get the location string from the
            "jobs-top-card__bullet" HTML class
            :param loc: str of the location
            :return: str location
            """
            if loc:
                return loc
            else:
                try:
                    loc = [l.get_text().strip()
                           for l in self.soup.find_all(
                            class_="jobs-top-card__bullet")][0]
                except IndexError:
                    loc = ""
            return loc

        try:
            location = [l.get_text().strip()
                        for l in self.soup.find_all(
                    class_="jobs-top-card__exact-location")][0]
        except IndexError:
            location = ""
        return validate_location(location).replace('\n', '').replace('\t', '').replace('\r', '').strip()

    def get_location(self):
        query = 'jobs-details-top-card__company-info t-14 t-black--light t-normal mt1'
        try:
            name = self.soup.find_all('div', class_=query)[0].find_all('span', class_='jobs-details-top-card__bullet')
            if len(name) > 1:
                name = name[0].text
            else:
                name = ''
        except IndexError:
            name = ''
        return name

    def get_company_name(self):
        try:
            name = self.soup.find_all(
                class_='jobs-details-top-card__company-url ember-view')[0].get_text()
        except IndexError:
            name = ""
        return name

    def get_full_field(self):
        """
        like : company + remote + location + country string
        """
        query = 'jobs-details-top-card__company-info t-14 t-black--light t-normal mt1'
        try:
            name = self.soup.find_all(
                class_=query)[0].text.replace('Company Name', '')
            name = ' '.join(name.split())
        except IndexError:
            name = ""
        return name

    def get_company_url(self):
        try:
            name = self.soup.find_all(
                class_='jobs-details-top-card__company-url ember-view')[0]['href']
            name = 'https://www.linkedin.com' + name

        except IndexError:
            name = ""
        return name

    def get_post_data(self):
        query = 'jobs-details-top-card__job-info t-14 t-black--light t-normal'
        try:
            name = self.soup.find_all('p',
                                      class_=query)[0].find_all('span')[0].text.replace('Posted Date', '')
            name = ' '.join(name.split())
        except IndexError:
            name = ""
        return name

    def get_views(self):
        query = 'jobs-details-top-card__job-info t-14 t-black--light t-normal'
        name = ''
        try:
            all_data = self.soup.find_all('p',
                                          class_=query)[0].find_all('span')

            for i in all_data:
                if 'views' in i.text.lower():
                    res = i.text.replace('Number of views', '')
                    res = ' '.join(res.split())
                    return res
        except IndexError:
            return ""
        return name

    def get_num_of_applicants(self):
        name = ''
        query = 'jobs-details-job-summary__list jobs-details-job-summary__list--divider pr2 ml5'
        try:
            jobs = self.soup.find_all('div', class_=query)[0].find_all('li')

            for i in jobs:
                if 'applicant' in i.text.lower():
                    name = i.text
                    name = ' '.join(name.split())
                    break
        except IndexError:
            name = ""
        return name

    def get_seniority(self):
        query = 'jobs-box__body js-formatted-exp-body'
        try:
            name = self.soup.find_all('p', class_=query)[0].get_text()
        except IndexError:
            name = ""
        return name

    def get_employee_num(self):
        name = ''
        try:
            jobs = self.soup.find_all('span', class_='jobs-details-job-summary__text--ellipsis')
            print()
            for i in jobs:
                if 'employee' in i.text.lower():
                    name = i.text
                    name = ' '.join(name.split())
                    break
        except IndexError:
            name = ""
        return name

    def get_job_location(self):
        query = 'jobs-details-top-card__company-info t-14 t-black--light t-normal mt1'
        try:
            name = self.soup.find_all('div', class_=query)[0].find_all('span', class_='jobs-details-top-card__bullet')
            name = name[-1].text
        except IndexError:
            name = ''
        return name

    def get_job_description(self):
        query = 'job-details'
        try:
            text = self.soup.find_all('div', id=query)[0].find_all('span', class_=None)[0].get_text()
        except IndexError:
            text = ''
        return text.replace(';', '\t')

    def get_employment_type(self):
        query = 'jobs-box__body js-formatted-employment-status-body'
        try:
            name = self.soup.find_all('p', class_=query)[0].text
            name = ''.join(name.split())
        except IndexError:
            name = ''
        return name

    def get_job_functions(self):
        query = 'jobs-box__list jobs-description-details__list js-formatted-job-functions-list'
        try:
            name = self.soup.find_all('ul', class_=query)[0].text
            name = ''.join(name.split())
        except IndexError:
            name = ''
        return name

    def get_industry(self):
        query = 'jobs-box__list jobs-description-details__list js-formatted-industries-list'
        try:
            name = self.soup.find_all('ul', class_=query)[0].text
            name = ''.join(name.split())
        except IndexError:
            name = ''
        return name

    def get_past_day_applicants(self):
        query = 'jobs-details-premium-insight__list jobs-premium-applicant-insights__list'
        try:
            res = self.soup.find_all('ul', class_=query)[0].find_all('li')[0].text.replace('Applicants', '')
        except IndexError:
            res = ''
        return res

    def get_applicants_seniority(self):
        query = 't-14 t-black--light t-normal mb2 mh0'
        res = ''
        try:
            levels = self.soup.find_all('p', class_=query)
            if levels:
                for i in levels:
                    res += i.text + '#'
        except:
            res = ''
        return ' '.join(res.split()).replace(' # ', '#').replace(' #', '')

    def get_applicants_education(self):
        query = 'jobs-premium-applicant-insights__list-item pb1'
        res = ''
        try:
            education = self.soup.find_all('li', class_=query)
            if education:
                for i in education:
                    res += i.text + '#'
        except:
            res = ''
        return ' '.join(res.split()).replace(' # ', '#').replace(' #', '')

    def get_applicants_location(self):
        query = 'jobs-details-premium-insight__list mt4'
        res = ''
        try:
            education = self.soup.find_all('ul', class_=query)[0].find_all('li')
            if education:
                for i in education:
                    res += i.text + '#'
        except:

            res = ''
        return ' '.join(res.split()).replace(' # ', '#').replace(' #', '')

    def get_company_growth(self):
        query = 'jobs-premium-company-growth__stat-item ph5'
        res = ''
        try:
            alt = self.soup.find_all('li', class_=query)[0]
            alt = alt.find_all('p')
            if alt:
                for i in alt:
                    if isinstance(i, str):
                        continue
                    res += i.text
            res = ' '.join(res.split())
        except:
            res = ''
        return res

    def get_followers(self):
        query = 'jobs-company-information__follow-count inline'
        try:
            name = self.soup.find_all('span', class_=query)[0].text
        except IndexError:
            name = ''
        return name

    def get_job_data(self):
        """
        Get the job data by using the get* methods of the class.
        Return a dictionary
        :return: dict job data
        """

        job_data = {
            "job_url_beta": self.url,
            "job_name": self.get_job_title(),
            "company": self.get_company_name(),
            "company_url": self.get_company_url(),
            "full_field": self.get_full_field(),
            "location": self.get_location(),
            "posted_on": self.get_post_data(),
            "views": self.get_views(),
            "num_of_applicants": self.get_num_of_applicants(),
            "seniority": self.get_seniority(),
            "num_of_employees": self.get_employee_num(),
            "job_location": self.get_job_location(),
            "job_description": self.get_job_description(),
            "employment_type": self.get_employment_type(),
            "job_functions": self.get_job_functions(),
            "industry": self.get_industry(),
            # premium now
            "past_day_applicants": self.get_past_day_applicants(),
            "applicants_seniority": self.get_applicants_seniority(),
            "applicants_education": self.get_applicants_education(),
            "applicants_location": self.get_applicants_location(),
            "company_growth": self.get_company_growth(),
            "followers": self.get_followers()
        }
        return self.convert(job_data)

    def convert(self, data):
        for key in data.keys():
            if type(data[key]) is str:
                data[key] = data[key].replace('\n', '').replace('\r', '').replace('\t', '').strip()
        return data


if __name__ == '__main__':
    from bs4 import BeautifulSoup

    # todo skip these 3 rows later
    with open('job1.html', 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    soup = soup.find('div', role='main')
    print(soup)
    result = JobScraper(soup, 'URL FOR A JOB').get_job_data()
    for col in result.keys():
        print(col, (20 - len(col)) * ' ', ': ', result[col])
