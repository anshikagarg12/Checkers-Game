// src/components/Square.js
import React from 'react';

// We added 'onClick' and 'isSelected' to the props
const Square = ({ isDark, children, onClick, isSelected }) => {
  let bgColor = isDark ? '#769656' : '#eeeed2';
  
  // If the square is selected, highlight it yellow!
  if (isSelected) {
    bgColor = '#f4d03f'; 
  }

  const squareStyle = {
    width: '60px',
    height: '60px',
    backgroundColor: bgColor,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    cursor: 'pointer', // Changes the mouse to a pointing hand
  };

  return (
    // We added the onClick event listener here
    <div style={squareStyle} onClick={onClick}>
      {children}
    </div>
  );
};

export default Square;