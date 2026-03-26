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

def generate_simple_coordinates(address, location):
    """Generate simple coordinates without any external dependencies"""
    # International city center coordinates
    city_centers = {
        # Canada
        'mississauga': [43.5890, -79.6441],
        'toronto': [43.6532, -79.3832],
        'vancouver': [49.2827, -123.1207],
        'montreal': [45.5017, -73.5673],
        'calgary': [51.0447, -114.0719],
        'ottawa': [45.4215, -75.6972],
        'brampton': [43.7315, -79.7624],
        'hamilton': [43.2557, -79.8711],
        'london': [42.9837, -81.2497],
        'kitchener': [43.4516, -80.4925],
        'waterloo': [43.4643, -80.5204],
        'halifax': [44.6476, -63.5752],
        'winnipeg': [49.8951, -97.1384],
        'edmonton': [53.5461, -113.4938],
        'victoria': [48.4284, -123.3656],
        'quebec city': [46.8139, -71.2080],
        'saskatoon': [52.1579, -106.6702],
        'regina': [50.4452, -104.6189],
        'st. john\'s': [47.5615, -52.7126],
        'barrie': [44.3894, -79.6903],
        'guelph': [43.5448, -80.2482],
        'kingston': [44.2312, -76.4860],
        'windsor': [42.3149, -83.0703],
        
        # USA
        'new york': [40.7128, -74.0060],
        'los angeles': [34.0522, -118.2437],
        'chicago': [41.8781, -87.6298],
        'houston': [29.7604, -95.3698],
        'phoenix': [33.4484, -112.0740],
        'philadelphia': [39.9526, -75.1652],
        'san antonio': [29.4241, -98.4936],
        'san diego': [32.7157, -117.1611],
        'dallas': [32.7767, -96.7970],
        'san jose': [37.3382, -121.8863],
        'austin': [30.2672, -97.7431],
        'jacksonville': [30.3322, -81.6557],
        'fort worth': [32.7555, -97.3308],
        'columbus': [39.9612, -82.9988],
        'charlotte': [35.2271, -80.8431],
        'san francisco': [37.7749, -122.4194],
        'indianapolis': [39.7684, -86.1581],
        'seattle': [47.6062, -122.3321],
        'denver': [39.7392, -104.9903],
        'washington': [38.9072, -77.0369],
        'boston': [42.3601, -71.0589],
        'el paso': [31.7619, -106.4850],
        'detroit': [42.3314, -83.0458],
        'nashville': [36.1627, -86.7816],
        'portland': [45.5152, -122.6784],
        'memphis': [35.1495, -90.0490],
        'oklahoma city': [35.4676, -97.5164],
        'las vegas': [36.1699, -115.1398],
        'louisville': [38.2527, -85.7585],
        'milwaukee': [43.0389, -87.9065],
        'albuquerque': [35.0844, -106.6504],
        'tucson': [32.2226, -110.9747],
        'fresno': [36.7378, -119.7871],
        'sacramento': [38.5816, -121.4944],
        'kansas city': [39.0997, -94.5786],
        'long beach': [33.7701, -118.1937],
        'mesa': [33.4152, -111.8315],
        'atlanta': [33.7490, -84.3880],
        'omaha': [41.2565, -95.9345],
        'raleigh': [35.7796, -78.6382],
        'miami': [25.7617, -80.1918],
        'minneapolis': [44.9778, -93.2650],
        'tampa': [27.9506, -82.4572],
        'tulsa': [36.1540, -95.9944],
        'arlington': [32.7357, -97.1081],
        'new orleans': [29.9511, -90.0715],
        
        # UK
        'london': [51.5074, -0.1278],
        'manchester': [53.4808, -2.2426],
        'birmingham': [52.4862, -1.8904],
        'glasgow': [55.8642, -4.2518],
        'leeds': [53.8008, -1.5491],
        'sheffield': [53.3811, -1.4701],
        'bristol': [51.4545, -2.5879],
        'liverpool': [53.4084, -2.9916],
        'edinburgh': [55.9533, -3.1883],
        'cardiff': [51.4816, -3.1791],
        
        # Australia
        'sydney': [-33.8688, 151.2093],
        'melbourne': [-37.8136, 144.9631],
        'brisbane': [-27.4698, 153.0251],
        'perth': [-31.9505, 115.8605],
        'adelaide': [-34.9285, 138.6007],
        'gold coast': [-28.0167, 153.4000],
        'canberra': [-35.2809, 149.1300],
        'newcastle': [-32.9283, 151.7817],
        'wollongong': [-34.4278, 150.8931],
        'hobart': [-42.8821, 147.3272],
        
        # Germany
        'berlin': [52.5200, 13.4050],
        'munich': [48.1351, 11.5820],
        'hamburg': [53.5511, 9.9937],
        'frankfurt': [50.1109, 8.6821],
        'cologne': [50.9375, 6.9603],
        'stuttgart': [48.7758, 9.1829],
        'dusseldorf': [51.2277, 6.7735],
        'dortmund': [51.5136, 7.4653],
        
        # France
        'paris': [48.8566, 2.3522],
        'marseille': [43.2965, 5.3698],
        'lyon': [45.7640, 4.8357],
        'toulouse': [43.6047, 1.4442],
        'nice': [43.7102, 7.2620],
        
        # Netherlands
        'amsterdam': [52.3676, 4.9041],
        'rotterdam': [51.9244, 4.4777],
        'the hague': [52.0705, 4.3007],
        
        # Spain
        'madrid': [40.4168, -3.7038],
        'barcelona': [41.3851, 2.1734],
        'valencia': [39.4699, -0.3763],
        'seville': [37.3891, -5.9845],
        
        # Italy
        'rome': [41.9028, 12.4964],
        'milan': [45.4642, 9.1900],
        'naples': [40.8518, 14.2681],
        
        # Japan
        'tokyo': [35.6762, 139.6503],
        'osaka': [34.6937, 135.5023],
        'kyoto': [35.0116, 135.7681],
        
        # Singapore
        'singapore': [1.3521, 103.8198],
        
        # New Zealand
        'auckland': [-36.8485, 174.7633],
        'wellington': [-41.2865, 174.7762],
        
        # Ireland
        'dublin': [53.3498, -6.2603],
        
        # Belgium
        'brussels': [50.8503, 4.3517],
        
        # Switzerland
        'zurich': [47.3769, 8.5417],
        'geneva': [46.2044, 6.1432],
        
        # Sweden
        'stockholm': [59.3293, 18.0686],
        
        # Norway
        'oslo': [59.9139, 10.7522],
        
        # Denmark
        'copenhagen': [55.6761, 12.5683],
        
        # Finland
        'helsinki': [60.1699, 24.9384],
        
        # Austria
        'vienna': [48.2082, 16.3738],
        
        # UAE
        'dubai': [25.2048, 55.2708],
        'abu dhabi': [24.4539, 54.3773],
        
        # Hong Kong
        'hong kong': [22.3193, 114.1694],
        
        # China
        'beijing': [39.9042, 116.4074],
        'shanghai': [31.2304, 121.4737],
        'guangzhou': [23.1291, 113.2644],
        'shenzhen': [22.5431, 114.0579],
        
        # South Korea
        'seoul': [37.5665, 126.9780],
        'busan': [35.1796, 129.0756],
        
        # India
        'mumbai': [19.0760, 72.8777],
        'delhi': [28.7041, 77.1025],
        'bangalore': [12.9716, 77.5946],
        'chennai': [13.0827, 80.2707],
        'kolkata': [22.5726, 88.3639],
        
        # Brazil
        'são paulo': [-23.5505, -46.6333],
        'rio de janeiro': [-22.9068, -43.1729],
        
        # Mexico
        'mexico city': [19.4326, -99.1332],
        
        # Argentina
        'buenos aires': [-34.6037, -58.3816],
        
        # South Africa
        'johannesburg': [-26.2041, 28.0473],
        'cape town': [-33.9249, 18.4241],
        
        # Israel
        'tel aviv': [32.0853, 34.7818],
        'jerusalem': [31.7683, 35.2137],
        
        # Turkey
        'istanbul': [41.0082, 28.9784],
        'ankara': [39.9334, 32.8597],
        
        # Russia
        'moscow': [55.7558, 37.6173],
        'saint petersburg': [59.9343, 30.3351],
    }
    
    # Get city center or default to New York
    center = city_centers.get(location.lower(), city_centers['new york'])
    
    # Add small random offset
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

