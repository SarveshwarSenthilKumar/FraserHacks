#!/usr/bin/env python3
"""
Test script to verify the sqft field is now optional
"""

import requests
import json

def test_optional_sqft():
    """Test that sqft field is now optional"""
    
    base_url = "http://localhost:5000"
    
    print("Testing Optional SQFT Field")
    print("=" * 40)
    
    # Test cases
    test_cases = [
        {
            "name": "Without sqft (should work)",
            "data": {
                "address": "123 Main St",
                "price": 3000,
                "bedrooms": 2,
                "bathrooms": 1,
                "location": "New York, NY"
                # No sqft field
            },
            "should_work": True
        },
        {
            "name": "With sqft empty string (should work)",
            "data": {
                "address": "123 Main St",
                "price": 3000,
                "bedrooms": 2,
                "bathrooms": 1,
                "location": "New York, NY",
                "sqft": ""
            },
            "should_work": True
        },
        {
            "name": "With valid sqft (should work)",
            "data": {
                "address": "123 Main St",
                "price": 3000,
                "bedrooms": 2,
                "bathrooms": 1,
                "location": "New York, NY",
                "sqft": 1000
            },
            "should_work": True
        },
        {
            "name": "Missing required field (should fail)",
            "data": {
                "address": "123 Main St",
                "price": 3000,
                "bedrooms": 2,
                "location": "New York, NY"
                # Missing bathrooms
            },
            "should_work": False
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        
        try:
            response = requests.post(
                f"{base_url}/analyze-rent",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                if test_case['should_work']:
                    print("✅ SUCCESS: Request accepted")
                    result = response.json()
                    if 'error' in result:
                        print(f"⚠️  Got error but 200 status: {result['error']}")
                    else:
                        print(f"✅ Analysis completed: {result.get('fairness_result', {}).get('classification', 'Unknown')}")
                else:
                    print("❌ UNEXPECTED: Should have failed but got success")
                    
            elif response.status_code == 400:
                result = response.json()
                error_msg = result.get('error', 'Unknown error')
                
                if not test_case['should_work']:
                    print("✅ SUCCESS: Correctly rejected invalid request")
                    print(f"Error: {error_msg}")
                else:
                    print("❌ UNEXPECTED: Should have worked but got error")
                    print(f"Error: {error_msg}")
            else:
                print(f"❌ UNEXPECTED STATUS: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to server. Make sure the app is running on http://localhost:5000")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_form_fields():
    """Test which fields are actually required"""
    
    print("\n" + "=" * 40)
    print("Testing Required Fields")
    print("=" * 40)
    
    # Start with all fields and remove one at a time
    base_data = {
        "address": "123 Main St",
        "price": 3000,
        "bedrooms": 2,
        "bathrooms": 1,
        "location": "New York, NY",
        "sqft": 1000
    }
    
    fields_to_test = ['address', 'price', 'bedrooms', 'bathrooms', 'location', 'sqft']
    
    for field in fields_to_test:
        print(f"\n--- Testing without {field} ---")
        
        test_data = base_data.copy()
        del test_data[field]
        
        try:
            response = requests.post(
                "http://localhost:5000/analyze-rent",
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ {field} is optional")
            elif response.status_code == 400:
                result = response.json()
                error_msg = result.get('error', 'Unknown error')
                if field.lower() in error_msg.lower():
                    print(f"✅ {field} is required")
                else:
                    print(f"⚠️  {field} failed for different reason: {error_msg}")
            else:
                print(f"❌ Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing {field}: {e}")

if __name__ == "__main__":
    print("RentFair SQFT Optional Field Test")
    print("This verifies the sqft field is now optional")
    print("=" * 50)
    
    # Test optional sqft
    test_optional_sqft()
    
    # Test required fields
    test_form_fields()
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("\nExpected Results:")
    print("- sqft should be optional (work without it)")
    print("- address, price, bedrooms, bathrooms, location should be required")
    print("- Form should work with just the required fields")
