import React, { useState } from 'react';

const io = require('socket.io-client');

const socket = io('http://127.0.0.1:5555');

function SessionPreparation({
  onSubmit,
  prompt,
  setPrompt,
}: {
  onSubmit: () => void;
  prompt: string;
  setPrompt: (prompt: string) => void;
}) {
  const [context, setContext] = useState('');
  const [dropdownValue, setDropdownValue] = useState('');
  const [useGoogleDoc, setUseGoogleDoc] = useState(false);

  const handleContextChange = (
    event: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setContext(event.target.value);
  };

  const handlePromptChange = (
    event: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setPrompt(event.target.value);
  };

  const handleDropdownChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setDropdownValue(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    socket.emit('start_recording', {
      data: {
        llm_model: dropdownValue === '' ? null : dropdownValue,
        llm_prompt: prompt,
        llm_context: context,
        googledoc_metadata: useGoogleDoc
          ? {
              name: 'Untitled',
              folder: '',
            }
          : null,
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
          <textarea
            style={{ width: '100%', height: '100px' }}
            value={context}
            onChange={handleContextChange}
            placeholder="Enter context for your conversation so LLM can understand better"
          />
        </label>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <label>
          Prompt:
          <textarea
            style={{ width: '100%', height: '100px' }}
            value={prompt}
            onChange={handlePromptChange}
          />
        </label>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <label>
          Use Google Doc:
          <input
            type="checkbox"
            checked={useGoogleDoc}
            onChange={(e) => setUseGoogleDoc(e.target.checked)}
          />
        </label>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button type="submit">Start</button>
      </div>
    </form>
  );
}

function SessionRecording({
  onStop,
  prompt,
}: {
  onStop: () => void;
  prompt: string;
}) {
  const [insight, setInsight] = useState('Waiting for insight...');

  const handleStopRecording = (event: React.MouseEvent<HTMLButtonElement>) => {
    socket.emit('stop_recording', {});
    onStop();
  };

  socket.on('llm_insight', (data: any) => {
    console.log(data);
    setInsight(data.data);
  });

  return (
    <div>
      <h3 style={{ textAlign: 'center' }}> Prompt: {prompt} </h3>
      <div
        contentEditable={false}
        style={{ height: '400px', overflow: 'auto' }}
      >
        {insight}
      </div>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button type="button" onClick={handleStopRecording}>
          Stop Recording
        </button>
      </div>
    </div>
  );
}

export default function Session() {
  const [recording, setRecording] = useState(false);
  const [prompt, setPrompt] = useState(
    'Could you summarize the top insights from the conversation in bullet points?'
  );
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <h1>Pilot Session</h1>
      </div>

      {!recording ? (
        <SessionPreparation
          onSubmit={() => setRecording(true)}
          prompt={prompt}
          setPrompt={setPrompt}
        />
      ) : (
        <SessionRecording onStop={() => setRecording(false)} prompt={prompt} />
      )}
    </div>
  );
}