def validate_and_clean_rent_data(user_listing):
    """Validate and clean rent data, return warnings if issues found"""
    warnings = []
    cleaned_listing = user_listing.copy()
    
    # Validate rent price
    if user_listing['price'] <= 0:
        warnings.append("Rent price must be greater than $0")
        cleaned_listing['price'] = max(user_listing['price'], 1000)
    
    # Check for unrealistic rent prices
    if user_listing['price'] > 10000:
        warnings.append("Rent price seems unusually high (>$10,000)")
    elif user_listing['price'] < 500:
        warnings.append("Rent price seems unusually low (<$500)")
    
    # Validate square footage
    if user_listing['sqft'] <= 0:
        warnings.append("Square footage must be greater than 0")
        cleaned_listing['sqft'] = 600  # Default minimum
    
    # Check for unrealistic square footage
    if user_listing['sqft'] > 5000:
        warnings.append("Square footage seems unusually large (>5000 sqft)")
    elif user_listing['sqft'] < 300:
        warnings.append("Square footage seems unusually small (<300 sqft)")
    
    # Validate bedroom count
    if user_listing['bedrooms'] <= 0 or user_listing['bedrooms'] > 10:
        warnings.append("Bedroom count seems unrealistic")
        cleaned_listing['bedrooms'] = max(1, min(user_listing['bedrooms'], 5))
    
    # Validate bathroom count
    if user_listing['bathrooms'] <= 0 or user_listing['bathrooms'] > 10:
        warnings.append("Bathroom count seems unrealistic")
        cleaned_listing['bathrooms'] = max(1, min(user_listing['bathrooms'], 5))
    
    # Check bedroom to bathroom ratio
    if user_listing['bathrooms'] > user_listing['bedrooms'] + 2:
        warnings.append("Bathroom count seems high compared to bedrooms")
    
    # Calculate price per square foot
    price_per_sqft = cleaned_listing['price'] / cleaned_listing['sqft']
    if price_per_sqft > 10:
        warnings.append("Price per square foot seems very high")
    elif price_per_sqft < 0.5:
        warnings.append("Price per square foot seems very low")
    
    return cleaned_listing, warnings

