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
import { useEffect } from 'react';
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

const socket = io('http://127.0.0.1:5555');

function Loading() {
  const navigate = useNavigate();

  useEffect(() => {
    socket.on('connect', () => {
      navigate('/hello');
    });
  }, []);

  return (
    <div>
      <h1>Waiting for server to come up...</h1>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Loading />} />
        <Route path="/hello" element={<Hello />} />
        <Route path="/Session" element={<Session />} />
      </Routes>
    </Router>
  );
}
