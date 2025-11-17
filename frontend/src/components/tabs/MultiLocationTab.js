import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import './PerformanceTab.css';

const MultiLocationTab = ({ data }) => {
  if (!data) return <div className="tab-content">No multi-location data available</div>;

  const multiLoc = data.multi_location || {};
  const locations = multiLoc.locations || [];
  const metrics = multiLoc.metrics || {};

  // Prepare chart data
  const chartData = locations.map(loc => ({
    name: loc.location_code,
    time: loc.page_load_time_ms,
    ttfb: loc.ttfb_ms,
    fcp: loc.fcp_ms
  }));

  const getStatusColor = (status) => {
    if (status === 'Pass') return '#10b981';
    if (status === 'Warn') return '#f59e0b';
    return '#ef4444';
  };

  const getRegionColor = (region) => {
    const colors = {
      'North America': '#3b82f6',
      'Europe': '#8b5cf6',
      'Asia Pacific': '#ec4899',
      'South America': '#f59e0b'
    };
    return colors[region] || '#6b7280';
  };

  return (
    <div className="tab-content">
      <div className="section">
        <h3>Multi-Location Performance Testing</h3>
        <p className="description">
          Test your website performance from multiple global locations. See how your site loads for users worldwide.
        </p>

        {/* Score Card */}
        <div className="score-card">
          <div className="score-number">{multiLoc.score || 0}</div>
          <div className="score-label">Global Performance</div>
          <div className={`score-grade grade-${multiLoc.grade || 'F'}`}>{multiLoc.grade || 'F'}</div>
        </div>

        {/* Metrics Summary */}
        <div className="metrics-grid">
          <div className="metric-box">
            <div className="metric-label">Locations Tested</div>
            <div className="metric-value">{metrics.locations_tested || 0}</div>
          </div>
          <div className="metric-box">
            <div className="metric-label">Average Load Time</div>
            <div className="metric-value">{metrics.average_load_time_ms} ms</div>
          </div>
          <div className="metric-box">
            <div className="metric-label">Fastest Region</div>
            <div className="metric-value">{metrics.fastest_region?.location_name?.split(',')[0] || 'N/A'}</div>
          </div>
          <div className="metric-box">
            <div className="metric-label">Slowest Region</div>
            <div className="metric-value">{metrics.slowest_region?.location_name?.split(',')[0] || 'N/A'}</div>
          </div>
        </div>

        {/* Performance Chart */}
        <div className="chart-container">
          <h4>Load Times by Location</h4>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
              <YAxis label={{ value: 'Load Time (ms)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="time" fill="#3b82f6" name="Total Load Time" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Locations Table */}
        <div className="locations-table-container">
          <h4>Detailed Results by Location</h4>
          <table className="locations-table">
            <thead>
              <tr>
                <th>Location</th>
                <th>Region</th>
                <th>Network</th>
                <th>Load Time</th>
                <th>TTFB</th>
                <th>FCP</th>
                <th>LCP</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {locations.map((location, index) => (
                <tr key={index}>
                  <td className="location-name">
                    <strong>{location.location_name}</strong>
                  </td>
                  <td>
                    <span
                      className="region-badge"
                      style={{ backgroundColor: getRegionColor(location.region) }}
                    >
                      {location.region}
                    </span>
                  </td>
                  <td>{location.base_latency_ms} ms latency</td>
                  <td>
                    <strong>{location.page_load_time_ms} ms</strong>
                  </td>
                  <td>{location.ttfb_ms} ms</td>
                  <td>{location.fcp_ms} ms</td>
                  <td>{location.lcp_ms} ms</td>
                  <td>
                    <span
                      className={`status-badge status-${location.status.toLowerCase()}`}
                      style={{ backgroundColor: getStatusColor(location.status) }}
                    >
                      {location.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Regional Summary */}
        <div className="regional-summary">
          <h4>Performance by Region</h4>
          <div className="region-cards">
            {['North America', 'Europe', 'Asia Pacific', 'South America'].map(region => {
              const regionLocs = locations.filter(l => l.region === region);
              const avgTime = regionLocs.length > 0
                ? Math.round(regionLocs.reduce((sum, l) => sum + l.page_load_time_ms, 0) / regionLocs.length)
                : 'N/A';
              const passCount = regionLocs.filter(l => l.status === 'Pass').length;
              
              return (
                <div key={region} className="region-card" style={{ borderLeftColor: getRegionColor(region) }}>
                  <div className="region-header">{region}</div>
                  <div className="region-stat">
                    <span>Avg Load Time:</span>
                    <strong>{avgTime} ms</strong>
                  </div>
                  <div className="region-stat">
                    <span>Locations:</span>
                    <strong>{regionLocs.length}</strong>
                  </div>
                  <div className="region-stat">
                    <span>Pass Rate:</span>
                    <strong>
                      {regionLocs.length > 0 ? Math.round((passCount / regionLocs.length) * 100) : 0}%
                    </strong>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Issues */}
        {multiLoc.issues && multiLoc.issues.length > 0 && (
          <div className="issues-section">
            <h4>⚠️ Issues Found</h4>
            <ul>
              {multiLoc.issues.map((issue, index) => (
                <li key={index}>{issue}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {multiLoc.recommendations && multiLoc.recommendations.length > 0 && (
          <div className="recommendations-section">
            <h4>✅ Recommendations</h4>
            <ul>
              {multiLoc.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <style jsx>{`
        .locations-table-container {
          margin: 30px 0;
          overflow-x: auto;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
        }

        .locations-table {
          width: 100%;
          border-collapse: collapse;
          font-size: 13px;
        }

        .locations-table th,
        .locations-table td {
          padding: 12px;
          text-align: left;
          border-bottom: 1px solid #e5e7eb;
        }

        .locations-table th {
          background-color: #f3f4f6;
          font-weight: 600;
          position: sticky;
          top: 0;
        }

        .location-name {
          font-weight: 600;
        }

        .region-badge {
          padding: 4px 8px;
          border-radius: 4px;
          color: white;
          font-size: 12px;
          font-weight: 600;
        }

        .status-badge {
          padding: 4px 8px;
          border-radius: 4px;
          color: white;
          font-size: 12px;
          font-weight: 600;
        }

        .status-pass {
          background-color: #10b981 !important;
        }

        .status-warn {
          background-color: #f59e0b !important;
        }

        .status-fail {
          background-color: #ef4444 !important;
        }

        .regional-summary {
          margin-top: 30px;
        }

        .region-cards {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 15px;
          margin-top: 15px;
        }

        .region-card {
          padding: 15px;
          background-color: #f9fafb;
          border-radius: 8px;
          border-left: 4px solid;
        }

        .region-header {
          font-weight: 700;
          font-size: 14px;
          margin-bottom: 10px;
        }

        .region-stat {
          display: flex;
          justify-content: space-between;
          font-size: 13px;
          margin-bottom: 8px;
        }

        .region-stat strong {
          color: #1f2937;
        }
      `}</style>
    </div>
  );
};

export default MultiLocationTab;
