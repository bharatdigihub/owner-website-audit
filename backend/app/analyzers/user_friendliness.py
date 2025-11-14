"""User friendliness analyzer module"""
from app.analyzers.base import BaseAnalyzer

class UserFriendlinessAnalyzer(BaseAnalyzer):
    """Analyze website user-friendliness and accessibility"""
    
    def analyze(self):
        """Perform user-friendliness analysis"""
        if not self.soup:
            return self.get_error_response()
        
        issues = []
        metrics = {}
        
        # Check accessibility
        accessibility_issues = self.check_accessibility()
        issues.extend(accessibility_issues)
        
        # Check navigation
        nav_issues = self.check_navigation()
        issues.extend(nav_issues)
        
        # Check content readability
        readability_issues = self.check_readability()
        issues.extend(readability_issues)
        
        # Check for interactive elements
        interactive = self.check_interactive_elements()
        metrics['interactive_elements'] = interactive
        
        # Check for breadcrumbs
        has_breadcrumbs = self.check_breadcrumbs()
        metrics['has_breadcrumbs'] = has_breadcrumbs
        if not has_breadcrumbs:
            issues.append({
                'type': 'no_breadcrumbs',
                'message': 'Breadcrumb navigation not found',
                'severity': 'low'
            })
        
        score = self.get_score(len(issues), 40)
        
        return {
            'score': score,
            'grade': self.get_grade(score),
            'metrics': metrics,
            'issues': issues,
            'recommendations': self.get_recommendations(issues)
        }
    
    def check_accessibility(self):
        """Check web accessibility (WCAG)"""
        issues = []
        
        try:
            # Check for proper form labels
            form_inputs = self.soup.find_all('input')
            unlabeled_inputs = 0
            
            for input_elem in form_inputs:
                input_id = input_elem.get('id')
                if input_id:
                    label = self.soup.find('label', {'for': input_id})
                    if not label:
                        unlabeled_inputs += 1
                else:
                    unlabeled_inputs += 1
            
            if unlabeled_inputs > 0:
                issues.append({
                    'type': 'unlabeled_inputs',
                    'message': f'{unlabeled_inputs} form inputs lack associated labels',
                    'severity': 'medium'
                })
            
            # Check for proper button text
            buttons = self.soup.find_all('button')
            for button in buttons:
                if not button.get_text(strip=True):
                    issues.append({
                        'type': 'empty_button_text',
                        'message': 'Button found with no text',
                        'severity': 'high'
                    })
                    break
            
            # Check for color contrast (check inline styles)
            elements_with_style = self.soup.find_all(style=True)
            for elem in elements_with_style:
                style = elem.get('style', '').lower()
                if 'color:' in style and 'background' in style:
                    # This is a simplified check
                    pass
        except Exception as e:
            print(f"Error checking accessibility: {e}")
        
        return issues
    
    def check_navigation(self):
        """Check website navigation quality"""
        issues = []
        
        try:
            # Check for main navigation
            nav_elements = self.soup.find_all('nav')
            if len(nav_elements) == 0:
                issues.append({
                    'type': 'no_main_navigation',
                    'message': 'No main navigation element found',
                    'severity': 'high'
                })
            
            # Check for search functionality
            search_forms = self.soup.find_all('form')
            has_search = any('search' in str(form).lower() for form in search_forms)
            if not has_search:
                issues.append({
                    'type': 'no_search',
                    'message': 'No search functionality found',
                    'severity': 'low'
                })
            
            # Check navigation clarity
            links = self.soup.find_all('a')
            unclear_links = 0
            for link in links:
                text = link.get_text(strip=True).lower()
                if text in ['click here', 'link', 'more', 'read more']:
                    unclear_links += 1
            
            if unclear_links > len(links) * 0.1:
                issues.append({
                    'type': 'unclear_link_text',
                    'message': f'{unclear_links} links have unclear text',
                    'severity': 'medium'
                })
        except Exception as e:
            print(f"Error checking navigation: {e}")
        
        return issues
    
    def check_readability(self):
        """Check content readability"""
        issues = []
        
        try:
            # Check for proper font size
            body_text = self.soup.find('body')
            if body_text:
                paragraphs = body_text.find_all('p')
                
                if len(paragraphs) == 0:
                    issues.append({
                        'type': 'no_paragraphs',
                        'message': 'No paragraph elements found',
                        'severity': 'low'
                    })
                else:
                    # Check paragraph length
                    long_paragraphs = 0
                    for para in paragraphs:
                        text = para.get_text(strip=True)
                        words = len(text.split())
                        if words > 150:
                            long_paragraphs += 1
                    
                    if long_paragraphs > len(paragraphs) * 0.3:
                        issues.append({
                            'type': 'long_paragraphs',
                            'message': 'Many paragraphs are too long (>150 words)',
                            'severity': 'low'
                        })
            
            # Check for sufficient whitespace
            divs = self.soup.find_all('div')
            if len(divs) < 5:
                issues.append({
                    'type': 'poor_spacing',
                    'message': 'Insufficient content structure/spacing',
                    'severity': 'low'
                })
        except Exception as e:
            print(f"Error checking readability: {e}")
        
        return issues
    
    def check_interactive_elements(self):
        """Check for interactive elements"""
        result = {
            'buttons': 0,
            'forms': 0,
            'modals': 0,
            'carousels': 0
        }
        
        try:
            result['buttons'] = len(self.soup.find_all('button'))
            result['forms'] = len(self.soup.find_all('form'))
            result['modals'] = len(self.soup.find_all(class_='modal'))
            # Simple carousel detection
            carousel_indicators = self.soup.find_all(class_=lambda x: x and 'carousel' in x.lower() if x else False)
            result['carousels'] = 1 if carousel_indicators else 0
        except:
            pass
        
        return result
    
    def check_breadcrumbs(self):
        """Check for breadcrumb navigation"""
        try:
            # Look for breadcrumb patterns
            breadcrumbs = self.soup.find_all(class_=lambda x: x and 'breadcrumb' in x.lower() if x else False)
            if breadcrumbs:
                return True
            
            # Look for schema.org breadcrumb
            breadcrumb_schema = self.soup.find('script', {'type': 'application/ld+json'})
            if breadcrumb_schema and 'breadcrumb' in breadcrumb_schema.string.lower():
                return True
        except:
            pass
        
        return False
    
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
        
        if 'no_main_navigation' in issue_types:
            recommendations.append('Add clear main navigation to help users find content')
        if 'unlabeled_inputs' in issue_types:
            recommendations.append('Label all form inputs for better accessibility')
        if 'unclear_link_text' in issue_types:
            recommendations.append('Use descriptive link text instead of generic phrases')
        if 'long_paragraphs' in issue_types:
            recommendations.append('Break long paragraphs into smaller chunks for readability')
        if 'no_search' in issue_types:
            recommendations.append('Add a search function to help users find content')
        
        return recommendations
    
    def get_error_response(self):
        """Return error response"""
        return {
            'score': 0,
            'grade': 'F',
            'metrics': {},
            'issues': [{'type': 'fetch_error', 'message': 'Could not fetch website', 'severity': 'critical'}],
            'recommendations': ['Check if the URL is correct and accessible']
        }
