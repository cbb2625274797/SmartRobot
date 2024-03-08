import re
text = "这是第一句话。这是第二句话？还有第三句话！"

# 使用正则表达式匹配以句号、问号或感叹号结尾的句子
sentence_pattern = r'(.+?)[。!?？！]'

while re.search(sentence_pattern, text):
    match = re.search(sentence_pattern, text)
    # 提取第一句话
    first_sentence = match.group(1)
    print(first_sentence)
    # 获取第一句话的结束位置（包括句号、问号或感叹号）
    end_index = match.end()
    # 删除第一句话，即截取第一个句号之后的部分
    text = text[end_index:]
