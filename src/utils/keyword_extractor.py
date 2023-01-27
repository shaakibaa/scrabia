from keybert import KeyBERT
from langdetect import detect
from keybert import KeyBERT
import pandas as pd

kw_model = KeyBERT()

def keyword_extractor(doc):
    # first detect the language (we just need english job description)
    lang = detect(doc)
    if lang == 'en':
        # extracting keywords using keyBERT
        keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 1), stop_words='english',
                                use_maxsum=True, nr_candidates=20, top_n=10)
        
        return str(keywords)
    
    else:
        return []


if __name__=="__main__":
    _df_job_result = pd.read_csv('test.csv')
    _df_job_result['Keywords'] = _df_job_result['Description'].apply(keyword_extractor)


    