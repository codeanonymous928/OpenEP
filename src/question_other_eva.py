#! python3
# -*- encoding: utf-8 -*-

import os
import re
import json
import pandas as pd
from openai  import OpenAI
import time
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import tiktoken
import random

from .utils.utils import generate_time_periods_4, chat_gpt_models
from .prompt import evaluation_instruct as EI_PROMPT 




def get_accuracy_scores(predictions, references, query, config):
    messages = []
    messages.append({'role': 'system', 'content': EI_PROMPT.accuracy_prompt.format(question=query, model_outputs=predictions, ground_truth=references)})
    selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 

    content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 
    check_flag = 3
    acc_score = 0
    con_per = 0.0
    while check_flag:
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 
        check_flag = check_flag - 1
        flag, parse_data = is_valid_json(content)
        if flag:
            if parse_data['answer'] == True or parse_data['answer'] == 'True':
                acc_score = 1
            con_per = float(parse_data['confidence_percentage'])
            check_flag = 0

    fin_score = 0
    if config['confidence_flag']:
        fin_score = acc_score * con_per * 0.01
    else:
        fin_score = acc_score

    return fin_score


def get_completeness_scores(predictions, references, query, config):
    messages = []
    messages.append({'role': 'system', 'content': EI_PROMPT.completeness_prompt.format(question=query, model_outputs=predictions, ground_truth=references)})
    selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 

    content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 
    check_flag = 3
    answer_number_in_ground_truth = 0
    answer_number_in_model_outputs = 0
    con_per = 0.0
    while check_flag:
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 
        check_flag = check_flag - 1
        flag, parse_data = is_valid_json(content)
        if flag:
            answer_number_in_ground_truth = parse_data['answer_number_in_ground_truth']
            answer_number_in_model_outputs = parse_data['answer_number_in_model_outputs']
            con_per = float(parse_data['confidence_percentage'])
            check_flag = 0

    fin_score = 0
    if answer_number_in_ground_truth != 0:
        if answer_number_in_ground_truth >= answer_number_in_model_outputs:
            fin_score = divide_and_convert( answer_number_in_model_outputs, answer_number_in_ground_truth)
        else:
            fin_score = 1.0
    else:
        fin_score = 0.0
    
    if config['confidence_flag']:
        fin_score = fin_score * con_per * 0.01

    return fin_score




def get_relevance_scores(predictions, references, query, config):
    messages = []
    messages.append({'role': 'system', 'content': EI_PROMPT.relevance_prompt.format(question=query, model_outputs=predictions, ground_truth=references)})
    selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 

    content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 
    check_flag = 3
    rel_score = 0.0
    con_per = 0.0
    while check_flag:
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 
        check_flag = check_flag - 1
        flag, parse_data = is_valid_json(content)
        if flag:
            rel_score = float(parse_data['relevance_score'])
            con_per = float(parse_data['confidence_percentage'])
            check_flag = 0
    rel_score = score_normalize(rel_score)
    fin_score = 0
    if config['confidence_flag']:
        fin_score = rel_score * con_per * 0.01
    else:
        fin_score = rel_score

    return fin_score


def get_focus_scores(predictions, references, query, config):
    messages = []
    messages.append({'role': 'system', 'content': EI_PROMPT.focus_prompt.format(question=query, model_outputs=predictions, ground_truth=references)})
    selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 

    content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 
    check_flag = 3
    focus_score = 0.0
    con_per = 0.0
    while check_flag:
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 
        check_flag = check_flag - 1
        flag, parse_data = is_valid_json(content)
        if flag:
            focus_score = float(parse_data['focus_score'])
            con_per = float(parse_data['confidence_percentage'])
            check_flag = 0
    focus_score = score_normalize(focus_score)
    fin_score = 0
    if config['confidence_flag']:
        fin_score = focus_score * con_per * 0.01
    else:
        fin_score = focus_score

    return fin_score


def get_reasonableness_scores(predictions, references, query, config):
    messages = []
    messages.append({'role': 'system', 'content': EI_PROMPT.reasonableness_prompt.format(question=query, model_outputs=predictions, ground_truth=references)})
    selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 

    check_flag = 3
    reason_score = 0.0
    con_per = 0.0
    while check_flag:
        content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 
        check_flag = check_flag - 1
        flag, parse_data = is_valid_json(content)
        if flag:
            reason_score = float(parse_data['reasonableness_score'])
            con_per = float(parse_data['confidence_percentage'])
            check_flag = 0
    reason_score = score_normalize(reason_score)
    fin_score = 0
    if config['confidence_flag']:
        fin_score = reason_score * con_per * 0.01
    else:
        fin_score = reason_score

    return fin_score



def is_valid_json(json_string):
    """
    Check if a given string can be loaded using json.loads

    Args:
    json_string (str): The string to check.

    Returns:
    bool: True if the string can be loaded as JSON, False otherwise.
    """
    json_string = json_string.replace('json', '').replace('```', '').replace('\n', '')
    try:
        json_data = json.loads(json_string)
        return True, json_data
    except ValueError:
        return False, 0

def score_normalize(score):
    if score > 1:
        return (score - 1) / 4
    else:
        return score / 4

def divide_and_convert(num1, num2):
    """
    Divide two integers and convert the result to a decimal and a percentage with three decimal places.
    
    Args:
    num1 (int): The numerator.
    num2 (int): The denominator.

    Returns:
    tuple: Decimal and percentage representation of the division result.
    """
    if num2 == 0:
        return "Error: Division by zero"

    decimal_result = num1 / num2

    return decimal_result