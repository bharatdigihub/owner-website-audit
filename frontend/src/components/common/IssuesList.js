import React from 'react';
import './IssuesList.css';

function IssuesList({ issues, title }) {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return '#c0392b';
      case 'high':
        return '#e74c3c';
      case 'medium':
        return '#f39c12';
      case 'low':
        return '#3498db';
      default:
        return '#95a5a6';
    }
  };

  return (
    <div className="issues-container">
      <h3>{title}</h3>
      <div className="issues-list">
        {issues.map((issue, index) => (
          <div 
            key={index} 
            className="issue-item"
            style={{ borderLeftColor: getSeverityColor(issue.severity) }}
          >
            <div className="issue-header">
              <span className="severity-badge" style={{ backgroundColor: getSeverityColor(issue.severity) }}>
                {issue.severity.toUpperCase()}
              </span>
              <h4>{issue.type.replace(/_/g, ' ')}</h4>
            </div>
            <p>{issue.message}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default IssuesList;
