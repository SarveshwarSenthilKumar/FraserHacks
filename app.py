from flask import Flask, render_template, request, jsonify
import json
import math
import statistics
from datetime import datetime
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY')

if GEMINI_API_KEY != 'YOUR_GEMINI_API_KEY':
    genai.configure(api_key=GEMINI_API_KEY)

# Sample rental data - in a real app, this would come from Gemini API
SAMPLE_LISTINGS = [
    {"price": 2200, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 850, "address": "123 Queen St E"},
    {"price": 2400, "bedrooms": 2, "bathrooms": 2, "location": "Mississauga", "sqft": 900, "address": "456 King St W"},
    {"price": 2100, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 800, "address": "789 Dundas St E"},
    {"price": 2600, "bedrooms": 2, "bathrooms": 2, "location": "Mississauga", "sqft": 1000, "address": "321 Yonge St"},
    {"price": 2300, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 875, "address": "654 Bloor St"},
    {"price": 2500, "bedrooms": 2, "bathrooms": 2, "location": "Mississauga", "sqft": 950, "address": "987 College St"},
    {"price": 2150, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 825, "address": "147 Spadina Ave"},
    {"price": 2450, "bedrooms": 2, "bathrooms": 2, "location": "Mississauga", "sqft": 925, "address": "258 Queen St W"},
    {"price": 2250, "bedrooms": 2, "bathrooms": 1, "location": "Mississauga", "sqft": 860, "address": "369 King St E"},
    {"price": 2350, "bedrooms": 2, "bathrooms": 2, "location": "Mississauga", "sqft": 890, "address": "741 Dundas St W"},
    {"price": 2800, "bedrooms": 3, "bathrooms": 2, "location": "Mississauga", "sqft": 1200, "address": "852 Yonge St"},
    {"price": 1900, "bedrooms": 1, "bathrooms": 1, "location": "Mississauga", "sqft": 650, "address": "963 Bloor St W"},
    {"price": 3200, "bedrooms": 3, "bathrooms": 2, "location": "Mississauga", "sqft": 1100, "address": "159 College St W"},
    {"price": 2000, "bedrooms": 1, "bathrooms": 1, "location": "Mississauga", "sqft": 600, "address": "753 Spadina Rd"},
    {"price": 2900, "bedrooms": 3, "bathrooms": 2, "location": "Mississauga", "sqft": 1150, "address": "951 Queen St E"},
]

def generate_simple_coordinates(address, location):
    """Generate simple coordinates without any external dependencies"""
    # Simple city center coordinates
    city_centers = {
        'mississauga': [43.5890, -79.6441],
        'toronto': [43.6532, -79.3832],
        'vancouver': [49.2827, -123.1207],
        'montreal': [45.5017, -73.5673],
        'calgary': [51.0447, -114.0719],
        'ottawa': [45.4215, -75.6972]
    }
    
    # Get city center or default to Mississauga
    center = city_centers.get(location.lower(), city_centers['mississauga'])
    
    # Add small random offset for variety
    import random
    lat_offset = (random.random() - 0.5) * 0.1  # ±0.05 degrees
    lng_offset = (random.random() - 0.5) * 0.1  # ±0.05 degrees
    
    return {
        'lat': center[0] + lat_offset,
        'lng': center[1] + lng_offset
    }

def geocode_address(address, location):
    """Simple coordinate generation without external APIs"""
    return generate_simple_coordinates(address, location)

