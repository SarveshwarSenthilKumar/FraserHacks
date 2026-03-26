#!/usr/bin/env python3
"""
Test script to verify comparable listings work with REAL API data only - NO FAKE DATA
"""

import logging
from api_services import DataAggregator
from app import RentFairAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_real_comparables_only():
    """Test the comparable listings functionality with REAL data only"""
    
    print("Testing Comparable Listings - REAL API Data Only")
    print("=" * 60)
    print("⚠️  This test uses NO fake/sample data")
    print("⚠️  Requires valid RentCast API key")
    print("=" * 60)
    
    # Test cases with real locations
    test_cases = [
        {
            'address': '123 Main St',
            'price': 3500,
            'bedrooms': 2,
            'bathrooms': 1,
            'location': 'New York, NY'
        },
        {
            'address': '456 Oak Ave',
            'price': 2800,
            'bedrooms': 1,
            'bathrooms': 1,
            'location': 'Los Angeles, CA'
        },
        {
            'address': '789 King St',
            'price': 4200,
            'bedrooms': 3,
            'bathrooms': 2,
            'location': 'Chicago, IL'
        }
    ]
    
    analyzer = RentFairAnalyzer()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Location: {test_case['location']}")
        print(f"Bedrooms: {test_case['bedrooms']}")
        print(f"Price: ${test_case['price']}")
        
        try:
            # Step 1: Find REAL comparables only
            comparables = analyzer.find_comparables(test_case)
            
            if comparables:
                print(f"✅ Found {len(comparables)} REAL comparable listings from RentCast API")
                
                # Show first few REAL comparables
                for j, comp in enumerate(comparables[:3], 1):
                    price = comp.get('price', 'N/A')
                    beds = comp.get('bedrooms', 'N/A')
                    baths = comp.get('bathrooms', 'N/A')
                    address = comp.get('address', 'N/A')
                    source = comp.get('source', 'unknown')
                    
                    print(f"   Comparable {j}: ${price} - {beds} bed/{baths} bath - {address} ({source})")
                
                # Step 2: Calculate REAL market stats
                market_stats = analyzer.calculate_market_stats(comparables)
                if market_stats:
                    print(f"✅ REAL Market Stats: Mean=${market_stats['mean']:.0f}, Median=${market_stats['median']:.0f}, Range=${market_stats['min']:.0f}-${market_stats['max']:.0f}")
                    
                    # Step 3: Calculate fairness with REAL data
                    fairness_result = analyzer.calculate_fairness_score(test_case['price'], market_stats)
                    if fairness_result:
                        print(f"✅ Fairness: {fairness_result['classification']} ({fairness_result['percent_difference']:.1f}% from REAL market)")
                    else:
                        print("❌ Failed to calculate fairness score")
                else:
                    print("❌ Failed to calculate REAL market stats")
            else:
                print("❌ NO REAL comparable listings found from RentCast API")
                print("   This means:")
                print("   - Your API key might be invalid")
                print("   - The location has no available listings")
                print("   - There's a network issue")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

def test_data_aggregator_real_only():
    """Test the data aggregator with REAL API data only"""
    
    print("\n" + "=" * 60)
    print("Testing Data Aggregator - REAL API Data Only")
    print("=" * 60)
    
    aggregator = DataAggregator()
    
    test_locations = [
        ("New York, NY", 2),
        ("Los Angeles, CA", 1),
        ("Chicago, IL", 3),
        ("Miami, FL", 2)
    ]
    
    for location, bedrooms in test_locations:
        print(f"\nTesting REAL API: {location} ({bedrooms} bedrooms)")
        
        try:
            comparables = aggregator.get_comparables(location, bedrooms)
            
            if comparables:
                print(f"✅ Got {len(comparables)} REAL listings from RentCast API")
                
                for i, comp in enumerate(comparables[:3], 1):
                    price = comp.get('price', 'N/A')
                    beds = comp.get('bedrooms', 'N/A')
                    address = comp.get('address', 'N/A')
                    source = comp.get('source', 'unknown')
                    
                    print(f"   {i}. ${price} - {beds} bed - {address} ({source})")
            else:
                print(f"❌ No REAL results found for {location}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def verify_no_fake_data():
    """Verify that no fake/sample data is being used"""
    
    print("\n" + "=" * 60)
    print("Verifying NO Fake Data is Used")
    print("=" * 60)
    
    # Check that SAMPLE_LISTINGS doesn't exist
    try:
        from app import SAMPLE_LISTINGS
        print("❌ FAKE DATA DETECTED: SAMPLE_LISTINGS still exists!")
        return False
    except ImportError:
        print("✅ CONFIRMED: No fake SAMPLE_LISTINGS found")
    
    # Check that _get_sample_data method doesn't exist
    aggregator = DataAggregator()
    if hasattr(aggregator, '_get_sample_data'):
        print("❌ FAKE DATA DETECTED: _get_sample_data method still exists!")
        return False
    else:
        print("✅ CONFIRMED: No fake data fallback methods found")
    
    return True

if __name__ == "__main__":
    print("RentFair - REAL API Data Test Only")
    print("This test verifies NO fake/sample data is used")
    print("=" * 60)
    
    # First verify no fake data
    if verify_no_fake_data():
        # Test with real data only
        test_real_comparables_only()
        
        # Test data aggregator
        test_data_aggregator_real_only()
    else:
        print("❌ Please remove all fake data before running tests")
    
    print("\n" + "=" * 60)
    print("REAL API Data Test Complete!")
    print("\nIf you see ✅ marks:")
    print("1. System is using REAL RentCast API data only")
    print("2. All addresses and prices are from real listings")
    print("3. No fake/sample data is being used")
    print("\nIf you see ❌ marks:")
    print("1. Check your RentCast API key")
    print("2. Ensure you have a valid RentCast account")
    print("3. Try different US locations")
