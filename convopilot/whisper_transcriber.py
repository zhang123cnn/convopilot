import os
import numpy as np
from convopilot.interface import PipelineModule

import whisper

model = whisper.load_model("medium")


class WhisperAudioTranscriber(PipelineModule):
    def __init__(self, name, output_dir, gdoc_writer):
        super().__init__(name)
        self.output_dir = output_dir
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
        # open local file to append result into it
        if self.output_dir == "":
            print(self.transcription_data)
        else:
            file_path = os.path.join(self.output_dir, "transcription.txt")
            with open(file_path, "w") as f:
                f.write(self.transcription_data)

        if self.gdoc_writer is not None:
            self.gdoc_writer.insert_paragraph_front(
                self.transcription_data + "\n")
            self.gdoc_writer.insert_paragraph_front(
                "Transcription:", 'HEADING_2')

        self.transcription_data = ""

        print("Stopped transcription.")
