import argparse
import pyaudio
import time
import threading
import queue
import whisper
import numpy as np

from gpt_api import gptapi
gptapi.setup_key(openai_key_path='/Users/xiaomeng/.openai/api_secret_key')
gptapi.set_budget(5)

CHUNK_DURATION = 20
RATE = 16000
CHANNELS = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
audio_queue = queue.Queue()
model = whisper.load_model("medium")

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

def transcribe_audio(q, outputfile):
    transcription_data = ""
    while True:
        chunk_data = q.get()
        data = np.frombuffer(chunk_data, np.int16).flatten().astype(np.float32) / 32768.0
        result = model.transcribe(data)
        # open local file to append result into it
        with open(outputfile, "a") as f:
           f.write(result['text'])

        transcription_data += result['text']
        print(result['text'])
        generate_llm_insights(transcription_data)

def generate_llm_insights(transcription_data): 
    prompt = f"""
    Could you summarize the top five insights from the conversation below?
    {transcription_data}
    """
    response = gptapi.generate_chat_response([
        {"role": "user", "content": prompt},
    ], model_name="gpt-4")

    print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--output_file", "-o", type=str, default="./transcription.txt", help="file to save the outputs")

    args = parser.parse_args().__dict__
    output_file: str = args.pop("output_file")

    record_thread = threading.Thread(target=record_audio, args=(audio_queue,))
    transcribe_thread = threading.Thread(target=transcribe_audio, args=(audio_queue, output_file))

    record_thread.start()
    transcribe_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping recording.")