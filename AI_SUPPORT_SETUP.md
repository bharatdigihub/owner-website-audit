# AI Support System Setup Guide

## Overview

The Website Analyzer now includes an **AI-powered support assistant** that provides intelligent tutorials and solutions for detected website issues. Website owners can click on any issue to get step-by-step fix instructions powered by AI.

## Features

### 1. **AI-Generated Tutorials** 
- Instant, customized solutions for each detected issue
- Step-by-step instructions with code examples
- Links to official documentation

### 2. **Issue Analytics**
- Prioritized issue list by severity and impact
- Estimated time to fix each issue
- Quick wins (issues fixable in 5 minutes)

### 3. **Fallback Support**
- Local knowledge base for instant responses
- Works offline if API is not available

## Setup Instructions

### Option 1: Using Google Gemini AI (Recommended)

**Step 1: Get a Google API Key**

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key

**Step 2: Configure Backend**

Create/Update `.env` file in the `backend` directory:

```env
GOOGLE_API_KEY=your_api_key_here
FLASK_PORT=5000
CORS_ORIGINS=http://localhost:3000
```

**Step 3: Test the Connection**

```bash
cd backend
python -c "from app.analyzers.ai_support import AISupportAssistant; print('AI Support Ready!' if AISupportAssistant().api_key else 'API Key Missing')"
```

### Option 2: Using OpenAI (Alternative)

You can modify `backend/app/analyzers/ai_support.py` to use OpenAI instead:

```python
import openai

class AISupportAssistant:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        openai.api_key = self.api_key
    
    def _generate_tutorial(self, issue, analysis_data):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

### Option 3: Offline Mode (No API Key Needed)

The system automatically falls back to the local knowledge base if:
- No API key is configured
- API calls fail
- Network is unavailable

No additional setup needed - it works out of the box!

## API Endpoints

### Get Issue Tutorials
```bash
POST /api/support/tutorials
Content-Type: application/json

{
  "issues": [
    {
      "title": "Missing Meta Tags",
      "description": "Page is missing meta title and description",
      "severity": "high",
      "category": "seo"
    }
  ],
  "analysis_data": { ... }
}
```

**Response:**
```json
{
  "status": "success",
  "total_issues": 1,
  "tutorials_generated": 1,
  "tutorials": [
    {
      "issue_title": "Missing Meta Tags",
      "issue_severity": "high",
      "tutorial": "Problem Explanation:\nMeta tags are HTML elements that describe your page...",
      "generated_at": "2025-11-18T10:30:00",
      "status": "success"
    }
  ]
}
```

### Get Issue Analytics
```bash
POST /api/support/analytics
Content-Type: application/json

{
  "analysis_results": {
    "performance": { "score": 85, "issues": [...] },
    "seo": { "score": 72, "issues": [...] },
    ...
  }
}
```

**Response:**
```json
{
  "status": "success",
  "total_issues": 24,
  "critical_issues": 2,
  "high_priority_issues": 5,
  "estimated_fix_time": {
    "total_minutes": 180,
    "estimated_hours": 3.0,
    "priority_focus_minutes": 90
  },
  "quick_wins": [
    {
      "title": "Add meta title tag",
      "category": "seo",
      "description": "Page is missing meta title",
      "estimated_time_minutes": 5
    }
  ],
  "prioritized_issues": [...]
}
```

### Get Quick Fix
```bash
POST /api/support/quick-fix
Content-Type: application/json

{
  "issue_title": "Large Images",
  "category": "performance"
}
```

**Response:**
```json
{
  "status": "success",
  "issue_title": "Large Images",
  "category": "performance",
  "quick_solution": "1. Use modern formats (WebP, AVIF)\n2. Compress images with tools like TinyPNG\n3. Implement responsive images with srcset\n4. Use lazy loading"
}
```

## Frontend Usage

### SupportPanel Component

The `SupportPanel` component is automatically integrated into the Dashboard's **AI Support** tab.

**Features:**
- Lists all detected issues with severity levels
- Click any issue to see AI-generated tutorial
- View analytics across all issues
- Identify quick wins (5-minute fixes)
- Estimated fix time for entire site

**Usage in React:**
```jsx
import SupportPanel from './components/SupportPanel';

function MyComponent({ analysisData }) {
  return <SupportPanel analysisData={analysisData} />;
}
```

## Customization

### Add Custom Solutions

Edit `backend/app/analyzers/ai_support.py`:

```python
LocalSupportAssistant.KNOWLEDGE_BASE = {
    'category_name': {
        'issues': [
            {
                'title': 'Issue Name',
                'solution': 'Step-by-step solution here'
            }
        ]
    }
}
```

### Modify AI Prompt

Edit the `_build_prompt` method in `AISupportAssistant` to customize how tutorials are generated:

```python
def _build_prompt(self, issue, analysis_data):
    # Customize the prompt template
    prompt = f"""Your custom prompt here..."""
    return prompt
```

## Troubleshooting

### 1. "AI support not configured" Message

**Solution:** Set `GOOGLE_API_KEY` environment variable
```bash
# Windows
set GOOGLE_API_KEY=your_key

# Linux/Mac
export GOOGLE_API_KEY=your_key
```

### 2. API Timeouts

**Solution:** Increase timeout in `ai_support.py`:
```python
requests.post(..., timeout=60)  # Increase from 30 to 60
```

### 3. Offline Mode Not Working

**Solution:** The system falls back automatically. Check:
```bash
cd backend
python -c "from app.analyzers.ai_support import LocalSupportAssistant; print('Offline mode working')"
```

## Best Practices

1. **Cache Results**: Store generated tutorials to reduce API calls
2. **Rate Limiting**: Implement rate limits for API endpoints
3. **Error Handling**: Always use try-catch blocks
4. **Logging**: Monitor AI API usage and errors
5. **Testing**: Test with various issue types before production

## Example: Complete Flow

```bash
# 1. Start backend
cd backend
python run.py

# 2. In another terminal, test the support system
curl -X POST http://localhost:5000/api/support/quick-fix \
  -H "Content-Type: application/json" \
  -d '{"issue_title": "Missing Meta Tags", "category": "seo"}'

# 3. Open frontend
# http://localhost:3000
# Analyze a website
# Go to "AI Support" tab
# Click on any issue to see tutorial
```

## Costs

- **Google Gemini API**: Free tier available (up to 60 calls/minute)
- **OpenAI**: ~$0.15-0.20 per 1K tokens
- **No API**: Completely free (uses local knowledge base)

## Support

For issues or feature requests:
- GitHub Issues: https://github.com/bharatdigihub/owner-website-audit/issues
- Email: support@example.com

---

**Next Steps:**
1. Set up API key (or use offline mode)
2. Test with sample websites
3. Customize solutions for your needs
4. Deploy to production
