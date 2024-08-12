#! python3
# -*- encoding: utf-8 -*-



query_background = '''Users provide a query to predict future events. However, the query has limited information and does not adequately convey the background of the event or the specifics of the prediction desired. Your task is to generate {background_query_count_} refined queries based on the user's original input. Use these queries to retrieve relevant news from the Bing browser to enhance the understanding of the described event and the details of the predicted occurrence.

1. The queries you generate should be as diverse as possible to fully understand the background of the user's query and the user's intent.
2. You must generate {background_query_count_} queries.
3. Each generated query must contain more than 15 words.
4. Please respond using {language_type}.
5. The output format is like: query1#query2. Separate each generated query with the "#" symbol.

Here is the user query:
{query}

'''


consistency_to_query = '''Please review the titles and background of the following news articles to determine if they are relevant to the query or helpful in answering the question posed in the query. Return '0' if they are not relevant, and '1' if they are relevant.

Note: You may only return the numbers 0 or 1.

Here is the query:
{query}

Here is the news title:
{title}

Here is the new background:
{desc}
'''


query_desc = '''Given a query and relevant news, your task is to generate a summary of the event described in the query using these news. This includes the background of the event, its development, and key information that can assist in answering the query.

1. The evolution of the event is influenced not only by its participants but also by significant entities that can propel its progress. Therefore, ensure that you retain those entities that significantly affect the event's course.
2. Timing is critical for the occurrence and development of the event, so please ensure that the relevant temporal information is preserved.
3. The maximum word length for the generated description of the news is {desc_length}.
4. Never fabricate facts, knowledge, or information.
5. Please respond using {language_type}.


Here is the query:
{query}

Here is the news content: 
{news_content_}
'''





stakeholder_abstraction_2 = '''Based on the user's query, the query background, and relevant news articles, extract stakeholders and their roles related to the event in the user's query from the news content.

1. Stakeholders of an event are individuals, organizations, or groups with a direct or indirect interest and influence in the event. These stakeholders may benefit or suffer from the event's outcome and can influence or drive the development of the event.
2. Specific instances/entities of stakeholders can be used to generate new queries to search for information related to the event described in the user's query on Bing.
3. The roles of stakeholders are used to generate new queries to search for information on similar events that have occurred in history. Therefore, the roles of the stakeholders are more flexible. For instance, for an event like "Internal conflicts at OpenAI, Altman left OpenAI, Microsoft invested in OpenAI," Microsoft's role as an investor is more convenient for searching similar events.
4. Please output only nouns, avoiding verbs, adjectives, and other non-noun terms that are not relevant for the current analysis.
5. Please output up to 6 most important stakeholders.
6. Please output up to 6 most important stakeholder roles. 
7. Please respond using {language_type}.
8. Never fabricate facts, knowledge, or information.
9. The output format is: stakeholder1#stakeholder2#...@@role1#role2#..., with each stakeholder separated by the symbol #, each role separated by #, and stakeholders and roles separated by the symbol @@.

Here is the query:
{query}


Here is the query background:
{query_desc_}

Here is the news content:
{news_content_}
'''


stakeholder_abstraction_3 = '''Based on the user's query, the relevant news articles, extract stakeholders and their roles related to the event in the user's query from the news content.

1. Stakeholders of an event are individuals, organizations, or groups with a direct or indirect interest and influence in the event. These stakeholders may benefit or suffer from the event's outcome and can influence or drive the development of the event.
2. Specific instances/entities of stakeholders can be used to generate new queries to search for information related to the event described in the user's query on Bing.
3. The roles of stakeholders are used to generate new queries to search for information on similar events that have occurred in history. Therefore, the roles of the stakeholders are more flexible. For instance, for an event like "Internal conflicts at OpenAI, Altman left OpenAI, Microsoft invested in OpenAI," Microsoft's role as an investor is more convenient for searching similar events.
4. Please output only nouns, avoiding verbs, adjectives, and other non-noun terms that are not relevant for the current analysis.
5. Please output up to 6 most important stakeholders.
6. Please output up to 6 most important stakeholder roles. 
7. Please respond using {language_type}.
8. Never fabricate facts, knowledge, or information.
9. The output format is: stakeholder1#stakeholder2#...@@role1#role2#..., with each stakeholder separated by the symbol #, each role separated by #, and stakeholders and roles separated by the symbol @@.


Here is the query:
{query}

Here is the news content:
{news_content_}
'''