def generate_comparable_listings_gemini(user_listing):
    """Generate comparable listings using Gemini API"""
    try:
        if GEMINI_API_KEY == 'YOUR_GEMINI_API_KEY':
            return SAMPLE_LISTINGS
        
        prompt = f"""
        Generate 10 realistic rental listings comparable to the following property in {user_listing['location']}:
        
        Target Property:
        - Price: ${user_listing['price']}/month
        - Bedrooms: {user_listing['bedrooms']}
        - Bathrooms: {user_listing['bathrooms']}
        - Location: {user_listing['location']}
        - Square Feet: {user_listing['sqft']}
        
        Please generate 10 comparable rental listings with realistic variations in price (±20%), 
        similar bedroom/bathroom counts, and realistic addresses in {user_listing['location']}.
        
        Format each listing as a JSON object with these exact keys:
        - price: monthly rent as number
        - bedrooms: number of bedrooms as number  
        - bathrooms: number of bathrooms as number
        - location: "{user_listing['location']}"
        - sqft: square footage as number
        - address: realistic street address in {user_listing['location']}
        - listing_url: MUST be a valid, complete URL starting with https:// (use real estate websites like zillow.com, realtor.ca, apartments.com, or zumper.com)
        
        IMPORTANT: The listing_url MUST be a complete, valid URL that starts with "https://". 
        Examples of good URLs:
        - "https://www.zillow.com/homedetails/123-Main-St-example-address/"
        - "https://www.realtor.ca/real-estate/example-address"
        - "https://www.apartments.com/example-address"
        
        Return only a valid JSON array of 10 listing objects. No additional text or markdown formatting.
        """
        
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Try to parse JSON response
        try:
            # Remove any markdown code blocks
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            listings = json.loads(response_text)
            
            # Validate and clean the data
            valid_listings = []
            for listing in listings:
                if all(key in listing for key in ['price', 'bedrooms', 'bathrooms', 'location', 'sqft', 'address', 'listing_url']):
                    # Ensure data types are correct
                    listing['price'] = float(listing['price'])
                    listing['bedrooms'] = int(listing['bedrooms'])
                    listing['bathrooms'] = int(listing['bathrooms'])
                    listing['sqft'] = int(listing['sqft'])
                    valid_listings.append(listing)
            
            return valid_listings if valid_listings else SAMPLE_LISTINGS
            
        except json.JSONDecodeError:
            print("Failed to parse Gemini response as JSON")
            return SAMPLE_LISTINGS
            
    except Exception as e:
        print(f"Error generating comparable listings: {e}")
        return SAMPLE_LISTINGS

def find_comparables(user_listing, all_listings):
    """Find comparable listings based on location, bedrooms, and property type"""
    comparables = []
    
    for listing in all_listings:
        # Same location
        if listing["location"].lower() != user_listing["location"].lower():
            continue
            
        # Same bedroom count or ±1
        if abs(listing["bedrooms"] - user_listing["bedrooms"]) > 1:
            continue
            
        # Similar bathroom count (±1)
        if abs(listing["bathrooms"] - user_listing["bathrooms"]) > 1:
            continue
            
        comparables.append(listing)
    
    return comparables

def calculate_fairness_score(user_rent, comparables):
    """Calculate fairness score using Z-score methodology"""
    if not comparables:
        return {"score": 0, "label": "Insufficient Data", "z_score": 0}
    
    # Extract prices from comparables
    prices = [comp["price"] for comp in comparables]
    
    # Calculate market statistics
    mean_price = statistics.mean(prices)
    median_price = statistics.median(prices)
    std_dev = statistics.stdev(prices) if len(prices) > 1 else 0
    
    # Calculate Z-score
    z_score = (user_rent - mean_price) / std_dev if std_dev > 0 else 0
    
    # Calculate percentage difference from mean
    percent_diff = ((user_rent - mean_price) / mean_price) * 100
    
    # Determine fairness label
    if percent_diff < -10:
        label = "Underpriced"
        color = "#3B82F6"  # Blue
    elif percent_diff < 10:
        label = "Fair"
        color = "#10B981"  # Green
    else:
        label = "Overpriced"
        color = "#EF4444"  # Red
    
    return {
        "score": percent_diff,
        "label": label,
        "color": color,
        "z_score": z_score,
        "mean_price": mean_price,
        "median_price": median_price,
        "std_dev": std_dev,
        "comparable_count": len(comparables)
    }

def generate_ai_explanation(user_listing, fairness_result, comparables):
    """Generate AI-powered explanation using Gemini API"""
    
    # Prepare the prompt for Gemini
    prompt = f"""
    You are a real estate expert analyzing rental prices. Based on the following data, provide a concise explanation of rent fairness and negotiation tips.

    User Listing:
    - Price: ${user_listing['price']}/month
    - Bedrooms: {user_listing['bedrooms']}
    - Bathrooms: {user_listing['bathrooms']}
    - Location: {user_listing['location']}
    - Square Feet: {user_listing['sqft']}

    Market Analysis:
    - Fairness Score: {fairness_result['score']:.1f}% ({'above' if fairness_result['score'] > 0 else 'below'} market)
    - Label: {fairness_result['label']}
    - Market Average: ${fairness_result['mean_price']:.0f}
    - Comparable Listings: {fairness_result['comparable_count']}
    - Price Range: ${min(comp['price'] for comp in comparables):.0f} - ${max(comp['price'] for comp in comparables):.0f}

    Please provide:
    1. A brief explanation of the rent fairness (2-3 sentences)
    2. 3-4 specific negotiation tips

    Format your response as:
    EXPLANATION: [Your explanation here]
    
    TIPS:
    • [Tip 1]
    • [Tip 2]
    • [Tip 3]
    • [Tip 4]
    """
    
    try:
        # Use Gemini API if available
        if GEMINI_API_KEY != 'YOUR_GEMINI_API_KEY':
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            response = model.generate_content(prompt)
            response_text = response.text
            
            # Parse the response
            if 'EXPLANATION:' in response_text and 'TIPS:' in response_text:
                explanation_part = response_text.split('EXPLANATION:')[1].split('TIPS:')[0].strip()
                tips_part = response_text.split('TIPS:')[1].strip()
                
                return {
                    "explanation": explanation_part,
                    "negotiation_tips": tips_part
                }
        
        # Fallback to predefined explanations if API fails
        return get_fallback_explanation(user_listing, fairness_result, comparables)
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return get_fallback_explanation(user_listing, fairness_result, comparables)

