// src/App.js
import React, { useState, useEffect } from 'react';
import Board from './components/Board';
import './App.css';

function App() {
  const [serverStatus, setServerStatus] = useState('Connecting...');
  const [boardState, setBoardState] = useState([]); 
  
  // NEW: Keep track of who won! (0 = no one, 1 = Player, -1 = Computer)
  const [winner, setWinner] = useState(0); 

  // Keep your actual Codespace URL!
  const BASE_URL = 'https://super-duper-giggle-wr449jvr65whg45r-5000.app.github.dev/api/..';

  const startNewGame = () => {
    setServerStatus('Starting new game...');
    setWinner(0); // Reset the winner
    
    fetch(`${BASE_URL}/api/game/start`)
      .then(response => response.json())
      .then(data => {
        if (data.status === "game_started") {
          setBoardState(data.board); 
          setServerStatus("Game loaded successfully!");
        }
      })
      .catch(error => setServerStatus('Failed to fetch game data.'));
  };

  // Start the game when the page first loads
  useEffect(() => {
    startNewGame();
  }, []);

  return (
    <div className="App" style={{ textAlign: 'center', padding: '20px' }}>
      <h1>RL Checkers</h1>
      
      {/* THE VICTORY BANNER */}
      {winner === 1 && <h2 style={{ color: 'green' }}>🏆 YOU WIN! 🏆</h2>}
      {winner === -1 && <h2 style={{ color: 'red' }}>💀 COMPUTER WINS! 💀</h2>}
      
      <div style={{ marginBottom: '20px', color: '#555' }}>
        <strong>Status:</strong> {serverStatus}
      </div>
      
      {/* Only let them play if the game isn't over! */}
      {winner === 0 ? (
        <Board 
          boardData={boardState} 
          setBoardState={setBoardState} 
          setWinner={setWinner} // Pass the setter so the Board can end the game
        /> 
      ) : (
        <button 
          onClick={startNewGame} 
          style={{ padding: '15px 30px', fontSize: '20px', cursor: 'pointer' }}
        >
          Play Again
        </button>
      )}
    </div>
  );
}

export default App;