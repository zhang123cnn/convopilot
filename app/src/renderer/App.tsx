/* eslint-disable no-alert */
/* eslint-disable no-console */
import {
  useNavigate,
  MemoryRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';
import icon from '../../assets/icon.svg';
import './App.css';

import Session from './Session';
import { useEffect, useState } from 'react';
const io = require('socket.io-client');

function Hello() {
  const navigate = useNavigate();

  const handleStartRecording = () => {
    navigate('/Session');
  };

  return (
    <div>
      <div className="Hello">
        <img width="200" alt="icon" src={icon} />
      </div>
      <h1 style={{ textAlign: 'center' }}>Convo Pilot</h1>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button type="button" onClick={handleStartRecording}>
          Start Session
        </button>
      </div>
    </div>
  );
}


function Loading() {
  const navigate = useNavigate();
  const [openaiKey, setOpenaiKey] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const socket = io('http://127.0.0.1:5555');

  useEffect(() => {
    window.electron.ipcRenderer.on('request-data-reply', (event: any, arg: any) => {
      console.log(event, arg)
      if (event.openaiKey !== "") {
        setOpenaiKey(event.openaiKey);
      }
    });
    window.electron.ipcRenderer.sendMessage('request-data', {});
  }, []);

  useEffect(() => {
    socket.on('connect', () => {
      console.log('connected')
      setIsConnected(true);
    });
  }, []);

  useEffect(() => {
    console.log(isConnected, openaiKey)
    if (isConnected && openaiKey !== '') {
      socket.emit('setup_tokens', { data: { openai_key: openaiKey } });
      navigate('/hello');
    }
  }, [openaiKey, isConnected]);

  return (
    <div>
      <h1>Waiting for server to come up...</h1>
    </div>
  );
}

function Setup() {
  const navigate = useNavigate();
  const [openaiKey, setOpenaiKey] = useState('');
  useEffect(() => {
    window.electron.ipcRenderer.on('request-data-reply', (event: any, arg: any) => {
      if (event.openaiKey !== "") {
        navigate('/loading');
      }
    });
    window.electron.ipcRenderer.sendMessage('request-data', {});
  });

  return (
    <div>
      <h1>Setup</h1>
      <form
        onSubmit={(event: React.FormEvent<HTMLFormElement>) => {
          event.preventDefault();
          if (openaiKey === '') {
            return;
          }

          window.electron.ipcRenderer.sendMessage('save-data', { openaiKey });
          navigate('/loading');
        }}
      >
        <div>
          <label htmlFor="openai_key">
            OpenAI Key
            <input type="text" id="openai_key" name="openai_key" onChange={(e) => setOpenaiKey(e.target.value)} />
          </label>
        </div>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <button type="submit">Save</button>
        </div>
      </form>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Setup />} />
        <Route path="/loading" element={<Loading />} />
        <Route path="/hello" element={<Hello />} />
        <Route path="/Session" element={<Session />} />
      </Routes>
    </Router>
  );
}
