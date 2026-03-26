#!/usr/bin/env python3
"""
Test script to verify RentCast API endpoints work correctly
"""

import requests
import json

# Test with your actual API key
API_KEY = "your-rentcast-api-key-here"  # Replace with your actual key
BASE_URL = "https://api.rentcast.io/v1"

def test_rentcast_endpoints():
    """Test various RentCast API endpoints to find the correct ones"""
    
    headers = {
        'accept': 'application/json',
        'X-API-Key': API_KEY
    }
    
    endpoints_to_test = [
        # Rental listings endpoints
        f"{BASE_URL}/listings/rental/long-term",
        f"{BASE_URL}/listings/rental-long-term",  # Old incorrect one
        f"{BASE_URL}/listings/rent/long-term",
        f"{BASE_URL}/listings/rental",
        
        # Rent estimate endpoints  
        f"{BASE_URL}/avm/rent/long-term",
        f"{BASE_URL}/avm/rent-estimate",
        f"{BASE_URL}/avm/rent",
        
        # Property endpoints
        f"{BASE_URL}/properties",
        f"{BASE_URL}/listings",
    ]
    
    print("Testing RentCast API endpoints...")
    print(f"API Key: {API_KEY[:10]}..." if API_KEY else "No API key provided")
    print("-" * 50)
    
    for endpoint in endpoints_to_test:
        print(f"\nTesting: {endpoint}")
        
        params = {
            'location': 'New York, NY',
            'status': 'active'
        }
        
        try:
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ SUCCESS - Found {len(data)} results")
                    if data:
                        print(f"Sample result: {json.dumps(data[0], indent=2)[:200]}...")
                elif isinstance(data, dict):
                    print(f"✅ SUCCESS - Got dict response")
                    print(f"Keys: {list(data.keys())}")
                else:
                    print(f"✅ SUCCESS - Got {type(data)} response")
                    
            elif response.status_code == 404:
                print("❌ 404 - Endpoint not found")
                
            elif response.status_code == 401:
                print("❌ 401 - Unauthorized (check API key)")
                
            elif response.status_code == 403:
                print("❌ 403 - Forbidden (check permissions)")
                
            else:
                print(f"❌ {response.status_code} - {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print("❌ Timeout - Request took too long")
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error - Can't reach server")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_with_sample_data():
    """Test with actual sample data"""
    print("\n" + "="*50)
    print("Testing with sample rental data...")
    
    headers = {
        'accept': 'application/json',
        'X-API-Key': API_KEY
    }
    
    # Test the correct endpoint we think works
    url = f"{BASE_URL}/listings/rental/long-term"
    
    params = {
        'location': 'New York, NY',
        'bedrooms': 2,
        'status': 'active'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Found {len(data)} rental listings")
            
            # Show sample data
            for i, listing in enumerate(data[:3]):
                print(f"\n--- Listing {i+1} ---")
                print(f"Price: ${listing.get('price', 'N/A')}")
                print(f"Bedrooms: {listing.get('bedrooms', 'N/A')}")
                print(f"Bathrooms: {listing.get('bathrooms', 'N/A')}")
                print(f"Address: {listing.get('address', 'N/A')}")
                
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # First test all endpoints
    test_rentcast_endpoints()
    
    # Then test with sample data
    test_with_sample_data()
    
    print("\n" + "="*50)
    print("Test complete!")
    print("If you see 404 errors, the endpoint doesn't exist.")
    print("If you see 401/403 errors, check your API key.")
    print("If you see 200 responses, that endpoint works!")
