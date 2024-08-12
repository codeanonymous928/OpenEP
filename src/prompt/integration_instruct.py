#! python3
# -*- encoding: utf-8 -*-

chunk_ext_rel_5 = '''Your task is to extract content fragments from news articles that are useful for answering user queries. Answering user queries requires information from different aspects; some content may not be directly related to the event in the user query but could be associated with stakeholders related to the event. Please combine the user query description, as well as the diverse queries generated based on the user query, think deeply, and then extract content fragments from the news articles that are helpful in answering the user query.

1. Each content fragment contain multiple sentences. 
2. The user query description refers to the background formed based on related news extracted from Bing.
3. Diverse queries refer to the need for information from different perspectives to answer the user query comprehensively. Relying solely on information retrieved using the user query may not be sufficient, so diverse queries are generated based on the user query to gather information from different perspectives.
4. Diverse queries are an extension of the user query, so if news content is helpful for answering diverse queries, it should also be extracted.
5. Please respond using {language_type}.
6. Never fabricate facts, knowledge, or information.
7. Please directly output the results with list format without any other things.
8. Please ensure that the outputs are strictly formatted as a JSON list, which can be directly used with json.loads(). The output should resemble: '[\"content fragment 1\", \"content fragment 2\"]'. Each element in the list is a content fragment.

Here is the user query:
{query}

Here is the description of user query:
{query_desc_}

Here is the diversity queries:
{diversity_quieries}

Here is the news content:
{news_content_}
'''


chunk_ext_rel_8 = '''Given the user query, the background of the user query, the generated diversity queries, and the news content, your task is to extract content segments from the news that help answer the user query and the diversity queries.

1. The background of the user query refers to the description of the event in the user query.
2. Please note that your task is solely to extract content segments from the news that assist in answering the user query and the diversity queries. Extract the original content directly. 
3. Each segment should contain multiple sentences, serving as an independent element in the output list.
4. Each content segments must contain at least two sentences.
5. Diverse queries refer to the need for information from different perspectives to answer the user query comprehensively. Relying solely on information retrieved using the user query may not be sufficient, so diverse queries are generated based on the user query to gather information from different perspectives.
6. Diverse queries are an extension of the user query, so if news content is helpful for answering diverse queries, it should also be extracted.
7. Please note that you should not extract information from the background of the user query. Only extract content from the news content.
8. Please respond using {language_type}.
9. Never fabricate facts, knowledge, or information.
10. Please directly output the results with list format without any other things.
11. Please ensure that the outputs are strictly formatted as a JSON list, which can be directly used with json.loads(). The output should resemble: '[\"content fragment 1\", \"content fragment 2\"]'. Each element in the list is a content fragment.

Here is the user query:
{query}

Here is the background of user query:
{query_desc_}

Here is the diversity queries:
{diversity_quieries}

Here is the news content:
{news_content_}
'''

chunk_ext_rel_9 = '''Given the user query, the background of the user query, the generated diversity queries, and the news content, your task is to extract content segments from the news that help answer the user query and the diversity queries.

1. The background of the user query refers to the description of the event in the user query.
2. Please note that your task is solely to extract content segments from the news that assist in answering the user query and the diversity queries. Extract the original content directly. 
3. Each segment should contain multiple sentences, serving as an independent element in the output list.
4. Each content segments must contain at least two sentences.
5. Diverse queries refer to the need for information from different perspectives to answer the user query comprehensively. Relying solely on information retrieved using the user query may not be sufficient, so diverse queries are generated based on the user query to gather information from different perspectives.
6. Diverse queries are an extension of the user query, so if news content is helpful for answering diverse queries, it should also be extracted.
7. Please note that you should not extract information from the background of the user query. Only extract content from the news content.
8. Please respond using {language_type}.
9. Never fabricate facts, knowledge, or information.
10. Please directly output the results without any other things.
11. The output format should be: content segment 1@@content segment 2@@content segment 3. Separate each generated content segment with the "@@" symbol.

Here is the user query:
{query}

Here is the background of user query:
{query_desc_}

Here is the diversity queries:
{diversity_quieries}

Here is the news content:
{news_content_}

'''



