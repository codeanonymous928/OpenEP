#! python3
# -*- encoding: utf-8 -*-

import os
import re
import json
import pandas as pd
from openai  import OpenAI
import time





class ChatDisambiguation():
    def __init__(self, config, search_fn, retrieval_module, verbose=False):
        self.config = config
        self.search_fn = search_fn
        self.retrieval = retrieval_module
        self.verbose = verbose
    
    def show_message(self,role, content):
        print(f'[{role}]:\n\n{content}\n\n')       



    def __call__(self, data, stop_words, start_time):
        print('ChatDisambiguation')

        if self.config['flag_qdis'] == False:

            res = self.retrieval(data, stop_words, start_time)
            
            return res
        else:

            raise f'The query disambiguation module is not implemented.'

         