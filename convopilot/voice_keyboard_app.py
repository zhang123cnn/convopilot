import rumps
import logging
import pyaudio
import pyautogui
from pynput import keyboard
import time

import pyperclip
from convopilot import pipeline
from convopilot.interface import PipelineModule

from convopilot.module_factory import ModuleFactory
from convopilot.pyaudio_recorder import PyAudioRecorder
from convopilot.whisper_transcriber import WhisperAudioTranscriber


class KeyboardWriter(PipelineModule):
    def __init__(self, name):
        super().__init__(name)
        self.cur_transcription_data = ""
        self.final_transcription_data = ""
        self.callback = None

    def find_first_difference(self, str1, str2):
        # Iterate over the shorter of the two strings
        for i in range(min(len(str1), len(str2))):
            if str1[i] != str2[i]:
                return i  # Return the index of first difference

        # If one string is a substring of the other
        if len(str1) != len(str2):
            return min(len(str1), len(str2))

        # If the strings are identical
        return -1

    def process(self, items):
        for data, source in items:
            print(data)
            is_final = data['is_final']
            text = data['text']
            index = self.find_first_difference(
                self.cur_transcription_data, text)
            if index == -1:
                continue

            num_to_clear = len(self.cur_transcription_data) - index
            print("Clearing", num_to_clear, "characters",
                  self.cur_transcription_data, text)
            pyautogui.press('backspace', presses=num_to_clear)
            pyperclip.copy(text[index:])
            time.sleep(0.1)
            pyautogui.keyDown('command')
            pyautogui.press('v')
            time.sleep(0.1)
            pyautogui.keyUp('command')

            if (is_final):
                self.final_transcription_data += self.cur_transcription_data + text
                self.cur_transcription_data = ""
            else:
                self.cur_transcription_data = text

    def onFinish(self):
        pyperclip.copy(self.final_transcription_data +
                       self.cur_transcription_data)
        self.final_transcription_data = ""
        self.cur_transcription_data = ""
        print("Stopped keyboard writer.")

        if self.callback:
            self.callback()

    def set_callback(self, callback):
        self.callback = callback


ModuleFactory.register_recorder('pyaudio', PyAudioRecorder)
ModuleFactory.register_transcriber('whisper', WhisperAudioTranscriber)
ModuleFactory.register_insight_generator('keyboardWriter', KeyboardWriter)


def buildPipeline():
    audio_recorder = ModuleFactory.create_recorder(
        'pyaudio', name='pyaudio_recorder', chunk_duration=600, rate=16000,
        channels=1, chunk=1024, format=pyaudio.paInt16)

    audio_transcriber = ModuleFactory.create_transcriber(
        'whisper', name='whisper_transcriber', batch_size=1, file_writer=None, gdoc_writer=None)

    keyboard_writer = ModuleFactory.create_insight_generator(
        'keyboardWriter', name='keyboard_writer')

    p = pipeline.Pipeline(stop_func=audio_recorder.stop)
    p.add_module(audio_recorder)
    p.add_module(audio_transcriber, upstreams=['pyaudio_recorder'])
    p.add_module(keyboard_writer, upstreams=['whisper_transcriber'])

    return p


class LogHandler(logging.Handler):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.log_messages = []
        self.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        message = self.format(record)
        self.log_messages.append(message)


class CommandKeyListener(rumps.App):
    def __init__(self):
        super().__init__("VK")
        self.last_cmd_press_time = 0
        self.cmd_press_interval = 0.5  # Time in seconds to consider as double press
        self.is_dictating = False
        self.pipeline = buildPipeline()
        self.pipeline.modules['keyboard_writer'].set_callback(
            lambda self=self: self.set_text('VK ✅'))
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.menu = ["Log"]
        self.log_handler = LogHandler(self)
        logging.getLogger().addHandler(self.log_handler)
        self._text = "VK"

    @rumps.clicked("Log")
    def show_log_window(self, sender):
        log_text = "\n".join(self.log_handler.log_messages[-20:])
        window = rumps.Window(
            "", "", default_text=log_text, ok=None, cancel=None, dimensions=(720, 720))
        window.run()

    def set_text(self, text):
        self._text = text

    @rumps.timer(0.3)
    def update(self, sender):
        self.title = self._text

    def on_press(self, key):
        try:
            if key == keyboard.Key.alt:
                current_time = time.time()
                if current_time - self.last_cmd_press_time < self.cmd_press_interval:
                    print('Double press detected!')
                    self.is_dictating = not self.is_dictating
                    if self.is_dictating:
                        print('Starting dictation')
                        self.pipeline.start()
                        self.set_text("VK 🎤")
                    else:
                        print('Stopping dictation')
                        self.set_text("VK 🚀")
                        self.pipeline.stop()

                    # Perform your action here
                self.last_cmd_press_time = current_time
        except AttributeError:
            pass


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

if __name__ == '__main__':
    try:
        CommandKeyListener().run()
    except:
        print("finishing")
