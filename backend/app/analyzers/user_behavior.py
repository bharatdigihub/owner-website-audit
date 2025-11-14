"""User behavior analyzer module"""
from app.analyzers.base import BaseAnalyzer

class UserBehaviorAnalyzer(BaseAnalyzer):
    """Analyze user behavior patterns"""
    
    def analyze(self):
        """Perform user behavior analysis"""
        if not self.soup:
            return self.get_error_response()
        
        insights = []
        metrics = {}
        
        # Analyze user journey paths
        journey_paths = self.analyze_user_journey()
        metrics['common_paths'] = journey_paths
        
        # Analyze popular content elements
        popular_elements = self.analyze_content_elements()
        metrics['popular_elements'] = popular_elements
        
        # Analyze interaction potential
        interaction_score = self.calculate_interaction_score()
        metrics['interaction_potential'] = interaction_score
        
        # Analyze time-on-page factors
        time_factors = self.analyze_time_factors()
        metrics['time_on_page_factors'] = time_factors
        
        # Generate insights
        if len(journey_paths) > 0:
            insights.append({
                'type': 'primary_user_flow',
                'message': f'Main user paths identified: {", ".join(journey_paths[:3])}',
                'impact': 'high'
            })
        
        if interaction_score > 7:
            insights.append({
                'type': 'high_interaction',
                'message': 'Website has good interactive elements for engagement',
                'impact': 'positive'
            })
        else:
            insights.append({
                'type': 'low_interaction',
                'message': 'Consider adding more interactive elements to boost engagement',
                'impact': 'negative'
            })
        
        score = min(100, interaction_score * 10)
        
        return {
            'score': round(score, 2),
            'grade': self.get_grade(score),
            'metrics': metrics,
            'insights': insights,
            'recommendations': self.get_recommendations(metrics)
        }
    
    def analyze_user_journey(self):
        """Analyze common user journey paths"""
        paths = []
        
        try:
            # Identify key conversion points
            cta_buttons = self.soup.find_all('button', class_=lambda x: x and 'cta' in x.lower() if x else False)
            cta_links = self.soup.find_all('a', class_=lambda x: x and 'cta' in x.lower() if x else False)
            
            conversion_elements = len(cta_buttons) + len(cta_links)
            if conversion_elements > 0:
                paths.append('Homepage → CTA/Button Click')
            
            # Check for multi-step processes
            forms = self.soup.find_all('form')
            if len(forms) > 1:
                paths.append('Homepage → Form Submission')
            
            # Check for common navigation patterns
            nav = self.soup.find('nav')
            if nav:
                nav_items = nav.find_all(['a', 'li'])
                if len(nav_items) > 0:
                    paths.append('Homepage → Navigation → Content Pages')
            
            # Check for product/service pages
            if self.soup.find_all(class_=lambda x: x and 'product' in x.lower() if x else False):
                paths.append('Homepage → Product Pages → Purchase')
            elif self.soup.find_all(class_=lambda x: x and 'service' in x.lower() if x else False):
                paths.append('Homepage → Service Pages → Inquiry')
            
            # Check for blog/article patterns
            if self.soup.find_all(['article', 'post']):
                paths.append('Homepage → Blog/Articles → Related Content')
        except Exception as e:
            print(f"Error analyzing user journey: {e}")
        
        return paths[:5]  # Return top 5 paths
    
    def analyze_content_elements(self):
        """Analyze popular content elements"""
        elements = {
            'images': 0,
            'videos': 0,
            'forms': 0,
            'buttons': 0,
            'links': 0,
            'headers': 0,
            'lists': 0
        }
        
        try:
            elements['images'] = len(self.soup.find_all('img'))
            elements['videos'] = len(self.soup.find_all(['video', 'iframe']))
            elements['forms'] = len(self.soup.find_all('form'))
            elements['buttons'] = len(self.soup.find_all('button'))
            elements['links'] = len(self.soup.find_all('a'))
            elements['headers'] = len(self.soup.find_all(['h1', 'h2', 'h3', 'h4']))
            elements['lists'] = len(self.soup.find_all(['ul', 'ol']))
        except Exception as e:
            print(f"Error analyzing content elements: {e}")
        
        return elements
    
    def calculate_interaction_score(self):
        """Calculate interaction potential score (0-10)"""
        score = 0
        
        try:
            # CTAs (max 3 points)
            ctas = len(self.soup.find_all('button')) + len(self.soup.find_all('a', class_=lambda x: x and 'cta' in x.lower() if x else False))
            score += min(3, ctas / 5)
            
            # Forms (max 2 points)
            forms = len(self.soup.find_all('form'))
            score += min(2, forms)
            
            # Media (max 2 points)
            media = len(self.soup.find_all(['video', 'iframe']))
            score += min(2, media / 2)
            
            # Interactive elements (max 2 points)
            interactives = len(self.soup.find_all(class_=lambda x: x and any(term in x.lower() for term in ['modal', 'carousel', 'accordion']) if x else False))
            score += min(2, interactives)
            
            # Links (max 1 point)
            links = len(self.soup.find_all('a'))
            score += min(1, links / 20)
        except Exception as e:
            print(f"Error calculating interaction score: {e}")
        
        return round(score, 1)
    
    def analyze_time_factors(self):
        """Analyze factors that affect time on page"""
        factors = {
            'content_depth': 'unknown',
            'media_richness': 'unknown',
            'engagement_elements': 'unknown',
            'readability': 'unknown'
        }
        
        try:
            # Content depth
            paragraphs = self.soup.find_all('p')
            total_words = sum(len(p.get_text().split()) for p in paragraphs)
            if total_words > 2000:
                factors['content_depth'] = 'high'
            elif total_words > 500:
                factors['content_depth'] = 'medium'
            else:
                factors['content_depth'] = 'low'
            
            # Media richness
            media_count = len(self.soup.find_all(['img', 'video', 'iframe']))
            if media_count > 10:
                factors['media_richness'] = 'high'
            elif media_count > 3:
                factors['media_richness'] = 'medium'
            else:
                factors['media_richness'] = 'low'
            
            # Engagement elements
            engagement = len(self.soup.find_all('button')) + len(self.soup.find_all('form'))
            if engagement > 5:
                factors['engagement_elements'] = 'high'
            elif engagement > 2:
                factors['engagement_elements'] = 'medium'
            else:
                factors['engagement_elements'] = 'low'
            
            # Readability (based on heading structure)
            headings = len(self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
            if headings > 10:
                factors['readability'] = 'good'
            elif headings > 3:
                factors['readability'] = 'fair'
            else:
                factors['readability'] = 'poor'
        except Exception as e:
            print(f"Error analyzing time factors: {e}")
        
        return factors
    
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
    
    def get_recommendations(self, metrics):
        """Get recommendations based on metrics"""
        recommendations = []
        
        try:
            elements = metrics.get('popular_elements', {})
            
            # Recommendations based on content elements
            if elements.get('forms', 0) == 0:
                recommendations.append('Add contact forms to capture user information')
            
            if elements.get('videos', 0) == 0:
                recommendations.append('Add video content to increase engagement')
            
            if elements.get('buttons', 0) < 3:
                recommendations.append('Add more clear call-to-action buttons')
            
            if elements.get('images', 0) < 5:
                recommendations.append('Increase visual content with relevant images')
            
            # Time factors recommendations
            time_factors = metrics.get('time_on_page_factors', {})
            if time_factors.get('content_depth') == 'low':
                recommendations.append('Add more detailed content to increase time on page')
            
            if time_factors.get('engagement_elements') == 'low':
                recommendations.append('Add interactive elements like polls, quizzes, or forms')
        except Exception as e:
            print(f"Error getting recommendations: {e}")
        
        return recommendations
    
    def get_error_response(self):
        """Return error response"""
        return {
            'score': 0,
            'grade': 'F',
            'metrics': {},
            'insights': [{'type': 'fetch_error', 'message': 'Could not fetch website', 'impact': 'critical'}],
            'recommendations': ['Check if the URL is correct and accessible']
        }
