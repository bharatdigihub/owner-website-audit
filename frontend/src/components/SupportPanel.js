import React, { useState } from 'react';
import './SupportPanel.css';
import { FiChevronDown, FiChevronUp, FiBook, FiAlertTriangle, FiCheckCircle, FiClock } from 'react-icons/fi';

function SupportPanel({ analysisData }) {
  const [expandedIssue, setExpandedIssue] = useState(null);
  const [tutorials, setTutorials] = useState({});
  const [loading, setLoading] = useState({});
  const [analytics, setAnalytics] = useState(null);
  const [showAnalytics, setShowAnalytics] = useState(false);

  // Extract all issues from analysis data
  const getAllIssues = () => {
    const issues = [];
    const categories = [
      'performance', 'security', 'seo', 'coding_standards',
      'user_friendliness', 'mobile_optimization', 'accessibility',
      'advanced_metrics'
    ];

    categories.forEach(cat => {
      if (analysisData[cat] && analysisData[cat].issues) {
        analysisData[cat].issues.forEach(issue => {
          issues.push({
            id: `${cat}-${issue.title}`,
            title: issue.title,
            description: issue.description,
            severity: issue.severity || 'medium',
            category: cat
          });
        });
      }
    });

    return issues;
  };

  const issues = getAllIssues();

  // Fetch analytics
  const fetchAnalytics = async () => {
    setShowAnalytics(true);
    if (analytics) return;

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
      const response = await fetch(`${apiUrl}/support/analytics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ analysis_results: analysisData })
      });

      if (response.ok) {
        const data = await response.json();
        setAnalytics(data);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  // Fetch tutorial for an issue
  const fetchTutorial = async (issue) => {
    if (tutorials[issue.id]) {
      setExpandedIssue(expandedIssue === issue.id ? null : issue.id);
      return;
    }

    setLoading(prev => ({ ...prev, [issue.id]: true }));

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
      const response = await fetch(`${apiUrl}/support/quick-fix`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          issue_title: issue.title,
          category: issue.category
        })
      });

      if (response.ok) {
        const data = await response.json();
        setTutorials(prev => ({
          ...prev,
          [issue.id]: data.quick_solution
        }));
        setExpandedIssue(issue.id);
      }
    } catch (error) {
      console.error('Error fetching tutorial:', error);
      setTutorials(prev => ({
        ...prev,
        [issue.id]: 'Unable to load tutorial. Please try again.'
      }));
    } finally {
      setLoading(prev => ({ ...prev, [issue.id]: false }));
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return '#e74c3c';
      case 'high':
        return '#f39c12';
      case 'medium':
        return '#3498db';
      case 'low':
        return '#2ecc71';
      default:
        return '#95a5a6';
    }
  };

  const getSeverityLabel = (severity) => {
    return severity.charAt(0).toUpperCase() + severity.slice(1);
  };

  if (issues.length === 0) {
    return (
      <div className="support-panel">
        <div className="no-issues">
          <FiCheckCircle size={48} color="#2ecc71" />
          <h3>No Issues Found!</h3>
          <p>Your website is in excellent condition. Keep monitoring regularly.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="support-panel">
      <div className="support-header">
        <h2>💡 AI Support Assistant</h2>
        <p>Get instant tutorials and solutions for detected issues</p>
        <button
          className="analytics-btn"
          onClick={fetchAnalytics}
        >
          <FiBook size={16} />
          {analytics ? 'View Analytics' : 'Analyze All Issues'}
        </button>
      </div>

      {showAnalytics && analytics && (
        <div className="analytics-section">
          <div className="analytics-grid">
            <div className="analytics-card">
              <FiAlertTriangle size={24} color="#e74c3c" />
              <div>
                <h4>{analytics.critical_issues}</h4>
                <p>Critical Issues</p>
              </div>
            </div>
            <div className="analytics-card">
              <FiAlertTriangle size={24} color="#f39c12" />
              <div>
                <h4>{analytics.high_priority_issues}</h4>
                <p>High Priority</p>
              </div>
            </div>
            <div className="analytics-card">
              <FiClock size={24} color="#3498db" />
              <div>
                <h4>{analytics.estimated_fix_time?.estimated_hours}h</h4>
                <p>Est. Fix Time</p>
              </div>
            </div>
            <div className="analytics-card">
              <FiCheckCircle size={24} color="#2ecc71" />
              <div>
                <h4>{analytics.quick_wins?.length || 0}</h4>
                <p>Quick Wins</p>
              </div>
            </div>
          </div>

          {analytics.quick_wins && analytics.quick_wins.length > 0 && (
            <div className="quick-wins-section">
              <h3>⚡ Quick Wins (Fix in 5 mins)</h3>
              {analytics.quick_wins.map((win, idx) => (
                <div key={idx} className="quick-win-item">
                  <h4>{win.title}</h4>
                  <p>{win.category}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="issues-list">
        <h3>Issues Detected: {issues.length}</h3>
        {issues.map(issue => (
          <div key={issue.id} className="issue-item">
            <div
              className="issue-header"
              onClick={() => fetchTutorial(issue)}
              style={{ borderLeftColor: getSeverityColor(issue.severity) }}
            >
              <div className="issue-title-section">
                <span
                  className="severity-badge"
                  style={{ backgroundColor: getSeverityColor(issue.severity) }}
                >
                  {getSeverityLabel(issue.severity)}
                </span>
                <div className="issue-text">
                  <h4>{issue.title}</h4>
                  <p>{issue.description}</p>
                </div>
              </div>

              <div className="issue-controls">
                {loading[issue.id] && <span className="loading">Loading...</span>}
                {expandedIssue === issue.id ? (
                  <FiChevronUp size={20} />
                ) : (
                  <FiChevronDown size={20} />
                )}
              </div>
            </div>

            {expandedIssue === issue.id && (
              <div className="issue-solution">
                {tutorials[issue.id] ? (
                  <div className="solution-content">
                    {tutorials[issue.id].split('\n').map((line, idx) => (
                      <p key={idx}>{line}</p>
                    ))}
                  </div>
                ) : (
                  <p>Loading solution...</p>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SupportPanel;
