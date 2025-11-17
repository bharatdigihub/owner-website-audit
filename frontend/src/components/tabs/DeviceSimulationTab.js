import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import './PerformanceTab.css';

const DeviceSimulationTab = ({ data }) => {
  const [selectedCategory, setSelectedCategory] = useState('all');

  if (!data) return <div className="tab-content">No device simulation data available</div>;

  const deviceSim = data.device_simulation || {};
  const devices = deviceSim.devices || [];
  const metrics = deviceSim.metrics || {};

  // Filter devices by category
  const filteredDevices = selectedCategory === 'all'
    ? devices
    : devices.filter(d => d.category === selectedCategory);

  // Prepare chart data
  const chartData = filteredDevices.map(device => ({
    name: device.device_name.split(' - ')[0],
    time: device.page_load_time_ms,
    category: device.category
  }));

  const getStatusColor = (status) => {
    if (status === 'Pass') return '#10b981';
    if (status === 'Warn') return '#f59e0b';
    return '#ef4444';
  };

  const getCategoryIcon = (category) => {
    const icons = {
      desktop: '🖥️',
      laptop: '💻',
      tablet: '📱',
      mobile: '📱'
    };
    return icons[category] || '?';
  };

  return (
    <div className="tab-content">
      <div className="section">
        <h3>Device Simulation & Testing</h3>
        <p className="description">
          Test your website across different devices, screen sizes, and network conditions to ensure optimal performance everywhere.
        </p>

        {/* Score Card */}
        <div className="score-card">
          <div className="score-number">{deviceSim.score || 0}</div>
          <div className="score-label">Cross-Device Performance</div>
          <div className={`score-grade grade-${deviceSim.grade || 'F'}`}>{deviceSim.grade || 'F'}</div>
        </div>

        {/* Metrics Summary */}
        <div className="metrics-grid">
          <div className="metric-box">
            <div className="metric-label">Mobile Avg Load</div>
            <div className="metric-value">{metrics.average_mobile_load_time_ms} ms</div>
          </div>
          <div className="metric-box">
            <div className="metric-label">Desktop Avg Load</div>
            <div className="metric-value">{metrics.average_desktop_load_time_ms} ms</div>
          </div>
          <div className="metric-box">
            <div className="metric-label">Mobile Pass Rate</div>
            <div className="metric-value">{metrics.mobile_pass_rate}</div>
          </div>
          <div className="metric-box">
            <div className="metric-label">Responsive Design</div>
            <div className="metric-value">{metrics.responsive_design ? '✓ Yes' : '✗ No'}</div>
          </div>
        </div>

        {/* Category Filter */}
        <div className="category-filter">
          <button
            className={`filter-btn ${selectedCategory === 'all' ? 'active' : ''}`}
            onClick={() => setSelectedCategory('all')}
          >
            All Devices
          </button>
          <button
            className={`filter-btn ${selectedCategory === 'mobile' ? 'active' : ''}`}
            onClick={() => setSelectedCategory('mobile')}
          >
            📱 Mobile
          </button>
          <button
            className={`filter-btn ${selectedCategory === 'tablet' ? 'active' : ''}`}
            onClick={() => setSelectedCategory('tablet')}
          >
            📱 Tablet
          </button>
          <button
            className={`filter-btn ${selectedCategory === 'desktop' ? 'active' : ''}`}
            onClick={() => setSelectedCategory('desktop')}
          >
            🖥️ Desktop
          </button>
          <button
            className={`filter-btn ${selectedCategory === 'laptop' ? 'active' : ''}`}
            onClick={() => setSelectedCategory('laptop')}
          >
            💻 Laptop
          </button>
        </div>

        {/* Performance Chart */}
        <div className="chart-container">
          <h4>Load Times by Device</h4>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} interval={0} />
              <YAxis label={{ value: 'Load Time (ms)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="time" radius={[8, 8, 0, 0]}>
                {chartData.map((entry, index) => {
                  const device = filteredDevices[index];
                  return (
                    <Cell key={`cell-${index}`} fill={getStatusColor(device.status)} />
                  );
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Devices Table */}
        <div className="devices-table-container">
          <h4>Detailed Results by Device</h4>
          <table className="devices-table">
            <thead>
              <tr>
                <th>Device</th>
                <th>Viewport</th>
                <th>Network</th>
                <th>Load Time</th>
                <th>FCP</th>
                <th>LCP</th>
                <th>TTI</th>
                <th>Mobile Friendly</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredDevices.map((device, index) => (
                <tr key={index}>
                  <td className="device-name">
                    <span>{getCategoryIcon(device.category)}</span>
                    <strong>{device.device_name}</strong>
                  </td>
                  <td className="viewport">{device.viewport}</td>
                  <td>{device.network}</td>
                  <td>
                    <strong>{device.page_load_time_ms} ms</strong>
                  </td>
                  <td>{device.fcp_ms} ms</td>
                  <td>{device.lcp_ms} ms</td>
                  <td>{device.tti_ms} ms</td>
                  <td>
                    {device.mobile_friendly ? (
                      <span className="check">✓</span>
                    ) : (
                      <span className="cross">✗</span>
                    )}
                  </td>
                  <td>
                    <span
                      className={`status-badge status-${device.status.toLowerCase()}`}
                      style={{ backgroundColor: getStatusColor(device.status) }}
                    >
                      {device.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Device Categories Summary */}
        <div className="device-categories">
          <h4>Performance by Device Category</h4>
          <div className="category-cards">
            {[
              { name: 'Mobile', type: 'mobile', icon: '📱' },
              { name: 'Tablet', type: 'tablet', icon: '📱' },
              { name: 'Desktop', type: 'desktop', icon: '🖥️' },
              { name: 'Laptop', type: 'laptop', icon: '💻' }
            ].map(cat => {
              const catDevices = devices.filter(d => d.category === cat.type);
              const avgTime = catDevices.length > 0
                ? Math.round(catDevices.reduce((sum, d) => sum + d.page_load_time_ms, 0) / catDevices.length)
                : 'N/A';
              const passCount = catDevices.filter(d => d.status === 'Pass').length;
              
              return (
                <div key={cat.type} className="category-card">
                  <div className="category-icon">{cat.icon}</div>
                  <div className="category-name">{cat.name}</div>
                  <div className="category-stat">
                    <span>Avg Load:</span>
                    <strong>{avgTime} ms</strong>
                  </div>
                  <div className="category-stat">
                    <span>Devices:</span>
                    <strong>{catDevices.length}</strong>
                  </div>
                  <div className="category-stat">
                    <span>Pass Rate:</span>
                    <strong>
                      {catDevices.length > 0 ? Math.round((passCount / catDevices.length) * 100) : 0}%
                    </strong>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Mobile Optimization */}
        <div className="mobile-optimization-section">
          <h4>Mobile Optimization Status</h4>
          <div className="optimization-items">
            <div className={`optimization-item ${metrics.responsive_design ? 'pass' : 'fail'}`}>
              <span className="item-icon">{metrics.responsive_design ? '✓' : '✗'}</span>
              <span className="item-text">Responsive Design Detected</span>
            </div>
            <div className={`optimization-item ${metrics.mobile_friendly ? 'pass' : 'fail'}`}>
              <span className="item-icon">{metrics.mobile_friendly ? '✓' : '✗'}</span>
              <span className="item-text">Mobile Friendly</span>
            </div>
          </div>
        </div>

        {/* Issues */}
        {deviceSim.issues && deviceSim.issues.length > 0 && (
          <div className="issues-section">
            <h4>⚠️ Issues Found</h4>
            <ul>
              {deviceSim.issues.map((issue, index) => (
                <li key={index}>{issue}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {deviceSim.recommendations && deviceSim.recommendations.length > 0 && (
          <div className="recommendations-section">
            <h4>✅ Recommendations</h4>
            <ul>
              {deviceSim.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <style jsx>{`
        .category-filter {
          display: flex;
          gap: 10px;
          margin: 20px 0;
          flex-wrap: wrap;
        }

        .filter-btn {
          padding: 8px 16px;
          border: 2px solid #d1d5db;
          background-color: white;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 500;
          transition: all 0.3s;
        }

        .filter-btn:hover {
          border-color: #3b82f6;
          color: #3b82f6;
        }

        .filter-btn.active {
          background-color: #3b82f6;
          color: white;
          border-color: #3b82f6;
        }

        .devices-table-container {
          margin: 30px 0;
          overflow-x: auto;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
        }

        .devices-table {
          width: 100%;
          border-collapse: collapse;
          font-size: 13px;
        }

        .devices-table th,
        .devices-table td {
          padding: 12px;
          text-align: left;
          border-bottom: 1px solid #e5e7eb;
        }

        .devices-table th {
          background-color: #f3f4f6;
          font-weight: 600;
          position: sticky;
          top: 0;
        }

        .device-name {
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 600;
        }

        .viewport {
          font-family: monospace;
          font-size: 12px;
        }

        .status-badge {
          padding: 4px 8px;
          border-radius: 4px;
          color: white;
          font-size: 12px;
          font-weight: 600;
        }

        .check {
          color: #10b981;
          font-weight: bold;
        }

        .cross {
          color: #ef4444;
          font-weight: bold;
        }

        .device-categories {
          margin-top: 30px;
        }

        .category-cards {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 15px;
          margin-top: 15px;
        }

        .category-card {
          padding: 15px;
          background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
          border-radius: 8px;
          text-align: center;
          border: 2px solid #d1d5db;
        }

        .category-icon {
          font-size: 32px;
          margin-bottom: 10px;
        }

        .category-name {
          font-weight: 700;
          margin-bottom: 10px;
        }

        .category-stat {
          display: flex;
          justify-content: space-between;
          font-size: 12px;
          margin-bottom: 6px;
        }

        .category-stat strong {
          color: #1f2937;
          font-weight: 600;
        }

        .mobile-optimization-section {
          margin-top: 30px;
          padding: 20px;
          background-color: #f0fdf4;
          border-radius: 8px;
          border-left: 4px solid #10b981;
        }

        .optimization-items {
          display: flex;
          gap: 20px;
          margin-top: 15px;
          flex-wrap: wrap;
        }

        .optimization-item {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px;
          background-color: white;
          border-radius: 6px;
          flex: 1;
          min-width: 200px;
        }

        .optimization-item.pass {
          border-left: 4px solid #10b981;
        }

        .optimization-item.fail {
          border-left: 4px solid #ef4444;
          background-color: #fef2f2;
        }

        .item-icon {
          font-weight: bold;
          font-size: 18px;
        }

        .optimization-item.pass .item-icon {
          color: #10b981;
        }

        .optimization-item.fail .item-icon {
          color: #ef4444;
        }

        .item-text {
          font-weight: 500;
        }
      `}</style>
    </div>
  );
};

export default DeviceSimulationTab;
