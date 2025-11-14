import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Analyzing your website...</p>
      <p className="spinner-text">This may take a few moments</p>
    </div>
  );
}

export default LoadingSpinner;
