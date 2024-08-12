#! python3
# -*- encoding: utf-8 -*-




prediction_res_10 = '''Given a user query, answer the query based on the query's background, and relevant and similar event information retrieved from Bing.

1. Relevant events refer to those that are directly associated with the event in user's query from different perspectives.
2. Stakeholders of an event are individuals, organizations, or groups with a direct or indirect interest and influence in the event. These stakeholders may benefit or suffer from the event's outcome and can influence or drive the development of the event.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please output the overall result first, followed by detailed results itemized.

Here is the user query:
{query}

Here is the query background:
{query_desc_}

Here is the relevant event information for the user query:
{rel_events}

Here is the similar event information for the user query:
{sim_events}
'''





time_question_pred_rel_5 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into five periods of three days each, plus an "other" category, resulting in six time periods. Please answer the user's query based on the background of the query, relevant events information. Below is a detailed description:
(1) Time periods are displayed in dictionary format: time_periods = {time_periods_}. The first five time periods, period_1 to period_5, each represent three days. 1-15 represent the next 1st to 15th days.The sixth period, "period_6", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(3) The background of the user query refers to the description of the event in the user query.
(5) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: the background of the query, relevant events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"period_5\": "the probability of period_5 occurring (a number between 0 and 1) in decimal form", \"period_6\": "the probability of period_6 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the background of user query:
{query_desc_}

Here is the relevant events: 
{relevant_data_}

'''


time_question_pred_rel_55 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into 3 periods of three days each, plus an "other" category, resulting in 4 time periods. Please answer the user's query based on the background of the query, relevant events information. Below is a detailed description:
(1) Time periods are displayed in dictionary format: time_periods = {time_periods_}. The first 3 time periods, period_1 to period_3, each represent five days. 1-15 represent the next 1st to 15th days.The forth period, "period_4", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(3) The background of the user query refers to the background of the event in the user query.
(5) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: the background of the query, relevant events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the background of user query:
{query_desc_}

Here is the relevant events: 
{relevant_data_}

'''


time_question_pred_rel_6 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into five periods of three days each, plus an "other" category, resulting in six time periods. Please answer the user's query based on the  relevant events information. Below is a detailed description:
(1) Time periods are displayed in dictionary format: time_periods = time_periods = {time_periods_}. The first five time periods, period_1 to period_5, each represent three days. 1-15 represent the next 1st to 15th days.The sixth period, "period_6", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(3) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: relevant events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"period_5\": "the probability of period_5 occurring (a number between 0 and 1) in decimal form", \"period_6\": "the probability of period_6 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the relevant events: 
{relevant_data_}

'''

time_question_pred_rel_66 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into three periods of three days each, plus an "other" category, resulting in four time periods. Please answer the user's query based on the  relevant events information. Below is a detailed description:
(1) Time periods are displayed in dictionary format: time_periods = time_periods = {time_periods_}. The first three time periods, period_1 to period_3, each represent five days. 1-15 represent the next 1st to 15th days.The forth period, "period_4", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(3) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: relevant events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the relevant events: 
{relevant_data_}
'''




time_question_pred_sim_55 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into three periods of three days each, plus an "other" category, resulting in four time periods. Please answer the user's query based on the background of the query and similar events information. Below is a detailed description:
(1) Time periods are displayed in dictionary format: time_periods = time_periods = {time_periods_}. The first three time periods, period_1 to period_3, each represent five days. 1-15 represent the next 1st to 15th days.The sixth period, "period_4", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(4) The background of the user query refers to the background of the event in the user query.
(5) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: the background of the query, and similar events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the background of user query:
{query_desc_}

Here is the similar events:
{similar_data_}

'''

time_question_pred_sim_6 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into five periods of three days each, plus an "other" category, resulting in six time periods. Please answer the user's query based on the similar events information. Below is a detailed description:
(1) Time periods are displayed in dictionary format: time_periods = time_periods = {time_periods_}. The first five time periods, period_1 to period_5, each represent three days. 1-15 represent the next 1st to 15th days.The sixth period, "period_6", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(4) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: the similar events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"period_5\": "the probability of period_5 occurring (a number between 0 and 1) in decimal form", \"period_6\": "the probability of period_6 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the similar events:
{similar_data_}

'''



time_question_pred_sim_66 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into three periods of three days each, plus an "other" category, resulting in four time periods. Please answer the user's query based on the similar events information. Below is a detailed description:
(1) Time periods are displayed in dictionary format: time_periods = time_periods = {time_periods_}. The first three time periods, period_1 to period_3, each represent five days. 1-15 represent the next 1st to 15th days.The sixth period, "period_4", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(4) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: the similar events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the similar events:
{similar_data_}

