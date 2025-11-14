import React from 'react';
import IssuesList from '../common/IssuesList';
import RecommendationsList from '../common/RecommendationsList';

function AdvancedMetricsTab({ data }) {
  if (!data) return <div>No data available</div>;

  const getVitalStatus = (status) => {
    return status === 'Good' ? '✓' : '⚠️';
  };

  return (
    <div className="tab-content">
      <div className="score-section">
        <h2>Advanced Metrics Score: {data.score}%</h2>
        <p>Grade: <strong>{data.grade}</strong></p>
      </div>

      {data.metrics && (
        <>
          <div className="metrics-section">
            <h3>🎯 Core Web Vitals</h3>
            <div className="metrics-grid">
              {data.metrics.core_web_vitals && (
                <>
                  <div className="metric-card">
                    <label>Largest Contentful Paint</label>
                    <value>{getVitalStatus(data.metrics.core_web_vitals.largest_contentful_paint)} {data.metrics.core_web_vitals.largest_contentful_paint}</value>
                  </div>
                  <div className="metric-card">
                    <label>First Input Delay</label>
                    <value>{getVitalStatus(data.metrics.core_web_vitals.first_input_delay)} {data.metrics.core_web_vitals.first_input_delay}</value>
                  </div>
                  <div className="metric-card">
                    <label>Cumulative Layout Shift</label>
                    <value>{getVitalStatus(data.metrics.core_web_vitals.cumulative_layout_shift)} {data.metrics.core_web_vitals.cumulative_layout_shift}</value>
                  </div>
                  <div className="metric-card">
                    <label>Time to Interactive</label>
                    <value>{getVitalStatus(data.metrics.core_web_vitals.time_to_interactive)} {data.metrics.core_web_vitals.time_to_interactive}</value>
                  </div>
                </>
              )}
            </div>
          </div>

          <div className="metrics-section">
            <h3>📦 Resource Efficiency</h3>
            <div className="metrics-grid">
              {data.metrics.resource_efficiency && data.metrics.resource_efficiency.metrics && (
                <>
                  <div className="metric-card">
                    <label>Total Images</label>
                    <value>{data.metrics.resource_efficiency.metrics.total_images || 0}</value>
                  </div>
                  <div className="metric-card">
                    <label>Optimized Images</label>
                    <value>{data.metrics.resource_efficiency.metrics.optimized_images || 0}</value>
                  </div>
                  <div className="metric-card">
                    <label>Render-Blocking Scripts</label>
                    <value>{data.metrics.resource_efficiency.metrics.render_blocking_scripts || 0}</value>
                  </div>
                  <div className="metric-card">
                    <label>Stylesheets</label>
                    <value>{data.metrics.resource_efficiency.metrics.stylesheets || 0}</value>
                  </div>
                </>
              )}
            </div>
          </div>

          <div className="metrics-section">
            <h3>🔗 Third-Party Impact</h3>
            <div className="metrics-grid">
              {data.metrics.third_party_impact && data.metrics.third_party_impact.metrics && (
                <>
                  <div className="metric-card">
                    <label>Third-Party Domains</label>
                    <value>{data.metrics.third_party_impact.metrics.third_party_domains || 0}</value>
                  </div>
                </>
              )}
              {data.metrics.third_party_impact && data.metrics.third_party_impact.metrics && data.metrics.third_party_impact.metrics.third_party_list && (
                <div className="metric-card full-width">
                  <label>Domains List</label>
                  <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                    {data.metrics.third_party_impact.metrics.third_party_list.map((domain, idx) => (
                      <li key={idx}>{domain}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          <div className="metrics-section">
            <h3>🔎 Advanced SEO</h3>
            <div className="metrics-grid">
              {data.metrics.advanced_seo && (
                <>
                  <div className="metric-card">
                    <label>Structured Data</label>
                    <value>{data.metrics.advanced_seo.structured_data ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Open Graph Tags</label>
                    <value>{data.metrics.advanced_seo.open_graph ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Twitter Card</label>
                    <value>{data.metrics.advanced_seo.twitter_card ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Canonical URL</label>
                    <value>{data.metrics.advanced_seo.canonical_url ? '✓' : '✗'}</value>
                  </div>
                  <div className="metric-card">
                    <label>Robots Meta</label>
                    <value>{data.metrics.advanced_seo.robots_meta ? '✓' : '✗'}</value>
                  </div>
                </>
              )}
            </div>
          </div>
        </>
      )}

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

export default AdvancedMetricsTab;
