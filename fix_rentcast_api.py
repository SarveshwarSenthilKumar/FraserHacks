#!/usr/bin/env python3
"""
RentCast API Key Fix and Validation Script
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_rentcast_api_key(api_key):
    """Test if the RentCast API key is valid"""
    
    print("Testing RentCast API Key...")
    print(f"API Key: {api_key[:10]}..." if api_key else "None")
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    url = "https://api.rentcast.io/v1/listings/rental/long-term"
    
    headers = {
        'accept': 'application/json',
        'X-API-Key': api_key
    }
    
    params = {
        'location': 'New York, NY',
        'status': 'active',
        'bedrooms': 2,
        'limit': 5
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"✅ API Key is VALID!")
                print(f"✅ Found {len(data)} real listings")
                
                # Show sample listing
                sample = data[0]
                print(f"Sample listing: ${sample.get('price', 'N/A')} - {sample.get('address', 'N/A')}")
                return True
            else:
                print("⚠️  API key works but no data returned")
                return False
                
        elif response.status_code == 401:
            print("❌ API Key is INVALID or EXPIRED")
            print("Error: Unauthorized - Please get a new API key")
            return False
            
        elif response.status_code == 403:
            print("❌ API Key is valid but no permissions")
            print("Error: Forbidden - Check your RentCast plan")
            return False
            
        elif response.status_code == 429:
            print("⚠️  Rate limited - Try again later")
            return False
            
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - Check internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Check internet connection")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_new_api_key_instructions():
    """Provide instructions for getting a new API key"""
    
    print("\n" + "="*60)
    print("HOW TO GET A NEW RENTCAST API KEY")
    print("="*60)
    
    print("\n1. Go to: https://app.rentcast.io/app/api")
    print("2. Sign up for a FREE account")
    print("3. Choose the Developer plan (500 requests/month free)")
    print("4. Copy your API key")
    print("5. Add it to your .env file:")
    
    print("\n   RENTCAST_API_KEY=your-new-api-key-here")
    
    print("\n6. Restart the application")
    print("7. Test again with this script")

def check_env_file():
    """Check the .env file configuration"""
    
    print("\n" + "="*60)
    print("CHECKING ENVIRONMENT CONFIGURATION")
    print("="*60)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        # Read .env file
        with open('.env', 'r') as f:
            content = f.read()
            
        if 'RENTCAST_API_KEY=' in content:
            print("✅ RENTCAST_API_KEY found in .env")
            
            # Extract the key
            for line in content.split('\n'):
                if line.startswith('RENTCAST_API_KEY='):
                    key = line.split('=', 1)[1].strip()
                    if key and key != 'your-rentcast-api-key-here':
                        return key
                    else:
                        print("❌ RENTCAST_API_KEY is still placeholder")
                        return None
        else:
            print("❌ RENTCAST_API_KEY not found in .env")
    else:
        print("❌ .env file does not exist")
        print("Copy .env.example to .env and add your API key")
    
    return None

def fix_env_file():
    """Help fix the .env file"""
    
    print("\n" + "="*60)
    print("FIXING .env FILE")
    print("="*60)
    
    # Check if .env.example exists
    if os.path.exists('.env.example'):
        print("✅ .env.example exists")
        
        # Read .env.example
        with open('.env.example', 'r') as f:
            content = f.read()
        
        # Write to .env
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ Created .env from .env.example")
        print("\nNow edit .env and add your actual API key:")
        print("RENTCAST_API_KEY=your-actual-api-key-here")
        
    else:
        print("❌ .env.example not found")
        print("Creating basic .env file...")
        
        basic_env = """# RentFair Environment Variables

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# RentCast API (Primary rental data source)
RENTCAST_API_KEY=your-rentcast-api-key-here

# Google Gemini API (for AI explanations)
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.5-flash-lite

# OpenStreetMap Nominatim (for geocoding)
# No API key required - uses free OpenStreetMap service
"""
        
        with open('.env', 'w') as f:
            f.write(basic_env)
        
        print("✅ Created basic .env file")

if __name__ == "__main__":
    print("RentCast API Key Fix Script")
    print("="*60)
    
    # Step 1: Check environment
    api_key = check_env_file()
    
    if api_key:
        # Step 2: Test the API key
        if test_rentcast_api_key(api_key):
            print("\n🎉 SUCCESS! Your RentCast API is working correctly!")
            print("The application should now find real comparable listings.")
        else:
            print("\n❌ Your API key is not working.")
            get_new_api_key_instructions()
    else:
        print("\n❌ No valid API key found in configuration.")
        fix_env_file()
        get_new_api_key_instructions()
    
    print("\n" + "="*60)
    print("After fixing your API key:")
    print("1. Restart the application: python app.py")
    print("2. Try submitting a rental listing")
    print("3. It should now find real comparable listings!")
