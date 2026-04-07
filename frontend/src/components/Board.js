// src/components/Board.js
import React, { useState } from 'react'; // Added useState
import Square from './Square';
import Piece from './Piece';
const Board = ({ boardData, setBoardState }) => {

  // This state Remembers which square is currently clicked
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

  // This function runs every time you click a square
  // This function runs every time you click ANY square
  const handleSquareClick = (row, col) => {
    const pieceValue = boardData[row][col];

    if (selectedSquare && pieceValue === 0) {
      // KEEP YOUR CODESPACE URL, but use the /move endpoint!
      const moveUrl = 'https://super-duper-giggle-wr449jvr65whg45r-5000.app.github.dev/api/game/move';
      
      // Send the move to Python
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
        if (data.status === "success") {
          // Overwrite the old board with the new board from Python!
          setBoardState(data.board); 
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
        
        // Check if this specific square is the one currently selected
        const isSelected = selectedSquare && selectedSquare.row === row && selectedSquare.col === col;

        squares.push(
          <Square 
            key={`${row}-${col}`} 
            isDark={isDark}
            isSelected={isSelected} // Pass the highlight status
            onClick={() => handleSquareClick(row, col)} // Pass the click function
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