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



def get_tar_period(time_periods, tar_time):
    flag_t = 0
    answer = ''
    for key in time_periods:
        if tar_time in time_periods[key]:
            flag_t = 1
            answer = key
    
    if flag_t == 0:
        answer = 'no_answer'

    return answer

def get_pred_time_period(data, periods, config):
    messages = []
    messages.append({'role': 'system', 'content': EI_PROMPT.period_extract_prompt.format(answer_list=list(periods.keys()), model_outputs=data)})
    selected_api_key = random.choice(config['api_key_gpts'][config['model_name']]) 
    content, role = chat_gpt_models(selected_api_key, config['base_url'], config['model_name'], messages, 0) 

    return content 

