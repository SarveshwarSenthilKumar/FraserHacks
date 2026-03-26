import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API Keys
    RENTCAST_API_KEY = os.environ.get('RENTCAST_API_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash-lite')
    
    # Legacy API Keys (kept for compatibility)
    RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
    RAPIDAPI_HOST = os.environ.get('RAPIDAPI_HOST')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN')
    ZILLOW_API_KEY = os.environ.get('ZILLOW_API_KEY')
    REALTOR_API_KEY = os.environ.get('REALTOR_API_KEY')
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///rentfair.db')
    
    # Cache
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Rate Limiting
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '100 requests per hour')
    
    # API Configuration
    API_TIMEOUT = 30  # seconds
    MAX_RETRIES = 3
    
    # Cache TTL (in seconds)
    CACHE_TTL = 3600  # 1 hour
    
    @classmethod
    def validate_required_keys(cls):
        """Validate that required API keys are present"""
        required_keys = []
        optional_keys = ['RENTCAST_API_KEY', 'GEMINI_API_KEY']
        
        missing_keys = []
        for key in required_keys:
            if not getattr(cls, key):
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
        
        # Warn about optional keys
        for key in optional_keys:
            if not getattr(cls, key):
                print(f"Warning: {key} not set. {key} features will be disabled.")
        
        # Note about Nominatim (no API key required)
        print("Info: Using Nominatim (OpenStreetMap) for geocoding - no API key required")
