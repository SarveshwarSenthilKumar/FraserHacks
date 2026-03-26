import requests
import json
import time
from typing import List, Dict, Optional
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIService:
    """Base class for API services"""
    
    def __init__(self):
        self.timeout = Config.API_TIMEOUT
        self.max_retries = Config.MAX_RETRIES
    
    def _make_request(self, url: str, headers: Dict = None, params: Dict = None, method: str = 'GET') -> Optional[Dict]:
        """Make HTTP request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"API request failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"API request failed after {self.max_retries} attempts: {e}")
                    return None

class RapidAPIService(APIService):
    """Service for RapidAPI rental data"""
    
    def __init__(self):
        super().__init__()
        self.api_key = Config.RAPIDAPI_KEY
        self.host = Config.RAPIDAPI_HOST
        
        if not self.api_key:
            logger.warning("RapidAPI key not configured")
    
    def search_properties(self, location: str, bedrooms: int = None, price_min: int = None, price_max: int = None) -> List[Dict]:
        """Search for properties using RapidAPI"""
        if not self.api_key:
            return []
        
        url = f"https://{self.host}/properties/v3/list"
        
        headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.host
        }
        
        params = {
            'location': location,
            'type': 'rent'
        }
        
        if bedrooms:
            params['beds_min'] = bedrooms
            params['beds_max'] = bedrooms + 1  # Allow ±1 bedroom
        
        if price_min:
            params['price_min'] = price_min
        if price_max:
            params['price_max'] = price_max
        
        try:
            data = self._make_request(url, headers, params)
            if data and 'properties' in data:
                return self._normalize_rapidapi_data(data['properties'])
        except Exception as e:
            logger.error(f"Error searching properties: {e}")
        
        return []
    
    def _normalize_rapidapi_data(self, properties: List[Dict]) -> List[Dict]:
        """Normalize RapidAPI data to our standard format"""
        normalized = []
        
        for prop in properties:
            try:
                normalized_property = {
                    'price': prop.get('price', 0),
                    'bedrooms': prop.get('beds', 0),
                    'bathrooms': prop.get('baths', 0),
                    'location': prop.get('address', {}).get('city', ''),
                    'sqft': prop.get('lot_size', 0) or prop.get('building_size', {}).get('size', 0),
                    'address': prop.get('address', {}).get('line', ''),
                    'latitude': prop.get('address', {}).get('lat'),
                    'longitude': prop.get('address', {}).get('lon'),
                    'source': 'rapidapi'
                }
                normalized.append(normalized_property)
            except Exception as e:
                logger.warning(f"Error normalizing property: {e}")
                continue
        
        return normalized

class RentCastService(APIService):
    """Service for RentCast API"""
    
    def __init__(self):
        super().__init__()
        self.api_key = Config.RENTCAST_API_KEY
        self.base_url = 'https://api.rentcast.io/v1'
        
        if not self.api_key:
            logger.warning("RentCast API key not configured")
    
    def search_rental_listings(self, location: str, bedrooms: int = None, price_min: int = None, price_max: int = None) -> List[Dict]:
        """Search rental listings using RentCast API"""
        if not self.api_key:
            logger.error("RentCast API key not configured")
            return []
        
        url = f"{self.base_url}/listings/rental/long-term"
        
        headers = {
            'accept': 'application/json',
            'X-API-Key': self.api_key
        }
        
        params = {
            'location': location,
            'status': 'active'
        }
        
        if bedrooms:
            params['bedrooms'] = bedrooms
        if price_min:
            params['priceMin'] = price_min
        if price_max:
            params['priceMax'] = price_max
        
        try:
            response = self._make_request(url, headers, params)
            if response and isinstance(response, list):
                logger.info(f"Successfully got {len(response)} listings from RentCast API")
                return self._normalize_rentcast_data(response)
            else:
                logger.warning(f"RentCast API returned unexpected response: {type(response)}")
                return []
        except Exception as e:
            error_msg = str(e).lower()
            if '401' in error_msg or 'unauthorized' in error_msg:
                logger.error("❌ RentCast API key is INVALID or EXPIRED")
                logger.error("Please get a new API key from: https://app.rentcast.io/app/api")
            elif '404' in error_msg:
                logger.error(f"❌ RentCast API endpoint not found for: {location}")
                logger.error("Try using a different US city/state format")
            else:
                logger.error(f"❌ RentCast API error: {e}")
            return []
    
    def get_rent_estimate(self, address: str) -> Dict:
        """Get rent estimate for a specific property"""
        if not self.api_key:
            return {}
        
        url = f"{self.base_url}/avm/rent/long-term"
        
        headers = {
            'accept': 'application/json',
            'X-API-Key': self.api_key
        }
        
        params = {
            'address': address
        }
        
        try:
            data = self._make_request(url, headers, params)
            return data or {}
        except Exception as e:
            logger.error(f"Error getting rent estimate: {e}")
            return {}
    
    def get_property_details(self, property_id: str) -> Dict:
        """Get detailed property information by ID"""
        if not self.api_key:
            return {}
        
        url = f"{self.base_url}/properties/{property_id}"
        
        headers = {
            'accept': 'application/json',
            'X-API-Key': self.api_key
        }
        
        try:
            data = self._make_request(url, headers)
            return data or {}
        except Exception as e:
            logger.error(f"Error getting property details: {e}")
            return {}
    
    def search_properties_by_location(self, city: str, state: str = None) -> List[Dict]:
        """Search properties in a specific city/state"""
        if not self.api_key:
            return []
        
        location = f"{city}, {state}" if state else city
        
        url = f"{self.base_url}/properties"
        
        headers = {
            'accept': 'application/json',
            'X-API-Key': self.api_key
        }
        
        params = {
            'location': location,
            'limit': 50
        }
        
        try:
            data = self._make_request(url, headers, params)
            if data and isinstance(data, list):
                return self._normalize_rentcast_data(data)
        except Exception as e:
            logger.error(f"Error searching properties by location: {e}")
        
        return []
    
    def _normalize_rentcast_data(self, listings: List[Dict]) -> List[Dict]:
        """Normalize RentCast data to our standard format"""
        normalized = []
        
        for listing in listings:
            try:
                # Handle different RentCast response formats
                price = 0
                if 'price' in listing:
                    price = listing['price']
                elif 'rentPrice' in listing:
                    price = listing['rentPrice']
                elif 'listPrice' in listing:
                    price = listing['listPrice']
                
                # Extract bedrooms count
                bedrooms = 0
                if 'bedrooms' in listing:
                    bedrooms = listing['bedrooms']
                elif 'beds' in listing:
                    bedrooms = listing['beds']
                elif 'numBedrooms' in listing:
                    bedrooms = listing['numBedrooms']
                
                # Extract bathrooms count
                bathrooms = 0
                if 'bathrooms' in listing:
                    bathrooms = listing['bathrooms']
                elif 'baths' in listing:
                    bathrooms = listing['baths']
                elif 'numBathrooms' in listing:
                    bathrooms = listing['numBathrooms']
                
                # Extract location/address info
                location = ''
                address = ''
                city = ''
                state = ''
                
                if 'address' in listing:
                    addr_data = listing['address']
                    if isinstance(addr_data, dict):
                        address = addr_data.get('streetAddress', '') or addr_data.get('line', '') or addr_data.get('fullAddress', '')
                        city = addr_data.get('city', '')
                        state = addr_data.get('state', '')
                        location = city
                    else:
                        address = str(addr_data)
                elif 'city' in listing:
                    city = listing['city']
                    location = city
                    if 'state' in listing:
                        location += f", {listing['state']}"
                
                # Extract square footage
                sqft = 0
                if 'livingArea' in listing:
                    sqft = listing['livingArea']
                elif 'area' in listing:
                    sqft = listing['area']
                elif 'squareFootage' in listing:
                    sqft = listing['squareFootage']
                elif 'lotSize' in listing:
                    sqft = listing['lotSize']
                
                # Extract coordinates
                latitude = listing.get('latitude') or listing.get('lat')
                longitude = listing.get('longitude') or listing.get('lon')
                
                # Extract property ID
                property_id = listing.get('id') or listing.get('propertyId') or listing.get('_id')
                
                normalized_property = {
                    'price': price,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'location': location,
                    'city': city,
                    'state': state,
                    'sqft': sqft,
                    'address': address,
                    'latitude': latitude,
                    'longitude': longitude,
                    'property_id': property_id,
                    'source': 'rentcast'
                }
                
                # Only include if we have essential data
                if price > 0 and bedrooms > 0:
                    normalized.append(normalized_property)
                    
            except Exception as e:
                logger.warning(f"Error normalizing RentCast listing: {e}")
                continue
        
        return normalized

class NominatimService(APIService):
    """Service for OpenStreetMap Nominatim geocoding"""
    
    def __init__(self):
        super().__init__()
        self.base_url = 'https://nominatim.openstreetmap.org'
        self.user_agent = 'RentFair/1.0 (rental-analysis-app)'
        self.timeout = 10  # Increased timeout for better reliability
        
        # Nominatim doesn't require API key, but has rate limits
        logger.info("Using Nominatim (OpenStreetMap) - no API key required")
    
    def geocode_address(self, address: str) -> Optional[Dict]:
        """Convert address to coordinates using Nominatim"""
        if not address:
            return None
        
        url = f"{self.base_url}/search"
        
        headers = {
            'User-Agent': self.user_agent
        }
        
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1,
            'countrycodes': 'ca,us'  # Canada and US
        }
        
        try:
            # Add delay to respect rate limits (1 request per second max)
            import time
            time.sleep(1)
            
            # Use longer timeout and retry logic
            data = self._make_request_with_retry(url, headers, params, max_retries=2)
            if data and len(data) > 0:
                result = data[0]
                return {
                    'latitude': float(result.get('lat', 0)),
                    'longitude': float(result.get('lon', 0)),
                    'formatted_address': result.get('display_name', ''),
                    'confidence': result.get('importance', 0),
                    'address_details': result.get('address', {}),
                    'osm_id': result.get('osm_id'),
                    'osm_type': result.get('osm_type')
                }
        except Exception as e:
            logger.error(f"Error geocoding address with Nominatim: {e}")
            # Return None instead of raising to allow graceful fallback
            return None
    
    def _make_request_with_retry(self, url: str, headers: Dict = None, params: Dict = None, max_retries: int = 2) -> Optional[Dict]:
        """Make HTTP request with retry logic for Nominatim"""
        import requests
        from requests.exceptions import RequestException, ConnectTimeout, ReadTimeout
        
        for attempt in range(max_retries + 1):
            try:
                response = requests.get(
                    url, 
                    headers=headers, 
                    params=params, 
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except ConnectTimeout:
                logger.warning(f"Connection timeout (attempt {attempt + 1}/{max_retries + 1}) for Nominatim")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    logger.error("Failed to connect to Nominatim after multiple attempts")
                    return None
            except ReadTimeout:
                logger.warning(f"Read timeout (attempt {attempt + 1}/{max_retries + 1}) for Nominatim")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    logger.error("Failed to read from Nominatim after multiple attempts")
                    return None
            except RequestException as e:
                logger.warning(f"Request error (attempt {attempt + 1}/{max_retries + 1}): {e}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    logger.error(f"Failed to connect to Nominatim: {e}")
                    return None
            except Exception as e:
                logger.error(f"Unexpected error (attempt {attempt + 1}/{max_retries + 1}): {e}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    return None
        
        return None
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """Convert coordinates to address using Nominatim"""
        url = f"{self.base_url}/reverse"
        
        headers = {
            'User-Agent': self.user_agent
        }
        
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
            'addressdetails': 1
        }
        
        try:
            # Add delay to respect rate limits
            import time
            time.sleep(1)
            
            data = self._make_request_with_retry(url, headers, params)
            if data:
                return {
                    'formatted_address': data.get('display_name', ''),
                    'address_details': data.get('address', {}),
                    'latitude': lat,
                    'longitude': lon
                }
        except Exception as e:
            logger.error(f"Error reverse geocoding with Nominatim: {e}")
        
        return None
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad, lon1_rad = radians(lat1), radians(lon1)
        lat2_rad, lon2_rad = radians(lat2), radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c

class GeminiService(APIService):
    """Service for Google Gemini API"""
    
    def __init__(self):
        super().__init__()
        self.api_key = Config.GEMINI_API_KEY
        self.base_url = 'https://generativelanguage.googleapis.com/v1beta'
        self.model_name = Config.GEMINI_MODEL or 'gemini-2.5-flash-lite'
        
        if not self.api_key:
            logger.warning("Gemini API key not configured")
    
    def generate_negotiation_tips(self, analysis_result: Dict) -> str:
        """Generate AI-powered negotiation tips using Gemini"""
        if not self.api_key:
            return self._generate_fallback_tips(analysis_result)
        
        url = f"{self.base_url}/models/{self.model_name}:generateContent"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        params = {
            'key': self.api_key
        }
        
        prompt = self._build_negotiation_prompt(analysis_result)
        
        data = {
            'contents': [{
                'parts': [{
                    'text': prompt
                }]
            }],
            'generationConfig': {
                'temperature': 0.7,
                'maxOutputTokens': 200,
                'topK': 40,
                'topP': 0.95
            }
        }
        
        try:
            response = requests.post(url, headers=headers, params=params, json=data, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    return candidate['content']['parts'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Error generating Gemini tips: {e}")
        
        return self._generate_fallback_tips(analysis_result)
    
    def _build_negotiation_prompt(self, analysis_result: Dict) -> str:
        """Build prompt for Gemini API"""
        user_listing = analysis_result.get('user_listing', {})
        fairness_result = analysis_result.get('fairness_result', {})
        market_stats = analysis_result.get('market_stats', {})
        
        prompt = f"""You are a helpful rental negotiation assistant. Based on this rental analysis, provide 2-3 specific, actionable negotiation tips. Be concise and practical.

