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






def query_expansion(query, ori_desc, generated_desc, pred_time, stop_words, flag_background, config, lang_type, search_fn):
    arg_sta_dict = {'stakeholders': [], 'stak_abstraction': []}
    # gengerate diversity queries to search relevant news for query
    news_content = background_retrieval(query, pred_time, lang_type, config, search_fn)
    news_content_copy = copy.deepcopy(news_content)
    news_content_copy = news_content_copy[:min(len(news_content_copy), 3)]

    # query description formalization
    re_query_desc = ''
    if flag_background in [4,5]:
        with ThreadPoolExecutor(max_workers=8) as executor:
            desc_list = executor.map(query_desc_format, news_content_copy, [query]*len(news_content_copy), [config]*len(news_content_copy), [lang_type]*len(news_content_copy)) 
        re_query_desc = list(desc_list)

    query_desc = ''
    if config['flag_background'] == 1:
        query_desc = ori_desc
    elif config['flag_background'] == 2:
        query_desc = generated_desc
    elif config['flag_background'] == 3:
        query_desc = ori_desc + '\n\n' + generated_desc
    elif config['flag_background'] == 4:
        query_desc = re_query_desc
    elif config['flag_background'] == 5:
        query_desc = ori_desc + '\n\n' + generated_desc + '\n\n' + re_query_desc

    # event stakeholders extraction and abstraction
    print('event stakeholders extraction and abstraction')
    with ThreadPoolExecutor(max_workers=8) as executor:
        sta_abs = executor.map(stakeholders_ext_abs, [query]*len(news_content), news_content, [query_desc]*len(news_content), [config]*len(news_content), [flag_background]*len(news_content), [lang_type]*len(news_content)) 
        for per_sta in list(sta_abs):
            arg_sta_dict['stakeholders'] += per_sta['entity']
            arg_sta_dict['stak_abstraction'] += per_sta['role']
    
    arg_sta_dict_clean = arg_stak_clean(arg_sta_dict, stop_words)
    
    return query_desc, arg_sta_dict_clean


def background_retrieval(query, pred_time, lang_type, config, search_fn):
    messages = []
    messages.append({'role': 'system', 'content': PROMPT_IR.query_background.format(background_query_count_=config['background_query_count_'], language_type=lang_type, query=query)})

    content = ''
    role = ''
    if 'gpt' in config['model_name']:
        selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, config['sleep'])
    elif 'glm' in config['model_name']:
        messages = []
        messages.append({'role': 'user', 'content': PROMPT_IR.query_background.format(background_query_count_=config['background_query_count_'], language_type=lang_type, query=query)})            
        selected_api_key = random.choice(config['api_key_glms'][config['model_name']]) 
        content, role = chat_glm_models(selected_api_key, config['model_name'], messages, config['sleep'])     

    div_news = []
    if content is not None:
        if '#' in content:
            div_news = content.strip().split('#')
            div_news = [i for i in div_news if len(i) > 1]
        elif '\n' in content:
            div_news = content.strip().split('\n')
            div_news = [i for i in div_news if len(i) > 1]                
        else:
            div_news = [content]
    
    news_list = []
    # retrieve news by original query and the diersity queries
    start_date = get_date_days_prior(pred_time, 180)
    news = search_fn.search(query, config['query_desc_ori_count'], '{}..{}'.format(start_date, pred_time), pred_time)
    news_list = news_list + news

    if len(div_news) > 0:
        with ThreadPoolExecutor(max_workers=8) as executor:
            item_news_ = executor.map(search_fn.search, div_news, [config['query_desc_div_count']]*len(div_news), ['{}..{}'.format(start_date, pred_time)]*len(div_news), [pred_time]*len(div_news)) 

        item_news = [item for result in list(item_news_) for item in result]
        news_list = news_list + item_news

    # news clean
    news_clean_date = news_filter_by_date(news_list, deadline=pred_time)
    with ThreadPoolExecutor(max_workers=8) as executor:
        consis_scores = executor.map(news_filter_by_consistency, [query]*len(news_clean_date), news_clean_date, [config]*len(news_clean_date)) 
    consis_scores = list(consis_scores)
    assert len(news_clean_date) == len(consis_scores)
    news_clean_consistency = [news_clean_date[idx] for idx, val in enumerate(consis_scores) if val == 1]

    if len(news_clean_consistency) < 1:
        news_clean_consistency = [news_clean_date[0]]

    # news content extract
    with ThreadPoolExecutor(max_workers=8) as executor:
        fusion_url_content = executor.map(search_fn.news_content_extract, news_clean_consistency) 
    news_content = [i['content'] for i in list(fusion_url_content) if len(i['content'])]
    assert len(news_content) > 0

    return news_content




