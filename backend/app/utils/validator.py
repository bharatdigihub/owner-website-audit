"""URL validator utility"""
import re
from urllib.parse import urlparse

def validate_url(url):
    """Validate if URL is properly formatted"""
    try:
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Parse URL
        result = urlparse(url)
        
        # Check if URL has required components
        if not all([result.scheme, result.netloc]):
            return False
        
        # Check scheme
        if result.scheme not in ('http', 'https'):
            return False
        
        # Simple domain validation
        domain_regex = r'^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        if not re.match(domain_regex, result.netloc):
            return False
        
        return True
    except:
        return False

def normalize_url(url):
    """Normalize URL by adding scheme if missing"""
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url
