import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils.keyword_extractor import keyword_extractor


def request_response(url):

    # getting the webpage, creating a Response object
    response = requests.get(url)

    # extracting the source code of the page & passing the source code to BeautifulSoup to create a BeautifulSoup object for it 
    soup = BeautifulSoup(response.content,'html.parser')
    return soup


class LinkedinSearcher:
    def __init__(self):

        # init jobs attributes
        self.webpage_url = None
        self.page_number = None
        self.jobs = None
        self._df_job_result = pd.DataFrame(columns=['Title', 'Company', 'Location', 'Apply', 'Description'])


    def job_scraper(self, webpage_url, page_number):
        self.webpage_url = webpage_url
        self.page_number = page_number
        next_page = self.webpage_url + str(self.page_number)
        soup = request_response(str(next_page))
        self.jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')


        for job in self.jobs:
            job_description = ''
            job_title = job.find('h3', class_='base-search-card__title').text.strip()
            job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
            job_location = job.find('span', class_='job-search-card__location').text.strip()
            job_link = job.find('a', class_='base-card__full-link')['href']
            job_soup = request_response(job_link)
            # adding job description
            job_description = job_soup.find_all('div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5')[0].text.strip()
            

            self._df_job_result = self._df_job_result.append(
                {'Title' : job_title,
                'Company' : job_company,
                'Location' : job_location,
                'Apply': job_link,
                'Description': job_description}, ignore_index = True)

        # adding keywords
        self._df_job_result['Keywords'] = self._df_job_result['Description'].apply(keyword_extractor)

        if self.page_number < 100:
            self.page_number = self.page_number + 25
            self.job_scraper(self.webpage_url, self.page_number)
        
        else:
            return

    

if __name__=="__main__":

    # job scraping
    url_ml = 'https://www.linkedin.com/jobs/search/?currentJobId=3428654835&f_TPR=r86400&geoId=100506914&keywords=machine%20learning%20engineer&location=Europe&refresh=true'
    url_ds = 'https://www.linkedin.com/jobs/search/?currentJobId=3428654835&f_TPR=r86400&geoId=100506914&keywords=data%20scientist&location=Europe&refresh=true'
    obj = LinkedinSearcher()
    obj.job_scraper(url_ds, 0)
    print(obj._df_job_result)
    # obj._df_job_result.to_csv('test.csv', index=False)
