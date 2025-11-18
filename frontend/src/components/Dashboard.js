import React, { useState } from 'react';
import './Dashboard.css';
import ScoreCard from './ScoreCard';
import TabNav from './TabNav';
import PerformanceTab from './tabs/PerformanceTab';
import SecurityTab from './tabs/SecurityTab';
import SEOTab from './tabs/SEOTab';
import CodeStandardsTab from './tabs/CodeStandardsTab';
import UserFriendlinessTab from './tabs/UserFriendlinessTab';
import UserBehaviorTab from './tabs/UserBehaviorTab';
import MobileOptimizationTab from './tabs/MobileOptimizationTab';
import AccessibilityTab from './tabs/AccessibilityTab';
import AdvancedMetricsTab from './tabs/AdvancedMetricsTab';
import CoreWebVitalsTab from './tabs/CoreWebVitalsTab';
import WaterfallTab from './tabs/WaterfallTab';
import MultiLocationTab from './tabs/MultiLocationTab';
import DeviceSimulationTab from './tabs/DeviceSimulationTab';
import SupportPanel from './SupportPanel';
import ReportGenerator from './ReportGenerator';
import { ScoreDistributionChart, RadarScoreChart, GradeDistributionChart, IssuesVsSeverityChart } from './charts/AnalysisCharts';

function Dashboard({ data, url, onNewAnalysis }) {
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'performance', label: 'Performance' },
    { id: 'security', label: 'Security' },
    { id: 'seo', label: 'SEO' },
    { id: 'code', label: 'Code Standards' },
    { id: 'friendliness', label: 'User Experience' },
    { id: 'behavior', label: 'User Behavior' },
    { id: 'mobile', label: 'Mobile' },
    { id: 'accessibility', label: 'Accessibility' },
    { id: 'advanced', label: 'Advanced' },
    { id: 'cwv', label: 'Core Web Vitals' },
    { id: 'waterfall', label: 'Waterfall' },
    { id: 'location', label: 'Multi-Location' },
    { id: 'devices', label: 'Device Simulation' },
    { id: 'support', label: '💡 AI Support' },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'performance':
        return <PerformanceTab data={data.performance} />;
      case 'security':
        return <SecurityTab data={data.security} />;
      case 'seo':
        return <SEOTab data={data.seo} />;
      case 'code':
        return <CodeStandardsTab data={data.coding_standards} />;
      case 'friendliness':
        return <UserFriendlinessTab data={data.user_friendliness} />;
      case 'behavior':
        return <UserBehaviorTab data={data.user_behavior} />;
      case 'mobile':
        return <MobileOptimizationTab data={data.mobile_optimization} />;
      case 'accessibility':
        return <AccessibilityTab data={data.accessibility} />;
      case 'advanced':
        return <AdvancedMetricsTab data={data.advanced_metrics} />;
      case 'cwv':
        return <CoreWebVitalsTab data={data} />;
      case 'waterfall':
        return <WaterfallTab data={data} />;
      case 'location':
        return <MultiLocationTab data={data} />;
      case 'devices':
        return <DeviceSimulationTab data={data} />;
      case 'support':
        return <SupportPanel analysisData={data} />;
      default:
        return (
          <div className="overview-tab">
            <div className="overview-grid">
              <ScoreCard 
                title="Performance" 
                score={data.performance.score}
                grade={data.performance.grade}
                icon="⚡"
              />
              <ScoreCard 
                title="Security" 
                score={data.security.score}
                grade={data.security.grade}
                icon="🔒"
              />
              <ScoreCard 
                title="SEO" 
                score={data.seo.score}
                grade={data.seo.grade}
                icon="🔍"
              />
              <ScoreCard 
                title="Code Standards" 
                score={data.coding_standards.score}
                grade={data.coding_standards.grade}
                icon="📝"
              />
              <ScoreCard 
                title="User-Friendliness" 
                score={data.user_friendliness.score}
                grade={data.user_friendliness.grade}
                icon="😊"
              />
              <ScoreCard 
                title="User Behavior" 
                score={data.user_behavior.score}
                grade={data.user_behavior.grade}
                icon="👥"
              />
              <ScoreCard 
                title="Mobile" 
                score={data.mobile_optimization.score}
                grade={data.mobile_optimization.grade}
                icon="📱"
              />
              <ScoreCard 
                title="Accessibility" 
                score={data.accessibility.score}
                grade={data.accessibility.grade}
                icon="♿"
              />
              <ScoreCard 
                title="Advanced Metrics" 
                score={data.advanced_metrics.score}
                grade={data.advanced_metrics.grade}
                icon="📊"
              />
              <ScoreCard 
                title="Core Web Vitals" 
                score={data.core_web_vitals.score}
                grade={data.core_web_vitals.grade}
                icon="💨"
              />
              <ScoreCard 
                title="Waterfall" 
                score={data.waterfall.score}
                grade={data.waterfall.grade}
                icon="📈"
              />
              <ScoreCard 
                title="Multi-Location" 
                score={data.multi_location.score}
                grade={data.multi_location.grade}
                icon="🌍"
              />
              <ScoreCard 
                title="Device Simulation" 
                score={data.device_simulation.score}
                grade={data.device_simulation.grade}
                icon="📱"
              />
            </div>

            <div className="overall-score">
              <h3>Overall Score</h3>
              <div className="overall-score-value">
                {Math.round((
                  data.performance.score +
                  data.security.score +
                  data.seo.score +
                  data.coding_standards.score +
                  data.user_friendliness.score +
                  data.user_behavior.score +
                  data.mobile_optimization.score +
                  data.accessibility.score +
                  data.advanced_metrics.score +
                  data.core_web_vitals.score +
                  data.waterfall.score +
                  data.multi_location.score +
                  data.device_simulation.score
                ) / 13)}%
              </div>
            </div>

            <div className="charts-section">
              <h2 style={{ marginTop: '40px', marginBottom: '20px' }}>📊 Detailed Analytics</h2>
              <div className="charts-grid">
                <ScoreDistributionChart data={data} />
                <RadarScoreChart data={data} />
                <div className="chart-full-width">
                  <GradeDistributionChart data={data} />
                </div>
                <div className="chart-full-width">
                  <IssuesVsSeverityChart data={data} />
                </div>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="dashboard-title">
          <h2>Analysis Results {data.form_factor === 'mobile' ? '📱' : '🖥️'} ({data.form_factor ? data.form_factor.charAt(0).toUpperCase() + data.form_factor.slice(1) : 'Desktop'})</h2>
          <p className="analyzed-url">{url}</p>
        </div>
        <button className="new-analysis-btn" onClick={onNewAnalysis}>
          New Analysis
        </button>
      </div>

      <TabNav tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />

      <div className="dashboard-content">
        {renderTabContent()}
        <ReportGenerator data={data} url={url} />
      </div>
    </div>
  );
}

export default Dashboard;
