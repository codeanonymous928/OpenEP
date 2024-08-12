#! python3
# -*- encoding: utf-8 -*-

import os
import re
import json
from tqdm import tqdm
import time

from .query_disambiguation import ChatDisambiguation
from .information_retrieval import ChatRetrieval
from .information_integration import ChatIntegration
from .event_prediction import ChatPrediction

from .search import BingSearch
from .hierarchical_tree import SBertEmbeddingModel, TreeBuilder
from .utils.utils import get_current_date, get_date_for_sim_event
from .utils.record import initialize_record


def build_world(config, lang_type):
    # load bing search
    print('Loading Bing Search ... ')
    bing_search = BingSearch(lang_type, config, config['news_api_key'], config['news_flag'], config['web_flag'], config['endpoint'])
    print(config['build_type'])

    # load embedding models
    print('Loading Embedding Models ... ')
    embedding_model = SBertEmbeddingModel(lang_type)

    # load tree builder
    print('Loading Tree Builder ... ')
    tree_builder = TreeBuilder(config, embedding_model, lang_type)

    if config['build_type'] == 'llm':
        return LLMBuilder(config, bing_search, tree_builder, lang_type=lang_type)
    elif config['build_type'] == 'slm':
        raise NotImplementedError(f'Build type {config["build_type"]} not implemented.')
    else:
        raise f'Build type {config["build_type"]} not found.'




class LLMBuilder():

    def __init__(self, config, search_fn, tree_builder, module_type='agent', lang_type='zh-CN'):
        self.config = config
        self.search_fn = search_fn
        self.module_type = module_type
        self.lang_type = lang_type
        self.tree_builder = tree_builder

        self.load_modules()


    
    def load_modules(self):
        if self.module_type == 'agent':
            print('Set up Event Prediction ... ')
            self.prediction = ChatPrediction(self.config, lang_type=self.lang_type, flag_background = self.config['flag_background'])

            print('Set up Information Integration ... ')
            self.integration = ChatIntegration(self.config, self.prediction, self.tree_builder, flag_background = self.config['flag_background'], lang_type=self.lang_type)

            print('Set up Information Retrieval ... ')
            self.retrieval = ChatRetrieval(self.config, self.search_fn, self.integration, flag_background = self.config['flag_background'], lang_type=self.lang_type)

            print('Set up Query Disambiguation ... ')
            self.disambiguation = ChatDisambiguation(self.config, self.search_fn, self.retrieval)
        else:
            raise f'Module type {self.module_type} not implementation.'


    
    def run(self, data, stop_words):
        curr_time = get_current_date()      
        for item in tqdm(data, desc='Processing'):
            start_time = time.time()
                
            res = self.disambiguation(item, stop_words, start_time)

        return res





