from flask import Flask, render_template, request, jsonify
import json
import statistics
import logging
from datetime import datetime
from config import Config
from api_services import DataAggregator, GeminiService, NominatimService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize services
data_aggregator = DataAggregator()
gemini_service = GeminiService()
nominatim_service = NominatimService()

class RentFairAnalyzer:
    def __init__(self):
        self.data_aggregator = data_aggregator
        self.gemini_service = gemini_service
        self.nominatim_service = nominatim_service
    
    def find_comparables(self, user_listing):
        """Find comparable listings based on location and bedrooms - real API data only"""
        target_beds = user_listing['bedrooms']
        target_location = user_listing['location']
        
        logger.info(f"Finding real comparables for {target_beds} bedrooms in {target_location}")
        
        # Use data aggregator to get real comparables from RentCast API only
        comparables = self.data_aggregator.get_comparables(target_location, target_beds)
        
        if comparables:
            logger.info(f"Found {len(comparables)} real comparable listings from RentCast API")
            # Debug: print first few comparables
            for i, comp in enumerate(comparables[:3], 1):
                logger.info(f"  {i}. ${comp.get('price', 'N/A')} - {comp.get('bedrooms', 'N/A')} bed - {comp.get('address', 'N/A')}")
        else:
            logger.warning("No real comparable listings found from RentCast API")
        
        return comparables
    
    def calculate_market_stats(self, comparables):
        """Calculate market statistics for real comparable listings only"""
        if not comparables:
            logger.warning("No real comparables available for market stats")
            return None
        
        # Ensure all comparables have valid prices from real data
        valid_prices = [c['price'] for c in comparables if c.get('price') and c['price'] > 0]
        
        if not valid_prices:
            logger.warning("No valid prices found in real comparables")
            return None
        
        logger.info(f"Calculating real market stats from {len(valid_prices)} valid prices: {valid_prices}")
        
        stats = {
            'mean': statistics.mean(valid_prices),
            'median': statistics.median(valid_prices),
            'std_dev': statistics.stdev(valid_prices) if len(valid_prices) > 1 else 0,
            'min': min(valid_prices),
            'max': max(valid_prices),
            'count': len(valid_prices)
        }
        
        logger.info(f"Real market stats calculated: {stats}")
        return stats
    
    def calculate_fairness_score(self, user_rent, market_stats):
        """Calculate fairness score and classification"""
        if not market_stats:
            return None
        
        # Fairness score as percentage difference from mean
        fairness_score = (user_rent - market_stats['mean']) / market_stats['mean']
        
        # Z-score calculation
        z_score = 0
        if market_stats['std_dev'] > 0:
            z_score = (user_rent - market_stats['mean']) / market_stats['std_dev']
        
        # Classification
        if fairness_score < -0.1:
            classification = "Underpriced"
            color = "blue"
        elif fairness_score < 0.1:
            classification = "Fair"
            color = "green"
        else:
            classification = "Overpriced"
            color = "red"
        
        return {
            'fairness_score': fairness_score,
            'z_score': z_score,
            'classification': classification,
            'color': color,
            'percent_difference': fairness_score * 100
        }
    
    def generate_explanation(self, user_listing, market_stats, fairness_result, comparables):
        """Generate explanation for the user"""
        if not market_stats or not fairness_result:
            return "Unable to generate analysis - not enough comparable data."
        
        location = user_listing['location']
        bedrooms = user_listing['bedrooms']
        user_rent = user_listing['price']
        
        explanation = f"This {bedrooms}-bedroom listing in {location} is "
        
        if fairness_result['classification'] == "Fair":
            explanation += f"fairly priced at ${user_rent:,}. "
        elif fairness_result['classification'] == "Overpriced":
            explanation += f"{abs(fairness_result['percent_difference']):.1f}% above market rate at ${user_rent:,}. "
        else:
            explanation += f"{abs(fairness_result['percent_difference']):.1f}% below market rate at ${user_rent:,}. "
        
        explanation += f"Most comparable {bedrooms}-bedroom units in {location} range between ${market_stats['min']:,}–${market_stats['max']:,}, "
        explanation += f"with an average of ${market_stats['mean']:,}."
        
        return explanation
    
    def generate_ai_negotiation_tips(self, analysis_result):
        """Generate AI-powered negotiation tips"""
        return self.gemini_service.generate_negotiation_tips(analysis_result)
    
    def geocode_address(self, address):
        """Convert address to coordinates"""
        return self.nominatim_service.geocode_address(address)

