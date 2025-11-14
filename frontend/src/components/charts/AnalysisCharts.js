import React from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './AnalysisCharts.css';

function ScoreDistributionChart({ data }) {
  const chartData = [
    { name: 'Performance', score: data.performance?.score || 0 },
    { name: 'Security', score: data.security?.score || 0 },
    { name: 'SEO', score: data.seo?.score || 0 },
    { name: 'Code Standards', score: data.coding_standards?.score || 0 },
    { name: 'User-Friendliness', score: data.user_friendliness?.score || 0 },
    { name: 'User Behavior', score: data.user_behavior?.score || 0 },
    { name: 'Mobile', score: data.mobile_optimization?.score || 0 },
    { name: 'Accessibility', score: data.accessibility?.score || 0 },
    { name: 'Advanced', score: data.advanced_metrics?.score || 0 },
  ];

  return (
    <div className="chart-container">
      <h3>📊 Overall Score Distribution</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-45} textAnchor="end" height={120} />
          <YAxis domain={[0, 100]} />
          <Tooltip 
            formatter={(value) => `${value}%`}
            contentStyle={{ backgroundColor: '#f9f9f9', border: '1px solid #e0e0e0' }}
          />
          <Bar dataKey="score" fill="#667eea" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function RadarScoreChart({ data }) {
  const chartData = [
    { category: 'Performance', score: data.performance?.score || 0 },
    { category: 'Security', score: data.security?.score || 0 },
    { category: 'SEO', score: data.seo?.score || 0 },
    { category: 'Code Quality', score: data.coding_standards?.score || 0 },
    { category: 'UX', score: data.user_friendliness?.score || 0 },
    { category: 'Behavior', score: data.user_behavior?.score || 0 },
    { category: 'Mobile', score: data.mobile_optimization?.score || 0 },
    { category: 'Accessibility', score: data.accessibility?.score || 0 },
  ];

  return (
    <div className="chart-container">
      <h3>🎯 Score Radar Chart</h3>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={chartData}>
          <PolarGrid stroke="#e0e0e0" />
          <PolarAngleAxis dataKey="category" />
          <PolarRadiusAxis domain={[0, 100]} />
          <Radar name="Score" dataKey="score" stroke="#667eea" fill="#667eea" fillOpacity={0.6} />
          <Tooltip 
            formatter={(value) => `${value}%`}
            contentStyle={{ backgroundColor: '#f9f9f9', border: '1px solid #e0e0e0' }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

function GradeDistributionChart({ data }) {
  const categories = [
    { name: 'Performance', grade: data.performance?.grade || 'F' },
    { name: 'Security', grade: data.security?.grade || 'F' },
    { name: 'SEO', grade: data.seo?.grade || 'F' },
    { name: 'Code Standards', grade: data.coding_standards?.grade || 'F' },
    { name: 'User-Friendliness', grade: data.user_friendliness?.grade || 'F' },
    { name: 'User Behavior', grade: data.user_behavior?.grade || 'F' },
    { name: 'Mobile', grade: data.mobile_optimization?.grade || 'F' },
    { name: 'Accessibility', grade: data.accessibility?.grade || 'F' },
  ];

  // Count grades
  const gradeCounts = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0,
    'F': 0,
  };

  categories.forEach(cat => {
    gradeCounts[cat.grade]++;
  });

  const pieData = [
    { name: 'A', value: gradeCounts.A, color: '#28a745' },
    { name: 'B', value: gradeCounts.B, color: '#17a2b8' },
    { name: 'C', value: gradeCounts.C, color: '#ffc107' },
    { name: 'D', value: gradeCounts.D, color: '#fd7e14' },
    { name: 'F', value: gradeCounts.F, color: '#dc3545' },
  ].filter(item => item.value > 0);

  return (
    <div className="chart-container">
      <h3>📈 Grade Distribution</h3>
      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={pieData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, value, percent }) => `${name}: ${value} (${(percent * 100).toFixed(0)}%)`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {pieData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip 
            formatter={(value) => `${value}`}
            contentStyle={{ backgroundColor: '#f9f9f9', border: '1px solid #e0e0e0' }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

function IssuesVsSeverityChart({ data }) {
  // Collect all issues from all categories
  const allIssues = [
    ...(data.performance?.issues || []),
    ...(data.security?.issues || []),
    ...(data.seo?.issues || []),
    ...(data.coding_standards?.issues || []),
    ...(data.user_friendliness?.issues || []),
    ...(data.user_behavior?.issues || []),
    ...(data.mobile_optimization?.issues || []),
    ...(data.accessibility?.issues || []),
    ...(data.advanced_metrics?.issues || []),
  ];

  const severityCounts = {
    'critical': 0,
    'high': 0,
    'medium': 0,
    'low': 0,
  };

  allIssues.forEach(issue => {
    const severity = issue.severity || 'medium';
    if (severity in severityCounts) {
      severityCounts[severity]++;
    }
  });

  const chartData = [
    { severity: 'Critical', count: severityCounts.critical, fill: '#dc3545' },
    { severity: 'High', count: severityCounts.high, fill: '#fd7e14' },
    { severity: 'Medium', count: severityCounts.medium, fill: '#ffc107' },
    { severity: 'Low', count: severityCounts.low, fill: '#28a745' },
  ];

  return (
    <div className="chart-container">
      <h3>⚠️ Issues by Severity</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} layout="vertical" margin={{ top: 20, right: 30, left: 120, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis dataKey="severity" type="category" width={100} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#f9f9f9', border: '1px solid #e0e0e0' }}
          />
          <Bar dataKey="count" fill="#667eea" radius={[0, 8, 8, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export { ScoreDistributionChart, RadarScoreChart, GradeDistributionChart, IssuesVsSeverityChart };
