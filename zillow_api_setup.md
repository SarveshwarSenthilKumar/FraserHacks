# 🏠 Private Zillow API Setup Guide

## 🔗 Direct API Link

**Private Zillow API:** https://rapidapi.com/oneapiproject/api/private-zillow/playground/apiendpoint_653d8fa2-eaa4-4447-bbdf-eb28b89b46bc

## 🚀 Quick Setup

### 1. Get Your RapidAPI Key

1. **Go to:** https://rapidapi.com/hub
2. **Sign up** for free account
3. **Navigate to:** https://rapidapi.com/oneapiproject/api/private-zillow
4. **Click "Subscribe to Test"** (Basic plan is free)
5. **Copy your RapidAPI key** from the dashboard

### 2. Configure Environment

Create `.env` file:
```bash
# Copy the template
cp .env.example .env

# Edit .env with your key
RAPIDAPI_KEY=your-actual-rapidapi-key-here
RAPIDAPI_HOST=private-zillow.p.rapidapi.com
```

### 3. Test the API

```python
# Test script
from api_services import ZillowAPIService

service = ZillowAPIService()
results = service.search_rental_listings("Mississauga", 2)
print(f"Found {len(results)} rental listings")
for result in results[:3]:
    print(f"- ${result['price']}: {result['bedrooms']} bed, {result['address']}")
```

## 📊 API Endpoints Available

### 1. Search Properties
**Endpoint:** `/search`
**Usage:** Find rental properties by location
```python
service.search_rental_listings("Mississauga", bedrooms=2)
```

### 2. Get Property Details
**Endpoint:** `/property`
**Usage:** Get detailed info by ZPID (Zillow Property ID)
```python
service.get_property_details(zpid=12345678)
```

### 3. Search by Address
**Endpoint:** `/search`
**Usage:** Find specific property by address
```python
service.search_by_address("123 Queen St, Mississauga")
```

## 🔧 API Response Format

The API returns data like this:
```json
{
  "results": [
    {
      "zpid": 12345678,
      "price": 2400,
      "bedrooms": 2,
      "bathrooms": 1,
      "address": {
        "streetAddress": "123 Queen St",
        "city": "Mississauga",
        "state": "ON",
        "zipCode": "L5B1B9"
      },
      "livingArea": 850,
      "latitude": 43.5890,
      "longitude": -79.6441
    }
  ]
}
```

## 🎯 Integration with RentFair

### Updated Data Flow

1. **User submits listing** → Flask app
2. **Zillow API** → Search for comparable rentals
3. **Data normalization** → Convert to standard format
4. **Fairness analysis** → Calculate scores
5. **Results** → Display with real data

### Key Features Enabled

- ✅ **Live rental data** from Zillow
- ✅ **Real-time pricing** 
- ✅ **Address validation**
- ✅ **Coordinates** for mapping
- ✅ **Property details** with ZPID

## 🚨 Important Notes

### Rate Limits
- **Free tier:** 100 requests/day
- **Basic plan:** 1,000 requests/day
- **Pro plan:** 10,000 requests/day

### Data Coverage
- **US:** Full coverage
- **Canada:** Limited coverage (major cities)
- **Other:** Variable coverage

### Error Handling
The system includes:
- Automatic fallback to sample data
- Retry logic with exponential backoff
- Comprehensive error logging
- Graceful degradation

## 🛠️ Troubleshooting

### Common Issues

**1. "API Key Not Working"**
```bash
# Test your key directly
curl -X GET "https://private-zillow.p.rapidapi.com/search?location=Mississauga&status=forRent" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: private-zillow.p.rapidapi.com"
```

**2. "No Results Found"**
- Try different city names (e.g., "Toronto, ON")
- Check if location is in Zillow's database
- Use broader search terms

**3. "Rate Limited"**
- Check your RapidAPI dashboard
- Upgrade plan if needed
- Implement caching

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Tips

### Caching Strategy
```python
# Cache results for 1 hour
@cache.memoize(timeout=3600)
def get_comparables(location, bedrooms):
    return zillow_service.search_rental_listings(location, bedrooms)
```

### Batch Requests
```python
# Search multiple areas at once
locations = ["Mississauga", "Toronto", "Brampton"]
for location in locations:
    results = service.search_rental_listings(location, 2)
```

## 🎉 Success Indicators

When properly configured, you should see:
- Real rental listings in results
- Current market prices
- Actual addresses and coordinates
- Property details with ZPID

**Test with:** `123 Queen St, Mississauga, $2400, 2 bed, 1 bath`

Should return comparable listings from Zillow with real pricing data! 🚀
