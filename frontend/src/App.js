// src/App.js
import React, { useState, useEffect } from 'react';
import Board from './components/Board';
import './App.css';

function App() {
  const [serverStatus, setServerStatus] = useState('Connecting to Python...');
  
  // THIS is the line that went missing! It holds the matrix.
  const [boardState, setBoardState] = useState([]); 

  useEffect(() => {
    // Your exact Codespace URL with the start endpoint
    const gameUrl = 'https://super-duper-giggle-wr449jvr65whg45r-5000.app.github.dev/api/game/start'; 

    fetch(gameUrl)
      .then(response => response.json())
      .then(data => {
        if (data.status === "game_started") {
          setBoardState(data.board); 
          setServerStatus("Game loaded successfully!");
        }
      })
      .catch(error => {
        console.error("Connection error:", error);
        setServerStatus('Failed to fetch game data.');
      });
  }, []);

  return (
    <div className="App" style={{ textAlign: 'center', padding: '20px' }}>
      <h1>RL Checkers</h1>
      <div style={{ marginBottom: '20px', color: '#555' }}>
        <strong>Status:</strong> {serverStatus}
      </div>
      
      {/* Passing the state and the updater function to the Board */}
      <Board boardData={boardState} setBoardState={setBoardState} /> 
    </div>
  );
}

export default App;