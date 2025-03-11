import wave
import numpy as np
import pyaudio

SAMPLE_RATE = 32000
FRAME_LENGTH_MS = 20
CHUNK = SAMPLE_RATE // 1000 * FRAME_LENGTH_MS
FORMAT = pyaudio.paInt16
CHANNELS = 8

RECORD_SECONDS = 20

wf = wave.open(f'record_{CHANNELS}ch.wav','wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(2)
wf.setframerate(SAMPLE_RATE)

try:
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    )

    print(f'Recording: sample_rate:{SAMPLE_RATE}, channels:{CHANNELS},format:{FORMAT} time:{RECORD_SECONDS}s')
    for _ in range(0, SAMPLE_RATE // CHUNK * RECORD_SECONDS):
        data = stream.read(CHUNK)
        wf.writeframes(data)
    print('Done')
finally:
    stream.close()
    p.terminate()
    wf.close()