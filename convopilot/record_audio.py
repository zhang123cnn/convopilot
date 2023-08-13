import argparse
import pyaudio
import time
import threading
import queue

from dotenv import load_dotenv

from convopilot import google_doc
from convopilot.llm_insight_generator import LLMInsightGenerator
from convopilot.module_factory import ModuleFactory
from convopilot.pyaudio_recorder import PyAudioRecorder
from convopilot.whisper_transcriber import WhisperAudioTranscriber

load_dotenv()

ModuleFactory.register_recorder('pyaudio', PyAudioRecorder)
ModuleFactory.register_transcriber('whisper', WhisperAudioTranscriber)
ModuleFactory.register_insight_generator('llm', LLMInsightGenerator)


def start(output_file, llm_model, llm_prompt, googledoc_metadata):
    audio_queue = queue.Queue()
    transcription_queue = queue.Queue()

    gdoc_writer = None
    if googledoc_metadata is not None:
        gdoc_writer = google_doc.GoogleDocWriter(
            googledoc_metadata['name'], googledoc_metadata['folder'])

    executors = []
    if llm_model != "none":
        context = input("Please enter some context for the conversation: ")
        insight_generator = ModuleFactory.create_insight_generator(
            'llm', input_queue=transcription_queue, llm_model=llm_model, 
            context=context, llm_prompt=llm_prompt, gdoc_writer=gdoc_writer)
        executors.append(insight_generator.generate)

    audio_recorder = ModuleFactory.create_recorder(
        'pyaudio', output_queue=audio_queue, chunk_duration=30, rate=16000, 
        channels=1, chunk=1024, format=pyaudio.paInt16)

    executors.append(audio_recorder.record)

    audio_transcriber = ModuleFactory.create_transcriber(
        'whisper', input_queue=audio_queue, output_queue=transcription_queue, 
        outputfile=output_file, gdoc_writer=gdoc_writer)

    executors.append(audio_transcriber.transcribe)

    threads = []
    for executor in executors:
        thread = threading.Thread(target=executor)
        thread.start()
        threads.append(thread)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        audio_recorder.stop()

    for thread in threads:
        thread.join()

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
