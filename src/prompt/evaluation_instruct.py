#! python3
# -*- encoding: utf-8 -*-


period_extract_prompt = '''Below are the model outputs, which include not only the answers but also the analysis process. You need to extract the specific answers from them:

Tips:
1. The output result should be one from the list of answers.
2. Please output only the answer, without including any other content.
3. Ensure that your output strictly adheres to the content provided in the results; do not fabricate any information.
4. You can only output one answer.

Here is the answer list:
{answer_list}

Here is the model outputs:
{model_outputs}
'''


accuracy_prompt = '''Given the question, model outputs, and ground truth, your task is to determine the accuracy of the model outputs based on the question and ground truth. The ground truth may contain multiple answers, but the result is considered true if the model outputs include at least one correct answer; it is false if it includes none. The evaluation process is as follows:
(1) Analyze the correct answers in the ground truth based on the question, which may contain several answers.
(2) Review the model outputs to determine if they contain any of the correct answers.
(3) If the model outputs include a correct answer, output True; if the model outputs are entirely incorrect, output False.
(4) Having evaluated the accuracy of the model output, please provide your confidence level in your assessment, expressed as a percentage between 0 and 100.

Tips:
1. Please note that since the model outputs are predictive results, they will not be identical to the correct answers in the ground truth. The model outputs are considered correct as long as their expressed meanings are consistent with the correct answers. For instance, in location-based questions, if the locations mentioned in the model outputs are close to or include the correct locations in the ground truth, they are deemed correct.
2. The ground truth may be a segment of a news article or an entire article, containing both relevant and irrelevant information. Therefore, you need to analyze and extract the answers to evaluate the accuracy of the model's outputs.
3. Examples 1. Question: Which cities in China will be impacted first? Answers: Beijing, Shanghai, Shenzhen. If the model correctly identifies any one of these locations, the result is True.
4. Example 2. Question: What are the impacts? Answers may include several impacts, but if the model correctly identifies at least one, the result is True.
5. Example 3. Question: What are the international reactions? Answers might involve reactions from multiple countries; if the model correctly identifies the reaction from any one country, the result is True.
6. You must not fabricate facts; all your evaluations must be based solely on the provided ground truth and model outputs.
7. You can only output one of the words: True or False.
8. Output DICT format, containing two keys: {{\"answer\": \"True or False, only output one\", \"confidence_percentage\": Output you confidence percentage for your evaluting on the accuracy of model outputs, expressed as a percentage between 0 and 100.}}
9. Please note that only the answer (in DICT format) should be outputted; do not include any analytical content.

Here is the question:
{question}

Here is the model outputs:
{model_outputs}

Here is the ground truth:
{ground_truth}
'''

completeness_prompt = '''Given the question, model outputs, and ground truth, your task is to determine the completeness of the model outputs based on the question and ground truth. The ground truth may contain multiple answers. The evaluation process is as follows:
(1) Analyze how many correct answers in the ground truth based on the question.
(2) Analyze how many answers the model outputs have correctly answered based on the answers in the ground truth.
(3) Having evaluated the completeness of the model output, please provide your confidence level in your assessment, expressed as a percentage between 0 and 100.

Tips:
1. Please note that since the model outputs are predictive results, they will not be identical to the correct answers in the ground truth. The model outputs are considered correct as long as their expressed meanings are consistent with the correct answers. For instance, in location-based questions, if the locations mentioned in the model outputs are close to or include the correct locations in the ground truth, they are deemed correct.
2. The ground truth may be a segment of a news article or an entire article, containing both relevant and irrelevant information. Therefore, you need to analyze and extract the answers to evaluate the completeness of the model's outputs.
3. Completeness. Assesses whether the prediction covers the different relevant aspects of answers, evaluating the thoroughness of the information provided.
4. Examples 1. Question: Which cities in China will be impacted first? Answers: Beijing, Shanghai, Shenzhen. Model outputs: Beijing. Thus, the ground truth contains three answers, while the model outputs contain one answer.
5. The number of answers in the ground truth is always greater than the number of correct answers in the model outputs.
6. You must not fabricate facts; all your evaluations must be based solely on the provided ground truth and model outputs.
7. Output DICT format, containing three keys: {{\"answer_number_in_ground_truth\": \"The number of correct answers contained in the ground truth, output as an integer\", \"answer_number_in_model_outputs\": The number of correct answers contained in the model outputs, output as an integer.\", \"confidence_percentage\": Output you confidence percentage for your evaluting on the completeness of model outputs, expressed as a percentage between 0 and 100.}}
8. Please note that only the answer (in DICT format) should be outputted; do not include any analytical content.

Here is the question:
{question}

Here is the model outputs:
{model_outputs}

Here is the ground truth:
{ground_truth}
'''

