import React from 'react';
import IssuesList from '../common/IssuesList';
import RecommendationsList from '../common/RecommendationsList';

function CodeStandardsTab({ data }) {
  if (!data) return <div>No data available</div>;

  return (
    <div className="tab-content">
      {data.issues && data.issues.length > 0 && (
        <IssuesList issues={data.issues} title="Code Standards Issues" />
      )}

      {data.recommendations && data.recommendations.length > 0 && (
        <RecommendationsList recommendations={data.recommendations} />
      )}
    </div>
  );
}

export default CodeStandardsTab;
