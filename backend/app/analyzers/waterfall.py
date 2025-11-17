from datetime import datetime
import time
from .base import BaseAnalyzer

class WaterfallAnalyzer(BaseAnalyzer):
    """
    Generates waterfall chart data showing resource load timeline.
    Simulates DNS, TCP, Request, Response, Render times for each resource.
    """
    
    def analyze(self):
        self.issues = []
        self.recommendations = []
        
        # Generate waterfall data for resources
        waterfall_data = self._generate_waterfall_data()
        
        # Calculate metrics from waterfall
        metrics = self._calculate_waterfall_metrics(waterfall_data)
        
        # Score based on overall load efficiency
        score = self._calculate_waterfall_score(waterfall_data)
        
        return {
            'score': score,
            'grade': self._get_grade(score),
            'metrics': metrics,
            'waterfall': waterfall_data,
            'issues': self.issues,
            'recommendations': self.recommendations
        }
    
    def _generate_waterfall_data(self):
        """Generate simulated waterfall chart data"""
        resources = []
        current_time = 0  # milliseconds
        
        # HTML document
        resources.append(self._create_resource(
            type='document',
            name='index.html',
            size=self._estimate_html_size(),
            start_time=current_time,
            dns=50,
            tcp=100,
            request=50,
            response=200
        ))
        current_time += 400
        
        # CSS files
        css_files = self._extract_css_files()
        for i, css in enumerate(css_files[:5]):  # Limit to 5 CSS files
            resources.append(self._create_resource(
                type='stylesheet',
                name=css.split('/')[-1] or 'style.css',
                size=30000 + (i * 5000),
                start_time=current_time + (i * 50),
                dns=30,
                tcp=80,
                request=30,
                response=100
            ))
        
        current_time += 500
        
        # JavaScript files
        js_files = self._extract_js_files()
        for i, js in enumerate(js_files[:8]):  # Limit to 8 JS files
            resources.append(self._create_resource(
                type='script',
                name=js.split('/')[-1] or f'script{i}.js',
                size=50000 + (i * 10000),
                start_time=current_time + (i * 100),
                dns=20,
                tcp=60,
                request=20,
                response=150
            ))
        
        current_time += 1000
        
        # Images
        image_files = self._extract_images()
        for i, img in enumerate(image_files[:10]):  # Limit to 10 images
            resources.append(self._create_resource(
                type='image',
                name=img.split('/')[-1] or f'image{i}.jpg',
                size=100000 + (i * 50000),
                start_time=current_time + (i * 200),
                dns=10,
                tcp=50,
                request=10,
                response=200 + (i * 50)
            ))
        
        return sorted(resources, key=lambda x: x['start_time'])
    
    def _create_resource(self, type, name, size, start_time, dns, tcp, request, response):
        """Create a single resource entry for waterfall"""
        return {
            'type': type,
            'name': name,
            'size': size,
            'size_kb': round(size / 1024, 2),
            'start_time': start_time,
            'dns_time': dns,
            'tcp_time': tcp,
            'request_time': request,
            'response_time': response,
            'total_time': dns + tcp + request + response,
            'end_time': start_time + dns + tcp + request + response,
            'blocked': 0,
            'status': 200,
            'mime_type': self._get_mime_type(name)
        }
    
    def _estimate_html_size(self):
        """Estimate HTML document size"""
        return len(self.html.encode('utf-8')) if self.html else 50000
    
    def _extract_css_files(self):
        """Extract CSS file references from HTML"""
        if not self.html:
            return ['style.css']
        
        import re
        css_pattern = r'href=["\']([^"\']*\.css[^"\']*)["\'"]'
        matches = re.findall(css_pattern, self.html)
        return matches or ['style.css']
    
    def _extract_js_files(self):
        """Extract JavaScript file references from HTML"""
        if not self.html:
            return ['script.js']
        
        import re
        js_pattern = r'src=["\']([^"\']*\.js[^"\']*)["\'"]'
        matches = re.findall(js_pattern, self.html)
        return matches or ['script.js']
    
    def _extract_images(self):
        """Extract image file references from HTML"""
        if not self.html:
            return ['image.jpg']
        
        import re
        img_pattern = r'src=["\']([^"\']*(?:\.jpg|\.png|\.gif|\.webp|\.svg)[^"\']*)["\'"]'
        matches = re.findall(img_pattern, self.html)
        return matches[:10] or ['image.jpg']
    
    def _get_mime_type(self, filename):
        """Determine MIME type from filename"""
        if '.css' in filename:
            return 'text/css'
        elif '.js' in filename:
            return 'application/javascript'
        elif any(x in filename for x in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']):
            return 'image/jpeg'
        return 'text/html'
    
    def _calculate_waterfall_metrics(self, waterfall_data):
        """Calculate aggregate metrics from waterfall"""
        if not waterfall_data:
            return {}
        
        total_requests = len(waterfall_data)
        total_size = sum(r['size'] for r in waterfall_data)
        total_time = max(r['end_time'] for r in waterfall_data) if waterfall_data else 0
        
        # Count by type
        by_type = {}
        for resource in waterfall_data:
            type_name = resource['type']
            if type_name not in by_type:
                by_type[type_name] = {'count': 0, 'size': 0, 'time': 0}
            by_type[type_name]['count'] += 1
            by_type[type_name]['size'] += resource['size']
            by_type[type_name]['time'] += resource['total_time']
        
        return {
            'total_requests': total_requests,
            'total_size_kb': round(total_size / 1024, 2),
            'total_time_ms': total_time,
            'page_load_time_ms': total_time,
            'by_type': by_type,
            'critical_path_time': total_time * 0.7  # Rough estimate
        }
    
    def _calculate_waterfall_score(self, waterfall_data):
        """Calculate efficiency score from waterfall"""
        if not waterfall_data:
            return 50
        
        score = 100
        
        # Penalize for slow resources
        slow_resources = sum(1 for r in waterfall_data if r['total_time'] > 500)
        score -= min(30, slow_resources * 5)
        
        # Penalize for large payloads
        total_size_kb = sum(r['size'] for r in waterfall_data) / 1024
        if total_size_kb > 2000:
            score -= 20
        elif total_size_kb > 1000:
            score -= 10
        
        # Penalize for many requests
        if len(waterfall_data) > 100:
            score -= 20
        elif len(waterfall_data) > 50:
            score -= 10
        
        return max(0, score)
    
    def _get_grade(self, score):
        if score >= 85:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 55:
            return 'C'
        elif score >= 40:
            return 'D'
        else:
            return 'F'
