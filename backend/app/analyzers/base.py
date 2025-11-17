"""Base analyzer class"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class BaseAnalyzer:
    """Base class for all analyzers"""
    
    def __init__(self, url, form_factor='desktop'):
        self.url = url
        self.form_factor = form_factor  # 'desktop' or 'mobile'
        self.html = None
        self.soup = None
        self.response = None
        self.fetch_page()
    
    def fetch_page(self):
        """Fetch the webpage"""
        try:
            # Different user agents for mobile vs desktop
            if self.form_factor == 'mobile':
                user_agent = 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
            else:
                user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            
            headers = {'User-Agent': user_agent}
            self.response = requests.get(self.url, headers=headers, timeout=10)
            self.html = self.response.text
            self.soup = BeautifulSoup(self.html, 'html.parser')
        except Exception as e:
            print(f"Error fetching page: {e}")
            self.html = None
            self.soup = None
    
    def analyze(self):
        """Override in subclasses"""
        raise NotImplementedError
    
    def get_score(self, issues_found, max_issues):
        """Calculate score based on issues found"""
        if max_issues == 0:
            return 100
        score = max(0, 100 - (issues_found / max_issues * 100))
        return round(score, 2)
