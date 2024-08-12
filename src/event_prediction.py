#! python3
# -*- encoding: utf-8 -*-

import random
import os
import re
import json


from .prompt import prediction_instruct as PROMPT_EP
from .utils.utils import generate_time_periods, chat_glm_models, chat_gpt_models
import time





class ChatPrediction():
    def __init__(self, config, lang_type, flag_background):
        self.config = config
        self.lang_type = lang_type
        self.flag_background = flag_background


    def message(self,role,content,name=None):
        m={'role':role, 'content':content}
        if name is not None: m['name']=name
        if self.verbose: self.show_message(m)
        return m
    
    def show_message(self,role, content):
        print(f'[{role}]:\n\n{content}\n\n')  

    def add_message(self, data):
        results = ''
        for idx, val in enumerate(data, start=1):
            results += 'This is the {} perspective of relevant events: {} \n'.format(idx, val)        

        return results

    def future_event_prediction(self, query, query_desc, relevant_data, similar_data, question_type, date_query):
        relevant_data = self.add_message(relevant_data)
        
        question_category = ['time', 'location', 'event development', 'event outcome', 'event impact', 'social response', 'other']
        assert question_type in question_category

        # openended question
        if question_type == 'time':
            time_periods = generate_time_periods(date_query)
            time_answer_rel = self.time_question_solving_rel(query, query_desc, relevant_data, similar_data, date_query, time_periods)

            time_answer_sim = self.time_question_solving_sim(query, query_desc, relevant_data, similar_data, date_query, time_periods)

            time_answer = self.time_question_solving(query, query_desc, relevant_data, similar_data, date_query, time_answer_rel, time_answer_sim, time_periods)

            return time_answer
        else:
            # w/o time question
            print('Solving main questions!!!')
            other_answer_rel = self.other_question_solving_rel(query, query_desc, relevant_data, similar_data, date_query)

            other_answer_rel_pers = self.other_question_solving_rel_perspective(query, query_desc, relevant_data, similar_data, date_query)

            other_answer_sim = self.other_question_solving_sim(query, query_desc, relevant_data, similar_data, date_query)

            other_answer = self.other_question_solving(query, query_desc, relevant_data, similar_data, date_query, other_answer_rel, other_answer_rel_pers, other_answer_sim)          

            return other_answer



    def binary_question_solving_rel(self, query, query_desc, relevant_data, similar_data, date_query):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.binary_question_pred_rel_4.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.binary_question_pred_rel_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.binary_question_pred_rel_4.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.binary_question_pred_rel_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content

    def binary_question_solving_sim(self, query, query_desc, relevant_data, similar_data, date_query):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.binary_question_pred_sim_4.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, similar_data_=similar_data)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.binary_question_pred_sim_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, similar_data_=similar_data)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.binary_question_pred_sim_4.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, similar_data_=similar_data)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.binary_question_pred_sim_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, similar_data_=similar_data)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content

    def binary_question_solving(self, query, query_desc, relevant_data, similar_data, date_query, answer_rel, answer_sim):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.binary_question_pred_ensemble_4.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_sim_=answer_sim)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.binary_question_pred_ensemble_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_sim_=answer_sim)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.binary_question_pred_ensemble_4.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_sim_=answer_sim)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.binary_question_pred_ensemble_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_sim_=answer_sim)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content


    def time_question_solving_rel(self, query, query_desc, relevant_data, similar_data, date_query, time_periods):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.time_question_pred_rel_55.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.time_question_pred_rel_66.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.time_question_pred_rel_55.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.time_question_pred_rel_66.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content

    def time_question_solving_sim(self, query, query_desc, relevant_data, similar_data, date_query, time_periods):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.time_question_pred_sim_55.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, similar_data_=similar_data)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.time_question_pred_sim_66.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, similar_data_=similar_data)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.time_question_pred_sim_55.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, similar_data_=similar_data)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.time_question_pred_sim_66.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, similar_data_=similar_data)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content
    
    def time_question_solving(self, query, query_desc, relevant_data, similar_data, date_query, answer_rel, answer_sim, time_periods):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.time_question_pred_ensemble_55.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_sim_=answer_sim)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.time_question_pred_ensemble_66.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_sim_=answer_sim)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:

            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.time_question_pred_ensemble_55.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_sim_=answer_sim)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.time_question_pred_ensemble_66.format(time_periods_=time_periods, language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_sim_=answer_sim)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content    

    def other_question_solving_rel(self, query, query_desc, relevant_data, similar_data, date_query):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.main_quesion_pred_rel_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.main_quesion_pred_rel_6.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.main_quesion_pred_rel_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.main_quesion_pred_rel_6.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content

    def other_question_solving_rel_perspective(self, query, query_desc, relevant_data, similar_data, date_query):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.main_quesion_pred_rel_7.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.main_quesion_pred_rel_8.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.main_quesion_pred_rel_7.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.main_quesion_pred_rel_8.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   


        return content

    def other_question_solving_sim(self, query, query_desc, relevant_data, similar_data, date_query):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.main_quesion_pred_sim_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, similar_data_=similar_data)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.main_quesion_pred_sim_6.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, similar_data_=similar_data)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.main_quesion_pred_sim_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, similar_data_=similar_data)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.main_quesion_pred_sim_6.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, similar_data_=similar_data)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content
    
    def other_question_solving(self, query, query_desc, relevant_data, similar_data, date_query, answer_rel, other_answer_rel_pers, answer_sim):
        messages = []
        if self.flag_background != 0:
            messages.append({'role': 'system', 'content': PROMPT_EP.main_quesion_pred_ensemble_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_rel_pers_=other_answer_rel_pers, results_sim_=answer_sim)})
        else:
            messages.append({'role': 'system', 'content': PROMPT_EP.main_quesion_pred_ensemble_6.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_rel_pers_=other_answer_rel_pers, results_sim_=answer_sim)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            if self.flag_background != 0:
                messages.append({'role': 'user', 'content': PROMPT_EP.main_quesion_pred_ensemble_5.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, query_desc_=query_desc, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_rel_pers_=other_answer_rel_pers, results_sim_=answer_sim)})
            else:
                messages.append({'role': 'user', 'content': PROMPT_EP.main_quesion_pred_ensemble_6.format(language_type=self.lang_type, query_=query, date_query_=date_query, date_pred_=date_query, relevant_data_=relevant_data, similar_data_=similar_data, results_rel_=answer_rel, results_rel_pers_=other_answer_rel_pers, results_sim_=answer_sim)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content    


    def binary_question_check(self, query):
        messages = []
        messages.append({'role': 'system', 'content': PROMPT_EP.binary_question_ins.format(query=query)})

        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            messages.append({'role': 'user', 'content': PROMPT_EP.binary_question_ins.format(query=query)})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return int(content)        


    def __call__(self, query_id, question, date_question, question_back, relevant_news, similar_news, rel_node_desc, sim_node_desc, question_type, start_time):
        print('Starting Event Prediction ... ')

        response = self.future_event_prediction(question, question_back, rel_node_desc, sim_node_desc, question_type, date_question)

        end_time = time.time()
        minutes, seconds = divmod(end_time - start_time, 60)
        # print(f"Total time: {int(minutes):02d}:{int(seconds):02d}")

        response_item = {'id': query_id, 'question': question, 'date_question': date_question, 'question_type': question_type, 'predictions': response}

        with open(self.config['response_path'], 'a+', encoding='utf-8') as _w:
            _w.write(json.dumps(response_item, ensure_ascii=False))
            _w.write('\n')        
        
        return response
        