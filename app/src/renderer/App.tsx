import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import icon from '../../assets/icon.svg';
import './App.css';

const io = require('socket.io-client');

const socket = io('http://127.0.0.1:5555');

function startServer() {
  const data = {
    llm_model: 'gpt-3.5',
    llm_prompt:
      'Could you summarize the top insights from the conversation in bullet points?',
    llm_context: 'no context',
  };

  fetch('http://127.0.0.1:5555/start', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then(() => {
      console.log('HTTP request sent successfully');
      return null;
    })
    .catch((error) => {
      console.error('Error sending HTTP request:', error);
    });
}

function stopServer() {
  fetch('http://127.0.0.1:5555/stop', {
    method: 'POST',
  })
    .then(() => {
      console.log('Server stopped successfully');
      return null;
    })
    .catch((error) => {
      console.error('Error stopping server:', error);
    });
}

function Hello() {
  return (
    <div>
      <div className="Hello">
        <img width="200" alt="icon" src={icon} />
      </div>
      <h1 style={{ textAlign: 'center' }}>Convo Pilot</h1>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button
          type="button"
          onClick={() => {
            socket.emit('start_recording', {
              data: {
                llm_model: 'gpt-3.5',
                llm_prompt:
                  'Could you summarize the top insights from the conversation in bullet points?',
                llm_context: 'no context',
              },
            });
          }}
        >
          Start
        </button>
        <button
          type="button"
          style={{ marginLeft: '10px' }}
          onClick={() => {
            socket.emit('stop_recording', {});
          }}
        >
          Stop
        </button>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Hello />} />
      </Routes>
    </Router>
  );
}
