
import logging
import time
import numpy as np
from convopilot.interface import PipelineModule

import whisper

model = whisper.load_model("medium.en")


class WhisperAudioTranscriber(PipelineModule):
    def __init__(self, name, file_writer, gdoc_writer, batch_size):
        super().__init__(name)
        self.file_writer = file_writer
        self.gdoc_writer = gdoc_writer
        self.transcription_data = ""
        self.batch_data = b''
        self.batch_size = batch_size
        self.cur_batch_count = 0

    def process(self, items):
        logging.debug(f'{self.name} received {len(items)} items')
        for data, source in items:
            self.batch_data += data
            self.cur_batch_count += 1

        logging.debug(f'{self.name} cur_batch_count {self.cur_batch_count}')

        chunk_data = np.frombuffer(self.batch_data, np.int16).flatten().astype(
            np.float32) / 32768.0

        cur_time = time.time()
        result = model.transcribe(chunk_data, language="en", fp16=False)
        after_time = time.time()
        diff = after_time - cur_time
        logging.debug(f'{self.name} transcribing takes {diff} secconds')
        logging.debug(f'{self.name} transcription raw result: {result}')

        text = self.get_text_from_transcribe_result(result)
        is_final = self.cur_batch_count >= self.batch_size

        if text != "":
            data = {'text': text, 'is_final': is_final}
            self.output_data(data)
            logging.debug(f'{self.name} output data {data}')

            if is_final:
                self.transcription_data += text

        if is_final:
            self.batch_data = b''
            self.cur_batch_count = 0

    def get_text_from_transcribe_result(self, result):
        text = ""
        for segment in sorted(result['segments'], key=lambda x: x['start']):
            if segment['no_speech_prob'] > 0.7:
                logging.debug(
                    f'{self.name} no speech ({segment["no_speech_prob"]}) detected from {segment["start"]} to {segment["end"]}. skipping')
                continue

            text += segment['text']

        logging.debug(f'{self.name} transcribed text: {text}')
        return text


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
