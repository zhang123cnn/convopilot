from flask_socketio import SocketIO, emit
from flask import Flask
from convopilot.interface import PipelineModule

import record_audio

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


pipeline = None

class ServerResponder(PipelineModule):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            latest = self.input_queue.get()
            if latest is None:
                break

            print(latest)
            socketio.emit('llm_insight', {'data': latest})
        
        self.output_data(None)


@socketio.on('start_recording')
def handle_start_recording(message):
    global pipeline

    if pipeline is not None:
        emit('error', {'message': 'session already started'})

    data = message['data']
    output_file = data.get('output_file', 'stdout')
    googledoc_metadata = data.get('googledoc_metadata', None)

    llm_model = data.get('llm_model', None)
    llm_prompt = data.get('llm_prompt', None)
    llm_context = data.get('llm_context', None)

    llm_metadata = None
    if llm_model != None:
        if llm_context is None or llm_prompt is None:
            emit('error', {'message': 'session already started'})

        llm_metadata = {
            "model": llm_model,
            "prompt": llm_prompt,
            "context": llm_context
        }

    pipeline = record_audio.buildPipeline(output_file=output_file, llm_metadata=llm_metadata,
                                          googledoc_metadata=googledoc_metadata)

    responder = ServerResponder()
    pipeline.add_module('server_responder', responder, upstreams=['llm_insight_generator'])
    pipeline.start()

    emit('started', {})


@socketio.on('stop_recording')
def handle_stop_recording(message):
    if pipeline is None:
        emit('error', {'message': 'session not started'})

    pipeline.stop()

    emit('stopped', {})


if __name__ == '__main__':
    socketio.run(app, port=5555, allow_unsafe_werkzeug=True)
