import pyaudio
from convopilot.interface import PipelineModule


class PyAudioRecorder(PipelineModule):
    def __init__(self, chunk_duration, rate, channels, chunk, format):
        super().__init__()
        self.p = pyaudio.PyAudio()
        self.chunk_duration = chunk_duration
        self.rate = rate
        self.channels = channels
        self.chunk = chunk

        self.stream = self.p.open(format=format, channels=channels, rate=rate,
                                  input=True, frames_per_buffer=chunk)
        self.should_stop = False

    def run(self):
        while not self.should_stop:
            chunk_data = b''
            for _ in range(0, int(self.rate / self.chunk * self.chunk_duration)):
                if self.should_stop:
                    break
                data = self.stream.read(self.chunk)
                chunk_data += data

            self.output_data(chunk_data)

        self.output_data(None)

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        print("Stopped recording.")

    def stop(self):
        self.should_stop = True

