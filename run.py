#! python3
# -*- encoding: utf-8 -*-

import os
import re
import json
import argparse

from config import common_config, query_dis_config, information_inte_config, information_retri_config
from src.world import build_world



def load_stop_words(data_path):
    stop_words = []
    with open(data_path, 'r', encoding='utf-8') as _f:
        for line in _f:
            stop_words.append(line.strip())
    return stop_words

def data_load_file(config):
    data = []
    with open(config['data_path'], 'r', encoding='utf-8') as _f:
        for line in _f:
            json_data = json.loads(line)
            data.append(json_data)

    return data

def load_response(configs):
    response_cases = []
    if os.path.exists(configs['response_path']):
        with open(configs['response_path'], 'r', encoding='utf-8') as _f:
            for line in _f:
                json_data = json.loads(line)
                if json_data['id'] not in response_cases:
                    response_cases.append(json_data['id'])

    return response_cases



def run_fep(configs):
    print('configs: {}'.format(configs)) 
    lang_type = configs['mkt']

    print('Starting build world ... ')
    world = build_world(configs, lang_type)
    print('World build finished ... ')

    print('Load data ... ')
    data = data_load_file(configs)
    print('data: {}'.format(len(data)))

    print("Load response ...")
    response_cases = load_response(configs)
    print('response_cases: {}'.format(len(response_cases)))

    filter_data = []
    for item in data:
        if item['id'] not in response_cases:
            filter_data.append(item)
    print('filter_data: {}'.format(len(filter_data)))

    print('Load stop words ...')
    stop_words = load_stop_words(configs['stop_words_path'])
    print('stop words: {}'.format(len(stop_words)))

    print('Start running ... ')
    world.run(filter_data, stop_words)
    print('Future event prediction finished ... ')














if __name__=="__main__":

    # loading configs
    parser = argparse.ArgumentParser()
    parser = common_config(parser)
    parser = query_dis_config(parser)
    parser = information_retri_config(parser)
    parser = information_inte_config(parser)
    parser = parser.parse_args()
    configs = vars(parser)

    run_fep(configs)







