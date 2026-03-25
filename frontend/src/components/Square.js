// src/components/Square.js
import React from 'react';

const Square = ({ isDark }) => {
  const squareStyle = {
    width: '60px',
    height: '60px',
    backgroundColor: isDark ? '#769656' : '#eeeed2', // Classic green and buff colors
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  };

  return <div style={squareStyle}></div>;
};

export default Square;