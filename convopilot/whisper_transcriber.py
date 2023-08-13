import numpy as np
from convopilot import google_doc
from convopilot.interface import AudioTranscriber

import whisper

model = whisper.load_model("medium")

class WhisperAudioTranscriber(AudioTranscriber):
    def __init__(self, input_queue, output_queue, outputfile, gdocument):
        self.transcription_data = ""
        self.outputfile = outputfile
        self.gdocument = gdocument
        self.input_queue = input_queue
        self.output_queue = output_queue

    def transcribe(self):
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

            self.transcription_data += result['text']
            self.output_queue.put(self.transcription_data)

        if self.gdocument is not None:
            google_doc.insert_paragraph(
                self.gdocument['documentId'], self.transcription_data + "\n")
            google_doc.insert_paragraph(
                self.gdocument['documentId'], "Transcription:", 'HEADING_2')

        self.output_queue.put(None)
        print("Stopping transcription.")