relevant_queries_2 = '''Given a user query, retrieve news of relevant events from Bing that can answer the query. The factors influencing the development of an event are multifaceted, involving not only the participants of the event itself but also the stakeholders related to the event, who may drive its development. Searching for news using only the user query may be insufficient. Therefore, your task is to generate {query_count_} new queries based on the user query, its description, and the stakeholders related to the event, to search for relevant event news on Bing.

1. To answer the user query, you need to generate {query_count_} new queries to search for relevant event news on Bing. These five queries should cover different aspects to comprehensively answer the user's query.
2.Relevant events refer to those that are directly associated with the event in user's query from different perspectives.
3. Stakeholders of an event are individuals, organizations, or groups with a direct or indirect interest and influence in the event. These stakeholders may benefit or suffer from the event's outcome and can influence or drive the development of the event.
5. Please respond using {language_type}.
6. Never fabricate facts, knowledge, or information.
7. Each generated query should contain at least 15 words.
8. The output format should be: query1#query2. Separate each generated query with the "#" symbol.

Here is the user query:
{query}

Here is the background of user query:
{query_desc_}

Here is stakeholder list of the user query:
{stakeholders}
'''


relevant_queries_3 = '''Given a user query, retrieve news of relevant events from Bing that can answer the query. The factors influencing the development of an event are multifaceted, involving not only the participants of the event itself but also the stakeholders related to the event, who may drive its development. Searching for news using only the user query may be insufficient. Therefore, your task is to generate {query_count_} new queries based on the user query, and the stakeholders related to the event, to search for relevant event news on Bing.

1. To answer the user query, you need to generate {query_count_} new queries to search for relevant event news on Bing. These five queries should cover different aspects to comprehensively answer the user's query.
2.Relevant events refer to those that are directly associated with the event in user's query from different perspectives.
3. Stakeholders of an event are individuals, organizations, or groups with a direct or indirect interest and influence in the event. These stakeholders may benefit or suffer from the event's outcome and can influence or drive the development of the event.
5. Please respond using {language_type}.
6. Never fabricate facts, knowledge, or information.
7. Each generated query should contain at least 15 words.
8. The output format should be like: query1#query2. Separate each generated query with the "#" symbol.

Here is the user query:
{query}

Here is stakeholder list of the user query:
{stakeholders}
'''



similar_queries_2 = '''Based on the given user query, generate new queries to search Bing for events similar to the one in the user's query. Similar events are not the event currently being queried by the user, but rather a historical event that is similar in nature and has already occurred. In addition to the user query, a background of the user query, and the stakeholders and their roles are provided. Please use this information to generate {query_count_} new queries to search Bing for similar event information. 

1. Stakeholders of an event are individuals, organizations, or groups with a direct or indirect interest and influence in the event. These stakeholders may benefit or suffer from the event's outcome and can influence or drive the development of the event.
2. Specific instances/entities of stakeholders can be used to generate new queries to search for information related to the event described in the user's query on Bing.
3. The roles of stakeholders are used to generate new queries to search for information on similar events that have occurred in history. Therefore, the roles of the stakeholders are more flexible. For instance, for an event like "Internal conflicts at OpenAI, Altman left OpenAI, Microsoft invested in OpenAI," Microsoft's role as an investor is more convenient for searching similar events.
4. User queries often involve specific events. The events in user query should be generalized into broader background using and stakeholder roles. For example, in this case, the specific situation "Sam Altman leaving OpenAI" should be generalized to "departures of CEOs from high-tech companies in history."
5. Please generate {query_count_} queries to search relevant events from Bing.
6. Please respond using {language_type}.
7. Never fabricate facts, knowledge, or information.
8. Each generated query for similar events should contain at least 15 words.
9. The retrieved similar events cannot be the events mentioned in the user's query.
10. The output format should be like: query1#query2. Separate each generated query with the "#" symbol.

Here is the user query:
{query}

Here is the background:
{query_desc_}

Here is stakeholder list of the user query:
{stakeholders}

Here is stakeholder role list of the user query:
{stakeholder_role}
'''



