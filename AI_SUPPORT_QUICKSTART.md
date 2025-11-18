# 🚀 AI Support System - Quick Start Guide

## 30-Second Setup

### No AI (Works Offline)
```bash
cd backend
python run.py
```
**Done!** The system uses the built-in knowledge base.

### With Google Gemini AI (Recommended)

**Step 1**: Get free API key (60 requests/minute free)
- Visit: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the key

**Step 2**: Set environment variable
```bash
# Windows Command Prompt
set GOOGLE_API_KEY=your_api_key_here

# Windows PowerShell
$env:GOOGLE_API_KEY="your_api_key_here"

# Linux/Mac
export GOOGLE_API_KEY=your_api_key_here
```

**Step 3**: Start backend
```bash
cd backend
python run.py
```

**Done!** AI support is now active.

---

## Using AI Support

### For Website Owners

1. **Analyze your website** on the app
2. **Click "💡 AI Support" tab** at the top
3. **Click any issue** to see the tutorial
4. **Follow the step-by-step fix**
5. **Click "Analyze All Issues"** to see priorities

### What You'll See

```
🔴 CRITICAL: SSL Certificate Missing
├─ Problem: Site is not HTTPS
├─ Steps:
│  1. Get free SSL from Let's Encrypt
│  2. Install on your server
│  3. Configure redirect HTTP → HTTPS
│  4. Test with https://www.ssllabs.com
└─ Resources: letsencrypt.org, docs

⚠️  HIGH: Missing Meta Tags
├─ Problem: Page has no title/description
├─ Steps:
│  1. Add <title> tag in <head>
│  2. Add <meta name="description">
│  3. Keep title under 60 chars
│  4. Keep description under 160 chars
└─ Quick Fix: 5 minutes
```

---

## Troubleshooting

### "AI support not configured"
**Solution**: 
```bash
set GOOGLE_API_KEY=your_key
# Restart the app
```

### Solutions aren't showing
**Solution**: 
- It falls back to knowledge base automatically
- Just refresh the page
- Check internet connection

### API timeout
**Solution**: 
- Network might be slow
- Wait a few seconds
- System will use KB fallback

---

## API Examples

### Get a Quick Fix

```bash
curl -X POST http://localhost:5000/api/support/quick-fix \
  -H "Content-Type: application/json" \
  -d '{"issue_title": "Large Images", "category": "performance"}'
```

**Response:**
```json
{
  "status": "success",
  "issue_title": "Large Images",
  "quick_solution": "1. Convert to WebP format\n2. Compress with TinyPNG\n3. Use responsive images..."
}
```

### Get Analytics

```bash
curl -X POST http://localhost:5000/api/support/analytics \
  -H "Content-Type: application/json" \
  -d '{"analysis_results": {...}}'
```

**Response:**
```json
{
  "total_issues": 24,
  "critical_issues": 2,
  "high_priority_issues": 5,
  "estimated_fix_time": {
    "estimated_hours": 3.0,
    "total_minutes": 180
  },
  "quick_wins": [
    {"title": "Add meta title", "estimated_time_minutes": 5}
  ]
}
```

---

## Features at a Glance

| Feature | Time | AI Needed | Works Offline |
|---------|------|-----------|---------------|
| Quick Fix | 2s | Optional | ✅ Yes |
| Issue Analytics | 3s | Optional | ✅ Yes |
| Detailed Tutorials | 5s | Required | ❌ Uses KB |
| Knowledge Base | <1s | No | ✅ Yes |

---

## Common Issues & Fixes

### Meta Tags Missing
```html
<!-- Add to <head> -->
<title>Your Page Title (50-60 chars)</title>
<meta name="description" content="Description (150-160 chars)">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="UTF-8">
```
**Time**: 5 minutes

### Images Not Optimized
```html
<!-- Add alt text and sizes -->
<img src="image.jpg" alt="Descriptive text" width="800" height="600">
```
**Tools**: TinyPNG, ImageOptim, FileZilla
**Time**: 15 minutes

### No SSL Certificate
1. Go to https://letsencrypt.org
2. Follow setup for your hosting
3. Auto-renews every 90 days
4. Free forever
**Time**: 30 minutes

### Slow Page Load
1. Enable gzip compression
2. Add browser caching headers
3. Minify CSS/JavaScript
4. Use CDN for static files
**Time**: 1 hour

---

## Tips & Tricks

### 💡 Start with Quick Wins
- Sort by "Quick Wins"
- Fix 5-minute issues first
- Build momentum
- Improves overall score

### 🎯 Focus on Critical Issues
- Address red (critical) issues first
- Then high priority (orange)
- Medium (blue) can wait
- Low (green) are nice-to-have

### ⏱️ Use Time Estimates
- UI shows estimated fix time
- Plan your day accordingly
- Major overhaul = 3-4 hours
- Minor fixes = 30-60 minutes

### 📊 Track Progress
- Fix 1-2 issues per day
- Rerun analysis
- Watch score improve
- Motivating!

---

## Need Help?

### Documentation
- **Setup**: See [AI_SUPPORT_SETUP.md](./AI_SUPPORT_SETUP.md)
- **Details**: See [AI_SUPPORT_IMPLEMENTATION.md](./AI_SUPPORT_IMPLEMENTATION.md)
- **Full Docs**: See [README.md](./README.md)

### Quick Questions
1. Check "Analyze All Issues" analytics
2. Read the tutorial provided
3. Click the resources link
4. Search the issue title online

### Report Issues
- GitHub Issues: https://github.com/bharatdigihub/owner-website-audit/issues
- Include error message
- Include issue title
- Describe what happened

---

## What's Covered

✅ Performance issues
✅ Security problems  
✅ SEO recommendations
✅ Accessibility fixes
✅ Code standards
✅ Mobile optimization
✅ And more!

---

## Next Steps

1. **Analyze a website** → Click "Analyze Website"
2. **Go to AI Support tab** → Click "💡 AI Support"
3. **Click any issue** → See the fix instructions
4. **Implement fixes** → Follow the tutorial
5. **Verify fixes** → Rerun analysis

**That's it!** Your website will be improved in no time. 🎉

---

**Need to configure?** → [AI_SUPPORT_SETUP.md](./AI_SUPPORT_SETUP.md)
**Want details?** → [AI_SUPPORT_IMPLEMENTATION.md](./AI_SUPPORT_IMPLEMENTATION.md)
**Back to basics?** → [README.md](./README.md)
