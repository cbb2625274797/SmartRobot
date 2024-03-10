import logging

import onnxruntime
from transformers import BertTokenizer
import numpy as np


class EmotionEngine:
    def __init__(self, model_path):
        logging.info('Initializing Sentiment Engine...')
        onnx_model_path = model_path

        self.ort_session = onnxruntime.InferenceSession(onnx_model_path, providers=['CPUExecutionProvider'])

        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

    def infer(self, text):
        tokens = self.tokenizer(text, return_tensors="np")
        input_dict = {
            "input_ids": tokens["input_ids"],
            "attention_mask": tokens["attention_mask"],
        }
        # Convert input_ids and attention_mask to int64
        input_dict["input_ids"] = input_dict["input_ids"].astype(np.int64)
        input_dict["attention_mask"] = input_dict["attention_mask"].astype(np.int64)
        logits = self.ort_session.run(["logits"], input_dict)[0]
        probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True)
        predicted = np.argmax(probabilities, axis=1)[0]
        logging.info(f'Sentiment Engine Infer: {predicted}')
        return predicted


if __name__ == '__main__':
    t = '我是零一万物开发的一个智能助手，我叫 Yi，我是由零一万物的研究团队通过大量的文本数据进行训练，学习了语言的各种模式和关联，从而能够生成文本、回答问题、翻译语言的'
    s = EmotionEngine('./models/sentiment.onnx')
    r = s.infer(t)
    print(r)