def validate_location(location):
    """Validate if location is a known international city/town and return currency info"""
    # International cities with their currencies
    international_locations = {
        # Canada
        'mississauga': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'toronto': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'vancouver': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'montreal': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'calgary': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'ottawa': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'brampton': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'hamilton': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'london': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'kitchener': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'waterloo': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'halifax': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'winnipeg': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'edmonton': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'victoria': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'quebec city': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'saskatoon': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'regina': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'st. john\'s': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'barrie': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'guelph': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'kingston': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        'windsor': {'country': 'Canada', 'currency': 'CAD', 'symbol': 'C$'},
        
        # USA
        'new york': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'los angeles': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'chicago': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'houston': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'phoenix': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'philadelphia': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'san antonio': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'san diego': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'dallas': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'san jose': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'austin': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'jacksonville': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'fort worth': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'columbus': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'charlotte': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'san francisco': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'indianapolis': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'seattle': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'denver': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'washington': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'boston': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'el paso': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'detroit': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'nashville': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'portland': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'memphis': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'oklahoma city': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'las vegas': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'louisville': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'milwaukee': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'albuquerque': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'tucson': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'fresno': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'sacramento': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'kansas city': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'long beach': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'mesa': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'atlanta': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'omaha': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'raleigh': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'miami': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'minneapolis': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'tampa': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'tulsa': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'arlington': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        'new orleans': {'country': 'USA', 'currency': 'USD', 'symbol': '$'},
        
        # UK
        'london': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        'manchester': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        'birmingham': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        'glasgow': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        'leeds': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        'sheffield': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        'bristol': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        'liverpool': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        'edinburgh': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        'cardiff': {'country': 'UK', 'currency': 'GBP', 'symbol': '£'},
        
        # Australia
        'sydney': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        'melbourne': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        'brisbane': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        'perth': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        'adelaide': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        'gold coast': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        'canberra': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        'newcastle': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        'wollongong': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        'hobart': {'country': 'Australia', 'currency': 'AUD', 'symbol': 'A$'},
        
        # Germany
        'berlin': {'country': 'Germany', 'currency': 'EUR', 'symbol': '€'},
        'munich': {'country': 'Germany', 'currency': 'EUR', 'symbol': '€'},
        'hamburg': {'country': 'Germany', 'currency': 'EUR', 'symbol': '€'},
        'frankfurt': {'country': 'Germany', 'currency': 'EUR', 'symbol': '€'},
        'cologne': {'country': 'Germany', 'currency': 'EUR', 'symbol': '€'},
        'stuttgart': {'country': 'Germany', 'currency': 'EUR', 'symbol': '€'},
        'dusseldorf': {'country': 'Germany', 'currency': 'EUR', 'symbol': '€'},
        'dortmund': {'country': 'Germany', 'currency': 'EUR', 'symbol': '€'},
        
        # France
        'paris': {'country': 'France', 'currency': 'EUR', 'symbol': '€'},
        'marseille': {'country': 'France', 'currency': 'EUR', 'symbol': '€'},
        'lyon': {'country': 'France', 'currency': 'EUR', 'symbol': '€'},
        'toulouse': {'country': 'France', 'currency': 'EUR', 'symbol': '€'},
        'nice': {'country': 'France', 'currency': 'EUR', 'symbol': '€'},
        
        # Netherlands
        'amsterdam': {'country': 'Netherlands', 'currency': 'EUR', 'symbol': '€'},
        'rotterdam': {'country': 'Netherlands', 'currency': 'EUR', 'symbol': '€'},
        'the hague': {'country': 'Netherlands', 'currency': 'EUR', 'symbol': '€'},
        
        # Spain
        'madrid': {'country': 'Spain', 'currency': 'EUR', 'symbol': '€'},
        'barcelona': {'country': 'Spain', 'currency': 'EUR', 'symbol': '€'},
        'valencia': {'country': 'Spain', 'currency': 'EUR', 'symbol': '€'},
        'seville': {'country': 'Spain', 'currency': 'EUR', 'symbol': '€'},
        
        # Italy
        'rome': {'country': 'Italy', 'currency': 'EUR', 'symbol': '€'},
        'milan': {'country': 'Italy', 'currency': 'EUR', 'symbol': '€'},
        'naples': {'country': 'Italy', 'currency': 'EUR', 'symbol': '€'},
        
        # Japan
        'tokyo': {'country': 'Japan', 'currency': 'JPY', 'symbol': '¥'},
        'osaka': {'country': 'Japan', 'currency': 'JPY', 'symbol': '¥'},
        'kyoto': {'country': 'Japan', 'currency': 'JPY', 'symbol': '¥'},
        
        # Singapore
        'singapore': {'country': 'Singapore', 'currency': 'SGD', 'symbol': 'S$'},
        
        # New Zealand
        'auckland': {'country': 'New Zealand', 'currency': 'NZD', 'symbol': 'NZ$'},
        'wellington': {'country': 'New Zealand', 'currency': 'NZD', 'symbol': 'NZ$'},
        
        # Ireland
        'dublin': {'country': 'Ireland', 'currency': 'EUR', 'symbol': '€'},
        
        # Belgium
        'brussels': {'country': 'Belgium', 'currency': 'EUR', 'symbol': '€'},
        
        # Switzerland
        'zurich': {'country': 'Switzerland', 'currency': 'CHF', 'symbol': 'CHF'},
        'geneva': {'country': 'Switzerland', 'currency': 'CHF', 'symbol': 'CHF'},
        
        # Sweden
        'stockholm': {'country': 'Sweden', 'currency': 'SEK', 'symbol': 'SEK'},
        
        # Norway
        'oslo': {'country': 'Norway', 'currency': 'NOK', 'symbol': 'NOK'},
        
        # Denmark
        'copenhagen': {'country': 'Denmark', 'currency': 'DKK', 'symbol': 'DKK'},
        
        # Finland
        'helsinki': {'country': 'Finland', 'currency': 'EUR', 'symbol': '€'},
        
        # Austria
        'vienna': {'country': 'Austria', 'currency': 'EUR', 'symbol': '€'},
        
        # UAE
        'dubai': {'country': 'UAE', 'currency': 'AED', 'symbol': 'AED'},
        'abu dhabi': {'country': 'UAE', 'currency': 'AED', 'symbol': 'AED'},
        
        # Hong Kong
        'hong kong': {'country': 'Hong Kong', 'currency': 'HKD', 'symbol': 'HK$'},
        
        # China
        'beijing': {'country': 'China', 'currency': 'CNY', 'symbol': '¥'},
        'shanghai': {'country': 'China', 'currency': 'CNY', 'symbol': '¥'},
        'guangzhou': {'country': 'China', 'currency': 'CNY', 'symbol': '¥'},
        'shenzhen': {'country': 'China', 'currency': 'CNY', 'symbol': '¥'},
        
        # South Korea
        'seoul': {'country': 'South Korea', 'currency': 'KRW', 'symbol': '₩'},
        'busan': {'country': 'South Korea', 'currency': 'KRW', 'symbol': '₩'},
        
        # India
        'mumbai': {'country': 'India', 'currency': 'INR', 'symbol': '₹'},
        'delhi': {'country': 'India', 'currency': 'INR', 'symbol': '₹'},
        'bangalore': {'country': 'India', 'currency': 'INR', 'symbol': '₹'},
        'chennai': {'country': 'India', 'currency': 'INR', 'symbol': '₹'},
        'kolkata': {'country': 'India', 'currency': 'INR', 'symbol': '₹'},
        
        # Brazil
        'são paulo': {'country': 'Brazil', 'currency': 'BRL', 'symbol': 'R$'},
        'rio de janeiro': {'country': 'Brazil', 'currency': 'BRL', 'symbol': 'R$'},
        
        # Mexico
        'mexico city': {'country': 'Mexico', 'currency': 'MXN', 'symbol': 'MX$'},
        
        # Argentina
        'buenos aires': {'country': 'Argentina', 'currency': 'ARS', 'symbol': 'ARS$'},
        
        # South Africa
        'johannesburg': {'country': 'South Africa', 'currency': 'ZAR', 'symbol': 'R'},
        'cape town': {'country': 'South Africa', 'currency': 'ZAR', 'symbol': 'R'},
        
        # Israel
        'tel aviv': {'country': 'Israel', 'currency': 'ILS', 'symbol': '₪'},
        'jerusalem': {'country': 'Israel', 'currency': 'ILS', 'symbol': '₪'},
        
        # Turkey
        'istanbul': {'country': 'Turkey', 'currency': 'TRY', 'symbol': '₺'},
        'ankara': {'country': 'Turkey', 'currency': 'TRY', 'symbol': '₺'},
        
        # Russia
        'moscow': {'country': 'Russia', 'currency': 'RUB', 'symbol': '₽'},
        'saint petersburg': {'country': 'Russia', 'currency': 'RUB', 'symbol': '₽'},
    }
    
    location_lower = location.lower().strip()
    
    if location_lower in international_locations:
        return True, international_locations[location_lower]
    else:
        # Default to USD for unknown locations
        return False, {'country': 'Unknown', 'currency': 'USD', 'symbol': '$'}

