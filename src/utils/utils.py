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

import transformers
import torch

from zhipuai import ZhipuAI


# from mistral_inference.model import Transformer
# from mistral_inference.generate import generate
# from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
# from mistral_common.protocol.instruct.messages import UserMessage
# from mistral_common.protocol.instruct.request import ChatCompletionRequest



def chat_gpt_models(api_key, base_url, model_name, messages, sleep_=0):
    '''
    This function interfaces with the OpenAI API to generate chat completions using a specified GPT model.

    Parameters:
    - api_key (str): Your API key for accessing the OpenAI GPT models.
    - base_url (str): The base URL of the OpenAI API endpoint.
    - model_name (str): Identifier for the specific GPT model to be used for generating completions.
    - messages (list of dicts): A list of message dictionaries. Each dictionary typically contains 
                               keys like 'role' (e.g., 'user', 'assistant') and 'content' (text of the message).
    - sleep_ (int, optional): Time in seconds to delay the request. Default is 0 (no delay).

    Returns:
    - A completion object as returned by the OpenAI API, containing the generated responses based
      on the input messages and the specified model.

    Raises:
    - Exception: If there is an issue with the API request, it catches exceptions related to network issues,
                 API limits, or data errors and will re-raise them.

    '''
    try:
        if sleep_:
            time.sleep(sleep_)

        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=0.2,
        )

        role = chat_completion.choices[0].message.role
        content = chat_completion.choices[0].message.content
        if content is not None:
            return content, role
        else:
            return '', role

    except Exception as exc:
        print(exc)
        print('-----------------bad case!------------------')

        return '', 'broken'
    



def chat_glm_models(api_key, model_name, messages, sleep_=0):
    '''
    This function interfaces with the GLMs API to generate chat completions.

    '''

    try:
        if sleep_:
            time.sleep(sleep_)

        client = ZhipuAI(api_key=api_key)

        response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        top_p= 0.7,
        temperature= 0.2,
        stream=True,
        )

        content = ''
        role = ''
        for chunk in response:
            # print(chunk.choices[0].delta.content)
            # print(chunk.choices[0].delta.role)
            role = chunk.choices[0].delta.role
            content += chunk.choices[0].delta.content

        if content is not None:
            return content, role
        else:
            return '', role


    except Exception as exc:
        print(exc)
        print('-----------------bad case!------------------')

        return '', 'broken'




def chat_llama_models(pipeline, messages, max_new_tokens=5000, temperature=0.2, top_p=0.7, do_sample=True):
    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = pipeline(
        messages,
        max_new_tokens=max_new_tokens,
        eos_token_id=terminators,
        do_sample=do_sample,
        temperature=temperature,
        top_p=top_p,
    )

    return outputs[0]["generated_text"][-1]['content']



def chat_mistral_models(pipeline, messages, max_new_tokens=5000, temperature=0.2, top_p=0.7, do_sample=True):
    outputs = pipeline(
        messages,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        temperature=temperature,
        top_p=top_p,
    )

    return outputs[0]["generated_text"][-1]['content']


def news_filter_by_date(news, deadline):
    results = []
    urls = []
    title = []
    for item in news:
        flag_time = compare_dates(item['datePublished'], deadline)
        
        if item['url'] not in urls and item['title'] not in title and flag_time == 1:
            urls.append(item['url'])
            title.append(item['title'])
            results.append(item)

    return results




def compare_dates(datePublished_str, deadline_str):
    """
    Compares two dates and prints whether the first date is before, after, or on the same day as the second date.

    Parameters:
    datePublished_str (str): The published date in ISO 8601 format with time and timezone.
    deadline_str (str): The deadline date in 'YYYY-MM-DD' format.
    """
    flag_time = 0

    datePublished_dt = datetime.strptime(datePublished_str, '%Y-%m-%d')
    deadline_dt = datetime.strptime(deadline_str, '%Y-%m-%d')

    if datePublished_dt <= deadline_dt:
        flag_time = 1
    
    return flag_time


def get_current_date():
    now = datetime.now()
    
    return f"{now.year}-{now.month}-{now.day}"


def get_date_for_sim_event(date_str: str) -> str:
    """Calculate the date one year before the given date.

    """
    given_date = datetime.strptime(date_str, "%Y-%m-%d")
    one_year_before = given_date - relativedelta(years=1)

    results = one_year_before.strftime("%Y-%m-%d")

    return '2000-01-01..{}'.format(results)


def get_date_days_prior(date_str, prior_days):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    prior_date = date - timedelta(days=prior_days)
    
    return prior_date.strftime("%Y-%m-%d")



def arg_stak_clean(arg_sta_dict, stop_words):
    results = {}
    for key in arg_sta_dict:
        tmp_ = []
        for item in arg_sta_dict[key]:
            if item not in tmp_ and item not in stop_words and 'role' not in item and 'stakeholder' not in item:
                tmp_.append(item)
        
        results[key] = tmp_
    
    return results



def load_records(data_path):
    data = []
    with open(data_path, 'r', encoding='utf-8') as _f:
        for line in _f:
            data.append(json.loads(line))

    return data


def count_tokens(text, model_name):
    encoding = tiktoken.encoding_for_model(model_name)

    tokens = encoding.encode(json.dumps(text))
    
    token_count = len(tokens)
    
    if token_count > 4090:
        return True, token_count
    else:
        return False, token_count

def generate_time_periods(start_time):
    start_date = datetime.strptime(start_time, "%Y-%m-%d")
    time_periods = {}

    for i in range(3):
        days = [(start_date + timedelta(days=j)).strftime("%Y-%m-%d") for j in range(i * 5, (i + 1) * 5)]
        time_periods[f'period_{i+1}'] = days
    
    time_periods['period_4'] = ['other']
    
    return time_periods


def count_vaild_tokens(text, tar_count, model_name='gpt-3.5-turbo'):
    encoding = tiktoken.encoding_for_model(model_name)

    tokens = encoding.encode(json.dumps(text))
    
    token_count = len(tokens)

    
    if token_count > tar_count:
        ori_tok = tokens[:tar_count]
        ori_tok = encoding.decode(ori_tok)
        return ori_tok
    else:
        return text



def generate_time_periods_4(start_time):
    start_date = datetime.strptime(start_time, "%Y-%m-%d")
    time_periods = {}

    for i in range(3):
        days = [(start_date + timedelta(days=j+1)).strftime("%Y-%m-%d") for j in range(i * 5, (i + 1) * 5)]
        time_periods[f'period_{i+1}'] = days
    
    time_periods['period_4'] = ['other']
    time_periods['period_1'] += [start_time]
    
    return time_periods











if __name__=="__main__":
    ''