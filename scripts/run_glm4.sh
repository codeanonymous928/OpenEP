CUDA_VISIBLE_DEVICES=9 python run.py \
    --data_path=data/question_samples.json \
    --response_path=response/response.json \
    --model_name=glm-4 \
    --mkt=zh-CN \
    --build_type=llm
