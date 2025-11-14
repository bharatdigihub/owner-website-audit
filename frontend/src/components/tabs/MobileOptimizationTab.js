import React from 'react';
import IssuesList from '../common/IssuesList';
import RecommendationsList from '../common/RecommendationsList';

function MobileOptimizationTab({ data }) {
  if (!data) return <div>No data available</div>;

  return (
    <div className="tab-content">
      <div className="score-section">
        <h2>Mobile Optimization Score: {data.score}%</h2>
        <p>Grade: <strong>{data.grade}</strong></p>
      </div>

      <div className="metrics-section">
        <h3>📱 Mobile Metrics</h3>
        <div className="metrics-grid">
          {data.metrics && (
            <>
              <div className="metric-card">
                <label>Mobile Score</label>
                <value>{data.metrics.mobile_score || 'N/A'}</value>
              </div>
              {data.metrics.responsive_design && (
                <>
                  <div className="metric-card">
                    <label>Has Viewport</label>
                    <value>{data.metrics.responsive_design.has_viewport ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Media Queries</label>
                    <value>{data.metrics.responsive_design.has_media_queries ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Responsive Images</label>
                    <value>{data.metrics.responsive_design.has_responsive_images ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Flexible Layout</label>
                    <value>{data.metrics.responsive_design.has_flexible_layout ? '✓' : '✗'}</value>
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </div>

      {data.issues && data.issues.length > 0 && (
        <div className="issues-section">
          <h3>⚠️ Issues Found</h3>
          <IssuesList issues={data.issues} />
        </div>
      )}

      {data.recommendations && data.recommendations.length > 0 && (
        <div className="recommendations-section">
          <h3>💡 Recommendations</h3>
          <RecommendationsList recommendations={data.recommendations} />
        </div>
      )}
    </div>
  );
}

export default MobileOptimizationTab;
