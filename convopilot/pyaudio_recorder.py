import pyaudio
from convopilot.interface import PipelineModule


class PyAudioRecorder(PipelineModule):
    def __init__(self, name, chunk_duration, rate, channels, chunk, format):
        super().__init__(name)
        self.p = pyaudio.PyAudio()
        self.chunk_duration = chunk_duration
        self.rate = rate
        self.channels = channels
        self.chunk = chunk

        self.stream = self.p.open(format=format, channels=channels, rate=rate,
                                  input=True, frames_per_buffer=chunk)

    def process(self, data, source):
        chunk_data = b''
        for _ in range(0, int(self.rate / self.chunk * self.chunk_duration)):
            if self.should_stop:
                return
            data_ = self.stream.read(self.chunk)
            chunk_data += data_

        self.output_data(chunk_data)

    def onFinish(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        print("Stopped recording.")
