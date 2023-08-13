import argparse
import pyaudio
import time
import threading
import queue

from dotenv import load_dotenv

from convopilot import google_doc
from convopilot.llm_insight_generator import LLMInsightGenerator
from convopilot.llm_models import get_llm_model
from convopilot.module_factory import ModuleFactory
from convopilot.pyaudio_recorder import PyAudioRecorder
from convopilot.whisper_transcriber import WhisperAudioTranscriber

load_dotenv()

audio_queue = queue.Queue()
transcription_queue = queue.Queue()

def register_modules():
    ModuleFactory.register_recorder('pyaudio', PyAudioRecorder)
    ModuleFactory.register_transcriber('whisper', WhisperAudioTranscriber)
    ModuleFactory.register_insight_generator('llm', LLMInsightGenerator)


def start(output_file, llm_model, llm_prompt, googledoc_metadata):
    register_modules()

    document = None
    if googledoc_metadata is not None:
        google_doc.init_creds()
        document = google_doc.create_doc(
            googledoc_metadata['name'], googledoc_metadata['folder'])
        print(
            f"Created google doc at https://docs.google.com/document/d/{document['documentId']}/edit")

    if llm_model != "none":
        context = input("Please enter some context for the conversation: ")
        insight_generator = ModuleFactory.create_insight_generator(
            'llm', llm_model=llm_model, context=context, llm_prompt=llm_prompt, gdocument=document)
        llm_thread = threading.Thread(
            target=insight_generator.generate, args=(transcription_queue,))
        llm_thread.start()

    audio_recorder = ModuleFactory.create_recorder(
        'pyaudio', chunk_duration=30, rate=16000, channels=1, chunk=1024, format=pyaudio.paInt16)

    audio_transcriber = ModuleFactory.create_transcriber(
        'whisper', outputfile=output_file, gdocument=document)

    record_thread = threading.Thread(
        target=audio_recorder.record, args=(audio_queue,))
    transcribe_thread = threading.Thread(target=audio_transcriber.transcribe, args=(
        audio_queue, transcription_queue))

    record_thread.start()
    transcribe_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        audio_recorder.stop()

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
