def get_emotion(input_text: str) -> str:
    if '开心' in input_text:
        return '开心'
    elif '害怕' in input_text:
        return '害怕'
    elif '生气' in input_text:
        return '生气'
    elif '失落' in input_text:
        return '失落'
    elif '好奇' in input_text:
        return '好奇'
    elif '戏谑' in input_text:
        return '戏谑'
    else:
        return '开心'
