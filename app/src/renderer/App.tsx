import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import icon from '../../assets/icon.svg';
import './App.css';

function Hello() {
  return (
    <div>
      <div className="Hello">
        <img width="200" alt="icon" src={icon} />
      </div>
      <h1 style={{ textAlign: 'center' }}>Convo Pilot</h1>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button
          onClick={() => {
            startServer();
          }}
        >
          Start
        </button>
        <button
          style={{ marginLeft: '10px' }}
          onClick={() => {
            stopServer();
          }}
        >
          Stop
        </button>
      </div>
    </div>
  );
}

function startServer() {
  const data = {
    llm_model: "gpt-3.5",
    llm_prompt: "Could you summarize the top insights from the conversation in bullet points?",
    llm_context: "no context"
  };

  fetch("http://127.0.0.1:5555/start", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => {
      console.log("HTTP request sent successfully");
    })
    .catch(error => {
      console.error("Error sending HTTP request:", error);
    });
}

function stopServer() {
  fetch('http://127.0.0.1:5555/stop', {
    method: 'POST'
  })
    .then(response => {
      console.log('Server stopped successfully');
    })
    .catch(error => {
      console.error('Error stopping server:', error);
    });
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
