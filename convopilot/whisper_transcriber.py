import numpy as np
from convopilot import google_doc
from convopilot.interface import AudioTranscriber

import whisper

model = whisper.load_model("medium")

class WhisperAudioTranscriber(AudioTranscriber):
    def __init__(self, outputfile, gdocument):
        self.transcription_data = ""
        self.outputfile = outputfile
        self.gdocument = gdocument

    def transcribe(self, input_queue, output_queue):
        while True:
            chunk_data = input_queue.get()
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
            output_queue.put(self.transcription_data)

        if self.gdocument is not None:
            google_doc.insert_paragraph(
                self.gdocument['documentId'], self.transcription_data + "\n")
            google_doc.insert_paragraph(
                self.gdocument['documentId'], "Transcription:", 'HEADING_2')

        output_queue.put(None)
        print("Stopping transcription.")