'''




time_question_pred_ensemble_55 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into five periods of three days each, plus an "other" category, resulting in six time periods. You have provided two answers based on relevant events and similar events respectively. Now, you need to comprehensively consider all the provided information and the two existing results to make a final prediction.

Please follow these rules:
(1) Time periods are displayed in dictionary format: time_periods = time_periods = {time_periods_}. The first three time periods, period_1 to period_3, each represent five days. 1-15 represent the next 1st to 15th days.The forth period, "period_4", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(3) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(4) The background of the user query refers to the background of the event in the user query.
(5) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: the background of the query, relevant events, and similar events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the background of user query:
{query_desc_}

Here is the relevant events: 
{relevant_data_}

Here is the similar events:
{similar_data_}

Here is the predictions based on the relevant events:
{results_rel_}

Here is the predictions based on the similar events:
{results_sim_}
'''


time_question_pred_ensemble_6 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into five periods of three days each, plus an "other" category, resulting in six time periods. You have provided two answers based on relevant events and similar events respectively. Now, you need to comprehensively consider all the provided information and the two existing results to make a final prediction.

Please follow these rules:
(1) Time periods are displayed in dictionary format: time_periods = time_periods = {time_periods_}. The first five time periods, period_1 to period_5, each represent three days. 1-15 represent the next 1st to 15th days.The sixth period, "period_6", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(3) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(5) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: relevant events, and similar events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"period_5\": "the probability of period_5 occurring (a number between 0 and 1) in decimal form", \"period_6\": "the probability of period_6 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the relevant events: 
{relevant_data_}

Here is the similar events:
{similar_data_}

Here is the predictions based on the relevant events:
{results_rel_}

Here is the predictions based on the similar events:
{results_sim_}
'''


time_question_pred_ensemble_66 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query asking about the likelihood of an event occurring within the next 15 days, divide the 15 days into five periods of three days each, plus an "other" category, resulting in six time periods. You have provided two answers based on relevant events and similar events respectively. Now, you need to comprehensively consider all the provided information and the two existing results to make a final prediction.

Please follow these rules:
(1) Time periods are displayed in dictionary format: time_periods = time_periods = {time_periods_}. The first three time periods, period_1 to period_3, each represent five days. 1-15 represent the next 1st to 15th days.The forth period, "period_4", represents any time outside the first 15 days or the event not occurring.
Please follow these rules:
(2) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(3) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(5) date_query refers to the time when the user raised the query
(6) date_prediction refers to the time when you answer the user's query.
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Please comprehensively consider the following three types of information: relevant events, and similar events information, before providing the result.
3. Please respond using {language_type}.
4. Never fabricate facts, knowledge, or information.
5. Please directly output the results with dict format without any other things.
6. The output should be in dictionary format and contain eight parts: {{ \"analysis\": "Insert your step-by-step consideration", \"period_1\": "the probability of period_1 occurring (a number between 0 and 1) in decimal form", \"period_2\": "the probability of period_2 occurring (a number between 0 and 1) in decimal form", \"period_3\": "the probability of period_3 occurring (a number between 0 and 1) in decimal form", \"period_4\": "the probability of period_4 occurring (a number between 0 and 1) in decimal form", \"period_5\": "the probability of period_5 occurring (a number between 0 and 1) in decimal form", \"period_6\": "the probability of period_6 occurring (a number between 0 and 1) in decimal form", \"answer\": "output your answer, the time period with the highest probability"}}
7. The probabilities for all time periods should sum to 1. The probabilities for different time periods cannot be the same. 
8. Your analysis should be consistent with the probabilities of each time period and the answer. The time period identified as most likely in your analysis should have the highest probability, and this time period should be the answer.

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the relevant events: 
{relevant_data_}

Here is the similar events:
{similar_data_}

Here is the predictions based on the relevant events:
{results_rel_}

Here is the predictions based on the similar events:
{results_sim_}
'''





