"""Accessibility Analyzer"""
from app.analyzers.base import BaseAnalyzer

class AccessibilityAnalyzer(BaseAnalyzer):
    """Analyze website accessibility compliance (WCAG 2.1)"""
    
    def analyze(self):
        """Perform accessibility analysis"""
        if not self.soup:
            return self.get_error_response()
        
        issues = []
        metrics = {}
        
        # Check ARIA labels
        aria_issues = self.check_aria_labels()
        issues.extend(aria_issues)
        
        # Check alt text
        alt_issues = self.check_alt_text()
        issues.extend(alt_issues)
        
        # Check heading structure
        heading_issues = self.check_heading_structure()
        issues.extend(heading_issues)
        
        # Check form labels
        form_issues = self.check_form_labels()
        issues.extend(form_issues)
        
        # Check color contrast
        contrast_issues = self.check_color_contrast()
        issues.extend(contrast_issues)
        
        # Check keyboard accessibility
        keyboard_issues = self.check_keyboard_accessibility()
        issues.extend(keyboard_issues)
        
        # Check WCAG compliance level
        # expose issues on the instance for methods that reference self.issues
        self.issues = issues
        wcag_level = self.check_wcag_level()
        metrics['wcag_level'] = wcag_level
        
        # Count accessibility features
        features = self.count_accessibility_features()
        metrics['accessibility_features'] = features
        
        score = self.get_score(len(issues), 50)
        
        return {
            'score': score,
            'grade': self.get_grade(score),
            'metrics': metrics,
            'issues': issues,
            'recommendations': self.get_recommendations(issues)
        }
    
    def check_aria_labels(self):
        """Check for proper ARIA labels"""
        issues = []
        
        try:
            # Check for unlabeled buttons
            buttons = self.soup.find_all('button')
            unlabeled_buttons = 0
            
            for btn in buttons:
                if not btn.get_text(strip=True) and not btn.get('aria-label'):
                    unlabeled_buttons += 1
            
            if unlabeled_buttons > 0:
                issues.append({
                    'type': 'missing_aria_labels',
                    'message': f'{unlabeled_buttons} button(s) missing accessible labels',
                    'severity': 'high'
                })
            
            # Check for unlabeled landmarks
            nav_sections = self.soup.find_all(['nav', 'main', 'aside', 'article', 'section'])
            for section in nav_sections:
                if section.name == 'nav' and not section.get('aria-label'):
                    issues.append({
                        'type': 'unlabeled_navigation',
                        'message': 'Navigation landmark missing aria-label',
                        'severity': 'medium'
                    })
                    break
        except Exception as e:
            print(f"Error checking ARIA labels: {e}")
        
        return issues
    
    def check_alt_text(self):
        """Check for alt text on images"""
        issues = []
        
        try:
            images = self.soup.find_all('img')
            
            if not images:
                return issues
            
            missing_alt = 0
            empty_alt = 0
            poor_alt = 0
            
            for img in images:
                alt = img.get('alt', '')
                src = img.get('src', 'unknown')
                
                if 'alt' not in img.attrs:
                    missing_alt += 1
                elif not alt.strip():
                    empty_alt += 1
                elif alt.lower() in ['image', 'picture', 'photo', 'img']:
                    poor_alt += 1
            
            if missing_alt > 0:
                issues.append({
                    'type': 'missing_alt_text',
                    'message': f'{missing_alt} image(s) missing alt text',
                    'severity': 'critical'
                })
            
            if empty_alt > 0:
                issues.append({
                    'type': 'empty_alt_text',
                    'message': f'{empty_alt} image(s) have empty alt text',
                    'severity': 'high'
                })
            
            if poor_alt > 0:
                issues.append({
                    'type': 'poor_alt_text',
                    'message': f'{poor_alt} image(s) have generic or non-descriptive alt text',
                    'severity': 'medium'
                })
        except Exception as e:
            print(f"Error checking alt text: {e}")
        
        return issues
    
    def check_heading_structure(self):
        """Check heading hierarchy"""
        issues = []
        
        try:
            headings = self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            if not headings:
                issues.append({
                    'type': 'no_headings',
                    'message': 'Page has no heading structure',
                    'severity': 'high'
                })
                return issues
            
            # Check for multiple H1s
            h1_count = len([h for h in headings if h.name == 'h1'])
            if h1_count == 0:
                issues.append({
                    'type': 'no_h1',
                    'message': 'Page missing H1 heading',
                    'severity': 'high'
                })
            elif h1_count > 1:
                issues.append({
                    'type': 'multiple_h1',
                    'message': f'Page has {h1_count} H1 headings (should have only 1)',
                    'severity': 'medium'
                })
            
            # Check heading hierarchy
            prev_level = 0
            hierarchy_broken = False
            for heading in headings:
                level = int(heading.name[1])
                if level > prev_level + 1:
                    hierarchy_broken = True
                    break
                prev_level = level
            
            if hierarchy_broken:
                issues.append({
                    'type': 'broken_heading_hierarchy',
                    'message': 'Heading hierarchy not properly structured',
                    'severity': 'medium'
                })
        except Exception as e:
            print(f"Error checking heading structure: {e}")
        
        return issues
    
    def check_form_labels(self):
        """Check for proper form labels"""
        issues = []
        
        try:
            inputs = self.soup.find_all(['input', 'textarea', 'select'])
            
            if not inputs:
                return issues
            
            unlabeled_inputs = 0
            
            for inp in inputs:
                input_id = inp.get('id')
                input_type = inp.get('type', 'text')
                
                # Skip hidden and submit buttons
                if input_type in ['hidden', 'submit', 'reset', 'button']:
                    continue
                
                # Check for label
                has_label = False
                
                if input_id:
                    label = self.soup.find('label', {'for': input_id})
                    has_label = bool(label)
                
                # Check for aria-label
                if inp.get('aria-label'):
                    has_label = True
                
                # Check for placeholder (not sufficient but counts)
                if inp.get('placeholder'):
                    has_label = True
                
                if not has_label:
                    unlabeled_inputs += 1
            
            if unlabeled_inputs > 0:
                issues.append({
                    'type': 'unlabeled_form_inputs',
                    'message': f'{unlabeled_inputs} form input(s) missing associated label',
                    'severity': 'high'
                })
        except Exception as e:
            print(f"Error checking form labels: {e}")
        
        return issues
    
    def check_color_contrast(self):
        """Check for sufficient color contrast"""
        issues = []
        
        try:
            # This is a basic check - full contrast checking would require CSS parsing
            styles = self.soup.find_all('style')
            
            # Look for suspicious color combinations
            styles_text = ''.join(str(s) for s in styles).lower()
            
            # Check for white text on light backgrounds (common issue)
            if 'color: white' in styles_text and 'background: #fff' in styles_text:
                issues.append({
                    'type': 'low_contrast',
                    'message': 'Potential low contrast text detected',
                    'severity': 'medium'
                })
        except Exception as e:
            print(f"Error checking color contrast: {e}")
        
        return issues
    
    def check_keyboard_accessibility(self):
        """Check for keyboard navigation support"""
        issues = []
        
        try:
            # Check for skip link
            skip_links = self.soup.find_all('a', {'href': ['#main', '#content', '#skip']})
            if not skip_links:
                issues.append({
                    'type': 'no_skip_link',
                    'message': 'Missing skip to main content link',
                    'severity': 'medium'
                })
            
            # Check for focusable elements
            focusable = self.soup.find_all(['a', 'button', 'input', 'select', 'textarea'])
            
            if not focusable:
                issues.append({
                    'type': 'no_focusable_elements',
                    'message': 'No keyboard focusable elements found',
                    'severity': 'high'
                })
            
            # Check for tabindex abuse (negative or very high values)
            elements_with_tabindex = self.soup.find_all(attrs={'tabindex': True})
            for elem in elements_with_tabindex:
                try:
                    tabindex = int(elem.get('tabindex', 0))
                    if tabindex > 0:
                        issues.append({
                            'type': 'positive_tabindex',
                            'message': 'Found positive tabindex values (should use 0 or -1 only)',
                            'severity': 'low'
                        })
                        break
                except ValueError:
                    pass
        except Exception as e:
            print(f"Error checking keyboard accessibility: {e}")
        
        return issues
    
    def check_wcag_level(self):
        """Determine WCAG compliance level (A, AA, AAA)"""
        # This is a simplified assessment
        critical_issues = sum(1 for issue in self.issues if issue.get('severity') == 'critical')
        
        if critical_issues > 5:
            return 'None'
        elif critical_issues > 2:
            return 'A'
        elif critical_issues > 0:
            return 'AA'
        else:
            return 'AAA'
    
    def count_accessibility_features(self):
        """Count accessibility features implemented"""
        features = {
            'has_semantic_html': False,
            'has_aria_labels': False,
            'has_alt_text': False,
            'has_skip_links': False,
            'has_lang_attribute': False
        }
        
        try:
            # Check for semantic HTML
            semantic_tags = ['nav', 'main', 'article', 'section', 'aside', 'header', 'footer']
            features['has_semantic_html'] = any(self.soup.find(tag) for tag in semantic_tags)
            
            # Check for ARIA
            features['has_aria_labels'] = bool(self.soup.find(attrs={'aria-label': True}))
            
            # Check for alt text
            images_with_alt = sum(1 for img in self.soup.find_all('img') if img.get('alt'))
            features['has_alt_text'] = images_with_alt > 0
            
            # Check for skip links
            features['has_skip_links'] = bool(self.soup.find('a', {'href': ['#main', '#content']}))
            
            # Check for lang attribute
            html_tag = self.soup.find('html')
            features['has_lang_attribute'] = bool(html_tag and html_tag.get('lang'))
        except Exception as e:
            print(f"Error counting accessibility features: {e}")
        
        return features
    
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
        
        if 'missing_alt_text' in issue_types:
            recommendations.append('Add descriptive alt text to all images describing their content')
        if 'no_h1' in issue_types:
            recommendations.append('Add a single H1 heading to describe the main content')
        if 'broken_heading_hierarchy' in issue_types:
            recommendations.append('Structure headings in logical order (H1 > H2 > H3, etc.)')
        if 'unlabeled_form_inputs' in issue_types:
            recommendations.append('Associate all form inputs with label elements or aria-label')
        if 'no_skip_link' in issue_types:
            recommendations.append('Add a skip to main content link at the beginning of the page')
        if 'missing_aria_labels' in issue_types:
            recommendations.append('Add aria-label attributes to buttons without text content')
        if 'no_focusable_elements' in issue_types:
            recommendations.append('Ensure interactive elements are keyboard accessible')
        
        return recommendations
    
    def get_score(self, issue_count, max_issues):
        """Calculate accessibility score"""
        if issue_count >= max_issues:
            return 0
        return 100 - (issue_count * (100 / max_issues))
    
    def get_error_response(self):
        """Return error response"""
        return {
            'score': 0,
            'grade': 'F',
            'metrics': {},
            'issues': [{'type': 'fetch_error', 'message': 'Could not fetch website', 'severity': 'critical'}],
            'recommendations': ['Check if the URL is correct and accessible']
        }
