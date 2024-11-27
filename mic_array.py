import pyaudio
import numpy as np
from scipy.signal import resample


# 假设你有以下自定义函数用于波束成形、降噪、AGC和语音唤醒检测
def beamforming_and_denoising(audio_data):
    # 这里添加你的波束成形和降噪算法
    # 返回单通道数据
    return audio_data.mean(axis=1)  # 示例：简单地取平均值作为单通道输出


def agc_processing(single_channel_data):
    # 这里添加你的AGC算法
    # 返回AGC处理后的单通道数据
    return single_channel_data  # 示例：不做任何处理


def voice_wake_detection(single_channel_data,block):
    # 这里添加你的语音唤醒检测算法
    # 返回是否检测到唤醒词
    if block % 200 == 0:
        return True
    else:
        return False


# PyAudio参数
FORMAT = pyaudio.paInt16  # 16位深度
CHANNELS = 2  # 8声道
RATE = 48000  # 设备采样率为48KHz
CHUNK = 960  # 每个数据块的大小

# 初始化PyAudio
audio = pyaudio.PyAudio()

# 打开流
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=9,
                    )

print("开始录音...")
block = 0
try:
    while True:
        # 第一步：从麦克风阵列采集数据
        data = stream.read(CHUNK)

        # 将数据转换为numpy数组，并重塑为多通道格式
        audio_data = np.frombuffer(data, dtype=np.int16)
        audio_data = np.reshape(audio_data, (CHUNK, CHANNELS))
        if block == 1:
            print(audio_data)
        # 第二步：将8通道数据转换为16K采样率
        resampled_audio_data = []
        for channel in range(CHANNELS):
            channel_data = audio_data[:, channel]
            num_samples = int(len(channel_data) * 16000 / RATE)
            resampled_channel_data = resample(channel_data, num_samples)
            resampled_audio_data.append(resampled_channel_data)

        # 将重新采样后的数据组合成一个二维数组
        resampled_audio_data = np.stack(resampled_audio_data, axis=-1)

        # 第三步：对8通道进行波束成形和降噪，AGC处理，得到单通道数据
        single_channel_data = beamforming_and_denoising(resampled_audio_data)
        single_channel_data = agc_processing(single_channel_data)

        # 第四步：针对单通道数据进行语音唤醒检测
        wake_detected = voice_wake_detection(single_channel_data,block)

        if wake_detected:
            print("检测到唤醒词！")
        block += 1

except KeyboardInterrupt:
    print("录音结束")

# 关闭流
stream.stop_stream()
stream.close()
audio.terminate()