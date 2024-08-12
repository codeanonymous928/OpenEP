#! python3
# -*- encoding: utf-8 -*-

import os
import re
import json




record = {
    'id': '',
    'question': '',
    'date_question': '',
    "question_type": '',
    'time_cost': 0,
    'config': {},
    'hot_topic': {},

    'question_disambiguation': {},
    'information_retrieval': {
        'question_background': {
            'question_desc': '',
            'question_similar': [],
            'question_similar_news': []

        },
        'stakeholder': {

        },
        'relevant_news_retrieval': {
            'diversity_queries': [],
            'news_list' : []

        },
        'similar_news_retrieval': [
            
        ]

    },
    'information_integration': {
        'relevant_news': {
            'chunks': [],
            'cluster_count': 0,
            'clusters_idx': [],
            'node_content': [],
            'node_desc': []

        },
        'similar_news': []

    },
    'event_prediction': {
        'answer_rel': '',
        'answer_sim': '',
        'answer': ''

    }
}

def initialize_record():

    return record


