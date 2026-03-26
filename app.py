from flask import Flask, render_template, request, jsonify
import json
import statistics
from datetime import datetime

app = Flask(__name__)

# Sample rental data - in production this would come from APIs
SAMPLE_LISTINGS = [
    {"price": 2100, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 850, "address": "123 Queen St"},
    {"price": 2250, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 900, "address": "456 King St"},
    {"price": 2400, "bedrooms": 2, "bathrooms": 2, "location": "Mississauga", "sqft": 950, "address": "789 Main St"},
    {"price": 1950, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 800, "address": "321 Dundas St"},
    {"price": 2500, "bedrooms": 2, "bathrooms": 2, "location": "Mississauga", "sqft": 1000, "address": "654 Hurontario St"},
    {"price": 2200, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 875, "address": "987 Burnhamthorpe Rd"},
    {"price": 2350, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 920, "address": "147 Eglinton Ave"},
    {"price": 2600, "bedrooms": 2, "bathrooms": 2, "location": "Mississauga", "sqft": 1050, "address": "258 Lakeshore Rd"},
    {"price": 2000, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 825, "address": "369 Britannia Rd"},
    {"price": 2450, "bedrooms": 2, "bathrooms": 2, "location": "Mississauga", "sqft": 980, "address": "741 Mavis Rd"},
    {"price": 1800, "bedrooms": 1, "bathrooms": 1, "location": "Toronto", "sqft": 650, "address": "100 Yonge St"},
    {"price": 2200, "bedrooms": 1, "bathrooms": 1, "location": "Toronto", "sqft": 700, "address": "200 Bay St"},
    {"price": 1900, "bedrooms": 1, "bathrooms": 1, "location": "Toronto", "sqft": 675, "address": "300 Queen St"},
    {"price": 3200, "bedrooms": 3, "bathrooms": 2, "location": "Toronto", "sqft": 1200, "address": "400 King St"},
    {"price": 3500, "bedrooms": 3, "bathrooms": 2, "location": "Toronto", "sqft": 1300, "address": "500 University Ave"},
]

class RentFairAnalyzer:
    def __init__(self):
        self.listings = SAMPLE_LISTINGS
    
    def find_comparables(self, user_listing):
        """Find comparable listings based on location and bedrooms"""
        comparables = []
        target_beds = user_listing['bedrooms']
        target_location = user_listing['location'].lower()
        
        for listing in self.listings:
            # Filter by same location (case insensitive)
            if listing['location'].lower() == target_location:
                # Allow ±1 bedroom difference
                if abs(listing['bedrooms'] - target_beds) <= 1:
                    comparables.append(listing)
        
        return comparables
    
    def calculate_market_stats(self, comparables):
        """Calculate market statistics for comparable listings"""
        if not comparables:
            return None
        
        prices = [c['price'] for c in comparables]
        return {
            'mean': statistics.mean(prices),
            'median': statistics.median(prices),
            'std_dev': statistics.stdev(prices) if len(prices) > 1 else 0,
            'min': min(prices),
            'max': max(prices),
            'count': len(comparables)
        }
    
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
        
        # Add negotiation tips if overpriced
        if fairness_result['classification'] == "Overpriced":
            explanation += f" You could reference comparable listings in the ${market_stats['min']:,}–${market_stats['median']:,} range when negotiating."
        
        return explanation

analyzer = RentFairAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze-rent', methods=['POST'])
def analyze_rent():
    try:
        data = request.get_json()
        
        user_listing = {
            'price': float(data['price']),
            'bedrooms': int(data['bedrooms']),
            'bathrooms': int(data['bathrooms']),
            'location': data['location'],
            'sqft': float(data.get('sqft', 0)) if data.get('sqft') else 0,
            'address': data.get('address', '')
        }
        
        # Find comparable listings
        comparables = analyzer.find_comparables(user_listing)
        
        if not comparables:
            return jsonify({
                'error': 'No comparable listings found. Try a different location or bedroom count.',
                'comparables': []
            }), 400
        
        # Calculate market statistics
        market_stats = analyzer.calculate_market_stats(comparables)
        
        # Calculate fairness score
        fairness_result = analyzer.calculate_fairness_score(user_listing['price'], market_stats)
        
        # Generate explanation
        explanation = analyzer.generate_explanation(user_listing, market_stats, fairness_result, comparables)
        
        return jsonify({
            'user_listing': user_listing,
            'comparables': comparables,
            'market_stats': market_stats,
            'fairness_result': fairness_result,
            'explanation': explanation
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
