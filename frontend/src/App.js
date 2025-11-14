import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import AnalysisForm from './components/AnalysisForm';
import Dashboard from './components/Dashboard';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentUrl, setCurrentUrl] = useState('');

  const handleAnalyze = async (url) => {
    setLoading(true);
    setError(null);
    setCurrentUrl(url);
    
    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
      const response = await fetch(`${apiUrl}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Analysis failed');
      }

      const data = await response.json();
      setAnalysisData(data);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNewAnalysis = () => {
    setAnalysisData(null);
    setCurrentUrl('');
    setError(null);
  };

  return (
    <div className="App">
      <Header />
      <main className="main-container">
        {!analysisData ? (
          <>
            <AnalysisForm onAnalyze={handleAnalyze} loading={loading} error={error} />
            {loading && <LoadingSpinner />}
          </>
        ) : (
          <Dashboard data={analysisData} url={currentUrl} onNewAnalysis={handleNewAnalysis} />
        )}
      </main>
    </div>
  );
}

export default App;
