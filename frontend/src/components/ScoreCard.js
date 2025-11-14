import React from 'react';
import './ScoreCard.css';

function ScoreCard({ title, score, grade, icon }) {
  const getScoreColor = (score) => {
    if (score >= 80) return '#27ae60';
    if (score >= 60) return '#f39c12';
    return '#e74c3c';
  };

  return (
    <div className="score-card">
      <div className="score-card-icon">{icon}</div>
      <div className="score-card-content">
        <h3>{title}</h3>
        <div className="score-display">
          <div className="score-circle" style={{ borderColor: getScoreColor(score) }}>
            <span className="score-number">{score}</span>
          </div>
          <div className="score-grade" style={{ backgroundColor: getScoreColor(score) }}>
            {grade}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ScoreCard;
