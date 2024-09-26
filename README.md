# OpenEP

This repository contains the data and code for the paper "OpenEP: Open-Ended Future Event Prediction". OpenEP aims to generate flexible and diverse predictions aligned with real-world scenarios. To facilitate the study of this task, we first construct OpenEPBench, an open-ended future event prediction dataset. Consequently, we propose StkFEP, a stakeholder-enhanced future event prediction framework that incorporates event characteristics for open-ended settings.

<p align = "center">    
<img  src="images/example_display.png" width="600" />
</p>

## 1. Quick Start
The code repository is based on Pytorch and Transformers. Please use the following command to install the necessary dependcies. `install -r requirements.txt`.


## 2. Data
We collect daily hot topics to generate predictive questions from seven persectives. 

The whole data is shown in `data/data/cn_valid_data.json` and `data/data/en_valid_data.json`.

The data samples with responses are shown in `data/samples/question_samples.json` and `data/samples/answer_samples.json`.


## 3. Run Experiments
We use GPT-3.5 and GLM-4 as the backbone models. To run the experiments, please follow the steps outlined below.
1. Place your api keys in file: `src/api_keys.py`.
2. Specify `data_path`, `response_path`, and `model_name` in files `script/run_gpt35_cn.sh` or `script/run_glm4_cn.sh`.

## 4. Evaluation
We use GPT-4 as the backbone model to evaluate the model predictions. Please follow the steps below.
1. Place your api keys in file: `src/api_keys.py`.
2. Specify `predictions_path`, `questions_path`, `ground_truth_path`, and `model_name` in file `script/run_evaluation.sh`.
