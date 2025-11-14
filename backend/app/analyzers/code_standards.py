"""Code standards analyzer module"""
from app.analyzers.base import BaseAnalyzer

class CodeStandardsAnalyzer(BaseAnalyzer):
    """Analyze code standards and best practices"""
    
    def analyze(self):
        """Perform code standards analysis"""
        if not self.soup:
            return self.get_error_response()
        
        issues = []
        
        # Check HTML standards
        html_issues = self.check_html_standards()
        issues.extend(html_issues)
        
        # Check CSS standards
        css_issues = self.check_css_standards()
        issues.extend(css_issues)
        
        # Check JavaScript standards
        js_issues = self.check_js_standards()
        issues.extend(js_issues)
        
        # Check semantic HTML
        semantic_issues = self.check_semantic_html()
        issues.extend(semantic_issues)
        
        score = self.get_score(len(issues), 40)
        
        return {
            'score': score,
            'grade': self.get_grade(score),
            'issues': issues,
            'recommendations': self.get_recommendations(issues)
        }
    
    def check_html_standards(self):
        """Check HTML best practices"""
        issues = []
        
        try:
            # Check doctype
            doctype = str(self.soup).split('\n')[0] if self.soup else ''
            if '<!DOCTYPE' not in doctype:
                issues.append({
                    'type': 'missing_doctype',
                    'message': 'DOCTYPE declaration missing',
                    'severity': 'high'
                })
            
            # Check for title tag
            title = self.soup.find('title')
            if not title:
                issues.append({
                    'type': 'missing_title',
                    'message': 'Page title tag missing',
                    'severity': 'high'
                })
            elif len(title.string or '') < 10:
                issues.append({
                    'type': 'short_title',
                    'message': 'Page title is too short',
                    'severity': 'medium'
                })
            
            # Check for lang attribute
            html_tag = self.soup.find('html')
            if html_tag and not html_tag.get('lang'):
                issues.append({
                    'type': 'missing_lang',
                    'message': 'HTML lang attribute missing',
                    'severity': 'medium'
                })
            
            # Check for deprecated tags
            deprecated_tags = ['marquee', 'blink', 'embed', 'applet']
            for tag_name in deprecated_tags:
                if self.soup.find(tag_name):
                    issues.append({
                        'type': 'deprecated_html',
                        'message': f'Deprecated HTML tag found: <{tag_name}>',
                        'severity': 'medium'
                    })
        except Exception as e:
            print(f"Error checking HTML standards: {e}")
        
        return issues
    
    def check_css_standards(self):
        """Check CSS standards"""
        issues = []
        
        try:
            # Check for inline styles (should be minimal)
            inline_styles = self.soup.find_all(style=True)
            if len(inline_styles) > 5:
                issues.append({
                    'type': 'excessive_inline_styles',
                    'message': f'Found {len(inline_styles)} elements with inline styles',
                    'severity': 'low'
                })
            
            # Check for CSS files
            stylesheets = self.soup.find_all('link', {'rel': 'stylesheet'})
            if len(stylesheets) == 0:
                issues.append({
                    'type': 'no_external_css',
                    'message': 'No external CSS files found',
                    'severity': 'low'
                })
        except Exception as e:
            print(f"Error checking CSS standards: {e}")
        
        return issues
    
    def check_js_standards(self):
        """Check JavaScript standards"""
        issues = []
        
        try:
            # Check for inline scripts
            inline_scripts = self.soup.find_all('script', string=True)
            if len(inline_scripts) > 3:
                issues.append({
                    'type': 'excessive_inline_js',
                    'message': f'Found {len(inline_scripts)} inline scripts',
                    'severity': 'low'
                })
            
            # Check for async/defer on scripts
            scripts = self.soup.find_all('script')
            unoptimized = sum(1 for s in scripts if not s.get('async') and not s.get('defer') and s.get('src'))
            if unoptimized > 2:
                issues.append({
                    'type': 'unoptimized_scripts',
                    'message': f'{unoptimized} scripts lack async/defer attributes',
                    'severity': 'medium'
                })
        except Exception as e:
            print(f"Error checking JS standards: {e}")
        
        return issues
    
    def check_semantic_html(self):
        """Check for semantic HTML usage"""
        issues = []
        
        try:
            # Check for semantic elements
            semantic_elements = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
            found_semantic = sum(1 for elem in semantic_elements if self.soup.find(elem))
            
            if found_semantic == 0:
                issues.append({
                    'type': 'no_semantic_html',
                    'message': 'No semantic HTML elements (header, nav, main, etc.) found',
                    'severity': 'medium'
                })
            
            # Check for proper use of nav
            navs = self.soup.find_all('nav')
            lists_in_nav = sum(1 for nav in navs for _ in nav.find_all('ul'))
            if len(navs) > 0 and lists_in_nav == 0:
                issues.append({
                    'type': 'poor_nav_structure',
                    'message': 'Navigation should use lists (ul/ol)',
                    'severity': 'low'
                })
        except Exception as e:
            print(f"Error checking semantic HTML: {e}")
        
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
        
        if 'missing_doctype' in issue_types:
            recommendations.append('Add HTML5 DOCTYPE declaration at the top')
        if 'missing_title' in issue_types:
            recommendations.append('Add a descriptive title tag to your page')
        if 'missing_lang' in issue_types:
            recommendations.append('Add lang attribute to html tag for accessibility')
        if 'excessive_inline_styles' in issue_types:
            recommendations.append('Move inline styles to external CSS files')
        if 'no_semantic_html' in issue_types:
            recommendations.append('Use semantic HTML elements (header, nav, main, etc.)')
        
        return recommendations
    
    def get_error_response(self):
        """Return error response"""
        return {
            'score': 0,
            'grade': 'F',
            'issues': [{'type': 'fetch_error', 'message': 'Could not fetch website', 'severity': 'critical'}],
            'recommendations': ['Check if the URL is correct and accessible']
        }