def validate_address_format(address, location):
    """Basic address format validation"""
    if not address or len(address.strip()) < 5:
        return False, "Address too short"
    
    # Check for basic address components
    has_number = any(char.isdigit() for char in address)
    has_street = any(word in address.lower() for word in ['st', 'street', 'ave', 'avenue', 'rd', 'road', 'dr', 'drive', 'blvd', 'boulevard'])
    
    if not has_number:
        return False, "Address should include a street number"
    
    if not has_street:
        return False, "Address should include a street type"
    
    return True, "Valid address format"

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
        response = model.generate_content(prompt, generation_config={"name": "rent_analysis"})
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
    
    try:
        # Use Gemini API if available
        if GEMINI_API_KEY != 'YOUR_GEMINI_API_KEY':
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            response = model.generate_content(prompt, generation_config={"name": "rent_analysis"})
            response_text = response.text
            
            # Parse the response
            if 'EXPLANATION:' in response_text and 'TIPS:' in response_text:
                explanation_part = response_text.split('EXPLANATION:')[1].split('TIPS:')[0].strip()
                tips_part = response_text.split('TIPS:')[1].strip()
                
                return {
                    "explanation": explanation_part,
                    "negotiation_tips": tips_part
                }
        
        # Fallback to detailed explanation if API fails
        return get_detailed_fallback_explanation(user_listing, fairness_result, comparables)
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return get_detailed_fallback_explanation(user_listing, fairness_result, comparables)

