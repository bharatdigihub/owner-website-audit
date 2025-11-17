import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import './PerformanceTab.css';

const CoreWebVitalsTab = ({ data }) => {
  if (!data) return <div className="tab-content">No Core Web Vitals data available</div>;

  const cwv = data.core_web_vitals || {};
  const metrics = cwv.metrics || {};

  // Helper to get color based on status
  const getStatusColor = (status) => {
    if (status === 'Good') return '#10b981';
    if (status === 'Needs Improvement') return '#f59e0b';
    return '#ef4444';
  };

  // Prepare chart data
  const chartData = [
    {
      name: 'LCP',
      value: metrics.lcp?.value || 0,
      unit: 'ms',
      status: metrics.lcp?.status || 'Unknown'
    },
    {
      name: 'FID',
      value: metrics.fid?.value || 0,
      unit: 'ms',
      status: metrics.fid?.status || 'Unknown'
    },
    {
      name: 'INP',
      value: metrics.inp?.value || 0,
      unit: 'ms',
      status: metrics.inp?.status || 'Unknown'
    }
  ];

  const clsData = [
    {
      name: 'CLS Score',
      value: (metrics.cls?.value || 0) * 100,
      status: metrics.cls?.status || 'Unknown'
    }
  ];

  return (
    <div className="tab-content">
      <div className="section">
        <h3>Core Web Vitals Metrics</h3>
        <p className="description">
          Core Web Vitals are essential metrics that measure user experience. Google uses these to rank pages.
        </p>

        {/* Score Card */}
        <div className="score-card">
          <div className="score-number">{cwv.score || 0}</div>
          <div className="score-label">Overall CWV Score</div>
          <div className={`score-grade grade-${cwv.grade || 'F'}`}>{cwv.grade || 'F'}</div>
        </div>

        {/* Metrics Display */}
        <div className="metrics-grid">
          {/* LCP */}
          <div className="metric-box">
            <div className="metric-header">
              <h4>LCP (Largest Contentful Paint)</h4>
              <span className={`badge ${metrics.lcp?.status?.replace(' ', '-').toLowerCase()}`}>
                {metrics.lcp?.status}
              </span>
            </div>
            <div className="metric-value">{metrics.lcp?.value || 0} ms</div>
            <div className="metric-info">
              <small>Target: &lt; {metrics.lcp?.threshold_good} ms (Good)</small>
              <small>Poor: &gt; {metrics.lcp?.threshold_poor} ms</small>
            </div>
            <div className="metric-description">{metrics.lcp?.description}</div>
          </div>

          {/* FID */}
          <div className="metric-box">
            <div className="metric-header">
              <h4>FID (First Input Delay)</h4>
              <span className={`badge ${metrics.fid?.status?.replace(' ', '-').toLowerCase()}`}>
                {metrics.fid?.status}
              </span>
            </div>
            <div className="metric-value">{metrics.fid?.value || 0} ms</div>
            <div className="metric-info">
              <small>Target: &lt; {metrics.fid?.threshold_good} ms (Good)</small>
              <small>Poor: &gt; {metrics.fid?.threshold_poor} ms</small>
            </div>
            <div className="metric-description">{metrics.fid?.description}</div>
          </div>

          {/* CLS */}
          <div className="metric-box">
            <div className="metric-header">
              <h4>CLS (Cumulative Layout Shift)</h4>
              <span className={`badge ${metrics.cls?.status?.replace(' ', '-').toLowerCase()}`}>
                {metrics.cls?.status}
              </span>
            </div>
            <div className="metric-value">{metrics.cls?.value || 0}</div>
            <div className="metric-info">
              <small>Target: &lt; {metrics.cls?.threshold_good} (Good)</small>
              <small>Poor: &gt; {metrics.cls?.threshold_poor}</small>
            </div>
            <div className="metric-description">{metrics.cls?.description}</div>
          </div>

          {/* INP */}
          <div className="metric-box">
            <div className="metric-header">
              <h4>INP (Interaction to Next Paint)</h4>
              <span className={`badge good`}>
                Good
              </span>
            </div>
            <div className="metric-value">{metrics.inp?.value || 0} ms</div>
            <div className="metric-info">
              <small>Target: &lt; {metrics.inp?.threshold_good} ms (Good)</small>
              <small>Replaces FID in future versions</small>
            </div>
            <div className="metric-description">{metrics.inp?.description}</div>
          </div>
        </div>

        {/* Charts */}
        <div className="chart-container">
          <h4>Performance Comparison</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis label={{ value: 'Milliseconds', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getStatusColor(entry.status)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Issues */}
        {cwv.issues && cwv.issues.length > 0 && (
          <div className="issues-section">
            <h4>⚠️ Issues Found</h4>
            <ul>
              {cwv.issues.map((issue, index) => (
                <li key={index}>{issue}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {cwv.recommendations && cwv.recommendations.length > 0 && (
          <div className="recommendations-section">
            <h4>✅ Recommendations</h4>
            <ul>
              {cwv.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default CoreWebVitalsTab;
