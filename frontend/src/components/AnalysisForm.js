import React, { useState } from 'react';
import './AnalysisForm.css';

function AnalysisForm({ onAnalyze, loading, error }) {
  const [url, setUrl] = useState('');
  const [formFactor, setFormFactor] = useState('desktop');
  const [inputError, setInputError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setInputError('');

    if (!url.trim()) {
      setInputError('Please enter a website URL');
      return;
    }

    onAnalyze(url.trim(), formFactor);
  };

  return (
    <div className="analysis-form-container">
      <div className="form-card">
        <h2>Analyze Your Website</h2>
        <p className="form-description">
          Enter your website URL to get a comprehensive analysis covering performance, security, SEO, and more.
        </p>
        
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="url">Website URL</label>
            <input
              id="url"
              type="text"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => {
                setUrl(e.target.value);
                setInputError('');
              }}
              disabled={loading}
              className={inputError ? 'error' : ''}
            />
            {inputError && <span className="error-message">{inputError}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="formFactor">Analysis Type</label>
            <select
              id="formFactor"
              value={formFactor}
              onChange={(e) => setFormFactor(e.target.value)}
              disabled={loading}
              className="form-select"
            >
              <option value="desktop">Desktop</option>
              <option value="mobile">Mobile</option>
            </select>
          </div>

          {error && <div className="form-error">{error}</div>}

          <button 
            type="submit" 
            className="submit-btn"
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze Website'}
          </button>
        </form>

        <div className="features">
          <h3>Analysis Includes:</h3>
          <ul>
            <li>⚡ Performance Metrics</li>
            <li>🔒 Security Checks</li>
            <li>📱 Mobile Friendliness</li>
            <li>🔍 SEO Analysis</li>
            <li>📝 Code Standards</li>
            <li>👥 User Behavior Insights</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default AnalysisForm;
