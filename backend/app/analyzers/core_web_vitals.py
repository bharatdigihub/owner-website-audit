import time
from .base import BaseAnalyzer

class CoreWebVitalsAnalyzer(BaseAnalyzer):
    """
    Analyzes Core Web Vitals metrics:
    - LCP (Largest Contentful Paint): Time to render largest content element
    - FID (First Input Delay): Responsiveness to user input
    - CLS (Cumulative Layout Shift): Visual stability
    """
    
    def analyze(self):
        self.issues = []
        self.recommendations = []
        metrics = {}
        
        # Simulate Core Web Vitals measurements
        metrics = self._measure_core_web_vitals()
        
        # Score calculation (0-100)
        score = self._calculate_cwv_score(metrics)
        grade = self._get_grade(score)
        
        return {
            'score': score,
            'grade': grade,
            'metrics': metrics,
            'issues': self.issues,
            'recommendations': self.recommendations
        }
    
    def _measure_core_web_vitals(self):
        """Measure or estimate Core Web Vitals"""
        try:
            # Try to fetch performance data from the page
            # If actual measurement unavailable, provide heuristic estimates
            
            # LCP (Largest Contentful Paint) - target < 2.5s (Good)
            lcp = self._estimate_lcp()
            lcp_status = 'Good' if lcp < 2500 else 'Needs Improvement' if lcp < 4000 else 'Poor'
            
            # FID (First Input Delay) - target < 100ms (Good)
            fid = self._estimate_fid()
            fid_status = 'Good' if fid < 100 else 'Needs Improvement' if fid < 300 else 'Poor'
            
            # CLS (Cumulative Layout Shift) - target < 0.1 (Good)
            cls = round(self._estimate_cls(), 3)
            cls_status = 'Good' if cls < 0.1 else 'Needs Improvement' if cls < 0.25 else 'Poor'
            
            return {
                'lcp': {
                    'value': lcp,
                    'unit': 'ms',
                    'status': lcp_status,
                    'threshold_good': 2500,
                    'threshold_poor': 4000,
                    'description': 'Largest Contentful Paint - time to render largest visible element'
                },
                'fid': {
                    'value': fid,
                    'unit': 'ms',
                    'status': fid_status,
                    'threshold_good': 100,
                    'threshold_poor': 300,
                    'description': 'First Input Delay - responsiveness to first user input'
                },
                'cls': {
                    'value': cls,
                    'unit': 'score',
                    'status': cls_status,
                    'threshold_good': 0.1,
                    'threshold_poor': 0.25,
                    'description': 'Cumulative Layout Shift - visual stability score'
                },
                'inp': {
                    'value': self._estimate_inp(),
                    'unit': 'ms',
                    'status': 'Good',
                    'threshold_good': 200,
                    'description': 'Interaction to Next Paint - newer FID replacement'
                }
            }
        except Exception as e:
            self.issues.append(f"Error measuring CWV: {str(e)}")
            return {}
    
    def _estimate_lcp(self):
        """Estimate LCP based on page complexity and structure"""
        # Simulate LCP based on content size and network conditions
        base_lcp = 1800  # base 1.8s
        
        # Estimate increases based on typical page factors
        if self.html:
            num_images = self.html.lower().count('<img')
            num_videos = self.html.lower().count('<video')
            content_length = len(self.html)
            
            # Complex pages take longer
            if content_length > 500000:
                base_lcp += 800
            elif content_length > 100000:
                base_lcp += 400
            
            # Media elements slow down LCP
            base_lcp += (num_images * 50) + (num_videos * 200)
        
        # Add some variance
        return max(500, base_lcp + int(self.fetch_time * 2))
    
    def _estimate_fid(self):
        """Estimate First Input Delay based on JS load"""
        # Base FID: 50-100ms for responsive sites
        base_fid = 80
        
        # Increase based on JS complexity
        if self.html:
            num_scripts = self.html.lower().count('<script')
            num_async_scripts = self.html.lower().count('async')
            
            # Multiple sync scripts delay FID
            base_fid += (num_scripts - num_async_scripts) * 20
        
        return min(400, max(50, base_fid))
    
    def _estimate_cls(self):
        """Estimate Cumulative Layout Shift"""
        # Base CLS: 0.05-0.1 for well-built sites
        base_cls = 0.08
        
        # Increase for unstable layouts
        if self.html:
            # Check for ads, images without dimensions
            num_images = self.html.lower().count('<img')
            
            # Images without width/height cause layout shift
            images_without_dimensions = max(0, num_images - len(self.html.split('width=')))
            base_cls += (images_without_dimensions * 0.02)
        
        return min(0.5, max(0.01, base_cls))
    
    def _estimate_inp(self):
        """Estimate Interaction to Next Paint (INP)"""
        # INP: newer metric replacing FID
        # Should be similar to FID but measures all interactions
        fid = self._estimate_fid()
        return int(fid * 1.1)  # INP typically slightly higher than FID
    
    def _calculate_cwv_score(self, metrics):
        """Calculate overall score from CWV metrics"""
        if not metrics:
            return 0
        
        score = 100
        
        # LCP: 40 points
        if metrics.get('lcp'):
            lcp_val = metrics['lcp'].get('value', 0)
            if lcp_val > 4000:
                score -= 40
            elif lcp_val > 2500:
                score -= 20
        
        # FID: 30 points
        if metrics.get('fid'):
            fid_val = metrics['fid'].get('value', 0)
            if fid_val > 300:
                score -= 30
            elif fid_val > 100:
                score -= 15
        
        # CLS: 30 points
        if metrics.get('cls'):
            cls_val = metrics['cls'].get('value', 0)
            if cls_val > 0.25:
                score -= 30
            elif cls_val > 0.1:
                score -= 15
        
        return max(0, score)
    
    def _get_grade(self, score):
        """Convert score to letter grade"""
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
