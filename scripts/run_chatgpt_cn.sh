CUDA_VISIBLE_DEVICES=8 python run.py \
    --data_path=data/question_samples.json \
    --response_path=response/response.json \
    --model_name=gpt-3.5-turbo-16k-0613 \
    --mkt=zh-CN \
    --build_type=llm