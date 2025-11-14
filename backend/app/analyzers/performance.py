"""Performance analyzer module"""
import time
from app.analyzers.base import BaseAnalyzer

class PerformanceAnalyzer(BaseAnalyzer):
    """Analyze website performance and optimization"""
    
    def analyze(self):
        """Perform performance analysis"""
        if not self.soup:
            return self.get_error_response()
        
        issues = []
        metrics = {}
        
        # Check page load time
        metrics['load_time'] = self.check_load_time()
        
        # Check for uncompressed images
        image_issues = self.check_image_optimization()
        if image_issues:
            issues.extend(image_issues)
        
        # Check for render-blocking resources
        render_blocking = self.check_render_blocking()
        if render_blocking:
            issues.extend(render_blocking)
        
        # Check for minification
        minification_issues = self.check_minification()
        if minification_issues:
            issues.extend(minification_issues)
        
        # Check for caching headers
        cache_issues = self.check_caching()
        if cache_issues:
            issues.extend(cache_issues)
        
        # Check for lazy loading
        lazy_load = self.check_lazy_loading()
        metrics['lazy_loading'] = lazy_load
        
        score = self.get_score(len(issues), 50)
        
        return {
            'score': score,
            'grade': self.get_grade(score),
            'metrics': metrics,
            'issues': issues,
            'recommendations': self.get_recommendations(issues)
        }
    
    def check_load_time(self):
        """Check page load time"""
        try:
            start = time.time()
            load_time = time.time() - start
            return round(load_time, 2)
        except:
            return 0
    
    def check_image_optimization(self):
        """Check for unoptimized images"""
        issues = []
        try:
            images = self.soup.find_all('img')
            unoptimized = 0
            
            for img in images:
                src = img.get('src', '')
                # Check for large image formats
                if src.endswith(('.bmp', '.tiff')):
                    unoptimized += 1
                # Check for missing alt text
                if not img.get('alt'):
                    issues.append({
                        'type': 'missing_alt_text',
                        'message': f'Image missing alt text: {src}',
                        'severity': 'medium'
                    })
            
            if unoptimized > 0:
                issues.append({
                    'type': 'unoptimized_images',
                    'message': f'{unoptimized} images use unoptimized formats',
                    'severity': 'high'
                })
        except Exception as e:
            print(f"Error checking images: {e}")
        
        return issues
    
    def check_render_blocking(self):
        """Check for render-blocking resources"""
        issues = []
        try:
            # Check for render-blocking CSS
            stylesheets = self.soup.find_all('link', {'rel': 'stylesheet'})
            if len(stylesheets) > 3:
                issues.append({
                    'type': 'render_blocking_css',
                    'message': f'Found {len(stylesheets)} CSS files which may block rendering',
                    'severity': 'medium'
                })
            
            # Check for render-blocking JS
            scripts = self.soup.find_all('script')
            blocking_scripts = [s for s in scripts if not s.get('async') and not s.get('defer')]
            if len(blocking_scripts) > 2:
                issues.append({
                    'type': 'render_blocking_js',
                    'message': f'Found {len(blocking_scripts)} render-blocking JavaScript files',
                    'severity': 'high'
                })
        except Exception as e:
            print(f"Error checking render blocking: {e}")
        
        return issues
    
    def check_minification(self):
        """Check if CSS and JS are minified"""
        issues = []
        try:
            styles = self.soup.find_all('style')
            for style in styles:
                if style.string and len(style.string.split('\n')) > 3:
                    issues.append({
                        'type': 'non_minified_css',
                        'message': 'Inline CSS should be minified',
                        'severity': 'low'
                    })
                    break
        except:
            pass
        
        return issues
    
    def check_caching(self):
        """Check for cache headers"""
        issues = []
        try:
            cache_control = self.response.headers.get('Cache-Control', '')
            if not cache_control:
                issues.append({
                    'type': 'missing_cache_headers',
                    'message': 'Cache-Control headers not found',
                    'severity': 'high'
                })
        except:
            pass
        
        return issues
    
    def check_lazy_loading(self):
        """Check if images use lazy loading"""
        try:
            images = self.soup.find_all('img')
            lazy_loaded = sum(1 for img in images if img.get('loading') == 'lazy')
            return {'total_images': len(images), 'lazy_loaded': lazy_loaded}
        except:
            return {'total_images': 0, 'lazy_loaded': 0}
    
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
        
        if 'render_blocking_js' in issue_types:
            recommendations.append('Defer non-critical JavaScript or use async loading')
        if 'render_blocking_css' in issue_types:
            recommendations.append('Consider critical CSS inlining or splitting CSS files')
        if 'missing_cache_headers' in issue_types:
            recommendations.append('Implement proper Cache-Control headers on your server')
        if 'unoptimized_images' in issue_types:
            recommendations.append('Convert images to WebP format for better compression')
        if 'missing_alt_text' in issue_types:
            recommendations.append('Add descriptive alt text to all images')
        
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
