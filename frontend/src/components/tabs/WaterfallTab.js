import React, { useState } from 'react';
import './PerformanceTab.css';

const WaterfallTab = ({ data }) => {
  const [sortBy, setSortBy] = useState('start_time');

  if (!data) return <div className="tab-content">No waterfall data available</div>;

  const waterfall = data.waterfall || {};
  const resources = waterfall.waterfall || [];
  const metrics = waterfall.metrics || {};

  // Sort resources
  const sortedResources = [...resources].sort((a, b) => {
    if (sortBy === 'start_time') return a.start_time - b.start_time;
    if (sortBy === 'total_time') return b.total_time - a.total_time;
    if (sortBy === 'size') return b.size - a.size;
    return 0;
  });

  // Get color for resource type
  const getTypeColor = (type) => {
    const colors = {
      document: '#3b82f6',
      stylesheet: '#8b5cf6',
      script: '#ef4444',
      image: '#10b981',
      font: '#f59e0b',
      other: '#6b7280'
    };
    return colors[type] || colors.other;
  };

  // Get max time for scaling
  const maxTime = Math.max(...resources.map(r => r.end_time), 1000);

  return (
    <div className="tab-content">
      <div className="section">
        <h3>Resource Waterfall Chart</h3>
        <p className="description">
          Waterfall chart shows the timeline and order of resource loading. Wider bars indicate slower resource loads.
        </p>

        {/* Score Card */}
        <div className="score-card">
          <div className="score-number">{waterfall.score || 0}</div>
          <div className="score-label">Waterfall Efficiency</div>
          <div className={`score-grade grade-${waterfall.grade || 'F'}`}>{waterfall.grade || 'F'}</div>
        </div>

        {/* Metrics Summary */}
        <div className="metrics-grid">
          <div className="metric-box">
            <div className="metric-label">Total Requests</div>
            <div className="metric-value">{metrics.total_requests}</div>
          </div>
          <div className="metric-box">
            <div className="metric-label">Total Size</div>
            <div className="metric-value">{metrics.total_size_kb} KB</div>
          </div>
          <div className="metric-box">
            <div className="metric-label">Page Load Time</div>
            <div className="metric-value">{metrics.page_load_time_ms} ms</div>
          </div>
          <div className="metric-box">
            <div className="metric-label">Critical Path</div>
            <div className="metric-value">{Math.round(metrics.critical_path_time)} ms</div>
          </div>
        </div>

        {/* Sort Options */}
        <div className="filter-section">
          <label>Sort by:</label>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="start_time">Start Time</option>
            <option value="total_time">Duration</option>
            <option value="size">File Size</option>
          </select>
        </div>

        {/* Waterfall Chart */}
        <div className="waterfall-container">
          <table className="waterfall-table">
            <thead>
              <tr>
                <th>Resource</th>
                <th>Type</th>
                <th>Size</th>
                <th>Timeline</th>
                <th>Duration</th>
              </tr>
            </thead>
            <tbody>
              {sortedResources.map((resource, index) => {
                const startPercent = (resource.start_time / maxTime) * 100;
                const durationPercent = (resource.total_time / maxTime) * 100;
                return (
                  <tr key={index}>
                    <td className="resource-name" title={resource.name}>
                      {resource.name.length > 30 ? resource.name.substring(0, 27) + '...' : resource.name}
                    </td>
                    <td>
                      <span className="badge" style={{ backgroundColor: getTypeColor(resource.type) }}>
                        {resource.type}
                      </span>
                    </td>
                    <td>{resource.size_kb} KB</td>
                    <td className="timeline-cell">
                      <div className="timeline-bar">
                        <div
                          className="timeline-segment dns"
                          style={{
                            left: `${startPercent}%`,
                            width: `${(resource.dns_time / maxTime) * 100}%`,
                            title: `DNS: ${resource.dns_time}ms`
                          }}
                          title={`DNS: ${resource.dns_time}ms`}
                        />
                        <div
                          className="timeline-segment tcp"
                          style={{
                            left: `${startPercent + (resource.dns_time / maxTime) * 100}%`,
                            width: `${(resource.tcp_time / maxTime) * 100}%`,
                            title: `TCP: ${resource.tcp_time}ms`
                          }}
                          title={`TCP: ${resource.tcp_time}ms`}
                        />
                        <div
                          className="timeline-segment request"
                          style={{
                            left: `${startPercent + ((resource.dns_time + resource.tcp_time) / maxTime) * 100}%`,
                            width: `${(resource.request_time / maxTime) * 100}%`,
                            title: `Request: ${resource.request_time}ms`
                          }}
                          title={`Request: ${resource.request_time}ms`}
                        />
                        <div
                          className="timeline-segment response"
                          style={{
                            left: `${startPercent + ((resource.dns_time + resource.tcp_time + resource.request_time) / maxTime) * 100}%`,
                            width: `${(resource.response_time / maxTime) * 100}%`,
                            title: `Response: ${resource.response_time}ms`
                          }}
                          title={`Response: ${resource.response_time}ms`}
                        />
                      </div>
                    </td>
                    <td>{resource.total_time} ms</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Legend */}
        <div className="waterfall-legend">
          <div className="legend-item">
            <span className="timeline-segment dns" style={{ backgroundColor: '#3b82f6' }} /> DNS Lookup
          </div>
          <div className="legend-item">
            <span className="timeline-segment tcp" style={{ backgroundColor: '#8b5cf6' }} /> TCP Connection
          </div>
          <div className="legend-item">
            <span className="timeline-segment request" style={{ backgroundColor: '#ef4444' }} /> Request Send
          </div>
          <div className="legend-item">
            <span className="timeline-segment response" style={{ backgroundColor: '#10b981' }} /> Response Download
          </div>
        </div>

        {/* By Type Summary */}
        {metrics.by_type && (
          <div className="by-type-section">
            <h4>Resources by Type</h4>
            <div className="type-summary">
              {Object.entries(metrics.by_type).map(([type, info]) => (
                <div key={type} className="type-summary-item">
                  <span className="type-name">{type}</span>
                  <span className="type-count">{info.count} files</span>
                  <span className="type-size">{Math.round(info.size / 1024)} KB</span>
                  <span className="type-time">{Math.round(info.time)} ms</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Issues */}
        {waterfall.issues && waterfall.issues.length > 0 && (
          <div className="issues-section">
            <h4>⚠️ Issues Found</h4>
            <ul>
              {waterfall.issues.map((issue, index) => (
                <li key={index}>{issue}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {waterfall.recommendations && waterfall.recommendations.length > 0 && (
          <div className="recommendations-section">
            <h4>✅ Recommendations</h4>
            <ul>
              {waterfall.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <style jsx>{`
        .waterfall-container {
          overflow-x: auto;
          margin: 20px 0;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
        }

        .waterfall-table {
          width: 100%;
          border-collapse: collapse;
          font-size: 13px;
        }

        .waterfall-table th,
        .waterfall-table td {
          padding: 10px;
          text-align: left;
          border-bottom: 1px solid #e5e7eb;
        }

        .waterfall-table th {
          background-color: #f3f4f6;
          font-weight: 600;
          position: sticky;
          top: 0;
        }

        .resource-name {
          font-family: monospace;
          color: #4b5563;
          max-width: 200px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .timeline-cell {
          min-width: 400px;
        }

        .timeline-bar {
          position: relative;
          height: 30px;
          background-color: #f0f0f0;
          border-radius: 4px;
          margin: 5px 0;
        }

        .timeline-segment {
          position: absolute;
          height: 100%;
          min-width: 2px;
          opacity: 0.9;
        }

        .timeline-segment.dns {
          background-color: #3b82f6;
        }

        .timeline-segment.tcp {
          background-color: #8b5cf6;
        }

        .timeline-segment.request {
          background-color: #ef4444;
        }

        .timeline-segment.response {
          background-color: #10b981;
        }

        .waterfall-legend {
          display: flex;
          gap: 20px;
          margin: 20px 0;
          flex-wrap: wrap;
        }

        .legend-item {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .by-type-section {
          margin-top: 30px;
        }

        .type-summary {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
          gap: 15px;
          margin-top: 15px;
        }

        .type-summary-item {
          display: flex;
          flex-direction: column;
          gap: 5px;
          padding: 15px;
          background-color: #f9fafb;
          border-radius: 8px;
          border-left: 4px solid #3b82f6;
        }

        .type-name {
          font-weight: 600;
          text-transform: capitalize;
        }

        .type-count,
        .type-size,
        .type-time {
          font-size: 12px;
          color: #6b7280;
        }

        .filter-section {
          display: flex;
          align-items: center;
          gap: 10px;
          margin: 15px 0;
        }

        .filter-section select {
          padding: 8px 12px;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          background-color: white;
          cursor: pointer;
        }
      `}</style>
    </div>
  );
};

export default WaterfallTab;
