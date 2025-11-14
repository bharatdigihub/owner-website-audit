import React from 'react';
import IssuesList from '../common/IssuesList';
import RecommendationsList from '../common/RecommendationsList';

function SecurityTab({ data }) {
  if (!data) return <div>No data available</div>;

  return (
    <div className="tab-content">
      <div className="metrics-grid">
        {data.metrics && Object.entries(data.metrics).map(([key, value]) => (
          <div key={key} className="metric-card">
            <h4>{key.replace(/_/g, ' ').toUpperCase()}</h4>
            {typeof value === 'object' ? (
              <div>
                {Object.entries(value).map(([k, v]) => (
                  <p key={k}><strong>{k}:</strong> {String(v)}</p>
                ))}
              </div>
            ) : (
              <p className="metric-value">{String(value)}</p>
            )}
          </div>
        ))}
      </div>

      {data.issues && data.issues.length > 0 && (
        <IssuesList issues={data.issues} title="Security Issues" />
      )}

      {data.recommendations && data.recommendations.length > 0 && (
        <RecommendationsList recommendations={data.recommendations} />
      )}
    </div>
  );
}

export default SecurityTab;
