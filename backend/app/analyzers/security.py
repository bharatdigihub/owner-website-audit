"""Security analyzer module"""
import ssl
import socket
from urllib.parse import urlparse
from app.analyzers.base import BaseAnalyzer

class SecurityAnalyzer(BaseAnalyzer):
    """Analyze website security"""
    
    def analyze(self):
        """Perform security analysis"""
        issues = []
        metrics = {}
        
        # Check SSL/TLS
        ssl_info = self.check_ssl()
        metrics['ssl'] = ssl_info
        if ssl_info['has_ssl']:
            metrics['ssl_grade'] = ssl_info.get('grade', 'Unknown')
        else:
            issues.append({
                'type': 'no_ssl',
                'message': 'Website does not use HTTPS',
                'severity': 'critical'
            })
        
        # Check security headers
        header_issues = self.check_security_headers()
        issues.extend(header_issues)
        
        # Check for mixed content
        if not self.check_mixed_content():
            issues.append({
                'type': 'mixed_content',
                'message': 'Mixed content detected (HTTP resources on HTTPS page)',
                'severity': 'high'
            })
        
        # Check for common vulnerabilities
        vuln_issues = self.check_vulnerabilities()
        issues.extend(vuln_issues)
        
        score = self.get_score(len(issues), 40)
        
        return {
            'score': score,
            'grade': self.get_grade(score),
            'metrics': metrics,
            'issues': issues,
            'recommendations': self.get_recommendations(issues)
        }
    
    def check_ssl(self):
        """Check SSL/TLS certificate"""
        result = {
            'has_ssl': False,
            'certificate_valid': False,
            'grade': 'F'
        }
        
        try:
            parsed_url = urlparse(self.url)
            hostname = parsed_url.netloc
            
            if parsed_url.scheme == 'https':
                result['has_ssl'] = True
                
                # Try to verify certificate
                try:
                    context = ssl.create_default_context()
                    with socket.create_connection((hostname, 443), timeout=5) as sock:
                        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                            cert = ssock.getpeercert()
                            result['certificate_valid'] = True
                            result['grade'] = 'A'
                except:
                    result['certificate_valid'] = False
                    result['grade'] = 'C'
        except Exception as e:
            print(f"Error checking SSL: {e}")
        
        return result
    
    def check_security_headers(self):
        """Check for security headers"""
        issues = []
        headers_to_check = {
            'Strict-Transport-Security': 'HSTS',
            'X-Content-Type-Options': 'X-Content-Type-Options',
            'X-Frame-Options': 'X-Frame-Options',
            'Content-Security-Policy': 'CSP',
            'X-XSS-Protection': 'X-XSS-Protection'
        }
        
        try:
            for header, name in headers_to_check.items():
                if header not in self.response.headers:
                    issues.append({
                        'type': f'missing_{name.lower()}',
                        'message': f'Missing security header: {name}',
                        'severity': 'medium' if name != 'CSP' else 'high'
                    })
        except:
            pass
        
        return issues
    
    def check_mixed_content(self):
        """Check for mixed content warnings"""
        try:
            if self.url.startswith('https'):
                # Look for http resources
                if self.html and 'http://' in self.html and 'https://' in self.html:
                    # Check if http URLs are actual resources
                    if 'src="http://' in self.html or 'href="http://' in self.html:
                        return False
        except:
            pass
        
        return True
    
    def check_vulnerabilities(self):
        """Check for common vulnerabilities"""
        issues = []
        
        try:
            # Check for outdated frameworks
            if self.soup:
                meta_tags = self.soup.find_all('meta', {'name': 'generator'})
                for tag in meta_tags:
                    content = tag.get('content', '')
                    if 'WordPress' in content or 'Joomla' in content:
                        issues.append({
                            'type': 'exposed_framework',
                            'message': f'Framework version exposed: {content}',
                            'severity': 'medium'
                        })
        except:
            pass
        
        return issues
    
    def get_grade(self, score):
        """Get letter grade from score"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def get_recommendations(self, issues):
        """Get recommendations based on issues"""
        recommendations = []
        issue_types = [issue['type'] for issue in issues]
        
        if 'no_ssl' in issue_types:
            recommendations.append('Enable HTTPS with a valid SSL certificate')
        if 'missing_csp' in issue_types:
            recommendations.append('Implement Content Security Policy (CSP) headers')
        if 'missing_hsts' in issue_types:
            recommendations.append('Add HSTS header to force HTTPS')
        if 'exposed_framework' in issue_types:
            recommendations.append('Hide server/framework information from headers')
        
        return recommendations