chunk_ext_sim_7 = '''Your task is to extract content fragments from news articles that are useful for addressing user query. The given news describes events similar to those in the user query. Similar events refer to historical events that resemble the event in the user query, and such information can provide useful insights for answering the user query. You need to extract content fragments from two main aspects: 
(1) extracting content fragments from the news that are useful for addressing the user query; 
(2) given the description of similar events, extracting information that can enrich the understanding of these similar events.

1. Description of similar events refers to a brief description of similar events.
2. Please respond using {language_type}.
3. Never fabricate facts, knowledge, or information.
4. Please ensure that the outputs are strictly formatted as a JSON list, which can be directly used with json.loads(). The output should resemble: '[\"content fragment 1\", \"content fragment 2\"]'. Each element in the list is a content fragment.


Here is the user query:
{query}

Here is the description of similar events:
{sim_event_desc_}

Here is the news content:
{news_content_}
'''



chunk_ext_sim_8 = '''Given the user query, the background of similar events, and the news content describing similar events. Similar events refer to historical events that resemble the event in the user query, and such information can provide useful insights for answering the user query. Your task is to extract the following three types of content segments from the news content:

(1) You need to extract content segments that serve as references for answering the user query.
(2) You need to extract content segments that are helpful in answering the user query.
(3) You need to extract content segments that enrich the description of similar events.

Tips:
1. Similar events can provide useful references for answering the user query. For example, given the user query "Will Ilya return to OpenAI after leaving?", a similar event would be "Steve Jobs left Apple, acquired Pixar, and later returned to Apple during its difficult period." This similar event serves as a reference for answering the user query.
2. Please note that your task is solely to extract content segments from the news. Extract the original content directly. 
3. Each segment should contain multiple sentences, serving as an independent element in the output list.
4. Each content segments must contain at least two sentences.
5. Please note that you should not extract information from the background of the similar events. Only extract content from the news content.
6. Please respond using {language_type}.
7. Never fabricate facts, knowledge, or information.
8. Please directly output the results without any other things.
9. The output format should be: content segment 1@@content segment 2@@content segment 3. Separate each generated content segment with the "@@" symbol.


Here is the user query:
{query}

Here is the background of similar events:
{sim_event_desc_}

Here is the news content:
{news_content_}
'''

chunk_ext_sim_9 = '''Given the user query, the background of similar events, and the news content describing similar events. Similar events refer to historical events that resemble the event in the user query, and such information can provide useful insights for answering the user query. Your task is to extract the following three types of content segments from the news content:

(1) You need to extract content segments that serve as references for answering the user query.
(2) You need to extract content segments that are helpful in answering the user query.
(3) You need to extract content segments that enrich the description of similar events.

Tips:
1. Similar events can provide useful references for answering the user query. For example, given the user query "Will Ilya return to OpenAI after leaving?", a similar event would be "Steve Jobs left Apple, acquired Pixar, and later returned to Apple during its difficult period." This similar event serves as a reference for answering the user query.
2. Please note that your task is solely to extract content segments from the news. Extract the original content directly. 
3. Each segment should contain multiple sentences, serving as an independent element in the output list.
4. Each content segments must contain at least two sentences.
5. Please note that you should not extract information from the background of the similar events. Only extract content from the news content.
6. Please respond using {language_type}.
7. Never fabricate facts, knowledge, or information.
8. Please directly output the results with list format without any other things.
9. Please ensure that the outputs are strictly formatted as a JSON list, which can be directly used with json.loads(). The output should resemble: '[\"content segment 1\", \"content segment 2\"]'. Each element in the list is a content segments.

Here is the user query:
{query}

Here is the background of similar events:
{sim_event_desc_}

Here is the news content:
{news_content_}
'''






node_desc_5 = '''Given a user query and several news snippets, generate a comprehensive and detailed description. These snippets come from various news sources but are relevant to the user query and useful in answering the user's question. Your task is to integrate these snippets into a coherent and complete description, providing clear and comprehensive information to the user.

1. Please retain the original news content as much as possible. Time information is important in the news and should be kept intact.
2. Output the generated description directly without any things, such as "The following is the description."
3. The output content should not exceed {max_node_words} words.
4. Please respond using {language_type}.
5. Never fabricate facts, knowledge, or information.

Here is the news contents for one group:
{news_content_}
'''
