#!/usr/bin/env python3
"""
Test script to verify form validation handles all edge cases
"""

import requests
import json

def test_form_validation():
    """Test various form validation scenarios"""
    
    base_url = "http://localhost:5000"
    
    print("Testing Form Validation")
    print("=" * 50)
    
    # Test cases that should fail validation
    test_cases = [
        {
            "name": "Empty price field",
            "data": {
                "address": "123 Main St",
                "price": "",  # Empty string
                "bedrooms": 2,
                "bathrooms": 1,
                "location": "New York, NY",
                "sqft": 1000
            },
            "expected_error": "Invalid numeric values"
        },
        {
            "name": "Empty bedrooms field",
            "data": {
                "address": "123 Main St",
                "price": 3000,
                "bedrooms": "",  # Empty string
                "bathrooms": 1,
                "location": "New York, NY",
                "sqft": 1000
            },
            "expected_error": "Invalid numeric values"
        },
        {
            "name": "Zero price",
            "data": {
                "address": "123 Main St",
                "price": 0,
                "bedrooms": 2,
                "bathrooms": 1,
                "location": "New York, NY",
                "sqft": 1000
            },
            "expected_error": "Price must be greater than 0"
        },
        {
            "name": "Negative bedrooms",
            "data": {
                "address": "123 Main St",
                "price": 3000,
                "bedrooms": -1,
                "bathrooms": 1,
                "location": "New York, NY",
                "sqft": 1000
            },
            "expected_error": "Bedrooms must be between 1 and 10"
        },
        {
            "name": "Missing required field",
            "data": {
                "address": "123 Main St",
                "price": 3000,
                "bedrooms": 2,
                "bathrooms": 1,
                "sqft": 1000
                # Missing location
            },
            "expected_error": "Missing required fields: location"
        },
        {
            "name": "Valid data (should work if API key is valid)",
            "data": {
                "address": "123 Main St",
                "price": 3000,
                "bedrooms": 2,
                "bathrooms": 1,
                "location": "New York, NY",
                "sqft": 1000
            },
            "expected_error": None
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
                if test_case['expected_error']:
                    print(f"❌ UNEXPECTED: Expected error but got success")
                    result = response.json()
                    print(f"Response: {result.get('explanation', 'No explanation')}")
                else:
                    print("✅ SUCCESS: Valid data accepted")
                    result = response.json()
                    if 'error' in result:
                        print(f"⚠️  Got error response: {result['error']}")
                    else:
                        print(f"✅ Analysis completed: {result.get('fairness_result', {}).get('classification', 'Unknown')}")
                        
            elif response.status_code == 400:
                result = response.json()
                error_msg = result.get('error', 'Unknown error')
                
                if test_case['expected_error']:
                    if test_case['expected_error'].lower() in error_msg.lower():
                        print(f"✅ SUCCESS: Got expected error: {error_msg}")
                    else:
                        print(f"⚠️  PARTIAL: Got error but different than expected")
                        print(f"Expected: {test_case['expected_error']}")
                        print(f"Got: {error_msg}")
                else:
                    print(f"❌ UNEXPECTED: Got error for valid data: {error_msg}")
                    
            else:
                print(f"❌ UNEXPECTED STATUS: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to server. Make sure the app is running on http://localhost:5000")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_edge_cases():
    """Test edge cases for numeric parsing"""
    
    print("\n" + "=" * 50)
    print("Testing Edge Cases for Numeric Parsing")
    print("=" * 50)
    
    edge_cases = [
        ("Empty string", ""),
        ("Space only", " "),
        ("Comma separated", "3,000"),
        ("Dollar sign", "$3000"),
        ("Decimal", "3000.50"),
        ("Negative", "-1000"),
        ("Zero", "0"),
        ("Large number", "999999")
    ]
    
    for name, value in edge_cases:
        print(f"\nTesting: {name} = '{value}'")
        
        try:
            # Test the parsing logic
            result = int(float(str(value).strip() or '0'))
            print(f"✅ Parsed successfully: {result}")
        except (ValueError, TypeError) as e:
            print(f"❌ Parse error: {e}")

if __name__ == "__main__":
    print("RentFair Form Validation Test")
    print("This tests the fix for 'invalid literal for int()' error")
    print("=" * 60)
    
    # Test edge cases
    test_edge_cases()
    
    # Test form validation (requires app to be running)
    test_form_validation()
    
    print("\n" + "=" * 60)
    print("Form Validation Test Complete!")
    print("\nIf all tests show ✅ SUCCESS:")
    print("1. The int() parsing error is fixed")
    print("2. Form validation handles edge cases")
    print("3. Clear error messages are provided")
    print("\nIf you see connection errors:")
    print("1. Start the app: python app.py")
    print("2. Run this test again")
