import os
import time

try:
    from funasr_onnx import Paraformer
except:
    os.system("pip install funasr_onnx jieba -i https://pypi.tuna.tsinghua.edu.cn/simple")
    from funasr_onnx import Paraformer


def load_model():
    path = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(path, './funasr-onnx-small')
    model_dir = model_dir.replace('\\', '/')

    model = Paraformer(model_dir, batch_size=1, quantize=True)
    print('***成功加载funasr_onnx***')
    return model


def inference(wav_path, model):
    result = model(wav_path)
    return result


if __name__ == '__main__':
    model = load_model()

    wav_path = '../EmotionEngine/EmotionList/paimon/开心.wav'
    result = inference(wav_path, model)
    print(result[0]['preds'][0])
    time.sleep(10)
    wav_path = '../EmotionEngine/EmotionList/paimon/失落.wav'
    result = inference(wav_path, model)
    print(result[0]['preds'][0])
    time.sleep(10)
    wav_path = '../EmotionEngine/EmotionList/paimon/生气.wav'
    result = inference(wav_path, model)
    print(result[0]['preds'][0])
