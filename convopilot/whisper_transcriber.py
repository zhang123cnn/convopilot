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

    def process(self, data, source):
        chunk_data = np.frombuffer(data, np.int16).flatten().astype(
            np.float32) / 32768.0

        result = model.transcribe(chunk_data)
        text = result['text']

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
