// src/components/Board.js
import React, { useState } from 'react';
import Square from './Square';
import Piece from './Piece';

// 1. We added setWinner right here at the top!
const Board = ({ boardData, setBoardState, setWinner }) => {
  const [selectedSquare, setSelectedSquare] = useState(null);

  const boardStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(8, 60px)',
    gridTemplateRows: 'repeat(8, 60px)',
    border: '4px solid #333',
    width: 'fit-content',
    margin: '20px auto',
  };

  if (!boardData || boardData.length === 0) {
    return <div>Loading board from Python...</div>;
  }

  const handleSquareClick = (row, col) => {
    const pieceValue = boardData[row][col];

    if (selectedSquare && pieceValue === 0) {
      // Keep your exact Codespace URL here
      const moveUrl = 'https://super-duper-giggle-wr449jvr65whg45r-5000.app.github.dev/api/game/move';
      
      fetch(moveUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          start: [selectedSquare.row, selectedSquare.col],
          end: [row, col]
        })
      })
      .then(response => response.json())
      .then(data => {
        // 2. We cleanly merged the updated logic here!
        if (data.status === "success" || data.status === "game_over") {
          setBoardState(data.board); 
          
          // If Python says someone won, trigger the game over screen!
          if (data.winner !== 0) {
             setWinner(data.winner); 
          }
        }
      })
      .catch(error => console.error("Move failed:", error));
      
      setSelectedSquare(null); 
    } 
    else if (pieceValue !== 0) {
      setSelectedSquare({ row, col });
    } 
    else {
      setSelectedSquare(null);
    }
  };

  const renderSquares = () => {
    let squares = [];
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const isDark = (row + col) % 2 !== 0;
        const pieceValue = boardData[row][col];
        
        const isSelected = selectedSquare && selectedSquare.row === row && selectedSquare.col === col;

        squares.push(
          <Square 
            key={`${row}-${col}`} 
            isDark={isDark}
            isSelected={isSelected}
            onClick={() => handleSquareClick(row, col)}
          >
            <Piece value={pieceValue} />
          </Square>
        );
      }
    }
    return squares;
  };

  return <div style={boardStyle}>{renderSquares()}</div>;
};

export default Board;