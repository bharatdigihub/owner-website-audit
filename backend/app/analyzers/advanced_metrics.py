"""Advanced Metrics Analyzer - Lighthouse-inspired metrics"""
from app.analyzers.base import BaseAnalyzer

class AdvancedMetricsAnalyzer(BaseAnalyzer):
    """Analyze advanced web metrics inspired by Lighthouse"""
    
    def analyze(self):
        """Perform advanced metrics analysis"""
        if not self.soup:
            return self.get_error_response()
        
        issues = []
        metrics = {}
        
        # Calculate Core Web Vitals indicators
        vitals = self.calculate_core_web_vitals()
        metrics['core_web_vitals'] = vitals
        
        # Check resource efficiency
        resource_metrics = self.check_resource_efficiency()
        metrics['resource_efficiency'] = resource_metrics
        issues.extend(resource_metrics.get('issues', []))
        
        # Check best practices
        practices_issues = self.check_best_practices()
        issues.extend(practices_issues)
        
        # Check third-party impacts
        third_party = self.check_third_party_content()
        metrics['third_party_impact'] = third_party
        issues.extend(third_party.get('issues', []))
        
        # Check SEO score
        seo_score = self.check_advanced_seo()
        metrics['advanced_seo'] = seo_score
        
        # Calculate overall score
        score = self.calculate_advanced_score(metrics, len(issues))
        
        return {
            'score': score,
            'grade': self.get_grade(score),
            'metrics': metrics,
            'issues': issues,
            'recommendations': self.get_recommendations(issues, metrics)
        }
    
    def calculate_core_web_vitals(self):
        """Calculate Core Web Vitals indicators"""
        vitals = {
            'largest_contentful_paint': 'Good',
            'first_input_delay': 'Good',
            'cumulative_layout_shift': 'Good',
            'time_to_interactive': 'Good'
        }
        
        try:
            # Estimate LCP based on page complexity
            images = len(self.soup.find_all('img'))
            videos = len(self.soup.find_all('video'))
            
            if images + videos > 20:
                vitals['largest_contentful_paint'] = 'Needs Improvement'
            
            # Check for layout shift causes
            if self.soup.find_all('img', {'width': False}):
                vitals['cumulative_layout_shift'] = 'Needs Improvement'
            
            # Check JavaScript impact
            scripts = self.soup.find_all('script')
            if len(scripts) > 10:
                vitals['time_to_interactive'] = 'Needs Improvement'
        except Exception as e:
            print(f"Error calculating Core Web Vitals: {e}")
        
        return vitals
    
    def check_resource_efficiency(self):
        """Check resource efficiency and optimization"""
        result = {'issues': []}
        metrics = {}
        
        try:
            # Check image optimization
            images = self.soup.find_all('img')
            unoptimized_images = 0
            
            for img in images:
                src = img.get('src', '').lower()
                width = img.get('width')
                height = img.get('height')
                
                # Check for common issues
                if src.endswith('.bmp'):
                    unoptimized_images += 1
                elif not width or not height:
                    unoptimized_images += 1
            
            if unoptimized_images > 0:
                result['issues'].append({
                    'type': 'unoptimized_images',
                    'message': f'{unoptimized_images} images may not be optimized',
                    'severity': 'medium'
                })
            
            metrics['optimized_images'] = len(images) - unoptimized_images
            metrics['total_images'] = len(images)
            
            # Check for render-blocking resources
            scripts = self.soup.find_all('script')
            render_blocking = sum(1 for s in scripts if not s.get('async') and not s.get('defer'))
            
            if render_blocking > 0:
                result['issues'].append({
                    'type': 'render_blocking_scripts',
                    'message': f'{render_blocking} scripts may block rendering',
                    'severity': 'high'
                })
            
            metrics['render_blocking_scripts'] = render_blocking
            
            # Check for unused CSS
            stylesheets = self.soup.find_all('link', {'rel': 'stylesheet'})
            metrics['stylesheets'] = len(stylesheets)
            
        except Exception as e:
            print(f"Error checking resource efficiency: {e}")
        
        result['metrics'] = metrics
        return result
    
    def check_best_practices(self):
        """Check best practices"""
        issues = []
        
        try:
            # Check for HTTPS (can't verify directly, but check for mixed content indicators)
            links = self.soup.find_all(['a', 'img', 'script', 'link'])
            mixed_content = sum(1 for link in links if 'http://' in str(link.get('href', '') + link.get('src', '')))
            
            if mixed_content > 0:
                issues.append({
                    'type': 'mixed_content',
                    'message': f'{mixed_content} resources may use insecure HTTP',
                    'severity': 'high'
                })
            
            # Check for deprecated HTML
            deprecated = self.soup.find_all(['center', 'font', 'marquee'])
            if len(deprecated) > 0:
                issues.append({
                    'type': 'deprecated_html',
                    'message': f'Found {len(deprecated)} deprecated HTML elements',
                    'severity': 'medium'
                })
            
            # Check for document title
            if not self.soup.find('title'):
                issues.append({
                    'type': 'missing_title',
                    'message': 'Missing document title',
                    'severity': 'high'
                })
            
            # Check for meta description
            meta_desc = self.soup.find('meta', {'name': 'description'})
            if not meta_desc:
                issues.append({
                    'type': 'missing_meta_description',
                    'message': 'Missing meta description',
                    'severity': 'medium'
                })
        except Exception as e:
            print(f"Error checking best practices: {e}")
        
        return issues
    
    def check_third_party_content(self):
        """Check impact of third-party content"""
        result = {'issues': []}
        metrics = {}
        
        try:
            # Count third-party requests
            third_party_domains = set()
            
            # Check scripts
            scripts = self.soup.find_all('script')
            for script in scripts:
                src = script.get('src', '')
                if src and self.is_third_party_url(src):
                    domain = self.extract_domain(src)
                    third_party_domains.add(domain)
            
            # Check iframes
            iframes = self.soup.find_all('iframe')
            for iframe in iframes:
                src = iframe.get('src', '')
                if src and self.is_third_party_url(src):
                    domain = self.extract_domain(src)
                    third_party_domains.add(domain)
            
            # Check external stylesheets
            links = self.soup.find_all('link', {'rel': 'stylesheet'})
            for link in links:
                href = link.get('href', '')
                if href and self.is_third_party_url(href):
                    domain = self.extract_domain(href)
                    third_party_domains.add(domain)
            
            metrics['third_party_domains'] = len(third_party_domains)
            
            if len(third_party_domains) > 5:
                result['issues'].append({
                    'type': 'too_many_third_party',
                    'message': f'Detected {len(third_party_domains)} third-party domains',
                    'severity': 'medium'
                })
            
            metrics['third_party_list'] = list(third_party_domains)[:10]
            
        except Exception as e:
            print(f"Error checking third-party content: {e}")
        
        return result
    
    def check_advanced_seo(self):
        """Check advanced SEO metrics"""
        seo = {
            'structured_data': False,
            'open_graph': False,
            'twitter_card': False,
            'canonical_url': False,
            'robots_meta': False
        }
        
        try:
            # Check for structured data
            json_ld = self.soup.find('script', {'type': 'application/ld+json'})
            seo['structured_data'] = bool(json_ld)
            
            # Check for Open Graph
            og_tags = self.soup.find_all('meta', {'property': lambda x: x and x.startswith('og:')})
            seo['open_graph'] = len(og_tags) > 0
            
            # Check for Twitter Card
            twitter_tags = self.soup.find_all('meta', {'name': lambda x: x and x.startswith('twitter:')})
            seo['twitter_card'] = len(twitter_tags) > 0
            
            # Check for canonical URL
            canonical = self.soup.find('link', {'rel': 'canonical'})
            seo['canonical_url'] = bool(canonical)
            
            # Check for robots meta
            robots = self.soup.find('meta', {'name': 'robots'})
            seo['robots_meta'] = bool(robots)
        except Exception as e:
            print(f"Error checking advanced SEO: {e}")
        
        return seo
    
    def calculate_advanced_score(self, metrics, issue_count):
        """Calculate advanced score"""
        score = 50
        
        try:
            # Core Web Vitals contribution
            vitals = metrics.get('core_web_vitals', {})
            good_vitals = sum(1 for v in vitals.values() if v == 'Good')
            score += (good_vitals / 4) * 20
            
            # Resource efficiency
            resources = metrics.get('resource_efficiency', {})
            resource_metrics = resources.get('metrics', {})
            if resource_metrics.get('total_images', 0) > 0:
                optimization_ratio = resource_metrics.get('optimized_images', 0) / resource_metrics.get('total_images', 1)
                score += optimization_ratio * 10
            
            # Third-party impact
            third_party = metrics.get('third_party_impact', {})
            third_party_count = third_party.get('metrics', {}).get('third_party_domains', 0)
            if third_party_count <= 3:
                score += 10
            elif third_party_count <= 6:
                score += 5
            
            # SEO metrics
            seo = metrics.get('advanced_seo', {})
            seo_points = sum(1 for v in seo.values() if v is True)
            score += (seo_points / 5) * 10
            
            # Deduct for issues
            score -= min(issue_count * 2, 20)
        except Exception as e:
            print(f"Error calculating advanced score: {e}")
        
        return max(0, min(100, score))
    
    def is_third_party_url(self, url):
        """Check if URL is from a third party"""
        third_party_indicators = [
            'analytics', 'google', 'facebook', 'twitter', 'pinterest',
            'cdn', 'cloudflare', 'aws', 'adservice', 'doubleclick'
        ]
        return any(indicator in url.lower() for indicator in third_party_indicators)
    
    def extract_domain(self, url):
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc or url
        except:
            return url
    
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
    
    def get_recommendations(self, issues, metrics):
        """Get recommendations"""
        recommendations = []
        issue_types = [issue['type'] for issue in issues]
        
        if 'render_blocking_scripts' in issue_types:
            recommendations.append('Use async or defer attributes on script tags to improve page load')
        if 'unoptimized_images' in issue_types:
            recommendations.append('Optimize images: use modern formats (WebP), set width/height, use srcset')
        if 'mixed_content' in issue_types:
            recommendations.append('Use HTTPS for all resources to avoid mixed content warnings')
        if 'too_many_third_party' in issue_types:
            recommendations.append('Review and minimize third-party scripts for better performance')
        
        # Recommend structured data
        if not metrics.get('advanced_seo', {}).get('structured_data'):
            recommendations.append('Add JSON-LD structured data (Schema.org) for better search visibility')
        
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
