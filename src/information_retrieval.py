#! python3
# -*- encoding: utf-8 -*-

import random
import os
import re
import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import copy

from .utils.utils import chat_gpt_models, news_filter_by_date, get_date_days_prior, arg_stak_clean, load_records, chat_glm_models,count_vaild_tokens
from .prompt import retrieval_instruct as PROMPT_IR
from .query_expansion import query_expansion


class ChatRetrieval():
    def __init__(self, config, search_fn, integration, flag_background, lang_type):
        self.config = config
        self.search_fn = search_fn
        self.integration = integration
        self.flag_background = flag_background
        self.lang_type = lang_type

    def message(self,role,content,name=None):
        m={'role':role, 'content':content}
        if name is not None: m['name']=name
        if self.verbose: self.show_message(m)
        return m
    
    def show_message(self,role, content):
        print(f'[{role}]:\n\n{content}\n\n')   


    def relevant_event_retrieval(self, query, pred_time, stak_en, desc):
        rel_queries = self.diversity_query_relevant(query, stak_en, desc)

        news_list = []
        news = self.search_fn.search(query, self.config['rel_ori_news_count'], '2020-01-01..{}'.format(pred_time), pred_time)
        news_list = news_list + news       

        start_date = get_date_days_prior(pred_time, 180)
        with ThreadPoolExecutor(max_workers=8) as executor:
            item_news_ = executor.map(self.search_fn.search, rel_queries, [self.config['rel_div_news_count']]*len(rel_queries), ['{}..{}'.format(start_date, pred_time)]*len(rel_queries), [pred_time]*len(rel_queries)) 
        item_news = [item for result in list(item_news_) for item in result]
        news_list = news_list + item_news

        # news clean
        news_clean_date = news_filter_by_date(news_list, deadline=pred_time)

        # news content extract
        with ThreadPoolExecutor(max_workers=8) as executor:
            fusion_url_content_ = executor.map(self.search_fn.news_content_extract, news_clean_date) 
        fusion_url_content = list(fusion_url_content_)
        news_content = [i['content'] for i in list(fusion_url_content) if i['content'] != [''] and len(i['content']) > 0]
        assert len(news_content) > 0
        
        return news_content, rel_queries

    def diversity_query_relevant(self, query, stak_en, desc):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_IR.relevant_queries_2.format(query_count_=self.config['diversity_query_count_'],language_type=self.lang_type,query=query, query_desc_=desc, stakeholders=stak_en)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_IR.relevant_queries_3.format(query_count_=self.config['diversity_query_count_'],language_type=self.lang_type,query=query, stakeholders=stak_en)})            

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 
            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_IR.relevant_queries_2.format(query_count_=self.config['diversity_query_count_'],language_type=self.lang_type,query=query, query_desc_=desc, stakeholders=stak_en)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_IR.relevant_queries_3.format(query_count_=self.config['diversity_query_count_'],language_type=self.lang_type,query=query, stakeholders=stak_en)})             
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 
            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   
        
        if '#' in content:
            queries = content.strip().split('#')
            queries = [i for i in queries if len(i) > 1]            
        elif '\n' in content:
            queries = content.strip().split('\n') 
            queries = [i for i in queries if len(i) > 1]            
        elif content == '':
            queries = [query]
        else:
            queries = [content]       
        
        queries = queries[:self.config['diversity_query_count_']] if len(queries) > self.config['diversity_query_count_'] else queries

        return queries


    def similar_event_retrieval(self, query, pred_time, stak_en, stak_role, desc):
        rel_queries = self.diversity_query_similar(query, stak_en, stak_role, desc)
        news_list = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            item_news_ = executor.map(self.search_fn.search, rel_queries, [self.config['sim_news_count']]*len(rel_queries), [self.config['date_similar_event']]*len(rel_queries), [pred_time]*len(rel_queries)) 
        item_news = [item for result in list(item_news_) for item in result]
        news_list = news_list + item_news        

        # news clean
        date_tar = get_date_days_prior(pred_time, 150)
        news_clean_date = news_filter_by_date(news_list, deadline=date_tar)
        print('news_clean_date: {}'.format(len(news_clean_date)))
      
        # news content extract
        with ThreadPoolExecutor(max_workers=8) as executor:
            fusion_url_content_ = executor.map(self.search_fn.news_content_extract, news_clean_date) 
        fusion_url_content = list(fusion_url_content_)
        news_content = [i['content'] for i in list(fusion_url_content) if len(i['content'])]
        assert len(news_content) > 0

        # compute the similar score between news and user query
        with ThreadPoolExecutor(max_workers=8) as executor:
            scores_ = executor.map(self.relevance_calculation, [query]*len(news_content), news_content) 

        # Sorting list a and keeping track of the indices
        sorted_indices = [i[0] for i in sorted(enumerate(scores_), key=lambda x: x[1], reverse=True)]
        # Reordering list b according to the sorted indices of list a
        root_sim_news= [fusion_url_content[index] for index in sorted_indices]
        if len(root_sim_news) > self.config['top_k_sim']:
            root_sim_news = root_sim_news[:self.config['top_k_sim']]
        if len(root_sim_news) < 1:
            root_sim_news = [fusion_url_content[0]]

        # obtain the diversity queries for similar news
        with ThreadPoolExecutor() as executor:
            diversity_queries_sim = executor.map(self.diversity_queries_similar_news, [query]*len(root_sim_news), root_sim_news)       
        diversity_queries_sim = list(diversity_queries_sim)
        assert len(root_sim_news) == len(diversity_queries_sim)

        sim_event_content = self.extract_sim_event_content(query, root_sim_news, diversity_queries_sim, date_tar)    

        return sim_event_content

    def diversity_query_similar(self, query, stak_en, stak_role, desc):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_IR.similar_queries_2.format(query_count_=self.config['sim_query_count_'],language_type=self.lang_type,query=query, query_desc_=desc, stakeholders=stak_en, stakeholder_role=stak_role)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_IR.similar_queries_3.format(query_count_=self.config['sim_query_count_'],language_type=self.lang_type,query=query, stakeholders=stak_en, stakeholder_role=stak_role)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 
            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_IR.similar_queries_2.format(query_count_=self.config['sim_query_count_'],language_type=self.lang_type,query=query, query_desc_=desc, stakeholders=stak_en, stakeholder_role=stak_role)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_IR.similar_queries_3.format(query_count_=self.config['sim_query_count_'],language_type=self.lang_type,query=query, stakeholders=stak_en, stakeholder_role=stak_role)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 
            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        if '#' in content:
            queries = content.strip().split('#')
            queries = [i for i in queries if len(i) > 1]             
        elif '\n' in content:
            queries = content.strip().split('\n') 
            queries = [i for i in queries if len(i) > 1]             
        elif content == '':
            queries = [query]
        else:
            queries = [content] 
        queries = queries[:self.config['sim_query_count_']] if len(queries) > self.config['sim_query_count_'] else queries         


        return queries

    def relevance_calculation(self, query, data):

        data = ' '.join(data)
        data = count_vaild_tokens(data, self.config['sim_score_query_count'])
        messages = []
        messages.append({'role': 'system', 'content': PROMPT_IR.similar_news_score.format(query=query, news_article=data)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 
            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            messages.append({'role': 'user', 'content': PROMPT_IR.similar_news_score.format(query=query, news_article=data)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 
            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])          

        if content.isdigit():
            return int(content)
        else:
            return 1

    def diversity_queries_similar_news(self, query, data):
        news_content = ' '.join(data['content'])
        news_content = count_vaild_tokens(news_content, self.config['sim_chunk_content_count'])
        messages = []
        messages.append({'role': 'system', 'content': PROMPT_IR.diversity_queries_sim_3.format(query_count_=self.config['sim_div_query_count_'], language_type=self.lang_type, query=query, news_article=news_content)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 
            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            messages.append({'role': 'user', 'content': PROMPT_IR.diversity_queries_sim_3.format(query_count_=self.config['sim_div_query_count_'], language_type=self.lang_type, query=query, news_article=news_content)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 
            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])     

        if '#' in content:
            queries = content.strip().split('#')
            queries = [i for i in queries if len(i) > 1]             
        elif '\n' in content:
            queries = content.strip().split('\n') 
            queries = [i for i in queries if len(i) > 1]             
        elif content == '':
            queries = [query]
        else:
            queries = [content] 
        queries = queries[:self.config['sim_query_count_']] if len(queries) > self.config['sim_query_count_'] else queries  

        return queries


    def extract_sim_event_content(self, query, root_sim_news, queries, pred_time):
        results = []
        for idx, val in enumerate(root_sim_news):
            desc_ = self.sim_news_desc_format(root_sim_news[idx])

            # obtain the news for similar news
            with ThreadPoolExecutor() as executor:
                news_sim_ = executor.map(self.search_fn.search, queries[idx], [self.config['sim_div_news_count']]*len(queries[idx]), [self.config['date_similar_event']]*len(queries[idx]), [pred_time]*len(queries[idx]))   
            news_sim = [item for result in list(news_sim_) for item in result]  

            with ThreadPoolExecutor(max_workers=8) as executor:
                news_sim_list = executor.map(self.search_fn.news_content_extract, news_sim) 
            news_sim_list = list(news_sim_list)
            news_sim_content = [i['content'] for i in news_sim_list if i['content'] != [''] and len(i['content']) > 0]

            results.append({'desc': desc_, 'news_list': root_sim_news[idx]['content'] + news_sim_content})

        return results

    def sim_news_desc_format(self, data):
        # assert isinstance(content, list)      
        news_content = ' '.join(data['content'])
        news_content = count_vaild_tokens(news_content, self.config['sim_chunk_content_count'])
        messages = []
        messages.append({'role': 'system', 'content': PROMPT_IR.sim_event_desc.format(desc_length=self.config['sim_query_desc_len'], language_type=self.lang_type, news_content_=news_content)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 
            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            messages.append({'role': 'user', 'content': PROMPT_IR.sim_event_desc.format(desc_length=self.config['sim_query_desc_len'], language_type=self.lang_type, news_content_=news_content)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 
            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   
        
        return content



    def __call__(self, data, stop_words, start_time):
        print('Starting Information Retrieval ... ')
        question = data['question']
        date_question = data['date_question']
        question_type = data['question_type'] 
        query_id = data['id']   
        ori_desc = data['hot_topic']['ori_background']   
        generated_desc = ''

        # extract query background
        # extarct arguments and stakeholders
        print('Starting query expansion!!!')
        query_desc, arg_sta_dict = query_expansion(question, ori_desc, generated_desc, date_question, stop_words, self.flag_background, self.config, self.lang_type, self.search_fn)

        # extract relevant event news
        print('Starting extract relevant event news!!!')
        relevant_news, div_rel_queries = self.relevant_event_retrieval(question, date_question, arg_sta_dict['stakeholders'], query_desc)

        # extract similar event news
        print('Starting extract relevant event news!!!')
        similar_news = self.similar_event_retrieval(question, date_question, arg_sta_dict['stakeholders'], arg_sta_dict['stak_abstraction'], query_desc) 

        res = self.integration(query_id, question, date_question, div_rel_queries, query_desc, relevant_news, similar_news, question_type, start_time)

        return res
        




if __name__=="__main__":
    ''