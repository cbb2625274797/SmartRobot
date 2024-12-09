---
tasks:
- punctuation
domain:
- audio
model-type:
- Classification
frameworks:
- onnx
metrics:
- f1_score
license: Apache License 2.0
language: 
- cn
tags:
- FunASR
- CT-Transformer
- Alibaba
- ICASSP 2020
datasets:
  train:
  - 33M-samples online data
  test:
  - wikipedia data test
  - 10000 industrial Mandarin sentences test
widgets:
  - task: punctuation
    inputs:
      - type: text
        name: input
        title: 文本
    examples:
      - name: 1
        title: 示例1
        inputs:
          - name: input
            data: 我们都是木头人不会讲话不会动
    inferencespec:
      cpu: 1 #CPU数量
      memory: 4096
---

# Paraformer模型介绍

## Highlights
模型为[Paraformer语音识别-中文-通用-8k-离线](https://www.modelscope.cn/models/damo/speech_paraformer_asr_nat-zh-cn-8k-common-vocab8358-tensorflow1/summary)的onnx量化导出版本


## <strong>[ModelScope-FunASR](https://github.com/alibaba-damo-academy/FunASR)</strong>
<strong>[FunASR](https://github.com/alibaba-damo-academy/FunASR)</strong>提供可便捷本地或者云端服务器部署的离线文件转写服务，内核为FunASR已开源runtime-SDK。 集成了达摩院语音实验室在Modelscope社区开源的语音端点检测(VAD)、Paraformer-large语音识别(ASR)、标点恢复(PUNC) 等相关能力，拥有完整的语音识别链路，可以将几十个小时的音频或视频识别成带标点的文字，而且支持上百路请求同时进行转写。

[**最新动态**](https://github.com/alibaba-damo-academy/FunASR#whats-new) 
| [**环境安装**](https://github.com/alibaba-damo-academy/FunASR#installation)
| [**介绍文档**](https://alibaba-damo-academy.github.io/FunASR/en/index.html)
| [**服务部署**](https://github.com/alibaba-damo-academy/FunASR/tree/main/funasr/runtime)
| [**模型库**](https://github.com/alibaba-damo-academy/FunASR/blob/main/docs/model_zoo/modelscope_models.md)
| [**联系我们**](https://github.com/alibaba-damo-academy/FunASR#contact)




## 快速上手

### 服务端启动

下载部署工具`funasr-runtime-deploy-offline-cpu-zh.sh`

```shell
curl -O https://raw.githubusercontent.com/alibaba-damo-academy/FunASR/main/funasr/runtime/deploy_tools/funasr-runtime-deploy-offline-cpu-zh.sh;
# 如遇到网络问题，中国大陆用户，可以用个下面的命令：
# curl -O https://isv-data.oss-cn-hangzhou.aliyuncs.com/ics/MaaS/ASR/shell/funasr-runtime-deploy-offline-cpu-zh.sh;
```

执行部署工具，在提示处输入回车键即可完成服务端安装与部署。目前便捷部署工具暂时仅支持Linux环境，其他环境部署参考开发指南（[点击此处](https://alibaba-damo-academy.github.io/FunASR/en/funasr/runtime/docs/SDK_tutorial_zh.html)）
```shell
sudo bash funasr-runtime-deploy-offline-cpu-zh.sh install --workspace ./funasr-runtime-resources
```

### 客户端测试与使用

运行上面安装指令后，会在./funasr-runtime-resources（默认安装目录）中下载客户端测试工具目录samples（[下载点击此处](https://isv-data.oss-cn-hangzhou.aliyuncs.com/ics/MaaS/ASR/sample/funasr_samples.tar.gz)），
我们以Python语言客户端为例，进行说明，支持多种音频格式输入（.wav, .pcm, .mp3等），也支持视频输入(.mp4等)，以及多文件列表wav.scp输入，其他版本客户端请参考文档（[点击此处](https://alibaba-damo-academy.github.io/FunASR/en/funasr/runtime/docs/SDK_tutorial_zh.html#id5)）

```shell
python3 wss_client_asr.py --host "127.0.0.1" --port 10095 --mode offline --audio_in "../audio/asr_example.wav"
```

更详细用法介绍（[点击此处](https://github.com/alibaba-damo-academy/FunASR/blob/main/funasr/runtime/docs/SDK_tutorial_zh.md)）

## 相关论文以及引用信息

```BibTeX
@inproceedings{chen2020controllable,
  title={Controllable Time-Delay Transformer for Real-Time Punctuation Prediction and Disfluency Detection},
  author={Chen, Qian and Chen, Mengzhe and Li, Bo and Wang, Wen},
  booktitle={ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  pages={8069--8073},
  year={2020},
  organization={IEEE}
}
```

