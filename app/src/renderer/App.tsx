/* eslint-disable no-alert */
/* eslint-disable no-console */
import {
  useNavigate,
  MemoryRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';
import Constants from 'main/utils/Constants';
import { useEffect, useState } from 'react';
import Messages from 'main/utils/Messages';
import icon from '../../assets/icon.svg';
import './App.css';

import Session from './Session';

function Hello() {
  const navigate = useNavigate();

  const [latestMessage, setLatestMessage] = useState('');
  const [installButtonTitle, setInstallButtonTitle] = useState(
    'Install Dependencies'
  );

  const [installerBusy, setInstallerBusy] = useState(false);
  useEffect(() => {
    const removeListener = window.electron.ipcRenderer.on(
      Constants.IPC_RENDERER_CHANNEL,
      async (event) => {
        console.log('event::');
        console.log(JSON.stringify(event));
        setLatestMessage(JSON.stringify(event));
      }
    );
    return () => {
      removeListener();
    };
  }, []);

  useEffect(() => {
    if (latestMessage === '') {
      return;
    }
    const message = JSON.parse(latestMessage);
    console.log('message::');
    console.log(message);
    if (message === Messages.MAIN_TO_RENDERER.START_INSTALL_EVENT) {
      console.log('Installing...');
      setInstallButtonTitle('Installing...');
      setInstallerBusy(true);
    } else if (message === Messages.MAIN_TO_RENDERER.SUCCESS_INSTALL_EVENT) {
      console.log('Installing Success');
      alert('Installing Success');
      setInstallerBusy(false);
    } else if (message === Messages.MAIN_TO_RENDERER.FAIL_INSTALL_EVENT) {
      console.log('Installing Failed');
      alert('Installing Failed, check console for more info.');
      setInstallerBusy(false);
    }
  }, [latestMessage]);

  const handleInstallClick = () => {
    if (installerBusy) {
      alert('Installer is busy, PLEASE WAIT!');
      return;
    }
    window.electron.ipcRenderer.sendMessage(Constants.IPC_MAIN_CHANNEL, [
      Messages.RENDERER_TO_MAIN.INSTALL_DEPS,
    ]);
  };

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
        <button type="button" onClick={handleInstallClick}>
          {installButtonTitle}
        </button>

        <button type="button" onClick={handleStartRecording}>
          Start Session
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
        <Route path="/Session" element={<Session />} />
      </Routes>
    </Router>
  );
}
