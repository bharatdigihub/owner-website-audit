"""Base analyzer class"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class BaseAnalyzer:
    """Base class for all analyzers"""
    
    def __init__(self, url):
        self.url = url
        self.html = None
        self.soup = None
        self.response = None
        self.fetch_page()
    
    def fetch_page(self):
        """Fetch the webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
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
