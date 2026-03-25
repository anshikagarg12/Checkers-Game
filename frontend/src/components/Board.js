// src/components/Board.js
import React from 'react';
import Square from './Square';

const Board = () => {
  const boardStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(8, 60px)',
    gridTemplateRows: 'repeat(8, 60px)',
    border: '4px solid #333',
    width: 'fit-content',
    margin: '20px auto',
  };

  const renderSquares = () => {
    let squares = [];
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        // A square is dark if the sum of its row and col index is odd
        const isDark = (row + col) % 2 !== 0;
        squares.push(<Square key={`${row}-${col}`} isDark={isDark} />);
      }
    }
    return squares;
  };

  return <div style={boardStyle}>{renderSquares()}</div>;
};

export default Board;