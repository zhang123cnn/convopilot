import React from 'react';

import React, { useState } from 'react';

const io = require('socket.io-client');

const socket = io('http://127.0.0.1:5555');

export default function Session() {
  const [recording, setRecording] = useState(false);
  const [input1, setInput1] = useState('');
  const [input2, setInput2] = useState('Could you summarize the top insights from the conversation in bullet points?');
  const [dropdownValue, setDropdownValue] = useState('');

  const handleInput1Change = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput1(event.target.value);
  };

  const handleInput2Change = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput2(event.target.value);
  };

  const handleDropdownChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setDropdownValue(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log('Input 1:', input1);
    console.log('Input 2:', input2);
    console.log('Dropdown value:', dropdownValue);
    socket.emit('start_recording', {
      data: {
        llm_model: dropdownValue === "" ? null : dropdownValue,
        llm_prompt: input2,
        llm_context: input1,
      },
    });
    setRecording(true);
  };

  const handleStopRecording = () => {
    socket.emit('stop_recording', {});
    setRecording(false);
  }

  return (
    <div>
      <h1>Pilot Session</h1>

      {!recording && <form onSubmit={handleSubmit}>
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
            <textarea style={{ width: '100%', height: '100px' }} value={input1} onChange={handleInput1Change} />
          </label>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <label>
            Prompt:
            <textarea style={{ width: '100%', height: '100px' }} value={input2} onChange={handleInput2Change} />
          </label>
        </div>
        <button type="submit">Submit</button>
      </form>}
      {recording && <button type="button" onClick={handleStopRecording}>Stop Recording</button>}
    </div>
  );
}

