"""SEO analyzer module"""
from app.analyzers.base import BaseAnalyzer

class SEOAnalyzer(BaseAnalyzer):
    """Analyze website SEO"""
    
    def analyze(self):
        """Perform SEO analysis"""
        if not self.soup:
            return self.get_error_response()
        
        issues = []
        metrics = {}
        
        # Check meta tags
        meta_issues = self.check_meta_tags()
        issues.extend(meta_issues)
        
        # Check headings
        heading_issues = self.check_headings()
        issues.extend(heading_issues)
        
        # Check for alt tags
        alt_issues = self.check_alt_tags()
        issues.extend(alt_issues)
        
        # Check URL structure
        url_issues = self.check_url_structure()
        issues.extend(url_issues)
        
        # Check for broken links
        broken_links = self.check_broken_links()
        metrics['broken_links'] = broken_links
        if broken_links > 0:
            issues.append({
                'type': 'broken_links',
                'message': f'Found {broken_links} broken internal links',
                'severity': 'high'
            })
        
        # Check robots.txt
        robots = self.check_robots_txt()
        metrics['has_robots_txt'] = robots
        if not robots:
            issues.append({
                'type': 'no_robots_txt',
                'message': 'robots.txt not found',
                'severity': 'low'
            })
        
        # Check sitemap
        sitemap = self.check_sitemap()
        metrics['has_sitemap'] = sitemap
        if not sitemap:
            issues.append({
                'type': 'no_sitemap',
                'message': 'sitemap.xml not found',
                'severity': 'low'
            })
        
        score = self.get_score(len(issues), 50)
        
        return {
            'score': score,
            'grade': self.get_grade(score),
            'metrics': metrics,
            'issues': issues,
            'recommendations': self.get_recommendations(issues)
        }
    
    def check_meta_tags(self):
        """Check for essential meta tags"""
        issues = []
        
        try:
            # Check meta description
            meta_desc = self.soup.find('meta', {'name': 'description'})
            if not meta_desc:
                issues.append({
                    'type': 'missing_meta_description',
                    'message': 'Meta description not found',
                    'severity': 'high'
                })
            else:
                content = meta_desc.get('content', '')
                if len(content) < 50 or len(content) > 160:
                    issues.append({
                        'type': 'meta_description_length',
                        'message': f'Meta description length is {len(content)}, should be 50-160 characters',
                        'severity': 'medium'
                    })
            
            # Check meta keywords
            meta_keywords = self.soup.find('meta', {'name': 'keywords'})
            if not meta_keywords:
                issues.append({
                    'type': 'missing_keywords',
                    'message': 'Meta keywords not found',
                    'severity': 'low'
                })
            
            # Check viewport
            viewport = self.soup.find('meta', {'name': 'viewport'})
            if not viewport:
                issues.append({
                    'type': 'missing_viewport',
                    'message': 'Viewport meta tag not found (mobile not optimized)',
                    'severity': 'high'
                })
        except Exception as e:
            print(f"Error checking meta tags: {e}")
        
        return issues
    
    def check_headings(self):
        """Check heading structure"""
        issues = []
        
        try:
            h1_tags = self.soup.find_all('h1')
            
            if len(h1_tags) == 0:
                issues.append({
                    'type': 'missing_h1',
                    'message': 'No H1 tag found on page',
                    'severity': 'high'
                })
            elif len(h1_tags) > 1:
                issues.append({
                    'type': 'multiple_h1',
                    'message': f'Multiple H1 tags found ({len(h1_tags)}), should have only one',
                    'severity': 'medium'
                })
            
            # Check heading hierarchy
            headings = self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if len(headings) < 3:
                issues.append({
                    'type': 'poor_heading_structure',
                    'message': 'Poor heading hierarchy, consider adding more structured headings',
                    'severity': 'low'
                })
        except Exception as e:
            print(f"Error checking headings: {e}")
        
        return issues
    
    def check_alt_tags(self):
        """Check for alt tags on images"""
        issues = []
        
        try:
            images = self.soup.find_all('img')
            missing_alt = 0
            
            for img in images:
                if not img.get('alt') or img.get('alt').strip() == '':
                    missing_alt += 1
            
            if missing_alt > 0:
                issues.append({
                    'type': 'missing_alt_tags',
                    'message': f'{missing_alt} images missing alt text (out of {len(images)})',
                    'severity': 'medium'
                })
        except Exception as e:
            print(f"Error checking alt tags: {e}")
        
        return issues
    
    def check_url_structure(self):
        """Check URL structure"""
        issues = []
        
        try:
            # Check if URL is friendly
            links = self.soup.find_all('a')
            unfriendly_urls = 0
            
            for link in links:
                href = link.get('href', '')
                if href and ('=' in href or '?' in href or '#' in href):
                    unfriendly_urls += 1
            
            if unfriendly_urls > len(links) * 0.3:
                issues.append({
                    'type': 'unfriendly_urls',
                    'message': 'Many URLs are not SEO-friendly (contain parameters/fragments)',
                    'severity': 'medium'
                })
        except Exception as e:
            print(f"Error checking URL structure: {e}")
        
        return issues
    
    def check_broken_links(self):
        """Check for broken internal links"""
        broken_count = 0
        
        try:
            links = self.soup.find_all('a')
            for link in links:
                href = link.get('href', '')
                if href and href.startswith('/'):
                    # This is an internal link
                    try:
                        response = self.request_url(self.url + href.lstrip('/'))
                        if response.status_code >= 400:
                            broken_count += 1
                    except:
                        pass
        except Exception as e:
            print(f"Error checking broken links: {e}")
        
        return broken_count
    
    def request_url(self, url):
        """Make a request to a URL"""
        import requests
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        return requests.head(url, headers=headers, timeout=5)
    
    def check_robots_txt(self):
        """Check if robots.txt exists"""
        try:
            from urllib.parse import urljoin
            import requests
            robots_url = urljoin(self.url, '/robots.txt')
            response = requests.head(robots_url, timeout=5)
            return response.status_code < 400
        except:
            return False
    
    def check_sitemap(self):
        """Check if sitemap.xml exists"""
        try:
            from urllib.parse import urljoin
            import requests
            sitemap_url = urljoin(self.url, '/sitemap.xml')
            response = requests.head(sitemap_url, timeout=5)
            return response.status_code < 400
        except:
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
        
        if 'missing_meta_description' in issue_types:
            recommendations.append('Add a compelling meta description (50-160 characters)')
        if 'missing_h1' in issue_types:
            recommendations.append('Add an H1 tag with your primary keyword')
        if 'missing_alt_tags' in issue_types:
            recommendations.append('Add descriptive alt text to all images')
        if 'missing_viewport' in issue_types:
            recommendations.append('Add viewport meta tag for mobile optimization')
        if 'no_sitemap' in issue_types:
            recommendations.append('Create and submit a sitemap.xml')
        if 'no_robots_txt' in issue_types:
            recommendations.append('Create a robots.txt file to guide search engines')
        
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
