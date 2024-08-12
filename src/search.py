#! python3
# -*- encoding: utf-8 -*-

import os
import re 
import json
import pandas as pd
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import openai
import random
from readability import Document

from .utils.utils import news_filter_by_date

class BingSearch():
    def __init__(self, args, mkt, news_api_key, news_flag, web_flag, endpoint, bing_clean_=True, timeout=10):
        # Set your endpoint
        self.endpoint = endpoint
        self.content_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}  
        self.timeout = timeout 
        self.mkt = mkt
        self.news_api_key = news_api_key
        self.args = args
        self.news_flag = news_flag
        self.web_flag = web_flag
        self.bing_clean_ = bing_clean_


    def search(self, query, news_count, freshness, end_time):
        '''
        Extracts the relevant news from bing. 

        '''
        headers = {'Ocp-Apim-Subscription-Key': self.news_api_key}
        if freshness:
            params = {'q': query, 'mkt': self.mkt, 'count': news_count, 'freshness': freshness}
        else:
            params = {'q': query, 'mkt': self.mkt, 'count': news_count}
            
        news = []
        urls = []
        # Call the API
        try:
            response = requests.get(self.endpoint, headers=headers, params=params)
            response.raise_for_status()
            response_json = response.json()                

            if 'news' in response_json and self.news_flag:
                res_news = response_json['news']
                for res in res_news['value']:
                    news.append({"title": res['name'], 'url': res['url'], 'datePublished': res['datePublished'].split('T')[0], 'desc': res['description']})
                    urls.append(res['url'])                

            if 'webPages' in response_json and self.web_flag:
                res_web = response_json['webPages']
                for res in res_web['value']:
                    if 'datePublished' in res:
                        news.append({"title": res['name'], 'url': res['url'], 'datePublished': res['datePublished'].split('T')[0], 'desc': res['snippet']})
                        urls.append(res['url'])  
        except Exception as ex:
            raise ex
        
        if self.bing_clean_:
            news = news_filter_by_date(news, end_time)

        if len(news) > news_count:
            news = news[:news_count]

        return news



    def news_content_extract(self, data):
        '''
        Extracts the main content and title from a news article given its URL. 

        '''
        data['content'] = []
        try:
            response = requests.get(data['url'], headers=self.content_headers, timeout=self.timeout)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return data

        if response.status_code != 200:
            print("Failed to fetch the URL: ", response.status_code)
            return data
        
        if 'qq.com' in data['url'] or 'www.msn.' in data['url']:
            doc = Document(response.text)
            readable_article = doc.summary()
            readable_title = doc.short_title()

            clean_text = re.sub(r'<[^>]+>', '', readable_article)
            clean_text = re.sub(r'\s+', ' ', clean_text.strip())
            data['content'] = [clean_text]

        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else "No title found"

            # Adjusting the method to fetch paragraphs might be necessary for different websites
            paragraphs = soup.find_all('p')
            content = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            data['content'] = content

        return data


    def news_content_extract_by_url(self, url):
        '''
        Extracts the main content and title from a news article given its URL. 

        Parameters:
        - url (str): The URL of the news article from which content needs to be extracted.

        Returns:
        - list: A list containing the extracted text content of the news article.

        '''
        try:
            response = requests.get(url, headers=self.content_headers, timeout=self.timeout)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []

        if response.status_code != 200:
            print("Failed to fetch the URL: ", response.status_code)
            return []

        content = []
        if 'qq.com' in url or 'www.msn.' in url:
            doc = Document(response.text)
            readable_article = doc.summary()
            readable_title = doc.short_title()

            clean_text = re.sub(r'<[^>]+>', '', readable_article)
            clean_text = re.sub(r'\s+', ' ', clean_text.strip())
            content = [clean_text]
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else "No title found"
            # Adjusting the method to fetch paragraphs might be necessary for different websites
            paragraphs = soup.find_all('p')
            content = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]

        return content
















if __name__=="__main__":
    ''













