"""Mobile Optimization Analyzer"""
from app.analyzers.base import BaseAnalyzer

class MobileOptimizationAnalyzer(BaseAnalyzer):
    """Analyze mobile optimization and responsiveness"""
    
    def analyze(self):
        """Perform mobile optimization analysis"""
        if not self.soup:
            return self.get_error_response()
        
        issues = []
        metrics = {}
        
        # Check viewport
        viewport_issues = self.check_viewport()
        issues.extend(viewport_issues)
        
        # Check text sizing
        text_issues = self.check_text_sizing()
        issues.extend(text_issues)
        
        # Check touch targets
        touch_issues = self.check_touch_targets()
        issues.extend(touch_issues)
        
        # Check mobile-friendly meta
        meta_issues = self.check_mobile_meta()
        issues.extend(meta_issues)
        
        # Check for mobile blocking content
        blocking_issues = self.check_blocking_content()
        issues.extend(blocking_issues)
        
        # Calculate mobile score
        mobile_score = self.calculate_mobile_score()
        metrics['mobile_score'] = mobile_score
        
        # Check responsive design
        responsive = self.check_responsive_design()
        metrics['responsive_design'] = responsive
        
        score = self.get_score(len(issues), 40)
        
        return {
            'score': score,
            'grade': self.get_grade(score),
            'metrics': metrics,
            'issues': issues,
            'recommendations': self.get_recommendations(issues)
        }
    
    def check_viewport(self):
        """Check viewport meta tag"""
        issues = []
        
        try:
            viewport = self.soup.find('meta', {'name': 'viewport'})
            
            if not viewport:
                issues.append({
                    'type': 'missing_viewport',
                    'message': 'Viewport meta tag not found',
                    'severity': 'critical'
                })
            else:
                content = viewport.get('content', '')
                if 'width=device-width' not in content:
                    issues.append({
                        'type': 'invalid_viewport',
                        'message': f'Viewport should include width=device-width. Current: {content}',
                        'severity': 'high'
                    })
                
                if 'initial-scale=1' not in content:
                    issues.append({
                        'type': 'missing_initial_scale',
                        'message': 'Viewport missing initial-scale=1',
                        'severity': 'medium'
                    })
        except Exception as e:
            print(f"Error checking viewport: {e}")
        
        return issues
    
    def check_text_sizing(self):
        """Check for appropriate text sizing"""
        issues = []
        
        try:
            # Check for font-size less than 12px
            styles = self.soup.find_all('style')
            for style in styles:
                if style.string and 'font-size:' in style.string.lower():
                    # Simple heuristic check
                    if 'font-size: 1px' in style.string.lower() or 'font-size: 2px' in style.string.lower():
                        issues.append({
                            'type': 'too_small_text',
                            'message': 'Found extremely small font sizes (< 12px)',
                            'severity': 'high'
                        })
        except Exception as e:
            print(f"Error checking text sizing: {e}")
        
        return issues
    
    def check_touch_targets(self):
        """Check for adequate touch target sizes"""
        issues = []
        
        try:
            # Check buttons and links
            buttons = self.soup.find_all('button')
            links = self.soup.find_all('a')
            
            total_interactive = len(buttons) + len(links)
            
            if total_interactive > 0:
                # Check for inline buttons/links that might be too small
                small_targets = 0
                for elem in buttons + links:
                    style = elem.get('style', '').lower()
                    if 'padding' not in style and not elem.find('span'):
                        small_targets += 1
                
                if small_targets > total_interactive * 0.2:
                    issues.append({
                        'type': 'small_touch_targets',
                        'message': f'{small_targets} interactive elements may have inadequate touch targets',
                        'severity': 'medium'
                    })
        except Exception as e:
            print(f"Error checking touch targets: {e}")
        
        return issues
    
    def check_mobile_meta(self):
        """Check for mobile-specific meta tags"""
        issues = []
        
        try:
            # Check for theme-color
            theme_color = self.soup.find('meta', {'name': 'theme-color'})
            if not theme_color:
                issues.append({
                    'type': 'no_theme_color',
                    'message': 'Missing theme-color meta tag (improves mobile appearance)',
                    'severity': 'low'
                })
            
            # Check for apple-mobile-web-app-capable
            apple_capable = self.soup.find('meta', {'name': 'apple-mobile-web-app-capable'})
            if not apple_capable:
                issues.append({
                    'type': 'not_app_capable',
                    'message': 'Missing apple-mobile-web-app-capable meta tag',
                    'severity': 'low'
                })
        except Exception as e:
            print(f"Error checking mobile meta: {e}")
        
        return issues
    
    def check_blocking_content(self):
        """Check for content that might block mobile users"""
        issues = []
        
        try:
            # Check for Flash
            if self.soup.find('embed') or self.soup.find('object'):
                issues.append({
                    'type': 'flash_content',
                    'message': 'Page contains embedded Flash content (not mobile-friendly)',
                    'severity': 'high'
                })
            
            # Check for unresponsive iframes
            iframes = self.soup.find_all('iframe')
            if len(iframes) > 5:
                issues.append({
                    'type': 'many_iframes',
                    'message': f'Found {len(iframes)} iframes which may not be responsive',
                    'severity': 'medium'
                })
        except Exception as e:
            print(f"Error checking blocking content: {e}")
        
        return issues
    
    def calculate_mobile_score(self):
        """Calculate mobile-specific score (0-100)"""
        score = 50  # Start with baseline
        
        try:
            # Check viewport
            if self.soup.find('meta', {'name': 'viewport'}):
                score += 10
            
            # Check responsive images
            images = self.soup.find_all('img')
            responsive_images = sum(1 for img in images if 'srcset' in img.attrs or 'sizes' in img.attrs)
            if images:
                score += (responsive_images / len(images)) * 15
            
            # Check media queries (if CSS is present)
            if self.soup.find('style'):
                score += 10
            
            # Check touch-friendly design
            buttons = self.soup.find_all('button')
            if len(buttons) > 0:
                score += 10
            
            # Check mobile-specific features
            if self.soup.find('meta', {'name': 'theme-color'}):
                score += 5
            
        except Exception as e:
            print(f"Error calculating mobile score: {e}")
        
        return min(100, score)
    
    def check_responsive_design(self):
        """Check for responsive design implementation"""
        result = {
            'has_viewport': False,
            'has_media_queries': False,
            'has_responsive_images': False,
            'has_flexible_layout': False
        }
        
        try:
            # Check viewport
            result['has_viewport'] = bool(self.soup.find('meta', {'name': 'viewport'}))
            
            # Check media queries
            styles = self.soup.find_all('style')
            has_media_queries = any('@media' in str(style) for style in styles)
            result['has_media_queries'] = has_media_queries
            
            # Check responsive images
            images = self.soup.find_all('img')
            responsive_images = sum(1 for img in images if 'srcset' in img.attrs)
            result['has_responsive_images'] = responsive_images > 0
            
            # Check for flexible layout (CSS Grid or Flexbox)
            styles = self.soup.find_all('style')
            styles_text = ''.join(str(s) for s in styles).lower()
            result['has_flexible_layout'] = 'display: flex' in styles_text or 'display: grid' in styles_text
        except Exception as e:
            print(f"Error checking responsive design: {e}")
        
        return result
    
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
        
        if 'missing_viewport' in issue_types:
            recommendations.append('Add viewport meta tag: <meta name="viewport" content="width=device-width, initial-scale=1">')
        if 'too_small_text' in issue_types:
            recommendations.append('Increase font sizes to at least 12px for better mobile readability')
        if 'small_touch_targets' in issue_types:
            recommendations.append('Ensure touch targets are at least 48x48 pixels')
        if 'flash_content' in issue_types:
            recommendations.append('Replace Flash content with HTML5 video or remove blocking content')
        if 'not_app_capable' in issue_types:
            recommendations.append('Add apple-mobile-web-app-capable meta tag for better iOS experience')
        
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
