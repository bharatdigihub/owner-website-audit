from flask import Blueprint, request, jsonify
from app.analyzers.performance import PerformanceAnalyzer
from app.analyzers.security import SecurityAnalyzer
from app.analyzers.seo import SEOAnalyzer
from app.analyzers.code_standards import CodeStandardsAnalyzer
from app.analyzers.user_friendliness import UserFriendlinessAnalyzer
from app.analyzers.user_behavior import UserBehaviorAnalyzer
from app.analyzers.mobile_optimization import MobileOptimizationAnalyzer
from app.analyzers.accessibility import AccessibilityAnalyzer
from app.analyzers.advanced_metrics import AdvancedMetricsAnalyzer
from app.analyzers.core_web_vitals import CoreWebVitalsAnalyzer
from app.analyzers.waterfall import WaterfallAnalyzer
from app.analyzers.multi_location import MultiLocationAnalyzer
from app.analyzers.device_simulation import DeviceSimulationAnalyzer
from app.utils.validator import validate_url
import traceback

analyzer_bp = Blueprint('analyzer', __name__)

@analyzer_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Website Analyzer API is running'}), 200

@analyzer_bp.route('/analyze', methods=['POST'])
def analyze_website():
    """Main analysis endpoint"""
    try:
        data = request.get_json()
        url = data.get('url')
        form_factor = data.get('form_factor', 'desktop')  # 'desktop' or 'mobile'
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate URL
        if not validate_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Run all analyses
        results = {
            'url': url,
            'form_factor': form_factor,
            'performance': PerformanceAnalyzer(url, form_factor=form_factor).analyze(),
            'security': SecurityAnalyzer(url).analyze(),
            'seo': SEOAnalyzer(url).analyze(),
            'coding_standards': CodeStandardsAnalyzer(url).analyze(),
            'user_friendliness': UserFriendlinessAnalyzer(url).analyze(),
            'user_behavior': UserBehaviorAnalyzer(url).analyze(),
            'mobile_optimization': MobileOptimizationAnalyzer(url).analyze(),
            'accessibility': AccessibilityAnalyzer(url).analyze(),
            'advanced_metrics': AdvancedMetricsAnalyzer(url).analyze(),
            'core_web_vitals': CoreWebVitalsAnalyzer(url, form_factor=form_factor).analyze(),
            'waterfall': WaterfallAnalyzer(url, form_factor=form_factor).analyze(),
            'multi_location': MultiLocationAnalyzer(url).analyze(),
            'device_simulation': DeviceSimulationAnalyzer(url, form_factor=form_factor).analyze(),
        }
        
        return jsonify(results), 200
    
    except Exception as e:
        print(f"Error during analysis: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/performance', methods=['POST'])
def analyze_performance():
    """Performance analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = PerformanceAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/security', methods=['POST'])
def analyze_security():
    """Security analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = SecurityAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/seo', methods=['POST'])
def analyze_seo():
    """SEO analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = SEOAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/code-standards', methods=['POST'])
def analyze_code_standards():
    """Code standards analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = CodeStandardsAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/user-friendliness', methods=['POST'])
def analyze_user_friendliness():
    """User friendliness analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = UserFriendlinessAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/user-behavior', methods=['POST'])
def analyze_user_behavior():
    """User behavior analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = UserBehaviorAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/mobile-optimization', methods=['POST'])
def analyze_mobile_optimization():
    """Mobile optimization analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = MobileOptimizationAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/accessibility', methods=['POST'])
def analyze_accessibility():
    """Accessibility analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = AccessibilityAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/advanced-metrics', methods=['POST'])
def analyze_advanced_metrics():
    """Advanced metrics analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = AdvancedMetricsAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/core-web-vitals', methods=['POST'])
def analyze_core_web_vitals():
    """Core Web Vitals analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = CoreWebVitalsAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/waterfall', methods=['POST'])
def analyze_waterfall():
    """Waterfall chart analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = WaterfallAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/multi-location', methods=['POST'])
def analyze_multi_location():
    """Multi-location testing analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = MultiLocationAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analyzer_bp.route('/analyze/device-simulation', methods=['POST'])
def analyze_device_simulation():
    """Device simulation analysis only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        analyzer = DeviceSimulationAnalyzer(url)
        results = analyzer.analyze()
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
