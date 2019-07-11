#!/usr/bin/env python
# coding: utf-8

# In[435]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs


baseurl = "https://charterbank.huygens.knaw.nl/?mivast=3593&miadt=3593&mizig=314&miview=tbl&milang=nl&micols=1&mires=0&mibj=1594&miej=1595"


# buildup of a url see https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse
parts = urlparse(baseurl)
parts

queryparts = dict(parse_qs(parts[4]))

url = "https://charterbank.huygens.knaw.nl"


def get_years(url= url, begin=1000, end=1800, step=1):
    """collect the number of results from a range of years between
    begin and end with a step"""
    year_overz = []
    years = range(begin, end, step)
    pairs = [(years[i], years[i + 1]) for i in range(len(years)-1)] 
    for pair in pairs:
        queryparts['mibj'] = pair[0]
        queryparts['miej'] = pair[1]   
        result = requests.get(url, params=queryparts)
        soup = BeautifulSoup(result.text, 'html5lib')
        aantal = soup.find_all(class_='mi_hits_hits_count')[0].text.strip()
        year_overz.append({'yr': '%s-%s' % (pair[0], pair[1]), 'number': aantal})
    return year_overz
    
def yr2dataframe(year_overz):
    yrdf = pd.DataFrame().from_records(year_overz)
    yrdf.number = yrdf.number.str.replace('.','')
    yrdf.number = yrdf.number.astype('int')
    return yrdf
