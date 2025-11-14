import React from 'react';

function UserBehaviorTab({ data }) {
  if (!data) return <div>No data available</div>;

  return (
    <div className="tab-content">
      <div className="metrics-grid">
        {data.metrics && (
          <>
            {data.metrics.common_paths && (
              <div className="metric-card">
                <h4>Common User Paths</h4>
                <ul className="list-content">
                  {data.metrics.common_paths.map((path, i) => (
                    <li key={i}>{path}</li>
                  ))}
                </ul>
              </div>
            )}

            {data.metrics.popular_elements && (
              <div className="metric-card">
                <h4>Content Elements</h4>
                <div className="element-content">
                  {Object.entries(data.metrics.popular_elements).map(([key, value]) => (
                    <p key={key}><strong>{key}:</strong> {value}</p>
                  ))}
                </div>
              </div>
            )}

            {data.metrics.interaction_potential && (
              <div className="metric-card">
                <h4>Interaction Potential</h4>
                <p className="metric-value">{data.metrics.interaction_potential}/10</p>
              </div>
            )}

            {data.metrics.time_on_page_factors && (
              <div className="metric-card">
                <h4>Time on Page Factors</h4>
                <div className="factor-content">
                  {Object.entries(data.metrics.time_on_page_factors).map(([key, value]) => (
                    <p key={key}><strong>{key}:</strong> {value}</p>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {data.insights && data.insights.length > 0 && (
        <div className="insights-section">
          <h3>Insights</h3>
          {data.insights.map((insight, i) => (
            <div key={i} className="insight-card">
              <h4>{insight.type.replace(/_/g, ' ')}</h4>
              <p>{insight.message}</p>
            </div>
          ))}
        </div>
      )}

      {data.recommendations && data.recommendations.length > 0 && (
        <div className="recommendations-section">
          <h3>Recommendations</h3>
          <ul>
            {data.recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        </div>
      )}

      <style>{`
        .list-content {
          list-style: none;
          padding: 0;
          margin: 0;
        }
        .list-content li {
          padding: 8px 0;
          color: #555;
          border-bottom: 1px solid #eee;
        }
        .element-content, .factor-content {
          font-size: 0.9rem;
        }
        .element-content p, .factor-content p {
          margin: 5px 0;
          color: #555;
        }
        .insights-section, .recommendations-section {
          margin-top: 30px;
        }
        .insights-section h3, .recommendations-section h3 {
          color: #333;
          margin-bottom: 15px;
        }
        .insight-card {
          background: #f8f9fa;
          padding: 15px;
          border-left: 4px solid #667eea;
          border-radius: 4px;
          margin-bottom: 10px;
        }
        .insight-card h4 {
          margin: 0 0 5px 0;
          color: #667eea;
          text-transform: capitalize;
        }
        .insight-card p {
          margin: 0;
          color: #555;
        }
        .recommendations-section ul {
          list-style: none;
          padding: 0;
        }
        .recommendations-section li {
          padding: 12px 15px;
          background: #f0f8ff;
          border-left: 4px solid #27ae60;
          border-radius: 4px;
          margin-bottom: 10px;
          color: #333;
        }
      `}</style>
    </div>
  );
}

export default UserBehaviorTab;