def query_desc_format(news_content, query, config, lang_type):
    assert isinstance(news_content, list)
    news_content = ' '.join(news_content)       
    news_content = count_vaild_tokens(news_content, config['sim_chunk_content_count'])

    messages = []
    messages.append({'role': 'system', 'content': PROMPT_IR.query_desc.format(desc_length=config['query_desc_len'], language_type=lang_type, query=query, news_content_=news_content)})
    content = ''
    role = ''
    if 'gpt' in config['model_name']:
        selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, config['sleep'])
    elif 'glm' in config['model_name']:
        messages = []
        messages.append({'role': 'user', 'content': PROMPT_IR.query_desc.format(desc_length=config['query_desc_len'], language_type=lang_type, query=query, news_content_=news_content)})            
        selected_api_key = random.choice(config['api_key_glms'][config['model_name']]) 
        content, role = chat_glm_models(selected_api_key, config['model_name'], messages, config['sleep'])   
    
    return content

def arguments_ext_abs(query, news_content, desc, config, flag_background, lang_type):
    news_content = ' '.join(news_content)
    news_content = count_vaild_tokens(news_content, config['arg_content_count'])
    messages = []
    if flag_background != 0:
        messages.append({'role': 'system', 'content': PROMPT_IR.argument_abstraction_2.format(language_type=lang_type, query=query, query_desc_=desc, news_content_=news_content)})
    else:
        messages.append({'role': 'system', 'content': PROMPT_IR.argument_abstraction_3.format(language_type=lang_type, query=query, news_content_=news_content)})            

    content = ''
    role = ''
    if 'gpt' in config['model_name']:
        selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, config['sleep'])
    elif 'glm' in config['model_name']:
        messages = []
        if flag_background != 0:
            messages.append({'role': 'user', 'content': PROMPT_IR.argument_abstraction_2.format(language_type=lang_type, query=query, query_desc_=desc, news_content_=news_content)})
        else:
            messages.append({'role': 'user', 'content': PROMPT_IR.argument_abstraction_3.format(language_type=lang_type, query=query, news_content_=news_content)})              
        selected_api_key = random.choice(config['api_key_glms'][config['model_name']]) 
        content, role = chat_glm_models(selected_api_key, config['model_name'], messages, config['sleep'])   
    
    arguments, arg_abs = split_entity_and_role(content)       

    return {'entity': arguments, 'role': arg_abs}


def stakeholders_ext_abs(query, news_content, desc, config, flag_background, lang_type):
    news_content = ' '.join(news_content)
    news_content = count_vaild_tokens(news_content, config['stka_content_count'])
    messages = []
    if flag_background != 0:
        messages.append({'role': 'system', 'content': PROMPT_IR.stakeholder_abstraction_2.format(language_type=lang_type, query=query, query_desc_=desc, news_content_=news_content)})
    else:
        messages.append({'role': 'system', 'content': PROMPT_IR.stakeholder_abstraction_3.format(language_type=lang_type, query=query, news_content_=news_content)})            

    content = ''
    role = ''
    if 'gpt' in config['model_name']:
        selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, config['sleep'])
    elif 'glm' in config['model_name']:
        messages = []
        if flag_background != 0:
            messages.append({'role': 'user', 'content': PROMPT_IR.stakeholder_abstraction_2.format(language_type=lang_type, query=query, query_desc_=desc, news_content_=news_content)})
        else:
            messages.append({'role': 'user', 'content': PROMPT_IR.stakeholder_abstraction_3.format(language_type=lang_type, query=query, news_content_=news_content)})              
        selected_api_key = random.choice(config['api_key_glms'][config['model_name']]) 
        content, role = chat_glm_models(selected_api_key, config['model_name'], messages, config['sleep'])   
    
    arguments, arg_abs = split_entity_and_role(content)       

    return {'entity': arguments, 'role': arg_abs}

def split_entity_and_role(data):
    entity, role = [], []
    if data is not None and '@@' in data:
        parts = data.split('@@')
        if '#' in parts[0]:
            entity = [item for item in parts[0].split('#') if len(item.strip()) < 20]
            if len(entity) > 10:
                entity = entity[:10]
        if '#' in parts[1]:
            role = [item for item in parts[1].split('#') if len(item.strip()) < 20]
            if len(role) > 10:
                role = role[:10]
    return entity, role




def news_filter_by_consistency(query, data, config):
    messages = []
    messages.append({'role': 'system', 'content': PROMPT_IR.consistency_to_query.format(query=query, title=data['title'], desc=data['desc'])})
    content = ''
    role = ''
    if 'gpt' in config['model_name']:
        selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, config['sleep'])
    elif 'glm' in config['model_name']:
        messages = []
        messages.append({'role': 'user', 'content': PROMPT_IR.consistency_to_query.format(query=query, title=data['title'], desc=data['desc'])})            
        selected_api_key = random.choice(config['api_key_glms'][config['model_name']]) 

        content, role = chat_glm_models(selected_api_key, config['model_name'], messages, config['sleep'])   

    if content is not None and '1' in content:  
        return 1
    else:
        return 0









