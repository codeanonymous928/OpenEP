#! python3
# -*- encoding: utf-8 -*-

import os
import re
import json
import argparse
from src.api_keys import GPT_MODEL_DICT, GLM_MODLE_DICT, BASE_URL, NEWS_API_KEY, ENDPOINT_BING




def common_config(parser):
    # data
    parser.add_argument("--data_path", default='', required=True, type=str, 
                        help='Data path for questions')

    parser.add_argument("--response_path", default='', required=True, type=str, 
                        help='Data path for prediction')

    parser.add_argument("--log_path", default='', type=str, 
                        help='log path')
    
    parser.add_argument("--bad_cases_path", default='', type=str, 
                        help='bad case path')  

    parser.add_argument("--stop_words_path", default='data/stopwords.json', type=str, 
                        help='stop word for query expansion')
 
    parser.add_argument("--date_similar_event", default='2000-01-01..2024-01-01', type=str, 
                        help='The start time for searching the similar event news.')    

    parser.add_argument("--flag_record", default=True, type=bool, 
                        help='Whether to store the answering process.')  

    # word build
    parser.add_argument("--build_type", default='llm', type=str,
                        help='The implementation of the FEP: llm, slm')    

    # llm gpts
    parser.add_argument("--model_name", default='gpt-3.5-turbo-16k', required=True,  type=str, 
                        help='GPT model list: {list(gpt_model_dict.keys())}')

    parser.add_argument("--base_url", default=BASE_URL, type=str, 
                        help='Using the base url')

    parser.add_argument("--api_key_gpts", default=GPT_MODEL_DICT, type=dict, 
                        help='The api keys for the gpt models, such as chatgpt, gpt4')

    parser.add_argument("--api_key_glms", default=GLM_MODLE_DICT, type=dict, 
                        help='The api keys for the glm models, such as glm4')

    parser.add_argument("--sleep", default=0, type=int, 
                        help='')

    # news
    parser.add_argument("--news_api_key", default=NEWS_API_KEY, type=str,
                        help='The news api key for searching news from bing')

    parser.add_argument("--mkt", default='zh-CN', required=True, type=str, 
                        help='The searching language list: zh-CN, en-US')

    parser.add_argument("--news_count", default=10, type=int, 
                        help='')
    
    parser.add_argument("--query_desc_ori_count", default=10, type=int, 
                        help='')    

    parser.add_argument("--query_desc_div_count", default=5, type=int, 
                        help='')

    parser.add_argument("--rel_ori_news_count", default=5, type=int, 
                        help='')

    parser.add_argument("--rel_div_news_count", default=5, type=int, 
                        help='')
    
    parser.add_argument("--sim_news_count", default=5, type=int, 
                        help='')

    parser.add_argument("--sim_div_news_count", default=5, type=int, 
                        help='')

    parser.add_argument("--query_desc_len", default=1000, type=int, 
                        help='The word length for generating query background.')

    parser.add_argument("--sim_query_desc_len", default=1000, type=int, 
                        help='')

    parser.add_argument("--sim_score_query_count", default=2000, type=int, 
                        help='')

    parser.add_argument("--sim_chunk_content_count", default=4000, type=int, 
                        help='')

    parser.add_argument("--rel_chunk_content_count", default=5000, type=int, 
                        help='')

    parser.add_argument("--arg_content_count", default=5000, type=int, 
                        help='')
    
    parser.add_argument("--stka_content_count", default=5000, type=int, 
                        help='')    

    parser.add_argument("--freshness", default='', type=str, 
                        help='To get articles discovered by Bing during a specific timeframe, specify a date range in the form, YYYY-MM-DD..YYYY-MM-DD. For example, &freshness=2019-02-01..2019-05-30. To limit the results to a single date, set this parameter to a specific date. For example, &freshness=2019-02-04.')

    parser.add_argument("--split_p", default=False, type=bool, 
                        help="Should the news content be divided into paragraphs. True means Yes, False means No")

    parser.add_argument("--news_flag", default=True, type=bool, 
                        help="search for news")

    parser.add_argument("--web_flag", default=True, type=bool, 
                        help="search for web pages")   

    parser.add_argument("--endpoint", default=ENDPOINT_BING, type=str, 
                        help="search for web pages") 

    return parser



def query_dis_config(parser):

    parser.add_argument("--flag_qdis", default=False, type=str, 
                        help='Indicate whether to use the module of query disambiguation. Select True to enable the module, or False to disable it.')

    return parser

def information_retri_config(parser):
    parser.add_argument("--flag_background", default=1, type=int,
                        help="Controls how background information is utilized. Choose options from 0 to 5 to specify how to handle and utilize background information: \
                            0 - No background, \
                            1 - Original background, \
                            2 - Generated background, \
                            3 - Combine 1 and 2, \
                            4 - Regenerated background, \
                            5 - Combine 1, 2 and 4.")

    parser.add_argument("--background_query_count_", default=5, type=int, 
                        help='The number of regenerated queries for query background.')

    parser.add_argument("--diversity_query_count_", default=5, type=int, 
                        help='The number of regenerated diversity queries.')

    parser.add_argument("--sim_query_count_", default=5, type=int, 
                        help='The number of regenerated sim queries.')

    parser.add_argument("--sim_div_query_count_", default=5, type=int, 
                        help='The number of regenerated sim and div queries.')

    parser.add_argument("--query_count", default=5, type=int, 
                        help='The number of regenerated queries for retrieving relevant/similar event news.')

    parser.add_argument("--top_k_sim", default=1, type=int, 
                        help='The number of similar events.')

    return parser


def information_inte_config(parser):
    parser.add_argument("--threshold", default=0.4, type=float, 
                        help='The smallest score to slect the node.')

    parser.add_argument("--max_clusters", default=20, type=int, 
                        help='Maximum number of clusters.')

    parser.add_argument("--min_clusters", default=6, type=int, 
                        help='Maximum number of clusters.')

    parser.add_argument("--max_words_node_desc", default=1000, type=int, 
                        help='Maximum word count for the node description derived via summarization method.')

    return parser






def evaluation_config(parser):
    parser.add_argument("--predictions_path", default='', required=True, type=str, 
                        help='Data path for model predictions')
    
    parser.add_argument("--questions_path", default='', required=True, type=str, 
                        help='Data path for questions')
    
    parser.add_argument("--ground_truth_path", default='', required=True, type=str, 
                        help='Data path for ground truth')    

    parser.add_argument("--confidence_flag", default=True,  type=bool, 
                        help='Whether utilize the confidence score')

    parser.add_argument("--model_name", default='gpt-4-turbo', required=True,  type=str, 
                        help='GPT model list: {list(gpt_model_dict.keys())}')

    parser.add_argument("--base_url", default=BASE_URL, type=str, 
                        help='Using the base url')

    parser.add_argument("--api_key_gpts", default=GPT_MODEL_DICT, type=dict, 
                        help='The api keys for the gpt models, such as chatgpt, gpt4')

    return parser