main_quesion_pred_rel_5 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query, please answer based on the background of the query, relevant events information. Below is a detailed description:
(1) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(2) The background of the user query refers to the background of the event in the user query.
(4) date_query refers to the time when the user raised the query
(5) date_prediction refers to the time when you answer the user's query.
(6) Since you are answering the user's query based on the provided background of the query, relevant events information, each of your conclusions should involve information from the background of the query and relevant events.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Your response should be more specific and avoid vague statements. Therefore, you must incorporate the background of the query, relevant events information in your answer. Your response must include specific information from the background of the query and relevant events.
3. Please comprehensively consider the following three types of information: the background of the query, relevant events information, before providing the result.
4. Please respond using {language_type}.
5. Never fabricate facts, knowledge, or information.
6. Please directly output the results with dict format without any other things.
7. The output should be in dictionary format, containing three parts: {{ \"analysis\": "Insert your step-by-step consideration. ", \"answer\": "output your answer item by item"}}

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the background of user query:
{query_desc_}

Here is the relevant events: 
{relevant_data_}

'''


main_quesion_pred_rel_6 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query, please answer based on the relevant events information. Below is a detailed description:
(1) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(2) date_query refers to the time when the user raised the query
(5) date_prediction refers to the time when you answer the user's query.
(6) Since you are answering the user's query based on the provided relevant events information, each of your conclusions should involve information from the relevant events.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Your response should be more specific and avoid vague statements. Therefore, you must incorporate the background of the query, relevant events information in your answer. Your response must include specific information from the  relevant events.
3. Please comprehensively consider the following three types of information: the relevant events information, before providing the result.
4. Please respond using {language_type}.
5. Never fabricate facts, knowledge, or information.
6. Please directly output the results with dict format without any other things.
7. The output should be in dictionary format, containing three parts: {{ \"analysis\": "Insert your step-by-step consideration. ", \"answer\": "output your answer item by item"}}

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the relevant events: 
{relevant_data_}

'''


main_quesion_pred_sim_5 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query, please answer based on the background of the query, similar events information. Below is a detailed description:
(1) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(3) The background of the user query refers to the background of the event in the user query.
(4) date_query refers to the time when the user raised the query
(5) date_prediction refers to the time when you answer the user's query.
(6) You must incorporate the background of the query, and similar events information to answer the user query. 


Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Your response should be more specific and avoid vague statements. Therefore, you must incorporate the background of the query, and similar events information in your answer. 
3. Please comprehensively consider the following three types of information: the background of the query, and similar events information, before providing the result.
4. Please respond using {language_type}.
5. Never fabricate facts, knowledge, or information.
6. Please directly output the results with dict format without any other things.
7. The output should be in dictionary format, containing three parts: {{ \"analysis\": "Insert your step-by-step consideration. ", \"answer\": "output your answer item by item"}}

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the background of user query:
{query_desc_}

Here is the similar events:
{similar_data_}

'''



main_quesion_pred_sim_6 = '''You are engaged in a short-term future event prediction task, forecasting events likely to occur within the next 15 days. Specifically, given a user query, please answer based on the similar events information. Below is a detailed description:
(1) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(3) date_query refers to the time when the user raised the query
(5) date_prediction refers to the time when you answer the user's query.
(6) You must incorporate the  similar events information to answer the user query. 


Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Your response should be more specific and avoid vague statements. Therefore, you must incorporate the similar events information in your answer. 
3. Please comprehensively consider the following three types of information: the  similar events information, before providing the result.
4. Please respond using {language_type}.
5. Never fabricate facts, knowledge, or information.
6. Please directly output the results with dict format without any other things.
7. The output should be in dictionary format, containing three parts: {{ \"analysis\": "Insert your step-by-step consideration. ", \"answer\": "output your answer item by item"}}

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the similar events:
{similar_data_}

'''



main_quesion_pred_ensemble_5 = '''Given a user query, please answer based on the background of the query, relevant events, and similar events information. You have provided three answers based on relevant events and similar events respectively. Now, you need to comprehensively consider all the provided information and the two existing results to make a final prediction.

Please follow these rules:
(1) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(2) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(3) The background of the user query refers to the background of the event in the user query.
(4) date_query refers to the time when the user raised the query
(5) date_prediction refers to the time when you answer the user's query.
(6) Since you are answering the user's query based on the provided background of the query, relevant events, and similar events information, each of your conclusions should involve information from the background of the query and relevant events.
(7) You must incorporate the background of the query, relevant events, and similar events information to answer the user query. Your response must include specific information from the background of the query and relevant events.
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Your response should be more specific and avoid vague statements. Therefore, you must incorporate the background of the query, relevant events, and similar events information in your answer. Your response must include specific information from the background of the query and relevant events.
3. Please comprehensively consider the following three types of information: the background of the query, relevant events, and similar events information, before providing the result.
4. Please respond using {language_type}.
5. Never fabricate facts, knowledge, or information.
6. Please directly output the results with dict format without any other things.
7. The output should be in dictionary format, containing three parts: {{ \"analysis\": "Insert your step-by-step consideration. Consideration starts with: The step-by-step consideration for the query {query_} is follows: ", \"answer\": "output your answer item by item"}}

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the background of user query:
{query_desc_}

Here is the relevant events: 
{relevant_data_}

Here is the similar events:
{similar_data_}

Here is the predictions based on the relevant events:
{results_rel_}

Here is the predictions based on the relevant events:
{results_rel_pers_}

Here is the predictions based on the similar events:
{results_sim_}

'''


main_quesion_pred_ensemble_6 = '''Given a user query, please answer based on the relevant events, and similar events information. You have provided three answers based on relevant events and similar events respectively. Now, you need to comprehensively consider all the provided information and the two existing results to make a final prediction.

Please follow these rules:
(1) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(2) Similar events are not the event currently being queried by the user but rather a historical event that is similar in nature and has already occurred. Because similar events have already happened, they can provide a reference to help answer the user's query.
(3) date_query refers to the time when the user raised the query
(5) date_prediction refers to the time when you answer the user's query.
(6) Since you are answering the user's query based on the provided  relevant events, and similar events information, each of your conclusions should involve information from the relevant events.
(7) You must incorporate the  relevant events, and similar events information to answer the user query. Your response must include specific information from the  relevant events.
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Your response should be more specific and avoid vague statements. Therefore, you must incorporate the relevant events, and similar events information in your answer. Your response must include specific information from the relevant events.
3. Please comprehensively consider the following three types of information: the relevant events, and similar events information, before providing the result.
4. Please respond using {language_type}.
5. Never fabricate facts, knowledge, or information.
6. Please directly output the results with dict format without any other things.
7. The output should be in dictionary format, containing three parts: {{ \"analysis\": "Insert your step-by-step consideration. Consideration starts with: The step-by-step consideration for the query {query_} is follows: ", \"answer\": "output your answer item by item"}}

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the relevant events: 
{relevant_data_}

Here is the similar events:
{similar_data_}

Here is the predictions based on the relevant events:
{results_rel_}

Here is the predictions based on the relevant events:
{results_rel_pers_}

Here is the predictions based on the similar events:
{results_sim_}

'''




main_quesion_pred_rel_7 = '''Given a user query, please answer based on the background of the query, relevant events information. Below is a detailed description:
(1) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(2) The background of the user query refers to the background of the event in the user query.
(4) date_query refers to the time when the user raised the query
(5) date_prediction refers to the time when you answer the user's query.
(6) Since you are answering the user's query based on the provided background of the query, relevant events information, each of your conclusions should involve information from the background of the query and relevant events.
(7) Relevant event information provides the necessary information to answer user queries from different perspectives. Therefore, you need to make targeted predictions from various angles. Combining your own knowledge, you should present specific, well-founded predictions for each perspective.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Your response should be more specific and avoid vague statements. Therefore, you must incorporate the background of the query, relevant events information in your answer. Your response must include specific information from the background of the query and relevant events.
3. Please comprehensively consider the following three types of information: the background of the query, relevant events information, before providing the result.
4. Please respond using {language_type}.
5. Never fabricate facts, knowledge, or information.
6. Please directly output the results with dict format without any other things.
7. The output should be in dictionary format, containing three parts: {{ \"analysis\": "Insert your step-by-step consideration. ", \"answer\": "output your answer item by item"}}

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the background of user query:
{query_desc_}

Here is the relevant events: 
{relevant_data_}

'''


main_quesion_pred_rel_8 = '''Given a user query, please answer based on the relevant events information. Below is a detailed description:
(1) Relevant events refer to those that are directly associated with the event in the user's query from different perspectives. This is the main basis for answering the question.
(2) date_query refers to the time when the user raised the query
(5) date_prediction refers to the time when you answer the user's query.
(6) Since you are answering the user's query based on the provided relevant events information, each of your conclusions should involve information from the relevant events.
(7) Relevant event information provides the necessary information to answer user queries from different perspectives. Therefore, you need to make targeted predictions from various angles. Combining your own knowledge, you should present specific, well-founded predictions for each perspective.

Please follow these rules:
1. The answer cannot be contradictory; you cannot output both yes and no, agree and disagree, or both positive and negative impacts simultaneously. You must hold only one stance. For example, if a user asks, "What impact will the success of the Chang'e 6 mission have on China's deep space exploration technology?", you cannot state both positive and negative impacts. You must choose the most likely result, such as listing several positive impacts.
2. Your response should be more specific and avoid vague statements. Therefore, you must incorporate the background of the query, relevant events information in your answer. Your response must include specific information from the  relevant events.
3. Please comprehensively consider the following three types of information: the relevant events information, before providing the result.
4. Please respond using {language_type}.
5. Never fabricate facts, knowledge, or information.
6. Please directly output the results with dict format without any other things.
7. The output should be in dictionary format, containing three parts: {{ \"analysis\": "Insert your step-by-step consideration. ", \"answer\": "output your answer item by item"}}

Here is the user query:
{query_}

Here is date_query: 
{date_query_}

Here is date_prediction: 
{date_pred_}

Here is the relevant events: 
{relevant_data_}

'''




