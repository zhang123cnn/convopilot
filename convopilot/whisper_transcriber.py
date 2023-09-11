
import logging
import time
import numpy as np
from convopilot.interface import PipelineModule

import whisper

model = whisper.load_model("medium")


class WhisperAudioTranscriber(PipelineModule):
    def __init__(self, name, file_writer, gdoc_writer):
        super().__init__(name)
        self.file_writer = file_writer
        self.gdoc_writer = gdoc_writer
        self.transcription_data = ""

    def process(self, items):
        logging.debug(f'{self.name} received {len(items)} items')
        total_data = b''
        for data, source in items:
            total_data += data

        chunk_data = np.frombuffer(total_data, np.int16).flatten().astype(
            np.float32) / 32768.0

        cur_time = time.time()
        result = model.transcribe(chunk_data)
        after_time = time.time()
        diff = after_time - cur_time
        logging.debug(f'{self.name} transcribing takes {diff} secconds')
        text = result['text']
        logging.debug(f'{self.name} transcribed text: {text}')

        self.output_data(text)
        self.transcription_data += text

    def onFinish(self):
        if self.file_writer is not None:
            self.file_writer.write("transcription.txt",
                                   self.transcription_data)

        if self.gdoc_writer is not None:
            self.gdoc_writer.insert_paragraph_front(
                self.transcription_data + "\n")
            self.gdoc_writer.insert_paragraph_front(
                "Transcription:", 'HEADING_2')

        self.transcription_data = ""

        print("Stopped transcription.")
