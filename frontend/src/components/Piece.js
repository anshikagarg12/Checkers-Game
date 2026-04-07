// src/components/Piece.js
import React from 'react';

const Piece = ({ value }) => {
  // If the backend matrix says '0', there is no piece here
  if (value === 0) return null; 

  const isPlayer1 = value === 1; 
  
  const pieceStyle = {
    width: '45px',
    height: '45px',
    borderRadius: '50%',
    backgroundColor: isPlayer1 ? '#cc0000' : '#ffffff', // Red for P1, White for P2
    border: '2px solid #333',
    boxShadow: 'inset 0 0 5px rgba(0,0,0,0.5)', // Gives it a nice 3D checker feel
  };

  return <div style={pieceStyle}></div>;
};

export default Piece;