def get_fallback_explanation(user_listing, fairness_result, comparables):
    """Fallback explanation when Gemini API is not available"""
    
    explanation = f"""
    This {user_listing['bedrooms']}-bedroom, {user_listing['bathrooms']}-bathroom listing in {user_listing['location']} 
    is {abs(fairness_result['score']):.1f}% {'above' if fairness_result['score'] > 0 else 'below'} the market average.
    
    Based on {fairness_result['comparable_count']} comparable listings, the average rent is ${fairness_result['mean_price']:.0f} 
    with most units ranging between ${min(comp['price'] for comp in comparables):.0f}-${max(comp['price'] for comp in comparables):.0f}.
    
    {'This appears to be a good deal compared to similar units in the area.' if fairness_result['label'] == 'Underpriced' else 
     'This is priced fairly for the market.' if fairness_result['label'] == 'Fair' else 
     'This is significantly overpriced compared to similar units.'}
    """
    
    negotiation_tips = """
    • Research comparable listings in the area to strengthen your negotiation position
    • Highlight any unique features or amenities the property offers
    • Consider the length of lease - longer terms may warrant lower monthly rent
    • Be prepared to walk away if the price doesn't align with market rates
    """
    
    return {
        "explanation": explanation.strip(),
        "negotiation_tips": negotiation_tips.strip()
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze-rent', methods=['POST'])
def analyze_rent():
    try:
        data = request.get_json()
        
        # Create user listing object
        user_listing = {
            "price": float(data['price']),
            "bedrooms": int(data['bedrooms']),
            "bathrooms": int(data['bathrooms']),
            "location": data['location'],
            "sqft": int(data.get('sqft', 0)) if data.get('sqft') else 0,
            "address": data.get('address', '')
        }
        
        # Generate comparable listings using Gemini
        gemini_listings = generate_comparable_listings_gemini(user_listing)
        
        # Add coordinates to all listings (simple and fast)
        for listing in gemini_listings:
            coords = geocode_address(listing['address'], listing['location'])
            listing['lat'] = coords['lat']
            listing['lng'] = coords['lng']
        
        # Find comparable listings from the generated data
        comparables = find_comparables(user_listing, gemini_listings)
        
        # Calculate fairness score
        fairness_result = calculate_fairness_score(user_listing["price"], comparables)
        
        # Generate AI explanation
        ai_explanation = generate_ai_explanation(user_listing, fairness_result, comparables)
        
        # Prepare response
        response = {
            "user_listing": user_listing,
            "fairness_result": fairness_result,
            "comparables": comparables[:10],  # Limit to top 10 for display
            "ai_explanation": ai_explanation,
            "price_distribution": {
                "min": min(comp['price'] for comp in comparables) if comparables else user_listing["price"],
                "max": max(comp['price'] for comp in comparables) if comparables else user_listing["price"],
                "prices": [comp['price'] for comp in comparables]
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/market-stats')
def market_stats():
    """Get general market statistics"""
    prices = [listing["price"] for listing in SAMPLE_LISTINGS]
    
    return jsonify({
        "total_listings": len(SAMPLE_LISTINGS),
        "average_price": statistics.mean(prices),
        "median_price": statistics.median(prices),
        "min_price": min(prices),
        "max_price": max(prices),
        "locations": list(set(listing["location"] for listing in SAMPLE_LISTINGS))
    })

if __name__ == '__main__':
    app.run(debug=True)
