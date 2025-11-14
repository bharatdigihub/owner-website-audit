import React from 'react';
import './RecommendationsList.css';

function RecommendationsList({ recommendations }) {
  return (
    <div className="recommendations-container">
      <h3>📋 Recommendations</h3>
      <div className="recommendations-list">
        {recommendations.map((recommendation, index) => (
          <div key={index} className="recommendation-item">
            <span className="recommendation-icon">💡</span>
            <p>{recommendation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecommendationsList;
