import pyaudio
from convopilot.interface import AudioRecorder


class PyAudioRecorder(AudioRecorder):
    def __init__(self, output_queue, chunk_duration, rate, channels, chunk, format):
        self.p = pyaudio.PyAudio()
        self.chunk_duration = chunk_duration
        self.rate = rate
        self.channels = channels
        self.chunk = chunk

        self.stream = self.p.open(format=format, channels=channels, rate=rate,
                                  input=True, frames_per_buffer=chunk)
        self.output_queue = output_queue
        self.should_stop = False

    def record(self):
        while not self.should_stop:
            chunk_data = b''
            for _ in range(0, int(self.rate / self.chunk * self.chunk_duration)):
                if self.should_stop:
                    break
                data = self.stream.read(self.chunk)
                chunk_data += data
            self.output_queue.put(chunk_data)

        self.output_queue.put(None)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        print("Stopped recording.")

    def stop(self):
        self.should_stop = True

