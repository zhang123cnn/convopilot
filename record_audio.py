import pyaudio
import time
import threading
import queue
import whisper
import numpy as np

CHUNK_DURATION = 10
RATE = 16000
CHANNELS = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
audio_queue = queue.Queue()
model = whisper.load_model("small")

#TODO
# 1. Write transcription data to file.

def record_audio(q):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Recording... Press Ctrl+C to stop.")
    
    while True:
        chunk_data = b''
        for _ in range(0, int(RATE / CHUNK * CHUNK_DURATION)):
            data = stream.read(CHUNK)
            chunk_data += data
        q.put(chunk_data)

def save_audio(q):
    while True:
        chunk_data = q.get()
        data = np.frombuffer(chunk_data, np.int16).flatten().astype(np.float32) / 32768.0
        result = model.transcribe(data)
        print(result['text'])

if __name__ == "__main__":
    record_thread = threading.Thread(target=record_audio, args=(audio_queue,))
    save_thread = threading.Thread(target=save_audio, args=(audio_queue,))

    record_thread.start()
    save_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping recording.")