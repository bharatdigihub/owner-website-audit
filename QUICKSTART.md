# Quick Start Guide

## Installation

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Start Backend Server

```bash
# From backend directory with venv activated
python run.py
```

Backend will start at: `http://localhost:5000`

### Start Frontend Development Server

Open a new terminal and run:

```bash
# From frontend directory
npm start
```

Frontend will open at: `http://localhost:3000`

## Testing the Application

1. Open your browser at `http://localhost:3000`
2. Enter a website URL (e.g., `https://example.com`)
3. Click "Analyze Website"
4. Wait for the analysis to complete
5. View detailed results in the dashboard

## File Structure

```
website-checker/
├── backend/                          # Python Flask API
│   ├── app/
│   │   ├── analyzers/               # Analysis modules
│   │   │   ├── performance.py       # Performance metrics
│   │   │   ├── security.py          # Security checks
│   │   │   ├── seo.py               # SEO analysis
│   │   │   ├── code_standards.py    # Code quality
│   │   │   ├── user_friendliness.py # UX analysis
│   │   │   └── user_behavior.py     # User journey
│   │   ├── utils/
│   │   │   └── validator.py         # URL validation
│   │   ├── routes.py                # API endpoints
│   │   └── __init__.py              # App factory
│   ├── run.py                       # Start server
│   ├── requirements.txt
│   └── .env                         # Config
│
└── frontend/                         # React UI
    ├── src/
    │   ├── components/
    │   │   ├── tabs/                # Analysis views
    │   │   ├── common/              # Shared components
    │   │   ├── Dashboard.js
    │   │   ├── AnalysisForm.js
    │   │   └── Header.js
    │   ├── App.js                   # Main component
    │   └── index.js
    ├── public/
    ├── package.json
    └── .env                         # Config
```

## API Endpoints

### Analyze Website
```bash
POST /api/analyze
Body: { "url": "https://example.com" }
```

### Specific Analysis
```bash
POST /api/analyze/performance
POST /api/analyze/security
POST /api/analyze/seo
POST /api/analyze/code-standards
POST /api/analyze/user-friendliness
```

### Health Check
```bash
GET /api/health
```

## Response Format

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

## Scoring System

- **A (90-100)**: Excellent
- **B (80-89)**: Good
- **C (70-79)**: Fair
- **D (60-69)**: Poor
- **F (0-59)**: Needs Improvement

## Troubleshooting

### CORS Errors
- Ensure both servers are running
- Check that frontend .env has correct API_URL
- Verify CORS_ORIGINS in backend .env

### Module Not Found
- Ensure all packages are installed
- Verify Python is using the correct virtual environment

### Connection Refused
- Check if ports 5000 and 3000 are available
- Restart the servers if needed

## Next Steps

1. Analyze your first website
2. Review the analysis results
3. Check recommendations for improvements
4. Compare multiple websites
5. Explore detailed metrics per category

## Production Deployment

For production deployment:

1. Update environment variables
2. Set `FLASK_ENV=production`
3. Build React: `npm run build`
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Enable HTTPS
6. Set up proper database if needed

---

For more information, see [README.md](../README.md)
