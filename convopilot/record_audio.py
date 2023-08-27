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


class Pipeline:
    def __init__(self):
        self.modules = {}

    def add_module(self, module_name, module, upstreams=[]):
        if module_name in self.modules:
            raise ValueError(f"Module with name {module_name} already exists!")

        for upstream in upstreams:
            q = queue.Queue()
            upstream.add_output_queue(q)
            module.set_input_queue(q)

        self.modules[module_name] = module


class Session(object):
    def __init__(self):
        self.threads = []
        self.audio_recorder = None
        self.hasStarted = False
        self.pipeline = Pipeline()

    def start(self, output_file, llm_metadata, googledoc_metadata):
        if (self.hasStarted):
            return False

        self.hasStarted = True

        gdoc_writer = None
        if googledoc_metadata is not None:
            gdoc_writer = google_doc.GoogleDocWriter(
                googledoc_metadata['name'], googledoc_metadata['folder'])

        executors = []
        self.audio_recorder = ModuleFactory.create_recorder(
            'pyaudio', chunk_duration=30, rate=16000,
            channels=1, chunk=1024, format=pyaudio.paInt16)

        self.pipeline.add_module('pyaudio_recorder', self.audio_recorder)

        executors.append(self.audio_recorder.record)

        audio_transcriber = ModuleFactory.create_transcriber(
            'whisper', outputfile=output_file, gdoc_writer=gdoc_writer)

        self.pipeline.add_module('whisper_transcriber', audio_transcriber, upstreams=[
                                 self.audio_recorder])

        executors.append(audio_transcriber.transcribe)

        if llm_metadata is not None:
            insight_generator = ModuleFactory.create_insight_generator(
                'llm', llm_metadata=llm_metadata, gdoc_writer=gdoc_writer)
            executors.append(insight_generator.generate)
            self.pipeline.add_module('llm_insight_generator',
                                     insight_generator, upstreams=[audio_transcriber])

        for executor in executors:
            thread = threading.Thread(target=executor)
            self.threads.append(thread)
            thread.start()

        return True

    def stop(self):
        if not self.hasStarted:
            return False

        self.hasStarted = False
        self.audio_recorder.stop()
        for thread in self.threads:
            thread.join()

        return True


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

    parser.add_argument("--llm_context", "-c", type=str, default="",
                        help="folder of the google doc to save the outputs")

    args = parser.parse_args().__dict__
    output_file: str = args.pop("output_file")
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

    session = Session()
    session.start(output_file, llm_metadata, googledoc_metadata)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        session.stop()

    print("convopilot stopped.")


if __name__ == "__main__":
    cli()
