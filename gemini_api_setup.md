# 🤖 Google Gemini API Setup Guide

## 🔗 Gemini API Links

**Main Website:** https://ai.google.dev/
**API Documentation:** https://ai.google.dev/docs
**API Keys:** https://makersuite.google.com/app/apikey
**Quickstart:** https://ai.google.dev/docs/quickstart

## 🚀 Quick Setup

### 1. Get Your Gemini API Key

1. **Go to:** https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Copy your API key** (it will look like: `AIzaSy...`)
5. **Save it securely** - treat it like a password

### 2. Configure Environment

Create `.env` file:
```bash
# Copy the template
cp .env.example .env

# Edit .env with your key
GEMINI_API_KEY=AIzaSyYourActualGeminiApiKeyHere
```

### 3. Test the API

```python
# Test script
from api_services import GeminiService

service = GeminiService()
mock_analysis = {
    'user_listing': {
        'address': '123 Main St',
        'price': 3500,
        'bedrooms': 2,
        'bathrooms': 1,
        'location': 'New York, NY'
    },
    'fairness_result': {
        'classification': 'Overpriced'
    },
    'market_stats': {
        'mean': 3000,
        'min': 2500,
        'max': 4000
    }
}

tips = service.generate_negotiation_tips(mock_analysis)
print(f"AI Tips: {tips}")
```

## 📊 Gemini API Features

### 1. Generate Content
**Endpoint:** `/models/gemini-1.5-flash:generateContent`
**Usage:** Generate AI-powered negotiation tips
```python
service.generate_negotiation_tips(analysis_result)
```

### 2. Available Models
- **gemini-1.5-flash**: Fast, lightweight, great for quick responses
- **gemini-1.5-pro**: More powerful, better for complex tasks
- **gemini-pro**: Previous generation model

### 3. Generation Config
- **Temperature**: 0.7 (balanced creativity)
- **Max Output Tokens**: 200 (concise responses)
- **TopK**: 40 (diversity control)
- **TopP**: 0.95 (nucleus sampling)

## 🔧 API Response Format

The API returns data like this:
```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "• Reference comparable listings in the $3,000 range\n• Highlight your strong rental history and stable income\n• Mention you're looking for a long-term lease"
          }
        ]
      }
    }
  ]
}
```

## 🎯 Integration with RentFair

### Updated Data Flow

1. **User submits listing** → Flask app receives data
2. **RentFairAnalyzer** → Calculates fairness scores
3. **Gemini API** → Generates personalized negotiation tips
4. **Results** → Display AI tips alongside analysis

### Key Features Enabled

- ✅ **AI-powered negotiation tips** based on market analysis
- ✅ **Personalized advice** for each specific listing
- ✅ **Contextual suggestions** considering price, location, and market data
- ✅ **Graceful fallback** when API is unavailable

## 🚨 Important Notes

### Rate Limits
- **Free tier:** 15 requests per minute
- **Paid tiers:** Higher limits available
- **Quota resets:** Every minute

### Pricing
- **Free:** Generous free tier for development
- **Pay-as-you-go:** $0.00025 per 1,000 characters
- **Pro tier:** Available for high-volume usage

### Model Capabilities
- **Text generation**: High-quality responses
- **Context understanding**: Analyzes rental market data
- **Practical advice**: Actionable negotiation tips
- **Safety filters**: Built-in content safety

## 🛠️ Troubleshooting

### Common Issues

**1. "API Key Not Working"**
```bash
# Test your key directly
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Hello, Gemini!"}]
    }]
  }'
```

**2. "Rate Limited"**
- Wait for quota to reset (every minute)
- Implement request queuing
- Use exponential backoff

**3. "Invalid Response"**
- Check API key format
- Verify model name is correct
- Ensure JSON payload is valid

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Tips

### Caching Strategy
```python
# Cache AI tips for similar analysis results
@cache.memoize(timeout=3600)  # 1 hour cache
def get_cached_tips(analysis_hash):
    return gemini_service.generate_negotiation_tips(analysis_result)
```

### Optimized Prompts
- Keep prompts concise and specific
- Include relevant context (price, location, market data)
- Request bullet points for better readability
- Limit response length with maxOutputTokens

## 🎉 Success Indicators

When properly configured, you should see:
- AI-generated negotiation tips in results
- Contextual advice based on market analysis
- Personalized suggestions for each listing
- Graceful fallback when API is unavailable

**Test with:** Any rental listing analysis
**Expected:** 2-3 bullet points with practical negotiation advice

## 🆚 Gemini vs OpenAI

| Feature | Gemini | OpenAI |
|---------|--------|---------|
| **Pricing** | More affordable | More expensive |
| **Free Tier** | Generous | Limited |
| **Speed** | Very fast | Moderate |
| **Context** | Good for practical tasks | Excellent for complex tasks |
| **Safety** | Built-in filters | Customizable |
| **Integration** | Simple REST API | Complex SDK |

## 💰 Cost Comparison

**Gemini 1.5 Flash:**
- Free: 15 requests/minute
- Paid: $0.00025 per 1,000 characters
- ~$0.05 per 1000 API calls (200 chars each)

**OpenAI GPT-3.5:**
- Free: Limited credits
- Paid: $0.002 per 1K tokens
- ~$0.40 per 1000 API calls

**Gemini is ~8x more cost-effective!** 💸

## 🔐 Security Best Practices

1. **Never commit API keys** to Git
2. **Use environment variables** for configuration
3. **Rotate keys regularly** for security
4. **Monitor usage** in Google Cloud Console
5. **Implement rate limiting** in your application

## 🚀 Getting Started Checklist

- [ ] Get Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Add GEMINI_API_KEY to .env file
- [ ] Test API with sample request
- [ ] Verify AI tips appear in RentFair results
- [ ] Monitor usage in Google Cloud Console

**You're ready to use Google Gemini for AI-powered rental advice!** 🤖✨
