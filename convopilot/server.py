from flask import Flask, jsonify, request

import record_audio

app = Flask(__name__)
session = record_audio.Session()

@app.route('/start', methods=['POST'])
def start():
    session.start(output_file='stdout', googledoc_metadata=None,
        llm_model='gpt-4', llm_prompt='Could you summarize the top insights from the conversation in bullet points?')
    return {}

@app.route('/stop', methods=['POST'])
def stop():
    session.stop()
    return {}

if __name__ == '__main__':
    app.run(port=5555)