def get_detailed_fallback_explanation(user_listing, fairness_result, comparables):
    """Generate detailed fallback explanation when Gemini API is unavailable"""
    
    # Calculate market statistics
    prices = [comp['price'] for comp in comparables]
    if prices:
        avg_price = statistics.mean(prices)
        median_price = statistics.median(prices)
        price_range = f"${min(prices):.0f} - ${max(prices):.0f}"
    else:
        avg_price = user_listing['price']
        median_price = user_listing['price']
        price_range = f"${user_listing['price']:.0f}"
    
    # Determine market position
    score = fairness_result.get('score', 0)
    if score > 10:
        market_position = "significantly above market"
        strategy = "emphasize competitive alternatives and be prepared to justify current rate"
    elif score > 5:
        market_position = "above market average"
        strategy = "highlight unique property features and negotiate for minor concessions"
    elif score < -5:
        market_position = "significantly below market"
        strategy = "leverage your strong position to request rent reduction or additional amenities"
    else:
        market_position = "fair market value"
        strategy = "focus on securing favorable lease terms and minor improvements"
    
    explanation = f"""
    This {user_listing['bedrooms']}-bedroom, {user_listing['bathrooms']}-bathroom property in {user_listing['location']} 
    is listed at ${user_listing['price']}/month, which is {market_position}. Based on our analysis of {len(comparables)} comparable listings 
    in the area, the market average is ${avg_price:.0f} with properties ranging from {price_range}.
    
    The price per square foot of ${user_listing['price'] / user_listing['sqft'] if user_listing['sqft'] else 0:.2f} 
    {'is competitive' if abs(score) <= 5 else 'offers good value' if score < -5 else 'requires market adjustment'}.
    
    {market_position.capitalize()} positioning provides you {strategy}.
    """
    
    tips = f"""
    • Research the {len(comparables)} comparable properties thoroughly to strengthen your negotiation position with specific market data points
    • Document any unique features or recent upgrades to the property that justify your {market_position} pricing
    • Consider the seasonal rental market in {user_listing['location']} - timing your negotiation during peak demand periods may yield better terms
    • Prepare alternative proposals with different rent amounts or lease terms to demonstrate flexibility during negotiations
    """
    
    return {
        "explanation": explanation.strip(),
        "negotiation_tips": tips.strip()
    }

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
        
        # Validate and clean data
        cleaned_listing, data_warnings = validate_and_clean_rent_data(user_listing)
        
        # Validate location
        is_valid_location, location_info = validate_location(cleaned_listing['location'])
        location_warnings = []
        
        if not is_valid_location:
            location_warnings.append(f"Location '{cleaned_listing['location']}' is not a recognized international city. Using {location_info['country']} with {location_info['currency']} currency for analysis.")
            # Use the provided location but with default currency info
        else:
            location_warnings.append(f"Analyzing property in {location_info['country']} using {location_info['currency']} currency.")
        
        # Add currency info to cleaned listing
        cleaned_listing['currency'] = location_info['currency']
        cleaned_listing['currency_symbol'] = location_info['symbol']
        cleaned_listing['country'] = location_info['country']
        
        # Validate address format
        address_valid, address_message = validate_address_format(cleaned_listing['address'], cleaned_listing['location'])
        address_warnings = []
        
        if not address_valid:
            address_warnings.append(address_message)
            # Generate a default address
            cleaned_listing['address'] = f"123 Main St, {cleaned_listing['location'].title()}"
        
        # Combine all warnings
        all_warnings = data_warnings + location_warnings + address_warnings
        
        # Generate comparable listings using Gemini with cleaned data
        gemini_listings = generate_comparable_listings_gemini(cleaned_listing)
        
        # Add coordinates to all listings (simple and fast)
        for listing in gemini_listings:
            coords = geocode_address(listing['address'], listing['location'])
            listing['lat'] = coords['lat']
            listing['lng'] = coords['lng']
        
        # Find comparable listings from the generated data
        comparables = find_comparables(cleaned_listing, gemini_listings)
        
        # Calculate fairness score
        fairness_result = calculate_fairness_score(cleaned_listing["price"], comparables)
        
        # Generate AI explanation with cleaned data
        ai_explanation = generate_ai_explanation(cleaned_listing, fairness_result, comparables)
        
        # Prepare response with warnings and currency info
        response = {
            "user_listing": cleaned_listing,
            "fairness_result": fairness_result,
            "comparables": comparables[:10],  # Limit to top 10 for display
            "ai_explanation": ai_explanation,
            "price_distribution": {
                "min": min(comp['price'] for comp in comparables) if comparables else cleaned_listing["price"],
                "max": max(comp['price'] for comp in comparables) if comparables else cleaned_listing["price"],
                "prices": [comp['price'] for comp in comparables]
            },
            "warnings": all_warnings,
            "data_quality": {
                "has_warnings": len(all_warnings) > 0,
                "warning_count": len(all_warnings),
                "data_cleaned": user_listing != cleaned_listing
            },
            "currency_info": {
                "currency": location_info['currency'],
                "symbol": location_info['symbol'],
                "country": location_info['country']
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
