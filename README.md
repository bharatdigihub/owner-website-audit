# Website Analyzer

A comprehensive web application that analyzes websites and provides detailed insights into performance, security, SEO, code standards, user experience, and user behavior.

## Overview

Website Analyzer is a full-stack application built with:
- **Backend**: Python Flask API
- **Frontend**: React Dashboard

The application analyzes websites across seven major categories:

### Analysis Categories

1. **Performance** ⚡
   - Page load times
   - Image optimization
   - Render-blocking resources
   - Minification status
   - Caching headers
   - Lazy loading implementation

2. **Security** 🔒
   - SSL/TLS certificate validation
   - Security headers (HSTS, CSP, X-Frame-Options, etc.)
   - Mixed content detection
   - Vulnerability detection
   - Framework exposure

3. **SEO** 🔍
   - Meta tags (title, description, keywords)
   - Heading structure
   - Alt text on images
   - URL friendliness
   - Broken links detection
   - Robots.txt and sitemap presence

4. **Code Standards** 📝
   - HTML best practices
   - CSS standards
   - JavaScript optimization
   - Semantic HTML usage
   - Deprecated tags detection

5. **User-Friendliness** 😊
   - Accessibility (WCAG compliance)
   - Navigation quality
   - Content readability
   - Interactive elements
   - Breadcrumb navigation

6. **User Behavior** 👥
   - Common user journey paths
   - Content element analysis
   - Interaction potential scoring
   - Time-on-page factors

7. **Mobile Optimization** 📱
   - Responsive design checking
   - Mobile performance metrics
   - Touch-friendly elements
   - Viewport configuration

8. **Accessibility** ♿
   - WCAG compliance
   - Color contrast checking
   - Semantic HTML usage
   - Screen reader compatibility

9. **Advanced Metrics** 📊
   - Core Web Vitals (LCP, FID, CLS)
   - Waterfall chart analysis
   - Multi-location performance
   - Device simulation

### 🤖 AI-Powered Support System

The analyzer now includes an intelligent support assistant that:
- **Generates custom tutorials** for each detected issue using Google Gemini AI
- **Prioritizes issues** by severity and impact
- **Identifies quick wins** - issues fixable in under 5 minutes
- **Estimates fix time** - how long it will take to resolve all issues
- **Provides step-by-step solutions** with code examples and best practices
- **Works offline** - fallback to local knowledge base when API unavailable

**Get started:** See [AI_SUPPORT_SETUP.md](./AI_SUPPORT_SETUP.md) for configuration

## Project Structure

```
website-checker/
├── backend/
│   ├── app/
│   │   ├── analyzers/
│   │   │   ├── base.py
│   │   │   ├── performance.py
│   │   │   ├── security.py
│   │   │   ├── seo.py
│   │   │   ├── code_standards.py
│   │   │   ├── user_friendliness.py
│   │   │   ├── user_behavior.py
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   ├── validator.py
│   │   │   └── __init__.py
│   │   ├── routes.py
│   │   └── __init__.py
│   ├── run.py
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── tabs/
    │   │   ├── common/
    │   │   ├── Header.js
    │   │   ├── Dashboard.js
    │   │   ├── AnalysisForm.js
    │   │   └── ...
    │   ├── App.js
    │   ├── index.js
    │   └── ...
    ├── public/
    ├── package.json
    └── .env
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   # Edit .env file with your settings
   ```

5. Run the Flask server:
   ```bash
   python run.py
   ```

The backend API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Main Analysis Endpoint
- **POST** `/api/analyze` - Analyze a website
  - Request: `{ "url": "https://example.com" }`
  - Response: Comprehensive analysis object

### Category-Specific Endpoints
- **POST** `/api/analyze/performance` - Performance analysis only
- **POST** `/api/analyze/security` - Security analysis only
- **POST** `/api/analyze/seo` - SEO analysis only
- **POST** `/api/analyze/code-standards` - Code standards analysis only
- **POST** `/api/analyze/user-friendliness` - User experience analysis only

### AI Support Endpoints (🤖 New!)
- **POST** `/api/support/tutorials` - Get AI-generated tutorials for issues
- **POST** `/api/support/analytics` - Get issue analytics and priorities
- **POST** `/api/support/quick-fix` - Get quick fix for a specific issue

### Health Check
- **GET** `/api/health` - API health status

## Analysis Output

Each analysis returns a comprehensive report with:

```json
{
  "url": "https://example.com",
  "performance": {
    "score": 85,
    "grade": "B",
    "metrics": {...},
    "issues": [...],
    "recommendations": [...]
  },
  "security": {...},
  "seo": {...},
  "coding_standards": {...},
  "user_friendliness": {...},
  "user_behavior": {...}
}
```

## Features

- ✅ **Real-time Analysis** - Instant website scanning and reporting
- ✅ **Interactive Dashboard** - Beautiful, responsive UI with detailed breakdowns
- ✅ **Multi-Category Analysis** - Comprehensive coverage of all important aspects
- ✅ **Actionable Insights** - Clear recommendations for improvement
- ✅ **Performance Scoring** - Grade-based scoring system (A-F)
- ✅ **Issue Severity Levels** - Critical, High, Medium, Low categorization
- ✅ **Responsive Design** - Works on desktop and mobile devices
- ✅ **AI-Powered Support** - Intelligent tutorial generation for issue fixes
- ✅ **Quick Win Identification** - 5-minute fixes prioritized
- ✅ **Issue Analytics** - Prioritized fix recommendations with time estimates
- ✅ **GTmetrix-like Features** - Waterfall charts, Core Web Vitals, multi-location testing
- ✅ **Device Simulation** - Test across 8+ device types and networks
- ✅ **Desktop & Mobile Analysis** - Separate testing for each form factor
- ✅ **Export Reports** - PDF, CSV, JSON export formats

## Technologies

### Backend
- Flask 3.0.0
- BeautifulSoup4 4.12.2
- Requests 2.31.0
- Python-dotenv 1.0.0

### Frontend
- React 18.2.0
- Axios 1.6.0
- Chart.js 4.4.0
- CSS3 with Flexbox and Grid

## Configuration

### Backend (.env)
```
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=app:create_app
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
SECRET_KEY=your-secret-key-change-in-production
FLASK_PORT=5000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Development

### Running in Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Building for Production

**Backend:**
```bash
# Set appropriate environment variables
export FLASK_ENV=production
python run.py
```

**Frontend:**
```bash
npm run build
```

## Performance Considerations

- Websites with large amounts of content may take longer to analyze
- Network requests are parallelized for efficiency
- Caching can be implemented for frequently analyzed websites
- Consider rate limiting in production

## Future Enhancements

- [ ] Database integration for storing analysis history
- [ ] User authentication and accounts
- [ ] Comparison reports for multiple analyses
- [ ] Scheduled website monitoring
- [ ] Advanced visualization with charts
- [ ] Export reports (PDF, CSV)
- [ ] Integration with third-party services
- [ ] Mobile app version
- [ ] API rate limiting and throttling
- [ ] Detailed audit logs

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure both backend and frontend are running and CORS_ORIGINS includes the frontend URL
2. **Network Errors**: Check that the API URL in frontend .env matches the backend server
3. **Analysis Failures**: Some websites may have restrictions on automated access
4. **Performance**: Large websites may take longer to analyze

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Support

For support, issues, or questions, please create an issue in the repository.

---

**Happy Analyzing! 🚀**
