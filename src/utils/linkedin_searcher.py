import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd


class LinkedinSearcher:
    """
        create an scraper agent for linkedin
    """
    def __init__(self):
        self.webpage_url = None
        self.page_number = None
        self.jobs = None
        self._df_job_result = pd.DataFrame(columns=['title', 'company', 'location', 'apply'])


    def job_scraper(self, webpage_url, page_number):
        self.webpage_url = webpage_url
        self.page_number = page_number
        next_page = self.webpage_url + str(self.page_number)
        response = requests.get(str(next_page))
        soup = BeautifulSoup(response.content,'html.parser')
        self.jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        
        for job in self.jobs:
            job_title = job.find('h3', class_='base-search-card__title').text.strip()
            job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
            job_location = job.find('span', class_='job-search-card__location').text.strip()
            job_link = job.find('a', class_='base-card__full-link')['href']
            self._df_job_result = self._df_job_result.append(
                {'title' : job_title,
                'company' : job_company,
                'location' : job_location,
                'apply': job_link}, ignore_index = True)

            
            
        if self.page_number < 100:
            self.page_number = self.page_number + 25
            self.job_scraper(self.webpage_url, self.page_number)
        
        else:
            return
            # print('File closed')

    
    def person_scraper(self):
        pass



if __name__=="__main__":

    url_ml = 'https://www.linkedin.com/jobs/search/?currentJobId=3428654835&f_TPR=r86400&geoId=100506914&keywords=machine%20learning%20engineer&location=Europe&refresh=true'
    url_ds = 'https://www.linkedin.com/jobs/search/?currentJobId=3428654835&f_TPR=r86400&geoId=100506914&keywords=data%20scientist&location=Europe&refresh=true'

    obj = LinkedinSearcher()
    obj.job_scraper(url_ds, 0)
    print(obj._df_job_result)