similar_queries_3 = '''Based on the given user query, generate new queries to search Bing for events similar to the one in the user's query. Similar events are not the event currently being queried by the user, but rather a historical event that is similar in nature and has already occurred. In addition to the user query, and the stakeholders and their roles are provided. Please use this information to generate {query_count_} new queries to search Bing for similar event information. 

1. Stakeholders of an event are individuals, organizations, or groups with a direct or indirect interest and influence in the event. These stakeholders may benefit or suffer from the event's outcome and can influence or drive the development of the event.
2. Specific instances/entities of stakeholders can be used to generate new queries to search for information related to the user's query on Bing.
3. The roles of stakeholders are used to generate new queries to search for information on similar events that have occurred in history. Therefore, the roles of the stakeholders are more flexible. For instance, for an event like "Internal conflicts at OpenAI, Altman left OpenAI, Microsoft invested in OpenAI," Microsoft's role as an investor is more convenient for searching similar events.
4. User queries often involve specific events. The events in user query should be generalized into broader descriptions using stakeholder roles. For example, in this case, the specific situation "Sam Altman leaving OpenAI" should be generalized to "departures of CEOs from high-tech companies in history."
5. Please generate {query_count_} queries to search relevant events from Bing.
6. Please respond using {language_type}.
7. Never fabricate facts, knowledge, or information.
8. Each generated query for similar events should contain at least 15 words.
9. The retrieved similar events cannot be the events mentioned in the user's query.
10. The output format should be like: query1#query2. Separate each generated query with the "#" symbol.

Here is the user query:
{query}

Here is stakeholder list of the user query:
{stakeholders}

Here is stakeholder role list of the user query:
{stakeholder_role}
'''


similar_news_score = '''Given a user query and a news article, please determine whether the news content is a similar event to the user query. Similar events are not the event currently being queried by the user, but rather a historical event that is similar in nature and has already occurred. You can only output a single integer between 1 and 3, where 1 indicates that the news is not a similar event to the user query, 2 indicates uncertainty, and 3 indicates that the news is a similar event to the user query.

Tips:
1. Your output must be a single number between 1 and 5.
2. Please note that similar events are not the same as those described in the user's query.

Here is the user query: 
{query}

Here is the news content:
{news_article}
'''


diversity_queries_sim_3 = '''Given a user query and news content, the news describes a similar event. A similar event is not the event the user is querying about; rather, it is a historical event that is similar in nature and has already occurred. Because this similar event has already happened, it can provide a reference to help answer the user's query. However, currently, only one news article is provided, which makes the information about the similar event incomplete. Your current task is to generate three questions based on the user query and news content. Use these questions to search Bing for news to supplement information about the similar event. The {query_count_} questions generated should aim to fulfill the following criteria as much as possible:
(1) They are intended to search Bing for news to supplement information about the similar event.
(2) The purpose of supplementing information about the similar event is ultimately to help answer the user's query, so the questions should focus on the user's query.
(3) The similar event is not the event described in the user's query, so questions should not directly pertain to the user's query."

Tips:
1. Each generated question must contain more than 15 words.
2. Please respond using {language_type}.
3. Please generate {query_count_} questions.
4. The output format should be: question1#question2#question3. Separate each generated question with the "#" symbol.

Here is the user query: 
{query}

Here is the news content:
{news_article}
'''



diversity_queries_sim_4 = '''Given a user's query and news content describing a similar historical event, it is important to note that the "similar event" is not the event currently being queried by the user, but rather a historical event that is similar in nature and has already occurred. As the information provided is incomplete, we need to gather more details about this similar event to assist in answering the user's query. Your task is to formulate three search questions based on the user's query and the provided news content. Use these questions to retrieve additional news through the Bing search engine to enhance our understanding of the similar event. The questions generated should meet the following three criteria:
(1) Purpose of Information Retrieval: Each question should aim to retrieve additional news information about the similar event through Bing.
(2) Connection to User Query: Although the questions are about a historical event, they should directly or indirectly assist in addressing the main query of the user.
(3) Avoid Direct Reference to the Current Event: The questions should focus on the historical similar event in the news content, not the current event described in the user's query.

Tips:
1. Each generated question must contain more than 15 words.
2. Please respond using {language_type}.
3. The output format should be: question1#question2#question3. Separate each generated question with the "#" symbol.

Here is the user query: 
{query}

Here is the news content:
{news_article}
'''


sim_event_desc = '''Given a news content, your task is to generate a summary of the news. This includes the background of the event, its development.

1. Timing is critical for the occurrence and development of the event, so please ensure that the relevant temporal information is preserved.
3. The maximum word length for the generated background of the news is {desc_length}.
4. Never fabricate facts, knowledge, or information.
5. Please respond using {language_type}.

Here is the news content: 
{news_content_}
'''


