relevance_prompt = '''Given the question, model outputs, and ground truth, your task is to determine the relevance of the model outputs based on the question and ground truth. The evaluation process is as follows:
(1) Analyze the correct answers in the ground truth based on the question.
(2) Analyze the relevance of the model outputs to the correct answers. Relevance evaluates how pertinent the model outputs is to the ground truth, ensuring that the prediction does not veer into unrelated details.
(3) Output the relevance score, a decimal between 0 and 5, where a higher value indicates greater relevance of the model outputs to the ground truth.
(4) Having evaluated the relevance of the model output, please provide your confidence level in your assessment, expressed as a percentage between 0 and 100.

Tips:
1. The ground truth may be a segment of a news article or an entire article, containing both relevant and irrelevant information. Therefore, you need to analyze and extract the answers to evaluate the relevance of the model's outputs.
2. You must not fabricate facts; all your evaluations must be based solely on the provided ground truth and model outputs.
3. Output DICT format, containing two keys: {{\"relevance_score\": \"Output the relevance score, a decimal between 0 and 5\", \"confidence_percentage\": Output you confidence percentage for your evaluting on the relevance of model outputs, expressed as a percentage between 0 and 100.}}
4. Please note that only the answer (in DICT format) should be outputted; do not include any analytical content.

Here is the question:
{question}

Here is the model outputs:
{model_outputs}

Here is the ground truth:
{ground_truth}
'''

focus_prompt = '''Given the question, model outputs, and ground truth, your task is to determine the focus of the model outputs based on the question and ground truth. The evaluation process is as follows:
(1) Analyze the correct answers in the ground truth based on the question.
(2) Analyze the focus of the model outputs to the correct answers. Focus analyzes the sharpness and specificity of the model outputs, ensuring that it is neither overly broad nor vague.
(3) Output the focus score, a decimal between 0 and 5, where a higher value indicates greater focus of the model outputs to the ground truth.
(4) Having evaluated the focus of the model output, please provide your confidence level in your assessment, expressed as a percentage between 0 and 100.

Tips:
1. The ground truth may be a segment of a news article or an entire article, containing both relevant and irrelevant information. Therefore, you need to analyze and extract the answers to evaluate the focus of the model's outputs.
2. You must not fabricate facts; all your evaluations must be based solely on the provided ground truth and model outputs.
3. Output DICT format, containing two keys: {{\"focus_score\": \"Output the focus score, a decimal between 0 and 5\", \"confidence_percentage\": Output you confidence percentage for your evaluting on the focus of model outputs, expressed as a percentage between 0 and 100.}}
6. Please note that only the answer (in DICT format) should be outputted; do not include any analytical content.

Here is the question:
{question}

Here is the model outputs:
{model_outputs}

Here is the ground truth:
{ground_truth}
'''

reasonableness_prompt = '''Given the question, model outputs, and ground truth, your task is to determine the reasonableness of the model outputs based on the question and ground truth. The evaluation process is as follows:
(1) Analyze the correct answers in the ground truth based on the question.
(2) Analyze the reasonableness of the model outputs to the correct answers. Reasonableness measures the logical coherence and believability of the prediction, checking whether the prediction aligns with general world knowledge and appears plausible.
(3) Output the reasonableness score, a decimal between 0 and 5, where a higher value indicates greater reasonableness of the model outputs to the ground truth.
(4) Having evaluated the reasonableness of the model output, please provide your confidence level in your assessment, expressed as a percentage between 0 and 100.

Tips:
1. The ground truth may be a segment of a news article or an entire article, containing both relevant and irrelevant information. Therefore, you need to analyze and extract the answers to evaluate the reasonableness of the model's outputs.
2. You must not fabricate facts; all your evaluations must be based solely on the provided ground truth and model outputs.
3. Output DICT format, containing two keys: {{\"reasonableness_score\": \"Output the reasonableness score, a decimal between 0 and 5\", \"confidence_percentage\": Output you confidence percentage for your evaluting on the reasonableness of model outputs, expressed as a percentage between 0 and 100.}}
4. Please note that only the answer (in DICT format) should be outputted; do not include any analytical content.

Here is the question:
{question}

Here is the model outputs:
{model_outputs}

Here is the ground truth:
{ground_truth}
'''



