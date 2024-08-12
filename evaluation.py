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
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import copy
from tqdm import tqdm

import argparse

from config import evaluation_config
from src.utils.utils import generate_time_periods_4, chat_gpt_models
from src.prompt import evaluation_instruct as EI_PROMPT 
from src.question_time_eva import *
from src.question_other_eva import *



def load_predictions(config):
    data = {}
    with open(config['predictions_path'], 'r', encoding='utf-8') as _f:
        for line in _f:
            json_data = json.loads(line)
            data[json_data['id']] = json_data

    return data

def load_ground_thuth(config):
    answers = {}
    with open(config['ground_truth_path'], 'r', encoding='utf-8') as _f:
        for line in _f:
            json_data = json.loads(line)
            answers[json_data['id']] = json_data
    questions = {}
    with open(config['questions_path'], 'r', encoding='utf-8') as _f:
        for line in _f:
            json_data = json.loads(line)
            questions[json_data['id']] = json_data

    for key in questions:
        tmp_ans = answers[key]['answer']
        ans_format = ''
        assert len(tmp_ans) > 0
        if len(tmp_ans) == 1:
            ans_format = tmp_ans[0]
        else:  
            ans_clean = []
            for item in tmp_ans:
                ans_clean += item
            ans_format = str(ans_clean)

        questions[key]['answer'] = ans_format

    return questions



def eva_question_time(data, answer, configs):
    overall_count = 0
    true_count = 0
    for key in data:
        if data[key]['question_type'] == 'time':
            overall_count += 1
            time_periods = generate_time_periods_4(data[key]['date_question'])
            tar_period = get_tar_period(time_periods, answer[key]['tar_time'])
            answer_fin_period = get_pred_time_period(data[key]['predictions'], time_periods, configs)
            if tar_period in answer_fin_period:
                true_count = 1            
    
    return overall_count, true_count, divide_and_convert(true_count, overall_count)


def eva_question_other(data, response, configs):
    overall_scores = {'location': {'count': 0, 'score': 0}, 'event development': {'count': 0, 'score': 0}, 'event outcome': {'count': 0, 'score': 0}, 'event impact': {'count': 0, 'score': 0}, 'social response': {'count': 0, 'score': 0},'other': {'count': 0, 'score': 0}}
    for key in data:
        question_type = response[key]['question_type']
        if question_type != 'time':
            question = response[key]['question']
            ground_truth = response[key]['answer']
            prediction = data[key]['predictions']

            acc_scores = get_accuracy_scores(prediction, ground_truth, question, configs)
            comp_scores = get_completeness_scores(prediction, ground_truth, question, configs)
            rel_scores = get_relevance_scores(prediction, ground_truth, question, configs)
            focus_scores = get_focus_scores(prediction, ground_truth, question, configs)
            reason_scores = get_reasonableness_scores(prediction, ground_truth, question, configs)
            if acc_scores == 0.0:
                comp_scores = 0.0
            tmp_score = (acc_scores + comp_scores + rel_scores + focus_scores + reason_scores) / 5
            overall_scores[question_type]['count'] += 1
            overall_scores[question_type]['score'] += tmp_score
    
    for key in overall_scores:
        if overall_scores[key]['count'] > 0:
            overall_scores[key] = divide_and_convert(overall_scores[key]['score'], overall_scores[key]['count'])
        else:
            overall_scores[key] = 0.0

    return overall_scores
    

            
            











def main(configs):

    # load data
    data = load_predictions(configs)
    print('predictions: {}'.format(len(data)))

    # load ground truth
    response = load_ground_thuth(configs)
    print('response: {}'.format(len(response)))
    _, _, time_acc = eva_question_time(data, response, configs)

    overall_scores = eva_question_other(data, response, configs)

    overall_scores['time'] = time_acc
    overall_scores = {key: round(value, 4) for key, value in overall_scores.items()}
    print('overall scores: {}'.format(overall_scores))






















if __name__=="__main__":

    # loading configs
    parser = argparse.ArgumentParser()
    parser = evaluation_config(parser)
    parser = parser.parse_args()
    configs = vars(parser)

    main(configs)










































