import os
import shutil
import ctypes.util

import logging

# Setup basic configuration for logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[logging.StreamHandler()]
)

LD_LIBRARY_PATH = os.environ.get('LD_LIBRARY_PATH')
print(f"LD_LIBRARY_PATH: {LD_LIBRARY_PATH}")
# print(util.find_library('libportaudio.2.dylib'))

library_name = ctypes.util.find_library('libportaudio.2.dylib')
print(library_name)

import pyaudio

p = pyaudio.PyAudio()
print("PortAudio version:", pyaudio.get_portaudio_version())
print("Default input device:", p.get_default_input_device_info())
ffmpeg_path = os.environ.get('FFMPEG_PATH')
if ffmpeg_path:
    os.environ['PATH'] = f"{ffmpeg_path}:{os.environ['PATH']}"

ffmpeg_executable = shutil.which('ffmpeg')

if ffmpeg_executable:
    print(f"FFmpeg is located at: {ffmpeg_executable}")
else:
    print("FFmpeg is not found.")

portaudio_executable = shutil.which('portaudio')

if portaudio_executable:
    print(f"portaudio is located at: {portaudio_executable}")
else:
    print("portaudio is not found.")



import argparse
import pyaudio
import time

from dotenv import load_dotenv

from convopilot import google_doc, pipeline, file_writer
from convopilot.llm_insight_generator import LLMInsightGenerator
from convopilot.module_factory import ModuleFactory
from convopilot.pyaudio_recorder import PyAudioRecorder
from convopilot.whisper_transcriber import WhisperAudioTranscriber

load_dotenv()

ModuleFactory.register_recorder('pyaudio', PyAudioRecorder)
ModuleFactory.register_transcriber('whisper', WhisperAudioTranscriber)
ModuleFactory.register_insight_generator('llm', LLMInsightGenerator)

def buildPipeline(output_dir, llm_metadata, googledoc_metadata):
    gdoc_writer = None
    if googledoc_metadata is not None:
        gdoc_writer = google_doc.GoogleDocWriter(
            googledoc_metadata['name'], googledoc_metadata['folder'])

    writer = None
    if output_dir != "":
        writer = file_writer.FileWriter(output_dir)

    audio_recorder = ModuleFactory.create_recorder(
        'pyaudio', name='pyaudio_recorder', chunk_duration=10, rate=16000,
        channels=1, chunk=1024, format=pyaudio.paInt16)

    audio_transcriber = ModuleFactory.create_transcriber(
        'whisper', name='whisper_transcriber', file_writer=writer, gdoc_writer=gdoc_writer)

    p = pipeline.Pipeline(stop_func=audio_recorder.stop)
    p.add_module(audio_recorder)
    p.add_module(audio_transcriber, upstreams=['pyaudio_recorder'])

    if llm_metadata is not None:
        insight_generator = ModuleFactory.create_insight_generator(
            'llm', name='llm_insight_generator', llm_metadata=llm_metadata, gdoc_writer=gdoc_writer)
        p.add_module(insight_generator, upstreams=['whisper_transcriber'])

    return p


def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--output_dir", "-o", type=str,
                        default="", help="directory to save the outputs")
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

    parser.add_argument("--llm_context", "-c", type=str, default="",
                        help="folder of the google doc to save the outputs")

    args = parser.parse_args().__dict__
    output_dir: str = args.pop("output_dir")
    llm_model: str = args.pop("llm_model")
    llm_prompt: str = args.pop("llm_prompt")
    llm_context: str = args.pop("llm_context")
    googledoc: bool = args.pop("googledoc")
    googledocname: str = args.pop("googledocname")
    googledocfolder: str = args.pop("googledocfolder")

    googledoc_metadata = None
    if googledoc:
        googledoc_metadata = {
            "name": googledocname,
            "folder": googledocfolder
        }

    llm_metadata = None
    if llm_model != "none":
        if (llm_context == ""):
            llm_context = input(
                "Please enter some context for the conversation: ")

        llm_metadata = {
            "model": llm_model,
            "prompt": llm_prompt,
            "context": llm_context
        }

    p = buildPipeline(output_dir, llm_metadata, googledoc_metadata)
    p.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        p.stop()

    print("convopilot stopped.")


if __name__ == "__main__":
    cli()
