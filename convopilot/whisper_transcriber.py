import numpy as np
from convopilot.interface import PipelineModule

import whisper

model = whisper.load_model("medium")

class WhisperAudioTranscriber(PipelineModule):
    def __init__(self, outputfile, gdoc_writer):
        super().__init__()
        self.outputfile = outputfile
        self.gdoc_writer = gdoc_writer

    def run(self):
        transcription_data = ""
        while True:
            chunk_data = self.input_queue.get()
            if (chunk_data is None):
                break
            data = np.frombuffer(chunk_data, np.int16).flatten().astype(
                np.float32) / 32768.0
            result = model.transcribe(data)
            # open local file to append result into it
            if self.outputfile == "stdout":
                print(result['text'])
            else:
                with open(self.outputfile, "a") as f:
                    f.write(result['text'])

            self.output_data(result['text'])

            transcription_data += result['text']

        if self.gdoc_writer is not None:
            self.gdoc_writer.insert_paragraph_front(transcription_data + "\n")
            self.gdoc_writer.insert_paragraph_front("Transcription:", 'HEADING_2')

        self.output_data(None)
        print("Stopping transcription.")
