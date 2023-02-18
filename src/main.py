from utils.db_manager import DBManager
from utils.linkedin_searcher import LinkedinSearcher


# my preferred links
url_ml = 'https://www.linkedin.com/jobs/search/?currentJobId=3428654835&f_TPR=r86400&geoId=100506914&keywords=machine%20learning%20engineer&location=Europe&refresh=true'
url_ds = 'https://www.linkedin.com/jobs/search/?currentJobId=3428654835&f_TPR=r86400&geoId=100506914&keywords=data%20scientist&location=Europe&refresh=true'

# scrape linkedin
linkedin_obj = LinkedinSearcher()
linkedin_obj.job_scraper(url_ds, 0)

# insert into db
db_manager = DBManager('localhost', 5432, 'scrabia', 'postgres', 'postgres')
params = [('title', 'text'),
            ('company', 'text'),
            ('location', 'text'),
            ('apply', 'text'),
            ('description', 'text'),
            ('keywords', 'text')]
db_manager.create_table('scrabia', params)
db_manager.df_to_table(linkedin_obj._df_job_result, 'scrabia')
