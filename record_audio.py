import sys
import pyaudio
import wave
import time
import threading
import queue
import whisper

CHUNK_DURATION = 20
RATE = 44100
CHANNELS = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
audio_queue = queue.Queue()
model = whisper.load_model("small")

def record_audio(q):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Recording... Press Ctrl+C to stop.")
    
    while True:
        frames = []
        for _ in range(0, int(RATE / CHUNK * CHUNK_DURATION)):
            data = stream.read(CHUNK)
            frames.append(data)
        q.put(frames)

def save_audio(q):
    file_num = 1
    while True:
        frames = q.get()
        filename = f"output_{file_num}.wav"
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        print(f"Saved {filename}")
        file_num += 1

        result = model.transcribe(filename)
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