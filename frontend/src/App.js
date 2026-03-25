// src/App.js (Updated)
import React, { useState, useEffect } from 'react';
import Board from './components/Board';
import './App.css';

function App() {
  const [serverMessage, setServerMessage] = useState('Checking server status...');

  useEffect(() => {
    // Keep your specific Codespace URL here!
    const backendUrl = 'https://super-duper-giggle-wr449jvr65whg45r-5000.app.github.dev//api/status'; 

    fetch(backendUrl)
      .then(response => response.json())
      .then(data => setServerMessage(data.message))
      .catch(error => {
        console.error("Connection error:", error);
        setServerMessage('Failed to connect to backend.');
      });
  }, []);

  return (
    <div className="App" style={{ textAlign: 'center', padding: '20px' }}>
      <h1>RL Checkers</h1>
      <div style={{ marginBottom: '20px', color: '#555' }}>
        <strong>Backend Status:</strong> {serverMessage}
      </div>
      
      {/* This renders our new 8x8 grid! */}
      <Board /> 
    </div>
  );
}

export default App;