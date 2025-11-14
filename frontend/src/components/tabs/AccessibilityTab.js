import React from 'react';
import IssuesList from '../common/IssuesList';
import RecommendationsList from '../common/RecommendationsList';

function AccessibilityTab({ data }) {
  if (!data) return <div>No data available</div>;

  const renderWCAGBadge = (level) => {
    const colors = {
      'A': '#ffd700',
      'AA': '#c0c0c0',
      'AAA': '#cd7f32',
      'None': '#999'
    };
    return <span style={{ color: colors[level], fontWeight: 'bold' }}>{level}</span>;
  };

  return (
    <div className="tab-content">
      <div className="score-section">
        <h2>Accessibility Score: {data.score}%</h2>
        <p>Grade: <strong>{data.grade}</strong></p>
      </div>

      <div className="metrics-section">
        <h3>♿ Accessibility Metrics</h3>
        <div className="metrics-grid">
          {data.metrics && (
            <>
              <div className="metric-card">
                <label>WCAG Level</label>
                <value>{renderWCAGBadge(data.metrics.wcag_level || 'Unknown')}</value>
              </div>
              {data.metrics.accessibility_features && (
                <>
                  <div className="metric-card">
                    <label>Semantic HTML</label>
                    <value>{data.metrics.accessibility_features.has_semantic_html ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>ARIA Labels</label>
                    <value>{data.metrics.accessibility_features.has_aria_labels ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Alt Text</label>
                    <value>{data.metrics.accessibility_features.has_alt_text ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Skip Links</label>
                    <value>{data.metrics.accessibility_features.has_skip_links ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Language Declared</label>
                    <value>{data.metrics.accessibility_features.has_lang_attribute ? '✓' : '✗'}</value>
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </div>

      {data.issues && data.issues.length > 0 && (
        <div className="issues-section">
          <h3>⚠️ Accessibility Issues</h3>
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

export default AccessibilityTab;
