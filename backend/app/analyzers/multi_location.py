import random
from .base import BaseAnalyzer

class MultiLocationAnalyzer(BaseAnalyzer):
    """
    Simulates performance testing from multiple global locations.
    Analyzes how page performs in different geographic regions.
    """
    
    GLOBAL_LOCATIONS = [
        {
            'code': 'US-WA',
            'name': 'Seattle, USA',
            'region': 'North America',
            'latency_ms': 50
        },
        {
            'code': 'US-VA',
            'name': 'Virginia, USA',
            'region': 'North America',
            'latency_ms': 60
        },
        {
            'code': 'EU-UK',
            'name': 'London, UK',
            'region': 'Europe',
            'latency_ms': 100
        },
        {
            'code': 'EU-DE',
            'name': 'Frankfurt, Germany',
            'region': 'Europe',
            'latency_ms': 110
        },
        {
            'code': 'ASIA-SG',
            'name': 'Singapore',
            'region': 'Asia Pacific',
            'latency_ms': 200
        },
        {
            'code': 'ASIA-JP',
            'name': 'Tokyo, Japan',
            'region': 'Asia Pacific',
            'latency_ms': 180
        },
        {
            'code': 'ASIA-IN',
            'name': 'Mumbai, India',
            'region': 'Asia Pacific',
            'latency_ms': 220
        },
        {
            'code': 'AUS-SY',
            'name': 'Sydney, Australia',
            'region': 'Asia Pacific',
            'latency_ms': 250
        },
        {
            'code': 'SA-BR',
            'name': 'São Paulo, Brazil',
            'region': 'South America',
            'latency_ms': 180
        }
    ]
    
    def analyze(self):
        self.issues = []
        self.recommendations = []
        
        # Test from multiple locations
        location_results = self._test_all_locations()
        
        # Analyze results
        metrics = self._calculate_location_metrics(location_results)
        
        # Score based on performance consistency
        score = self._calculate_location_score(location_results)
        
        return {
            'score': score,
            'grade': self._get_grade(score),
            'metrics': metrics,
            'locations': location_results,
            'issues': self.issues,
            'recommendations': self.recommendations
        }
    
    def _test_all_locations(self):
        """Simulate testing from all global locations"""
        results = []
        base_time = self.fetch_time if self.fetch_time else 1000
        
        for location in self.GLOBAL_LOCATIONS:
            # Add latency based on location
            latency_factor = 1 + (location['latency_ms'] / 1000)
            total_time = int(base_time * latency_factor)
            
            # Add some variance
            variance = random.randint(-50, 50)
            total_time = max(100, total_time + variance)
            
            results.append({
                'location_code': location['code'],
                'location_name': location['name'],
                'region': location['region'],
                'base_latency_ms': location['latency_ms'],
                'page_load_time_ms': total_time,
                'ttfb_ms': int(total_time * 0.2),  # Time to First Byte
                'fcp_ms': int(total_time * 0.4),   # First Contentful Paint
                'lcp_ms': int(total_time * 0.7),   # Largest Contentful Paint
                'status': 'Pass' if total_time < 3000 else 'Warn' if total_time < 5000 else 'Fail',
                'speed_index': int(total_time * 0.6),
                'fully_loaded_ms': total_time
            })
        
        return results
    
    def _calculate_location_metrics(self, location_results):
        """Calculate aggregate metrics across locations"""
        if not location_results:
            return {}
        
        times = [r['page_load_time_ms'] for r in location_results]
        
        return {
            'fastest_region': min(location_results, key=lambda x: x['page_load_time_ms']),
            'slowest_region': max(location_results, key=lambda x: x['page_load_time_ms']),
            'average_load_time_ms': int(sum(times) / len(times)),
            'median_load_time_ms': sorted(times)[len(times) // 2],
            'performance_variance': max(times) - min(times),
            'locations_tested': len(location_results),
            'pass_count': sum(1 for r in location_results if r['status'] == 'Pass'),
            'regions_covered': len(set(r['region'] for r in location_results))
        }
    
    def _calculate_location_score(self, location_results):
        """Calculate score based on geographic consistency"""
        if not location_results:
            return 50
        
        score = 100
        times = [r['page_load_time_ms'] for r in location_results]
        
        # Penalize slow regions
        slow_locations = sum(1 for t in times if t > 3000)
        score -= min(25, slow_locations * 3)
        
        # Penalize performance variance
        variance = max(times) - min(times)
        if variance > 2000:
            score -= 20
        elif variance > 1000:
            score -= 10
        
        # Reward consistent performance
        pass_count = sum(1 for r in location_results if r['status'] == 'Pass')
        score += min(15, pass_count)
        
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
