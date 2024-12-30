from pydub import AudioSegment


def read(filename):
    # 打开文件
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 如果需要去除每行末尾的换行符
    lines = [line.strip() for line in lines]
    return lines


def mp3_to_16k_wav(mp3_file, output_wav):
    audio = AudioSegment.from_mp3(mp3_file)
    audio = audio.set_frame_rate(16000)
    audio.export(output_wav, format="wav")


# results = []
# #filepath = f"wanye.{i}.mp3"
# for i in range(1, 51):
#     filepath = f"wanye.{i}.wav"
#     results.append(AU.STT(filepath)[0])
#     print(read("list5.txt")[i])
