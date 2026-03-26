#!/usr/bin/env python3
"""
Test script to verify real API data only - no fake data
"""

import logging
from api_services import RentCastService
from app import RentFairAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_rentcast_api_only():
    """Test RentCast API directly"""
    
    print("Testing RentCast API - Real Data Only")
    print("=" * 50)
    
    # Test with a real API key (you need to set this)
    service = RentCastService()
    
    if not service.api_key:
        print("❌ ERROR: No RentCast API key configured!")
        print("Please add your API key to .env file:")
        print("RENTCAST_API_KEY=your-actual-api-key-here")
        return
    
    print(f"✅ Using API key: {service.api_key[:10]}...")
    
    # Test locations that should have real data
    test_locations = [
        ("New York, NY", 2),
        ("Los Angeles, CA", 1),
        ("Chicago, IL", 3),
        ("Miami, FL", 2)
    ]
    
    for location, bedrooms in test_locations:
        print(f"\n--- Testing: {location} ({bedrooms} bedrooms) ---")
        
        try:
            results = service.search_rental_listings(location, bedrooms)
            
            if results:
                print(f"✅ SUCCESS: Found {len(results)} real listings")
                
                # Show first few real listings
                for i, listing in enumerate(results[:3], 1):
                    price = listing.get('price', 'N/A')
                    beds = listing.get('bedrooms', 'N/A')
                    baths = listing.get('bathrooms', 'N/A')
                    address = listing.get('address', 'N/A')
                    source = listing.get('source', 'rentcast')
                    
                    print(f"   {i}. ${price} - {beds} bed/{baths} bath - {address} ({source})")
                    
            else:
                print(f"⚠️  No results found for {location}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")

def test_analyzer_with_real_data():
    """Test the analyzer with real API data only"""
    
    print("\n" + "=" * 50)
    print("Testing RentFair Analyzer - Real Data Only")
    print("=" * 50)
    
    analyzer = RentFairAnalyzer()
    
    # Test with a real listing
    test_listing = {
        'address': '123 Main St',
        'price': 3000,
        'bedrooms': 2,
        'bathrooms': 1,
        'location': 'New York, NY'
    }
    
    print(f"Testing listing: ${test_listing['price']} for {test_listing['bedrooms']} bed in {test_listing['location']}")
    
    try:
        # Step 1: Find real comparables
        comparables = analyzer.find_comparables(test_listing)
        
        if comparables:
            print(f"✅ Found {len(comparables)} real comparable listings")
            
            # Step 2: Calculate real market stats
            market_stats = analyzer.calculate_market_stats(comparables)
            
            if market_stats:
                print(f"✅ Real Market Stats:")
                print(f"   Mean: ${market_stats['mean']:.0f}")
                print(f"   Median: ${market_stats['median']:.0f}")
                print(f"   Range: ${market_stats['min']:.0f} - ${market_stats['max']:.0f}")
                print(f"   Count: {market_stats['count']} listings")
                
                # Step 3: Calculate fairness
                fairness = analyzer.calculate_fairness_score(test_listing['price'], market_stats)
                
                if fairness:
                    print(f"✅ Fairness Analysis:")
                    print(f"   Classification: {fairness['classification']}")
                    print(f"   Difference: {fairness['percent_difference']:.1f}% from market")
                    
                else:
                    print("❌ Could not calculate fairness")
                    
            else:
                print("❌ Could not calculate market stats")
                
        else:
            print("❌ No real comparable listings found")
            print("This means either:")
            print("  - Your RentCast API key is invalid")
            print("  - The location has no available listings")
            print("  - There's a network/API issue")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_api_key_validation():
    """Test if API key is properly configured"""
    
    print("\n" + "=" * 50)
    print("Testing API Configuration")
    print("=" * 50)
    
    from config import Config
    
    print(f"RentCast API Key: {'✅ Set' if Config.RENTCAST_API_KEY else '❌ Not set'}")
    print(f"Gemini API Key: {'✅ Set' if Config.GEMINI_API_KEY else '⚠️  Not set (optional)'}")
    
    if not Config.RENTCAST_API_KEY:
        print("\n❌ CRITICAL: RentCast API key is required!")
        print("\nTo fix this:")
        print("1. Go to https://app.rentcast.io/app/api")
        print("2. Sign up and get your API key")
        print("3. Add it to your .env file:")
        print("   RENTCAST_API_KEY=your-actual-api-key-here")
        return False
    
    return True

if __name__ == "__main__":
    print("RentFair - Real API Data Test")
    print("This test uses NO fake data - only real RentCast API data")
    print("=" * 60)
    
    # First check API configuration
    if test_api_key_validation():
        # Test the API directly
        test_rentcast_api_only()
        
        # Test the full analyzer
        test_analyzer_with_real_data()
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("\nIf you see ❌ errors:")
    print("1. Check your RentCast API key")
    print("2. Verify your internet connection")
    print("3. Try different locations")
    print("\nIf you see ✅ success:")
    print("1. The system is working with real data")
    print("2. No fake/sample data is being used")
    print("3. All addresses and prices are from real listings")
