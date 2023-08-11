import argparse
import pyaudio
import time
import threading
import queue
import whisper
import numpy as np

from dotenv import load_dotenv

load_dotenv()

from convopilot.llm_models import get_llm_model
from convopilot import google_doc

CHUNK_DURATION = 30
RATE = 16000
CHANNELS = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16
audio_queue = queue.Queue()
transcription_queue = queue.Queue()
model = whisper.load_model("medium")
should_stop = False


def record_audio(q):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print("Recording... Press Ctrl+C to stop.")

    while not should_stop:
        chunk_data = b''
        for _ in range(0, int(RATE / CHUNK * CHUNK_DURATION)):
            if should_stop:
                break
            data = stream.read(CHUNK)
            chunk_data += data
        q.put(chunk_data)

    q.put(None)
    print("Stopping recording.")


def transcribe_audio(q, tq, outputfile, gdocument):
    transcription_data = ""
    while True:
        chunk_data = q.get()
        if (chunk_data is None):
            break
        data = np.frombuffer(chunk_data, np.int16).flatten().astype(
            np.float32) / 32768.0
        result = model.transcribe(data)
        # open local file to append result into it
        if outputfile == "stdout":
            print(result['text'])
        else:
            with open(outputfile, "a") as f:
                f.write(result['text'])

        transcription_data += result['text']
        tq.put(transcription_data)

    if gdocument is not None:
        google_doc.insert_paragraph(gdocument['documentId'], transcription_data + "\n")
        google_doc.insert_paragraph(gdocument['documentId'], "Transcription:", 'HEADING_2')

    tq.put(None)
    print("Stopping transcription.")


def generate_llm_insights(tq, context, llm_model, llm_prompt, gdocument):
    model = get_llm_model(llm_model)
    previous_response = ""
    while True:
        transcription_data = tq.get()
        if transcription_data is None:
            break

        prompt = f"""
        You are the best AI conversation facilitator. You are helping a group of people have a conversation about a topic. 
        This is the context for the conversation:
        {context}
        This is what the group want you to help answer:
        {llm_prompt}
        This is your answer up until 30 seconds ago:
        {previous_response}
        This is the latest 2000 words of the conversation:
        {transcription_data[-2000:]}

        Given the information above, could you generate a new answer considering your previous answer and latest conversation?
        """

        response = model.generate_text(prompt)
        previous_response = response
        print(response)

    if gdocument is not None:
        google_doc.insert_paragraph(gdocument['documentId'], previous_response + "\n")
        google_doc.insert_paragraph(gdocument['documentId'], llm_prompt, 'HEADING_2')
        google_doc.insert_paragraph(gdocument['documentId'], f"{context} \n")
        google_doc.insert_paragraph(gdocument['documentId'], "Context:", 'HEADING_2')

    print("Stopping llm generation.")


def start(output_file, llm_model, llm_prompt, googledoc_metadata):
    document = None
    if googledoc_metadata is not None:
        google_doc.init_creds()
        document = google_doc.create_doc(googledoc_metadata['name'], googledoc_metadata['folder'])
        print(f"Created google doc at https://docs.google.com/document/d/{document['documentId']}/edit")

    if llm_model != "none":
        context = input("Please enter some context for the conversation: ")
        llm_thread = threading.Thread(target=generate_llm_insights, args=(
            transcription_queue, context, llm_model, llm_prompt, document))
        llm_thread.start()

    record_thread = threading.Thread(target=record_audio, args=(audio_queue,))
    transcribe_thread = threading.Thread(target=transcribe_audio, args=(
        audio_queue, transcription_queue, output_file, document))

    record_thread.start()
    transcribe_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        global should_stop
        should_stop = True

    record_thread.join()
    transcribe_thread.join()
    if llm_model != "none":
        llm_thread.join()

    print("convopilot stopped.")


def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--output_file", "-o", type=str,
                        default="stdout", help="file to save the outputs")
    parser.add_argument("--llm_model", "-m", type=str, default="none",
                        help="llm model to use for conversation analysis")
    parser.add_argument("--llm_prompt", "-p", type=str, default="Could you summarize the top insights from the conversation in bullet points?",
                        help="prompt used for real time conversation analysis")
    parser.add_argument("--googledoc", "-t", type=bool,
                        default=False, help="use google doc to save the outputs")
    parser.add_argument("--googledocname", "-n", type=str, default="Untitled",
                        help="name of the google doc to save the outputs")
    parser.add_argument("--googledocfolder", "-f", type=str, default="",
                        help="folder of the google doc to save the outputs")

    args = parser.parse_args().__dict__
    output_file: str = args.pop("output_file")
    llm_model: str = args.pop("llm_model")
    llm_prompt: str = args.pop("llm_prompt")
    googledoc: bool = args.pop("googledoc")
    googledocname: str = args.pop("googledocname")
    googledocfolder: str = args.pop("googledocfolder")

    googledoc_metadata = None
    if googledoc:
        googledoc_metadata = {
            "name": googledocname,
            "folder": googledocfolder
        }

    start(output_file, llm_model, llm_prompt, googledoc_metadata)


if __name__ == "__main__":
    cli()
