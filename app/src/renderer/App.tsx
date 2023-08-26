import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import icon from '../../assets/icon.svg';
import './App.css';

import { useNavigate } from 'react-router-dom';

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

import Session from './Session';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Hello />} />
        <Route path="/Session" element={<Session />} />
      </Routes>
    </Router>
  );
}
