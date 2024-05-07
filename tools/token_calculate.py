import os

# 使用安全认证AK/SK鉴权，通过环境变量方式初始化;
os.environ["QIANFAN_ACCESS_KEY"] = "3d9df86f23d64f0f8a072eb391ec1dad"
os.environ["QIANFAN_SECRET_KEY"] = "465151a1ed0f426a9e9662d6f3cdd7a9"

from qianfan.resources.tools import tokenizer

text = "这是1段text(混合中英文）"
token_cnt = tokenizer.Tokenizer().count_tokens(
    text=text,
    mode='remote',
    model="ernie-bot-4"
)
print(token_cnt)
