# Website Analyzer - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Website Analyzer System                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐                ┌──────────────────────┐
│   FRONTEND (React)   │                │  BACKEND (Flask)     │
│   Port: 3000         │◄───────────────►│  Port: 5000          │
├──────────────────────┤    HTTP/REST    ├──────────────────────┤
│                      │    JSON API     │                      │
│ • Dashboard UI       │                 │ • API Routes         │
│ • Score Cards        │                 │ • Analysis Engine    │
│ • Tab Navigation     │                 │ • 6 Analyzers       │
│ • Analysis Form      │                 │ • Data Processing    │
│ • Results Display    │                 │                      │
│                      │                 │ ┌────────────────┐   │
│ Components:          │                 │ │   Analyzers    │   │
│ ├─ Header           │                 │ ├────────────────┤   │
│ ├─ AnalysisForm     │                 │ │ Performance    │   │
│ ├─ Dashboard        │                 │ │ Security       │   │
│ ├─ ScoreCard        │                 │ │ SEO            │   │
│ ├─ TabNav           │                 │ │ Code Standards │   │
│ ├─ 6 Tab Pages      │                 │ │ User-Friendly  │   │
│ └─ Common Components │                 │ │ User Behavior  │   │
│                      │                 │ └────────────────┘   │
└──────────────────────┘                 └──────────────────────┘

                         ▼
            ┌────────────────────────┐
            │   HTML Parsing &       │
            │   Web Analysis         │
            │   (BeautifulSoup)      │
            └────────────────────────┘
                         ▼
            ┌────────────────────────┐
            │   Target Website       │
            │   (HTTPS/HTTP)         │
            └────────────────────────┘
```

## Data Flow Diagram

```
User Input (URL)
       ▼
┌─────────────────────┐
│  Frontend Form      │
│  Validation         │
└─────────────────────┘
       ▼
    POST /api/analyze
    Content-Type: application/json
    {"url": "https://example.com"}
       ▼
┌─────────────────────────────────────┐
│  Backend API Route Handler          │
│  1. Validate URL                    │
│  2. Start Analysis                  │
└─────────────────────────────────────┘
       ▼
    ┌──────────────────────────────────────┐
    │  Performance Analyzer               │
    │  ├─ Fetch website                   │
    │  ├─ Parse HTML                      │
    │  ├─ Check metrics                   │
    │  └─ Calculate score                 │
    └──────────────────────────────────────┘
    ┌──────────────────────────────────────┐
    │  Security Analyzer                   │
    │  ├─ Check SSL/TLS                    │
    │  ├─ Verify security headers          │
    │  └─ Scan vulnerabilities             │
    └──────────────────────────────────────┘
    ┌──────────────────────────────────────┐
    │  SEO Analyzer                        │
    │  ├─ Check meta tags                  │
    │  ├─ Verify headings                  │
    │  └─ Analyze links                    │
    └──────────────────────────────────────┘
    ┌──────────────────────────────────────┐
    │  Code Standards Analyzer             │
    │  ├─ Check HTML validity              │
    │  ├─ Verify CSS/JS practices          │
    │  └─ Detect semantic issues           │
    └──────────────────────────────────────┘
    ┌──────────────────────────────────────┐
    │  User-Friendliness Analyzer          │
    │  ├─ Check accessibility              │
    │  ├─ Evaluate navigation              │
    │  └─ Assess readability               │
    └──────────────────────────────────────┘
    ┌──────────────────────────────────────┐
    │  User Behavior Analyzer              │
    │  ├─ Identify user paths              │
    │  ├─ Analyze interactions             │
    │  └─ Calculate engagement             │
    └──────────────────────────────────────┘
       ▼
┌─────────────────────────────────────┐
│  Aggregate Results                  │
│  • Combine all scores               │
│  • Generate recommendations         │
│  • Format response                  │
└─────────────────────────────────────┘
       ▼
    JSON Response
    {
      "url": "...",
      "performance": {...},
      "security": {...},
      "seo": {...},
      "coding_standards": {...},
      "user_friendliness": {...},
      "user_behavior": {...}
    }
       ▼
┌─────────────────────────────┐
│  Frontend Receives Results  │
│  1. Parse JSON              │
│  2. Calculate overall score │
│  3. Render dashboard        │
└─────────────────────────────┘
       ▼
