import React, { useState } from 'react';

const io = require('socket.io-client');

const socket = io('http://127.0.0.1:5555');

function SessionPreparation({ onSubmit }: {
  onSubmit: () => void;
}) {
  const [input1, setInput1] = useState('');
  const [input2, setInput2] = useState('Could you summarize the top insights from the conversation in bullet points?');
  const [dropdownValue, setDropdownValue] = useState('');

  const handleInput1Change = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput1(event.target.value);
  };

  const handleInput2Change = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput2(event.target.value);
  };

  const handleDropdownChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setDropdownValue(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    socket.emit('start_recording', {
      data: {
        llm_model: dropdownValue === "" ? null : dropdownValue,
        llm_prompt: input2,
        llm_context: input1,
      },
    });
    onSubmit();
  };

  return (
    <form onSubmit={handleSubmit}>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <label>
          LLM Model:
          <select value={dropdownValue} onChange={handleDropdownChange}>
            <option value="">None</option>
            <option value="gpt-4">GPT-4 (Need openai API Key)</option>
          </select>
        </label>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <label>
          Context:
          <textarea style={{ width: '100%', height: '100px' }} value={input1} onChange={handleInput1Change} placeholder="Enter context for your conversation so LLM can understand better" />
        </label>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <label>
          Prompt:
          <textarea style={{ width: '100%', height: '100px' }} value={input2} onChange={handleInput2Change} />
        </label>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button type="submit">Start</button>
      </div>
    </form>
  );
}

function SessionRecording({ onStop }: {
  onStop: () => void
}) {
  const handleStopRecording = (event: React.MouseEvent<HTMLButtonElement>) => {
    socket.emit('stop_recording', {});
    onStop();
  };

  return (
    <div>
      <button type="button" onClick={handleStopRecording}>Stop Recording</button>
    </div>
  );
}

export default function Session() {
  const [recording, setRecording] = useState(false);
  return (
    <div>
      <h1>Pilot Session</h1>

      {!recording
        ? <SessionPreparation onSubmit={() => setRecording(true)} />
        : <SessionRecording onStop={() => setRecording(false)} />}
    </div>
  );
}

