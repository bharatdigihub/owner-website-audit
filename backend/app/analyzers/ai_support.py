"""AI-powered support system for website issues using Google Gemini API"""
import os
import json
import requests
from typing import Dict, List, Any

class AISupportAssistant:
    """
    AI-powered assistant that provides tutorials and solutions for website issues.
    Uses Google Generative AI (Gemini) API for intelligent recommendations.
    """
    
    def __init__(self):
        """Initialize the AI support assistant"""
        self.api_key = os.getenv('GOOGLE_API_KEY', '')
        self.api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'
        self.model = 'gemini-1.5-flash'
    
    def get_issue_tutorials(self, issues: List[Dict], analysis_data: Dict) -> Dict[str, Any]:
        """
        Get AI-generated tutorials for detected issues.
        
        Args:
            issues: List of detected issues with category and description
            analysis_data: Complete analysis data for context
            
        Returns:
            Dictionary with tutorials and solutions for each issue
        """
        if not self.api_key:
            return {
                'status': 'warning',
                'message': 'AI support not configured. Set GOOGLE_API_KEY environment variable.',
                'tutorials': []
            }
        
        tutorials = []
        
        for issue in issues[:10]:  # Limit to 10 issues per request
            tutorial = self._generate_tutorial(issue, analysis_data)
            if tutorial:
                tutorials.append(tutorial)
        
        return {
            'status': 'success',
            'total_issues': len(issues),
            'tutorials_generated': len(tutorials),
            'tutorials': tutorials
        }
    
    def _generate_tutorial(self, issue: Dict, analysis_data: Dict) -> Dict[str, Any]:
        """Generate a tutorial for a specific issue using AI"""
        try:
            prompt = self._build_prompt(issue, analysis_data)
            
            response = requests.post(
                self.api_url,
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{
                        'parts': [{'text': prompt}]
                    }],
                    'generationConfig': {
                        'temperature': 0.7,
                        'topK': 40,
                        'topP': 0.95,
                        'maxOutputTokens': 1024,
                    }
                },
                params={'key': self.api_key},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                
                return {
                    'issue_title': issue.get('title', 'Unknown Issue'),
                    'issue_severity': issue.get('severity', 'medium'),
                    'issue_description': issue.get('description', ''),
                    'tutorial': content,
                    'generated_at': self._get_timestamp(),
                    'status': 'success'
                }
            else:
                return None
        
        except Exception as e:
            print(f"Error generating tutorial: {e}")
            return {
                'issue_title': issue.get('title', 'Unknown Issue'),
                'status': 'error',
                'error': str(e)
            }
    
    def _build_prompt(self, issue: Dict, analysis_data: Dict) -> str:
        """Build a detailed prompt for AI tutorial generation"""
        issue_title = issue.get('title', 'Unknown Issue')
        issue_desc = issue.get('description', '')
        issue_severity = issue.get('severity', 'medium')
        
        prompt = f"""You are an expert web developer and SEO specialist providing clear, actionable tutorials.

WEBSITE ISSUE DETECTED:
Title: {issue_title}
Severity: {issue_severity}
Description: {issue_desc}

Please provide a comprehensive tutorial that includes:

1. **Problem Explanation**: Briefly explain what this issue means and why it matters
2. **Impact**: How this affects website performance, SEO, or user experience
3. **Step-by-Step Solution**:
   - List 3-5 clear, numbered steps to fix this issue
   - Include code examples where relevant
   - Provide specific HTML/CSS/JavaScript snippets if applicable
4. **Quick Wins**: Any immediate fixes that can be done in minutes
5. **Best Practices**: General recommendations to prevent this issue in the future
6. **Tools to Verify**: Tools or methods to verify the fix is working
7. **Resources**: Links to documentation (Google Docs, MDN, official guides)

Keep the language simple but professional. Focus on practical solutions over theory.
Be specific to the detected issue. Use markdown formatting for clarity."""
        
        return prompt
    
    def get_issue_analytics(self, analysis_results: Dict) -> Dict[str, Any]:
        """
        Analyze all issues and provide prioritized fix recommendations.
        
        Args:
            analysis_results: Complete analysis results from all analyzers
            
        Returns:
            Prioritized list of issues with fix recommendations
        """
        issues = self._extract_all_issues(analysis_results)
        
        if not issues:
            return {
                'status': 'success',
                'total_issues': 0,
                'message': 'No issues found! Your website is in great shape.',
                'recommendations': []
            }
        
        # Prioritize issues by severity and impact
        prioritized = self._prioritize_issues(issues)
        
        return {
            'status': 'success',
            'total_issues': len(issues),
            'critical_issues': sum(1 for i in issues if i.get('severity') == 'critical'),
            'high_priority_issues': sum(1 for i in issues if i.get('severity') == 'high'),
            'prioritized_issues': prioritized,
            'quick_wins': self._identify_quick_wins(issues),
            'estimated_fix_time': self._estimate_fix_time(issues)
        }
    
    def _extract_all_issues(self, analysis_results: Dict) -> List[Dict]:
        """Extract all issues from analysis results"""
        issues = []
        
        # Map analyzer names to issue categories
        analyzers = [
            'performance', 'security', 'seo', 'coding_standards',
            'user_friendliness', 'mobile_optimization', 'accessibility',
            'advanced_metrics', 'core_web_vitals'
        ]
        
        for analyzer_name in analyzers:
            if analyzer_name in analysis_results:
                analyzer_data = analysis_results[analyzer_name]
                if isinstance(analyzer_data, dict) and 'issues' in analyzer_data:
                    for issue in analyzer_data.get('issues', []):
                        issue['category'] = analyzer_name
                        issue['severity'] = issue.get('severity', 'medium')
                        issues.append(issue)
        
        return issues
    
    def _prioritize_issues(self, issues: List[Dict]) -> List[Dict]:
        """Prioritize issues by severity and impact"""
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        sorted_issues = sorted(
            issues,
            key=lambda x: (
                severity_order.get(x.get('severity', 'medium'), 99),
                -len(x.get('description', ''))  # Longer descriptions = more detailed
            )
        )
        
        return sorted_issues[:20]  # Return top 20 prioritized issues
    
    def _identify_quick_wins(self, issues: List[Dict]) -> List[Dict]:
        """Identify issues that can be fixed quickly"""
        quick_win_keywords = ['meta', 'title', 'alt text', 'heading', 'compression', 'cache']
        
        quick_wins = []
        for issue in issues:
            title = issue.get('title', '').lower()
            if any(keyword in title for keyword in quick_win_keywords):
                quick_wins.append({
                    'title': issue.get('title'),
                    'category': issue.get('category'),
                    'description': issue.get('description'),
                    'estimated_time_minutes': 5
                })
        
        return quick_wins[:5]
    
    def _estimate_fix_time(self, issues: List[Dict]) -> Dict:
        """Estimate total time to fix all issues"""
        time_estimates = {
            'critical': 60,
            'high': 30,
            'medium': 15,
            'low': 5
        }
        
        total_minutes = sum(
            time_estimates.get(issue.get('severity', 'medium'), 15)
            for issue in issues
        )
        
        return {
            'total_minutes': total_minutes,
            'estimated_hours': round(total_minutes / 60, 1),
            'priority_focus_minutes': sum(
                time_estimates.get(issue.get('severity', 'medium'), 15)
                for issue in issues
                if issue.get('severity') in ['critical', 'high']
            )
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


# Fallback support if no API key is available
class LocalSupportAssistant:
    """
    Local support system with pre-built knowledge base.
    Used when AI API is not available.
    """
    
    KNOWLEDGE_BASE = {
        'performance': {
            'issues': [
                {
                    'title': 'Large Images',
                    'solution': '1. Use modern formats (WebP, AVIF)\n2. Compress images with tools like TinyPNG\n3. Implement responsive images with srcset\n4. Use lazy loading'
                },
                {
                    'title': 'Render-Blocking Resources',
                    'solution': '1. Defer non-critical JavaScript\n2. Inline critical CSS\n3. Split large CSS files\n4. Load scripts asynchronously'
                },
                {
                    'title': 'Poor Caching',
                    'solution': '1. Set cache headers (max-age, etag)\n2. Implement service workers\n3. Use CDN for static assets\n4. Version your assets'
                }
            ]
        },
        'seo': {
            'issues': [
                {
                    'title': 'Missing Meta Tags',
                    'solution': '1. Add meta title (50-60 chars)\n2. Add meta description (150-160 chars)\n3. Use semantic HTML tags\n4. Add Open Graph tags for social sharing'
                },
                {
                    'title': 'Poor Heading Structure',
                    'solution': '1. Use one H1 per page\n2. Use H2, H3 hierarchically\n3. Avoid skipping levels\n4. Include keywords naturally'
                }
            ]
        },
        'security': {
            'issues': [
                {
                    'title': 'Missing HTTPS',
                    'solution': '1. Get SSL certificate (free via Let\'s Encrypt)\n2. Install certificate on server\n3. Redirect HTTP to HTTPS\n4. Update internal links'
                },
                {
                    'title': 'Missing Security Headers',
                    'solution': '1. Add CSP header\n2. Add X-Frame-Options\n3. Add X-Content-Type-Options\n4. Add Strict-Transport-Security'
                }
            ]
        }
    }
    
    @staticmethod
    def get_solution(issue_title: str, category: str) -> str:
        """Get solution for an issue from knowledge base"""
        category_issues = LocalSupportAssistant.KNOWLEDGE_BASE.get(category, {}).get('issues', [])
        
        for issue in category_issues:
            if issue['title'].lower() in issue_title.lower():
                return issue['solution']
        
        return 'See documentation for detailed troubleshooting steps.'