┌─────────────────────────────┐
│  Display to User            │
│  • Overview tab             │
│  • Detailed tabs            │
│  • Interactive UI           │
└─────────────────────────────┘
```

## Component Hierarchy (Frontend)

```
App
├── Header
├── AnalysisForm (OR Dashboard)
│   ├── LoadingSpinner
│   └── Error Display
└── Dashboard (when results available)
    ├── Dashboard Header
    │   ├── Title & URL
    │   └── New Analysis Button
    ├── TabNav
    │   ├── Overview Tab
    │   ├── Performance Tab
    │   ├── Security Tab
    │   ├── SEO Tab
    │   ├── Code Standards Tab
    │   ├── User-Friendliness Tab
    │   └── User Behavior Tab
    └── Tab Content
        ├── ScoreCard (multiple)
        ├── IssuesList
        ├── RecommendationsList
        └── Metrics Grid
```

## API Endpoint Hierarchy

```
/api
├── GET /health
│   └── {status: "healthy"}
│
└── POST /analyze (main endpoint)
│   ├── Requests individual analyzers
│   └── Returns complete analysis
│
├── POST /analyze/performance
├── POST /analyze/security
├── POST /analyze/seo
├── POST /analyze/code-standards
├── POST /analyze/user-friendliness
└── POST /analyze/user-behavior
```

## Analysis Process Flow

```
Each Analyzer:

1. Initialize
   ├─ Fetch webpage
   ├─ Parse HTML
   └─ Create BeautifulSoup object

2. Analyze
   ├─ Run specific checks
   ├─ Detect issues
   ├─ Collect metrics
   └─ Identify problems

3. Score
   ├─ Count issues
   ├─ Calculate percentage
   └─ Convert to grade (A-F)

4. Recommend
   ├─ Map issues to solutions
   ├─ Generate actionable advice
   └─ Prioritize recommendations

5. Return
   └─ {
        "score": number,
        "grade": "A-F",
        "metrics": {...},
        "issues": [...],
        "recommendations": [...]
      }
```

## File Organization

```
website-checker/
│
├── backend/                    # Flask API
│   ├── app/
│   │   ├── analyzers/         # 6 analyzer modules
│   │   ├── utils/             # Helpers & validators
│   │   ├── routes.py          # API routes
│   │   └── __init__.py        # App factory
│   ├── run.py                 # Entry point
│   ├── requirements.txt
│   └── .env
│
├── frontend/                   # React UI
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   └── .env
│
├── Documentation/
│   ├── README.md              # Full documentation
│   ├── QUICKSTART.md          # Quick setup guide
│   ├── PROJECT_SUMMARY.md     # This overview
│   ├── CONFIGURATION.md       # Setup guide
│   └── .github/
│       └── copilot-instructions.md
│
└── .gitignore
```

## Technology Stack

```
Frontend Stack:
├── React 18.2.0           UI Framework
├── Axios 1.6.0            HTTP Client
├── Chart.js 4.4.0         Charting Library
└── CSS3                   Styling

Backend Stack:
├── Flask 3.0.0            Web Framework
├── BeautifulSoup4 4.12.2  HTML Parser
├── Requests 2.31.0        HTTP Library
└── Python 3.8+            Runtime

Infrastructure:
├── npm                    Frontend Package Manager
├── pip                    Python Package Manager
├── CORS                   Cross-Origin Requests
└── REST API               Communication Protocol
```

## Scoring Algorithm

```
For each category:

Issues Found: [
  {type: "issue1", severity: "critical/high/medium/low"},
  {type: "issue2", severity: "critical/high/medium/low"},
  ...
]

Score Calculation:
1. Count all issues: N
2. Max possible issues: MAX (category-specific)
3. Score = MAX(0, 100 - (N / MAX * 100))
4. Grade Assignment:
   - 90-100 → A
   - 80-89  → B
   - 70-79  → C
   - 60-69  → D
   - 0-59   → F

Overall Score:
= (Performance + Security + SEO + CodeStandards + UX + UserBehavior) / 6
```

## Request/Response Cycle

```
CLIENT REQUEST:
POST /api/analyze
{
  "url": "https://example.com"
}

SERVER PROCESSING:
1. Validate URL format
2. Fetch and parse webpage
3. Run 6 analyzers in sequence
4. Aggregate results
5. Generate recommendations

SERVER RESPONSE:
{
  "url": "https://example.com",
  "performance": {
    "score": 82,
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

## Security Flow

```
Frontend:
├── HTTPS only (production)
├── URL validation
├── Input sanitization
└── Error handling

Backend:
├── CORS verification
├── SSL validation for target
├── Input validation
├── Error logging
└── Security headers
```

---

This architecture provides a scalable, maintainable solution for comprehensive website analysis.
