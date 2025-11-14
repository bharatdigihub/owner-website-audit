import React from 'react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import './ReportGenerator.css';

function ReportGenerator({ data, url }) {
  const calculateOverallScore = () => {
    return Math.round((
      data.performance.score +
      data.security.score +
      data.seo.score +
      data.coding_standards.score +
      data.user_friendliness.score +
      data.user_behavior.score +
      data.mobile_optimization.score +
      data.accessibility.score +
      data.advanced_metrics.score
    ) / 9);
  };

  const exportToPDF = async () => {
    try {
      const element = document.getElementById('pdf-content');
      const canvas = await html2canvas(element, {
        backgroundColor: '#ffffff',
        scale: 2,
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageHeight = pdf.internal.pageSize.getHeight();
      const pageWidth = pdf.internal.pageSize.getWidth();
      const margin = 10;
      const maxWidth = pageWidth - 2 * margin;

      // Calculate image dimensions to fit page
      const imgWidth = maxWidth;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      let heightLeft = imgHeight;
      let position = 0;

      pdf.addImage(imgData, 'PNG', margin, position + margin, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', margin, position + margin, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      pdf.save(`website-analysis-${new Date().toISOString().split('T')[0]}.pdf`);
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Error generating PDF. Please try again.');
    }
  };

  const exportToJSON = () => {
    const jsonData = {
      url: url,
      timestamp: new Date().toISOString(),
      overallScore: calculateOverallScore(),
      analysisData: data,
    };

    const dataStr = JSON.stringify(jsonData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url_obj = URL.createObjectURL(dataBlob);

    const link = document.createElement('a');
    link.href = url_obj;
    link.download = `website-analysis-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url_obj);
  };

  const exportToCSV = () => {
    let csv = 'Category,Score,Grade\n';

    csv += `Performance,${data.performance.score},${data.performance.grade}\n`;
    csv += `Security,${data.security.score},${data.security.grade}\n`;
    csv += `SEO,${data.seo.score},${data.seo.grade}\n`;
    csv += `Code Standards,${data.coding_standards.score},${data.coding_standards.grade}\n`;
    csv += `User-Friendliness,${data.user_friendliness.score},${data.user_friendliness.grade}\n`;
    csv += `User Behavior,${data.user_behavior.score},${data.user_behavior.grade}\n`;
    csv += `Mobile Optimization,${data.mobile_optimization.score},${data.mobile_optimization.grade}\n`;
    csv += `Accessibility,${data.accessibility.score},${data.accessibility.grade}\n`;
    csv += `Advanced Metrics,${data.advanced_metrics.score},${data.advanced_metrics.grade}\n`;

    csv += '\n\nURL,' + url + '\n';
    csv += 'Timestamp,' + new Date().toISOString() + '\n';
    csv += 'Overall Score,' + calculateOverallScore() + '%\n';

    const csvBlob = new Blob([csv], { type: 'text/csv' });
    const url_obj = URL.createObjectURL(csvBlob);

    const link = document.createElement('a');
    link.href = url_obj;
    link.download = `website-analysis-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url_obj);
  };

  return (
    <div className="report-generator">
      <div className="export-buttons">
        <button className="btn btn-pdf" onClick={exportToPDF}>
          📄 Export as PDF
        </button>
        <button className="btn btn-json" onClick={exportToJSON}>
          { } Export as JSON
        </button>
        <button className="btn btn-csv" onClick={exportToCSV}>
          📊 Export as CSV
        </button>
      </div>

      <div id="pdf-content" className="pdf-content" style={{ display: 'none' }}>
        <div className="pdf-header">
          <h1>Website Analysis Report</h1>
          <p>{url}</p>
          <p>{new Date().toLocaleString()}</p>
        </div>

        <div className="pdf-overall">
          <h2>Overall Score: {calculateOverallScore()}%</h2>
        </div>

        <div className="pdf-section">
          <h3>Analysis Results</h3>
          <table>
            <thead>
              <tr>
                <th>Category</th>
                <th>Score</th>
                <th>Grade</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Performance</td>
                <td>{data.performance.score}%</td>
                <td>{data.performance.grade}</td>
              </tr>
              <tr>
                <td>Security</td>
                <td>{data.security.score}%</td>
                <td>{data.security.grade}</td>
              </tr>
              <tr>
                <td>SEO</td>
                <td>{data.seo.score}%</td>
                <td>{data.seo.grade}</td>
              </tr>
              <tr>
                <td>Code Standards</td>
                <td>{data.coding_standards.score}%</td>
                <td>{data.coding_standards.grade}</td>
              </tr>
              <tr>
                <td>User-Friendliness</td>
                <td>{data.user_friendliness.score}%</td>
                <td>{data.user_friendliness.grade}</td>
              </tr>
              <tr>
                <td>User Behavior</td>
                <td>{data.user_behavior.score}%</td>
                <td>{data.user_behavior.grade}</td>
              </tr>
              <tr>
                <td>Mobile Optimization</td>
                <td>{data.mobile_optimization.score}%</td>
                <td>{data.mobile_optimization.grade}</td>
              </tr>
              <tr>
                <td>Accessibility</td>
                <td>{data.accessibility.score}%</td>
                <td>{data.accessibility.grade}</td>
              </tr>
              <tr>
                <td>Advanced Metrics</td>
                <td>{data.advanced_metrics.score}%</td>
                <td>{data.advanced_metrics.grade}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default ReportGenerator;
