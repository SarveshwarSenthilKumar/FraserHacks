# 🚀 API Integration Setup Guide

This guide will help you set up RentFair with real rental data APIs and AI capabilities.

## 📋 Prerequisites

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Copy environment template:**
```bash
cp .env.example .env
```

## 🔑 API Keys Setup

### 1. RentCast API (Recommended)

**Steps:**
1. Go to [RentCast API Dashboard](https://app.rentcast.io/app/api)
2. Sign up for free account
3. Choose Developer plan (500 requests/month free)
4. Copy your API key

**Add to .env:**
```bash
RENTCAST_API_KEY=your-rentcast-api-key-here
```

### 2. Google Gemini API (For AI Explanations)

**Steps:**
1. Go to [Gemini API Keys](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

**Add to .env:**
```bash
GEMINI_API_KEY=your-gemini-api-key-here
```

### 3. Mapbox (For Location Intelligence)

**Steps:**
1. Go to [Mapbox](https://mapbox.com/)
2. Sign up for free account
3. Go to Account > Tokens
4. Copy your default public token

**Add to .env:**
```bash
MAPBOX_ACCESS_TOKEN=your-mapbox-access-token-here
```

## 🏗️ Architecture Overview

### API Services Structure

```
api_services.py
├── APIService (Base class)
├── RentCastService (Primary rental data)
├── NominatimService (Geocoding & distance)
├── GeminiService (AI explanations)
└── DataAggregator (Combines all sources)
```

### Data Flow

1. **User submits listing** → Flask app receives data
2. **RentCast API** → Fetches real rental listings
3. **DataAggregator** → Normalizes and processes data
4. **RentFairAnalyzer** → Calculates fairness scores
5. **GeminiService** → Generates AI tips
6. **NominatimService** → Geocodes address
7. **Results** → Returned to frontend

## 🔧 Configuration Options

### Environment Variables

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# API Keys (Required for features)
RENTCAST_API_KEY=your-rentcast-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here

# OpenStreetMap Nominatim (for geocoding)
# No API key required - uses free OpenStreetMap service

# Legacy API Keys (deprecated)
# RAPIDAPI_KEY=your-rapidapi-key-here
# OPENAI_API_KEY=your-openai-api-key-here
# MAPBOX_ACCESS_TOKEN=your-mapbox-access-token-here
# ZILLOW_API_KEY=your-zillow-api-key-here

# Performance
API_RATE_LIMIT=100 requests per hour
API_TIMEOUT=30
MAX_RETRIES=3
CACHE_TTL=3600
```

## 📊 API Integration Details

### RentCast Integration

**Supported Features:**
- Property search by location
- Filter by bedrooms, bathrooms, price range
- Get detailed property information
- Real-time rental data across US
- AI-powered rent estimates

**Example Usage:**
```python
rentcast_service.search_rental_listings(
    location="New York, NY",
    bedrooms=2,
    price_min=1500,
    price_max=4000
)
```

### Nominatim Integration (OpenStreetMap)

**Supported Features:**
- Free address geocoding (no API key required)
- Reverse geocoding (coordinates → address)
- Distance calculations between properties
- Global coverage via OpenStreetMap

**Example Usage:**
```python
nominatim_service.geocode_address("123 Main St, New York, NY")
# Returns: {'latitude': 40.7128, 'longitude': -74.0060, 'formatted_address': '...'}
```

### Gemini Integration

**Supported Features:**
- AI-powered negotiation tips
- Contextual advice based on market analysis
- Personalized recommendations
- Graceful fallback when unavailable

**Example Usage:**
```python
gemini_service.generate_negotiation_tips({
    'user_listing': {'price': 3500, 'bedrooms': 2},
    'fairness_result': {'classification': 'Overpriced'},
    'market_stats': {'mean': 3000, 'min': 2500, 'max': 4000}
})
```

### Mapbox Integration

**Features:**
- Address geocoding (address → coordinates)
- Distance calculations between properties
- Location clustering for comparables

**Example Usage:**
```python
coordinates = mapbox_service.geocode_address("123 Queen St, Mississauga")
# Returns: {'latitude': 43.5890, 'longitude': -79.6441}
```

## 🛠️ Testing the Integration

### 1. Test API Keys

```python
# Test RentCast
from api_services import RentCastService
service = RentCastService()
results = service.search_rental_listings("New York, NY", 2)
print(f"Found {len(results)} properties")

# Test Gemini
from api_services import GeminiService
gemini_service = GeminiService()
tips = gemini_service.generate_negotiation_tips(mock_data)
print(tips)

# Test Nominatim (OpenStreetMap)
from api_services import NominatimService
nominatim_service = NominatimService()
coords = nominatim_service.geocode_address("123 Main St, New York, NY")
print(coords)
```

### 2. Test Full Integration

Start the app and submit a test listing:
- Address: `123 Main St, New York, NY`
- Rent: `$3500`
- Bedrooms: `2`
- Bathrooms: `1`

**Expected Results:**
- RentCast data should appear in comparables
- Gemini AI tips should be generated (if API key is set)
- Nominatim coordinates should be calculated (no key required)

## 🚨 Error Handling

### Graceful Degradation

The system is designed to work even without all APIs:

- **No API keys**: Falls back to sample data
- **API failures**: Shows error messages but continues working
- **Rate limits**: Implements exponential backoff
- **Missing data**: Provides fallback explanations

### Common Issues

**1. API Key Not Working**
```bash
# Check if key is set
echo $RENTCAST_API_KEY

# Test API directly
curl -X GET "https://api.rentcast.io/v1/listings/rental-long-term?location=New%20York%2C%20NY&status=active" \
  -H "accept: application/json" \
  -H "X-API-Key: YOUR_KEY"
```

**2. Rate Limiting**
- Check RentCast dashboard for usage limits
- Implement caching to reduce API calls
- Upgrade plan if needed (500 requests/month free)

**3. Invalid Locations**
- Use standardized city names
- Implement location validation
- Provide location suggestions

## 📈 Performance Optimization

### Caching Strategy

```python
# Redis caching for API responses
@cache.memoize(timeout=3600)  # 1 hour cache
def get_comparables(location, bedrooms):
    return data_aggregator.get_comparables(location, bedrooms)
```

### Rate Limiting

```python
# Implement rate limiting per user
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/analyze-rent', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_rent():
    # Your code here
```

## 🔮 Future Enhancements

### Additional APIs to Consider

1. **Craigslist API** - More rental listings
2. **Apartments.com API** - Apartment-specific data
3. **Google Places API** - Location amenities
4. **Walk Score API** - Neighborhood walkability
5. **Transit APIs** - Public transportation data

### Advanced Features

1. **Historical Price Tracking** - Store and analyze price trends
2. **User Accounts** - Save analyses and set alerts
3. **Mobile App** - React Native implementation
4. **Machine Learning** - Predictive pricing models
5. **Market Reports** - PDF generation for detailed analysis

## 🆘 Troubleshooting

### Quick Fixes

**Issue: "No comparable listings found"**
- Check if RentCast API key is valid
- Verify location format (use "City, State" format)
- Try broader search parameters
- Check if location is in RentCast coverage area

**Issue: "AI tips not showing"**
- Verify Gemini API key
- Check Google Cloud Console for usage
- Review API quota limits (15 requests/minute free)

**Issue: "Coordinates not calculated"**
- Check internet connection (Nominatim requires internet)
- Verify address format and spelling
- Wait for rate limit (1 request per second max)

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs for API responses and errors.

---

**Need help?** Check the API documentation for each service or create an issue in the repository.
