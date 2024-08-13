#! python3
# -*- encoding: utf-8 -*-

import os
import re
import json
import numpy as np
import tiktoken
import umap
from sklearn.mixture import GaussianMixture
import random
from sklearn.cluster import KMeans  
from concurrent.futures import ThreadPoolExecutor
import copy

from openai import OpenAI
from sentence_transformers import SentenceTransformer
from .utils.utils import chat_gpt_models, news_filter_by_date, chat_glm_models
from .prompt import integration_instruct as PROMPT_II

from tenacity import retry, stop_after_attempt, wait_random_exponential

RANDOM_SEED = 928
random.seed(RANDOM_SEED)








def get_optimal_clusters(
    embeddings: np.ndarray, max_clusters, random_state: int = RANDOM_SEED
) -> int:
    max_clusters = min(max_clusters, len(embeddings))
    n_clusters = np.arange(1, max_clusters)
    bics = []
    for n in n_clusters:
        gm = GaussianMixture(n_components=n, random_state=random_state)
        gm.fit(embeddings)
        bics.append(gm.bic(embeddings))
    optimal_clusters = n_clusters[np.argmin(bics)]
    return optimal_clusters


def KMEANS_cluster(embeddings: np.ndarray, max_clusters: int=20, min_clusters: int=5, random_state: int = 0):
    n_clusters = get_optimal_clusters(embeddings, max_clusters)
    if n_clusters < min_clusters:
        n_clusters = min_clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)  
    kmeans.fit(embeddings)  
    labels = kmeans.predict(embeddings)  
    centroids = kmeans.cluster_centers_  

    return n_clusters, labels.tolist()


def GMM_cluster(embeddings: np.ndarray, threshold: float, random_state: int = 0):
    n_clusters = get_optimal_clusters(embeddings)
    gm = GaussianMixture(n_components=n_clusters, random_state=random_state)
    gm.fit(embeddings)
    probs = gm.predict_proba(embeddings)
    labels = [np.where(prob > threshold)[0] for prob in probs]
    return labels, n_clusters



class SBertEmbeddingModel():
    def __init__(self, lang_type):
        self.lang_type = lang_type
        assert self.lang_type in ['zh-CN', 'en-US']

        if 'zh-CN' in self.lang_type:
            self.model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-cos-v1")
        else:
            self.model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased-v1")


    def create_embedding(self, text):
        return self.model.encode(text)






class TreeBuilder:
    """
    The TreeBuilder class is responsible for building a hierarchical text abstraction
    structure, known as a "tree," using summarization models and
    embedding models.
    """

    def __init__(self, config, embedding_model, lang_type):
        self.config = config
        self.embedding_model = embedding_model
        self.lang_type = lang_type


    def perform_clustering(self, data, flag_first=True):
        embeddings = self.embedding_model.create_embedding(data)
        cluster_count, cluster_label = KMEANS_cluster(embeddings, self.config['max_clusters'], self.config['min_clusters'])

        node_clusters = {}
        for idx, val in enumerate(cluster_label):
            if val not in node_clusters:
                node_clusters[val] = [data[idx]]
            else:
                node_clusters[val].append(data[idx])

        return cluster_count, cluster_label, node_clusters



    def summary(self, data):
        messages = []
        messages.append({'role': 'system', 'content': PROMPT_II.node_desc_5.format(max_node_words=self.config['max_words_node_desc'], language_type=self.lang_type, news_content_=json.dumps(data, ensure_ascii=False))})
         
        content = ''
        role = ''
        if 'gpt' in self.config['model_name']:
            selected_api_key = random.choice(self.config['api_key_gpts'][self.config['model_name']]) 

            content, role = chat_gpt_models(selected_api_key, self.config['base_url'], self.config['model_name'], messages, self.config['sleep'])
        elif 'glm' in self.config['model_name']:
            messages = []
            messages.append({'role': 'user', 'content': PROMPT_II.node_desc_5.format(max_node_words=self.config['max_words_node_desc'], language_type=self.lang_type, news_content_=json.dumps(data, ensure_ascii=False))})            
            selected_api_key = random.choice(self.config['api_key_glms'][self.config['model_name']]) 

            content, role = chat_glm_models(selected_api_key, self.config['model_name'], messages, self.config['sleep'])   

        return content


    def node_description(self, data):
        if len(data) < self.config['min_clusters']:
            data += ['There is no data.'] * (5 - len(data))

        cluster_count, cluster_labels, node_contents = self.perform_clustering(data)
        content_list = list(node_contents.values())

        with ThreadPoolExecutor(max_workers=8) as executor:
            node_desc = executor.map(self.summary, content_list) 
        node_desc = list(node_desc)

        return cluster_labels, cluster_count, node_contents, node_desc

