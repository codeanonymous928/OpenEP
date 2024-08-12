#! python3
# -*- encoding: utf-8 -*-

import os
import re
import json
from concurrent.futures import ThreadPoolExecutor
import copy
import random

from .utils.utils import chat_gpt_models, news_filter_by_date, chat_glm_models, count_vaild_tokens
from .prompt import integration_instruct as PROMPT_II
from .hierarchical_tree import SBertEmbeddingModel, TreeBuilder







class ChatIntegration():
    def __init__(self, config, prediction_module, tree_builder, flag_background, lang_type):
        self.config = config
        self.prediction = prediction_module
        self.flag_background = flag_background
        self.lang_type = lang_type
        self.tree_builder = tree_builder


    def message(self,role,content,name=None):
        m={'role':role, 'content':content}
        if name is not None: m['name']=name
        if self.verbose: self.show_message(m)
        return m
    
    def show_message(self,role, content):
        print(f'[{role}]:\n\n{content}\n\n')  
    

    def chunk_extraction_rel(self, query, data, desc, diversity_queries):
        data = ' '.join(data)
        data = count_vaild_tokens(data, self.config['rel_chunk_content_count'])        
        
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_II.chunk_ext_rel_8.format(language_type=self.lang_type,query=query, query_desc_=desc, diversity_quieries=diversity_queries, news_content_=data)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_II.chunk_ext_rel_7.format(language_type=self.lang_type,query=query, diversity_quieries=diversity_queries, news_content_=data)})          

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 
            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_II.chunk_ext_rel_8.format(language_type=self.lang_type,query=query, query_desc_=desc, diversity_quieries=diversity_queries, news_content_=data)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_II.chunk_ext_rel_7.format(language_type=self.lang_type,query=query, diversity_quieries=diversity_queries, news_content_=data)})                
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 
            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        try:
            content = self.data_clean_json(content)
            parsed_json = json.loads(content)
            return parsed_json
        except json.JSONDecodeError:
            return []            



    def chunk_extraction_sim(self, query, data, desc):
        data = ' '.join(data)
        data = count_vaild_tokens(data, self.config['sim_chunk_content_count'])              
        messages = []
        messages.append({'role': 'system', 'content': PROMPT_II.chunk_ext_sim_9.format(language_type=self.lang_type,query=query, sim_event_desc_=desc, news_content_=data)})
          
        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 
            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            messages.append({'role': 'user', 'content': PROMPT_II.chunk_ext_sim_9.format(language_type=self.lang_type,query=query, sim_event_desc_=desc, news_content_=data)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 
            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        try:
            content = self.data_clean_json(content)
            parsed_json = json.loads(content)
            return parsed_json
        except json.JSONDecodeError:
            return []          

    def data_clean_json(self, data):
        data = re.sub(r'```(?:python)?|json|Content is blocked|dict|list', '', data.strip())
        return data


    def is_valid_dict_string(self, data):
        try:
            data = re.sub(r'```(?:python)?|json|Content is blocked|dict|list', '', data.strip())
            parsed = json.loads(data)
            return isinstance(parsed, list)
        except ValueError:
            return False
        

    def __call__(self, query_id, question, date_question, div_rel_queries, query_desc, relevant_news, similar_news, question_type, start_time):
        print('Starting information integration ... ')     
        with ThreadPoolExecutor(max_workers=8) as executor:
            rel_chunks = executor.map(self.chunk_extraction_rel, [question]*len(relevant_news), relevant_news, [query_desc]*len(relevant_news), [div_rel_queries]*len(relevant_news)) 
        rel_chunks = list(rel_chunks)

        rel_total_chunks = []
        rel_unique_chunks = []
        for item in rel_chunks:
            rel_total_chunks += item
        rel_unique_chunks = list(set(rel_total_chunks))

        print('Hierarchical Tree for Relevant News ...')
        rel_clusters_idx, rel_cluster_count, rel_node_content, rel_node_desc =  self.tree_builder.node_description(rel_unique_chunks)

        print('Chunks Extarction Similar News ... ')
        sim_node_list = []
        for idx, item in enumerate(similar_news):
            sim_id = idx
            sim_desc = item['desc']
            sim_news_list = item['news_list']

            with ThreadPoolExecutor(max_workers=8) as executor:
                sim_chunks = executor.map(self.chunk_extraction_sim, [question]*len(sim_news_list), sim_news_list, [sim_desc]*len(sim_news_list)) 
            sim_chunks = list(sim_chunks)

            sim_total_chunks = []
            sim_unique_chunks = []
            for item in sim_chunks:
                sim_total_chunks += item
            sim_unique_chunks = list(set(sim_total_chunks))
            
            # build the hierarchical tree for similar news
            print('Hierarchical Tree for Similar News ...')
            clusters_idx, cluster_count, sim_node_content, sim_node_desc = self.tree_builder.node_description(sim_unique_chunks)
            sim_node_list.append(sim_node_desc)

        res = self.prediction(query_id, question, date_question, query_desc, relevant_news, similar_news, rel_node_desc, sim_node_desc, question_type, start_time)

        return res
        

if __name__=="__main__":
    tree_builder = TreeBuilder()