Listing Details:
- Address: {user_listing.get('address', 'N/A')}
- Rent: ${user_listing.get('price', 0):,}
- {user_listing.get('bedrooms', 0)} bed, {user_listing.get('bathrooms', 0)} bath
- Location: {user_listing.get('location', 'N/A')}

Market Analysis:
- Classification: {fairness_result.get('classification', 'N/A')}
- Market Average: ${market_stats.get('mean', 0):,}
- Price Range: ${market_stats.get('min', 0):,} - ${market_stats.get('max', 0):,}

Provide practical, respectful negotiation advice in 2-3 bullet points."""
        
        return prompt
    
    def _generate_fallback_tips(self, analysis_result: Dict) -> str:
        """Generate fallback tips without AI"""
        fairness_result = analysis_result.get('fairness_result', {})
        market_stats = analysis_result.get('market_stats', {})
        classification = fairness_result.get('classification', 'Fair')
        
        if classification == 'Overpriced':
            return f"• Reference comparable listings in the ${market_stats.get('median', 0):,} range\n• Highlight your strong rental history and stable income\n• Mention you're looking for a long-term lease"
        elif classification == 'Underpriced':
            return "• Be prepared to act quickly as this is a good deal\n• Have all documentation ready (references, credit check)\n• Consider offering a longer lease for stability"
        else:
            return "• This appears to be fairly priced\n• Focus on other terms like lease duration or amenities\n• Be prepared with references to show you're a reliable tenant"

class DataAggregator:
    """Aggregates data from multiple sources"""
    
    def __init__(self):
        self.rentcast_service = RentCastService()
        self.nominatim_service = NominatimService()
        self.gemini_service = GeminiService()
    
    def get_comparables(self, location: str, bedrooms: int, max_results: int = 50) -> List[Dict]:
        """Get comparable listings from RentCast API only - no fake data"""
        
        logger.info(f"Searching for {bedrooms} bedroom rentals in {location}")
        
        # Try RentCast API only - no fallback to fake data
        try:
            rentcast_results = self.rentcast_service.search_rental_listings(location, bedrooms)
            
            if rentcast_results:
                logger.info(f"Got {len(rentcast_results)} real listings from RentCast API")
                
                # Limit results and remove duplicates
                unique_comparables = self._remove_duplicates(rentcast_results)
                final_results = unique_comparables[:max_results]
                
                logger.info(f"Returning {len(final_results)} unique real listings")
                return final_results
            else:
                logger.warning("RentCast API returned no results")
                return []
                
        except Exception as e:
            logger.error(f"Error calling RentCast API: {e}")
            return []
    
    def _remove_duplicates(self, listings: List[Dict]) -> List[Dict]:
        """Remove duplicate listings based on address and price"""
        seen = set()
        unique = []
        
        for listing in listings:
            key = (listing.get('address', ''), listing.get('price', 0))
            if key not in seen:
                seen.add(key)
                unique.append(listing)
        
        return unique
    
    
