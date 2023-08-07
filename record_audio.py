import argparse
import pyaudio
import time
import threading
import queue
import whisper
import numpy as np

from llm_models import get_llm_model

CHUNK_DURATION = 20
RATE = 16000
CHANNELS = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
audio_queue = queue.Queue()
transcription_queue = queue.Queue()
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

def transcribe_audio(q, tq, outputfile):
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
        tq.put(transcription_data)


def generate_llm_insights(tq, context, llm_model, llm_prompt): 
    model = get_llm_model(llm_model)
    while True:
        transcription_data = tq.get()
        prompt = f"""
        Context: {context}
        Given the context above, {llm_prompt}
        {transcription_data}
        """

        response = model.generate_text(prompt)
        print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--output_file", "-o", type=str, default="./transcription.txt", help="file to save the outputs")
    parser.add_argument("--llm_model", "-m", type=str, default="none", help="llm model to use for conversation analysis")
    parser.add_argument("--llm_prompt", "-p", type=str, default="Could you summarize the top insights from the conversation below", help="prompt used for real time conversation analysis")

    args = parser.parse_args().__dict__
    output_file: str = args.pop("output_file")
    llm_model: str = args.pop("llm_model")
    llm_prompt: str = args.pop("llm_prompt")

    if llm_model != "none":
        context = input("Please enter some context for the conversation: ")
        llm_thread = threading.Thread(target=generate_llm_insights, args=(transcription_queue, context, llm_model, llm_prompt))

    record_thread = threading.Thread(target=record_audio, args=(audio_queue,))
    transcribe_thread = threading.Thread(target=transcribe_audio, args=(audio_queue, transcription_queue, output_file))

    record_thread.start()
    transcribe_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping recording.")