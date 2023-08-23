from flask import abort
from flask import Flask, jsonify, request

import record_audio

app = Flask(__name__)
session = record_audio.Session()


@app.route('/start', methods=['POST'])
def start():
    data = request.json
    output_file = data.get('output_file', 'stdout')
    googledoc_metadata = data.get('googledoc_metadata', None)

    llm_model = data.get('llm_model', None)
    llm_prompt = data.get('llm_prompt', None)
    llm_context = data.get('llm_context', None)

    llm_metadata = None
    if llm_model != None:
        if llm_context is None or llm_prompt is None:
            abort(400, 'llm_context and llm_prompt is required')

        llm_metadata = {
            "model": llm_model,
            "prompt": llm_prompt,
            "context": llm_context
        }

    success = session.start(output_file=output_file, llm_metadata=llm_metadata,
                  googledoc_metadata=googledoc_metadata)

    if not success:
        abort(500, 'session already started')

    return {}


@app.route('/stop', methods=['POST'])
def stop():
    success = session.stop()
    if not success:
        abort(500, 'session not started')

    return {}


if __name__ == '__main__':
    app.run(port=5555)
