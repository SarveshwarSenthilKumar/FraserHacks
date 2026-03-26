# 🏠 RentCast API Setup Guide

## 🔗 RentCast API Links

**Main Website:** https://www.rentcast.io/api
**API Documentation:** https://developers.rentcast.io/
**Direct API Dashboard:** https://app.rentcast.io/app/api

## 🚀 Quick Setup

### 1. Get Your RentCast API Key

1. **Go to:** https://app.rentcast.io/app/api
2. **Sign up** for free account
3. **Choose your plan:**
   - **Developer:** Free (500 requests/month)
   - **Foundation:** $29/month (5,000 requests)
   - **Growth:** $99/month (20,000 requests)
4. **Copy your API key** from the dashboard

### 2. Configure Environment

Create `.env` file:
```bash
# Copy the template
cp .env.example .env

# Edit .env with your key
RENTCAST_API_KEY=your-actual-rentcast-api-key-here
```

### 3. Test the API

```python
# Test script
from api_services import RentCastService

service = RentCastService()
results = service.search_rental_listings("New York, NY", 2)
print(f"Found {len(results)} rental listings")
for result in results[:3]:
    print(f"- ${result['price']}: {result['bedrooms']} bed, {result['address']}")
```

## RentCast API Endpoints

### 1. Search Rental Listings
**Endpoint:** `/listings/rental/long-term`
**Usage:** Find active rental properties
```python
rentcast_service.search_rental_listings("New York, NY", bedrooms=2, price_min=2000, price_max=4000)
```

### 2. Get Rent Estimate
**Endpoint:** `/avm/rent/long-term`
**Usage:** Get AI-powered rent estimate for specific address
```python
service.get_rent_estimate("123 Main St, New York, NY")
```

### 3. Search Properties
**Endpoint:** `/properties`
**Usage:** Get property records by location
```python
service.search_properties_by_location("New York", "NY")
```

### 4. Property Details
**Endpoint:** `/properties/{id}`
**Usage:** Get detailed property information
```python
service.get_property_details("property_id_here")
```

## 🔧 API Response Format

The API returns data like this:
```json
[
  {
    "id": "12345678",
    "address": {
      "streetAddress": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zipCode": "10001"
    },
    "price": 3500,
    "bedrooms": 2,
    "bathrooms": 1,
    "livingArea": 850,
    "latitude": 40.7128,
    "longitude": -74.0060
  }
]
```

## 🎯 Integration with RentFair

### Updated Data Flow

1. **User submits listing** → Flask app
2. **RentCast API** → Search for comparable rentals
3. **Data normalization** → Convert to standard format
4. **Fairness analysis** → Calculate scores
5. **Results** → Display with real data

### Key Features Enabled

- ✅ **Live rental data** from RentCast
- ✅ **Real-time pricing** across US markets
- ✅ **Address validation**
- ✅ **Coordinates** for mapping
- ✅ **Property details** with comprehensive data
- ✅ **Rent estimates** for any address

## 🚨 Important Notes

### Coverage Areas
- **US:** Full coverage (all 50 states)
- **Canada:** Limited coverage
- **International:** Not available

### Rate Limits
- **Developer:** 500 requests/month
- **Foundation:** 5,000 requests/month
- **Growth:** 20,000 requests/month
- **Scale:** 100,000 requests/month

### Data Quality
- **140+ million property records**
- **Real-time updates**
- **AI-powered rent estimates**
- **Comprehensive property details**

## 🛠️ Troubleshooting

### Common Issues

**1. "API Key Not Working"**
```bash
# Test your key directly
curl -X GET "https://api.rentcast.io/v1/listings/rental-long-term?location=New%20York%2C%20NY&status=active" \
  -H "accept: application/json" \
  -H "X-API-Key: YOUR_KEY"
```

**2. "No Results Found"**
- Try different location formats: "New York, NY" or "New York"
- Check if location is in RentCast's database
- Use broader search terms

**3. "Rate Limited"**
- Check your RentCast dashboard
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
    return rentcast_service.search_rental_listings(location, bedrooms)
```

### Optimized Queries
```python
# Use specific filters to reduce API calls
results = service.search_rental_listings(
    location="New York, NY",
    bedrooms=2,
    price_min=2000,
    price_max=4000
)
```

## 🎉 Success Indicators

When properly configured, you should see:
- Real rental listings from RentCast
- Current market prices across US cities
- Actual addresses with coordinates
- Comprehensive property details
- AI-powered rent estimates

**Test with:** `New York, NY, $3500, 2 bed, 1 bath`

Should return comparable listings from RentCast with real pricing data! 🚀

## 🆚 RentCast vs Previous APIs

| Feature | RentCast | Zillow/RapidAPI |
|---------|----------|-----------------|
| **Coverage** | US nationwide | Variable |
| **Data Quality** | 140M+ records | Limited |
| **API Stability** | Professional | Hobbyist |
| **Documentation** | Comprehensive | Basic |
| **Pricing** | Transparent | Variable |
| **Support** | 24/7 chat | Community |

## 💰 Pricing Plans

| Plan | Price | Requests/Month | Features |
|------|-------|---------------|----------|
| Developer | Free | 500 | Basic access |
| Foundation | $29 | 5,000 | Full features |
| Growth | $99 | 20,000 | Priority support |
| Scale | $299 | 100,000 | Enterprise features |

**Recommendation:** Start with Developer plan, upgrade as needed!
