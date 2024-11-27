import wave
import sys
from scipy.signal import resample

import numpy as np
import pyaudio

CHUNK = 960
FORMAT = pyaudio.paInt16
CHANNELS = 8
SAMPLED_CHANNELS = 4
ORIGIN_RATE = 48000
SAMPLED_RATE = 16000
RECORD_SECONDS = 60

wf_origin = wave.open('origin_48K_8ch.wav','wb')
wf_origin.setnchannels(CHANNELS)
wf_origin.setsampwidth(2)
wf_origin.setframerate(ORIGIN_RATE)
wf_sampled = wave.open(f'sampled_16K_{SAMPLED_CHANNELS}ch.wav','wb')
wf_sampled.setnchannels(SAMPLED_CHANNELS)
wf_sampled.setsampwidth(2)
wf_sampled.setframerate(SAMPLED_RATE)

try:
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=ORIGIN_RATE,
                    input=True,
                    input_device_index=11,
                    )

    print('Recording...')
    for _ in range(0, ORIGIN_RATE // CHUNK * RECORD_SECONDS):
        data = stream.read(CHUNK)
        wf_origin.writeframes(data)
        audio_data = np.frombuffer(data,dtype=np.int16)
        audio_data = np.reshape(audio_data,(CHUNK,CHANNELS))

        resampled_audio_data = []
        for channel in range(SAMPLED_CHANNELS):
            channel_data = audio_data[:, channel]
            num_samples = int(len(channel_data) * SAMPLED_RATE / ORIGIN_RATE)
            resampled_channel_data = resample(channel_data, num_samples)
            resampled_audio_data.append(resampled_channel_data)
        resampled_audio_data = np.stack(resampled_audio_data,axis=-1)
        wf_sampled.writeframes(resampled_audio_data.astype(np.int16).tobytes())
    print('Done')
finally:
    stream.close()
    p.terminate()
    wf_origin.close()
    wf_sampled.close()