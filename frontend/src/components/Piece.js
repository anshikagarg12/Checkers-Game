// src/components/Piece.js
import React from 'react';

const Piece = ({ value }) => {
  if (value === 0) return null; 

  // 1 and 2 are Red. -1 and -2 are White.
  const isPlayer1 = value === 1 || value === 2; 
  
  // If the absolute value is 2, it's a King!
  const isKing = Math.abs(value) === 2;
  
  const pieceStyle = {
    width: '45px',
    height: '45px',
    borderRadius: '50%',
    backgroundColor: isPlayer1 ? '#cc0000' : '#ffffff', 
    // Add a gold border if it's a King
    border: isKing ? '4px solid gold' : '2px solid #333', 
    boxShadow: 'inset 0 0 5px rgba(0,0,0,0.5)', 
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    color: isPlayer1 ? 'white' : 'black',
    fontSize: '24px',
    paddingBottom: '4px' // Centers the crown slightly better
  };

  // If it's a King, render a little crown symbol inside it!
  return <div style={pieceStyle}>{isKing ? '♔' : ''}</div>;
};

export default Piece;