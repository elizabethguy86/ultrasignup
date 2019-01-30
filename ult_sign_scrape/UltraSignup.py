import requests
from selenium.webdriver import (Chrome)
from string import ascii_lowercase
from pymongo import MongoClient
from bs4 import BeautifulSoup
import json
import sys
import pandas as pd
import time
from scipy.stats import ttest_ind
import plotly.plotly as py
import plotly.graph_objs as go

root_url = 'http://ultrasignup.com'
#index_url = root_url + '/results_event.aspx?did=41880' #add index for event of interest


def get_results(index_url):
    '''Starts web scraper to get table
    with runner results.  Returns column headers
    and result data.'''
    browser = Chrome()
    browser.get(index_url)
    sel = "gbox_list" 
    cascade100results=browser.find_element_by_id(sel) #setting a css selector
    table_rows = cascade100results.text.split('\n')
    runner_rows = [row.split() for row in table_rows]
    cols = runner_rows[0:10] #column headers
    content = runner_rows[11:] #the actual runner results
    return (cols, content)

#find index of Did Not Finish and Did Not Start
def find_idx(content):
    indices = []
    for idx, row in enumerate(content):
        if row[0] == 'Did':
            indices.append(idx)
    return indices



def make_finisher_df(content, idx_1):
    '''take in runner row content and the index
    indicating the end of the finishers list (idx_1).  
    return dataframe with the male and female times.'''
    finished = content[0:idx_1]
    gender = []
    times = []
    for row in finished:
        times.append(row[-2])
        gender.append(row[-4])
    df = pd.DataFrame({'Gender': gender, 'Time': times})
    df['Time'] = cascade1002017['Time'].str.split(':')
    df['Time'] = cascade1002017['Time'].apply(lambda x: int(x[0]) * 60 + int(x[1]) + float(x[2])/60)
    return df

