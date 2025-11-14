import React from 'react';
import IssuesList from '../common/IssuesList';
import RecommendationsList from '../common/RecommendationsList';
import './PerformanceTab.css';

function PerformanceTab({ data }) {
  if (!data) return <div>No data available</div>;

  return (
    <div className="tab-content">
      <div className="metrics-grid">
        {data.metrics && Object.entries(data.metrics).map(([key, value]) => (
          <div key={key} className="metric-card">
            <h4>{key.replace(/_/g, ' ').toUpperCase()}</h4>
            {typeof value === 'object' ? (
              <pre>{JSON.stringify(value, null, 2)}</pre>
            ) : (
              <p className="metric-value">{value}</p>
            )}
          </div>
        ))}
      </div>

      {data.issues && data.issues.length > 0 && (
        <IssuesList issues={data.issues} title="Performance Issues" />
      )}

      {data.recommendations && data.recommendations.length > 0 && (
        <RecommendationsList recommendations={data.recommendations} />
      )}
    </div>
  );
}

export default PerformanceTab;