analyzer = RentFairAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze-rent', methods=['POST'])
def analyze_rent():
    try:
        data = request.get_json()
        
        # Validate required fields (only essential ones)
        required_fields = ['address', 'price', 'bedrooms', 'bathrooms', 'location']
        missing_fields = [field for field in required_fields if not data.get(field) or str(data.get(field)).strip() == '']
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'solution': 'Please fill in all required fields with valid values'
            }), 400
        
        # Extract and validate user listing data
        try:
            user_listing = {
                'address': str(data.get('address', '')).strip(),
                'price': int(float(str(data.get('price', '0')).strip() or '0')),
                'bedrooms': int(float(str(data.get('bedrooms', '0')).strip() or '0')),
                'bathrooms': int(float(str(data.get('bathrooms', '0')).strip() or '0')),
                'location': str(data.get('location', '')).strip(),
                'sqft': int(float(str(data.get('sqft', '0')).strip() or '0')) if data.get('sqft') and str(data.get('sqft')).strip() else 0
            }
        except (ValueError, TypeError) as e:
            return jsonify({
                'error': f'Invalid numeric values: {str(e)}',
                'solution': 'Please ensure price, bedrooms, and bathrooms are valid numbers'
            }), 400
        
        # Validate numeric ranges (sqft is optional)
        if user_listing['price'] <= 0:
            return jsonify({'error': 'Price must be greater than 0'}), 400
        if user_listing['bedrooms'] <= 0 or user_listing['bedrooms'] > 10:
            return jsonify({'error': 'Bedrooms must be between 1 and 10'}), 400
        if user_listing['bathrooms'] <= 0 or user_listing['bathrooms'] > 10:
            return jsonify({'error': 'Bathrooms must be between 1 and 10'}), 400
        if user_listing['sqft'] > 0 and (user_listing['sqft'] < 100 or user_listing['sqft'] > 10000):
            return jsonify({'error': 'Square footage must be between 100 and 10,000 (or leave blank)'}), 400
        
        logger.info(f"Analyzing rental: {user_listing}")
        
        # Get coordinates
        coordinates = analyzer.geocode_address(user_listing['address'])
        
        # Find comparable listings
        comparables = analyzer.find_comparables(user_listing)
        
        if not comparables:
            logger.error("No comparable listings found - API key issue likely")
            return jsonify({
                'error': 'No comparable listings found. This usually means the RentCast API key is invalid or expired.',
                'solution': 'Please update your RENTCAST_API_KEY in the .env file. Get a new key from https://app.rentcast.io/app/api',
                'debug_info': {
                    'location': user_listing['location'],
                    'bedrooms': user_listing['bedrooms'],
                    'api_key_set': bool(Config.RENTCAST_API_KEY)
                }
            }), 400
        
        # Calculate market statistics
        market_stats = analyzer.calculate_market_stats(comparables)
        
        if not market_stats:
            return jsonify({'error': 'Could not calculate market statistics'}), 500
        
        # Calculate fairness score
        fairness_result = analyzer.calculate_fairness_score(user_listing['price'], market_stats)
        
        # Generate AI tips
        ai_tips = analyzer.generate_ai_negotiation_tips({
            'user_listing': user_listing,
            'fairness_result': fairness_result,
            'market_stats': market_stats
        })
        
        # Prepare response
        response = {
            'user_listing': user_listing,
            'comparables': comparables[:10],  # Limit to top 10
            'market_stats': market_stats,
            'fairness_result': fairness_result,
            'ai_tips': ai_tips,
            'coordinates': coordinates,
            'explanation': analyzer.generate_explanation(user_listing, market_stats, fairness_result)
        }
        
        logger.info(f"Analysis complete: {fairness_result['classification']} ({fairness_result['percent_difference']:.1f}%)")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in analyze_rent: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/market-stats/<location>/<int:bedrooms>')
def get_market_stats(location, bedrooms):
    """Get market statistics for a specific location and bedroom count"""
    try:
        mock_listing = {'location': location, 'bedrooms': bedrooms}
        comparables = analyzer.find_comparables(mock_listing)
        market_stats = analyzer.calculate_market_stats(comparables)
        
        return jsonify({
            'location': location,
            'bedrooms': bedrooms,
            'comparables_count': len(comparables),
            'market_stats': market_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
