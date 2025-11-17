import random
from .base import BaseAnalyzer

class DeviceSimulationAnalyzer(BaseAnalyzer):
    """
    Simulates page performance across different devices and network conditions.
    Tests responsive design and mobile-first optimization.
    """
    
    DEVICES = [
        {
            'name': 'Desktop - Chrome',
            'category': 'desktop',
            'viewport': '1920x1080',
            'network': '4G',
            'ua': 'Chrome Desktop',
            'cpu_throttle': 1.0,
            'bandwidth_mbps': 25
        },
        {
            'name': 'Laptop - Safari',
            'category': 'laptop',
            'viewport': '1440x900',
            'network': 'WiFi',
            'ua': 'Safari Laptop',
            'cpu_throttle': 1.0,
            'bandwidth_mbps': 30
        },
        {
            'name': 'iPhone 15 - Safari',
            'category': 'mobile',
            'viewport': '390x844',
            'network': '4G',
            'ua': 'Safari Mobile',
            'cpu_throttle': 1.0,
            'bandwidth_mbps': 10
        },
        {
            'name': 'iPhone 12 - Safari',
            'category': 'mobile',
            'viewport': '390x844',
            'network': '3G',
            'ua': 'Safari Mobile',
            'cpu_throttle': 1.2,
            'bandwidth_mbps': 3
        },
        {
            'name': 'Samsung Galaxy S24 - Chrome',
            'category': 'mobile',
            'viewport': '360x800',
            'network': '4G',
            'ua': 'Chrome Mobile',
            'cpu_throttle': 1.1,
            'bandwidth_mbps': 8
        },
        {
            'name': 'iPad Pro - Safari',
            'category': 'tablet',
            'viewport': '1024x1366',
            'network': 'WiFi',
            'ua': 'Safari Tablet',
            'cpu_throttle': 1.0,
            'bandwidth_mbps': 25
        },
        {
            'name': 'Samsung Galaxy Tab S10 - Chrome',
            'category': 'tablet',
            'viewport': '1920x1200',
            'network': '4G',
            'ua': 'Chrome Tablet',
            'cpu_throttle': 1.0,
            'bandwidth_mbps': 12
        },
        {
            'name': 'Low-End Android - Chrome',
            'category': 'mobile',
            'viewport': '360x640',
            'network': '2G',
            'ua': 'Chrome Mobile',
            'cpu_throttle': 2.0,
            'bandwidth_mbps': 0.5
        }
    ]
    
    def analyze(self):
        self.issues = []
        self.recommendations = []
        
        # Test on multiple devices
        device_results = self._test_all_devices()
        
        # Analyze results
        metrics = self._calculate_device_metrics(device_results)
        
        # Score based on cross-device performance
        score = self._calculate_device_score(device_results)
        
        # Add recommendations for poor performers
        self._add_device_recommendations(device_results)
        
        return {
            'score': score,
            'grade': self._get_grade(score),
            'metrics': metrics,
            'devices': device_results,
            'issues': self.issues,
            'recommendations': self.recommendations
        }
    
    def _test_all_devices(self):
        """Simulate testing on all device types"""
        results = []
        # Calculate base load time from response
        base_time = int(self.response.elapsed.total_seconds() * 1000) if self.response and hasattr(self.response, 'elapsed') else 1000
        
        for device in self.DEVICES:
            # Calculate load time based on device capabilities
            load_time = int(base_time * device['cpu_throttle'])
            
            # Apply bandwidth throttling
            bandwidth_factor = 25 / device['bandwidth_mbps'] if device['bandwidth_mbps'] > 0 else 10
            load_time = int(load_time * (bandwidth_factor / 10))
            
            # Add variance
            variance = random.randint(-100, 100)
            load_time = max(200, load_time + variance)
            
            # Determine pass/fail
            if device['category'] == 'mobile':
                threshold = 2500
            elif device['category'] == 'tablet':
                threshold = 3000
            else:
                threshold = 3500
            
            status = 'Pass' if load_time < threshold else 'Warn' if load_time < threshold * 1.5 else 'Fail'
            
            results.append({
                'device_name': device['name'],
                'category': device['category'],
                'viewport': device['viewport'],
                'network': device['network'],
                'cpu_throttle': device['cpu_throttle'],
                'bandwidth_mbps': device['bandwidth_mbps'],
                'page_load_time_ms': load_time,
                'fcp_ms': int(load_time * 0.4),
                'lcp_ms': int(load_time * 0.7),
                'tti_ms': int(load_time * 0.8),  # Time to Interactive
                'status': status,
                'responsive': self._check_responsive(device['viewport']),
                'mobile_friendly': self._check_mobile_friendly(device)
            })
        
        return results
    
    def _check_responsive(self, viewport):
        """Check if page is responsive for viewport"""
        # Check for viewport meta tag
        if self.html:
            if 'viewport' in self.html.lower():
                return True
        return False
    
    def _check_mobile_friendly(self, device):
        """Check if page is mobile-friendly"""
        if device['category'] != 'mobile':
            return True
        
        # Check for common mobile-friendly indicators
        if self.html:
            checks = [
                'viewport' in self.html.lower(),
                'mobile' in self.html.lower(),
                '@media' in self.html,
            ]
            return sum(checks) >= 2
        return False
    
    def _calculate_device_metrics(self, device_results):
        """Calculate aggregate metrics across devices"""
        if not device_results:
            return {}
        
        mobile_results = [r for r in device_results if r['category'] == 'mobile']
        desktop_results = [r for r in device_results if r['category'] == 'desktop']
        tablet_results = [r for r in device_results if r['category'] == 'tablet']
        
        def avg_time(results):
            return int(sum(r['page_load_time_ms'] for r in results) / len(results)) if results else 0
        
        return {
            'average_mobile_load_time_ms': avg_time(mobile_results),
            'average_desktop_load_time_ms': avg_time(desktop_results),
            'average_tablet_load_time_ms': avg_time(tablet_results),
            'mobile_pass_rate': f"{sum(1 for r in mobile_results if r['status'] == 'Pass') / len(mobile_results) * 100:.0f}%" if mobile_results else "N/A",
            'desktop_pass_rate': f"{sum(1 for r in desktop_results if r['status'] == 'Pass') / len(desktop_results) * 100:.0f}%" if desktop_results else "N/A",
            'responsive_design': all(r['responsive'] for r in device_results),
            'mobile_friendly': all(r['mobile_friendly'] for r in mobile_results)
        }
    
    def _calculate_device_score(self, device_results):
        """Calculate score based on cross-device performance"""
        if not device_results:
            return 50
        
        score = 100
        
        # Penalize failed tests
        failures = sum(1 for r in device_results if r['status'] == 'Fail')
        score -= min(30, failures * 5)
        
        # Penalize for slow mobile performance
        mobile_results = [r for r in device_results if r['category'] == 'mobile']
        if mobile_results:
            avg_mobile = sum(r['page_load_time_ms'] for r in mobile_results) / len(mobile_results)
            if avg_mobile > 3000:
                score -= 20
            elif avg_mobile > 2000:
                score -= 10
        
        # Reward mobile-friendly
        if all(r['mobile_friendly'] for r in mobile_results):
            score += 10
        
        # Reward responsive
        if all(r['responsive'] for r in device_results):
            score += 10
        
        return max(0, score)
    
    def _add_device_recommendations(self, device_results):
        """Add recommendations based on device performance"""
        # Check mobile performance
        mobile_results = [r for r in device_results if r['category'] == 'mobile']
        if mobile_results:
            avg_mobile = sum(r['page_load_time_ms'] for r in mobile_results) / len(mobile_results)
            if avg_mobile > 2500:
                self.recommendations.append(
                    "Optimize for mobile devices - average mobile load time is above 2.5s. Consider lazy loading images and minifying CSS/JS."
                )
        
        # Check low-end devices
        low_end = [r for r in device_results if 'Low-End' in r['device_name']]
        if low_end and low_end[0]['status'] == 'Fail':
            self.recommendations.append(
                "Improve performance on low-end devices. Use progressive enhancement and lightweight alternatives where possible."
            )
        
        # Check responsive design
        if not all(r['responsive'] for r in device_results):
            self.recommendations.append(
                "Add viewport meta tag and ensure responsive CSS for all breakpoints."
            )
    
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
