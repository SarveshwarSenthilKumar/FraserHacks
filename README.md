# RentFair - Smart Rent Analysis System

🏠 **RentFair** is a comprehensive rent fairness analysis platform that helps renters determine if a rental listing is fairly priced compared to the market.

## 🚀 Features

- **📊 Fairness Scoring**: Advanced Z-score based algorithm to determine rent fairness
- **📈 Data Visualization**: Interactive charts showing price distribution
- **🗺️ Location Intelligence**: Map view of comparable listings
- **🤖 AI Insights**: Powered by Gemini API for intelligent explanations and negotiation tips
- **🎯 Comparable Analysis**: Smart filtering of similar listings
- **💫 Modern UI**: Beautiful, responsive design with smooth animations

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **Gemini API** - AI-powered insights
- **Statistics** - Mathematical calculations

### Frontend
- **HTML5/CSS3/JavaScript** - Core web technologies
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Interactive data visualization
- **Leaflet** - Interactive maps
- **Font Awesome** - Icon library

## 📋 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FraserHacks
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini API Key**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the `app.py` file with your API key:
   ```python
   genai.configure(api_key="YOUR_GEMINI_API_KEY")
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🧮 Algorithm

### Fairness Score Calculation

The system uses a sophisticated Z-score based approach:

1. **Find Comparables**: Filter listings by location, bedrooms (±1), and bathrooms (±1)
2. **Calculate Market Stats**: Compute mean, median, and standard deviation
3. **Z-Score Formula**: 
   ```
   z = (user_rent - market_mean) / market_std_dev
   ```
4. **Classification**:
   - **Underpriced**: < -10% below market
   - **Fair**: ±10% of market
   - **Overpriced**: > +10% above market

## 📊 Data Sources

The system currently uses a curated sample dataset of rental listings in Mississauga. In production, this can be extended with:

- **Zillow API** (unofficial)
- **Realtor API**
- **RapidAPI** rental listings
- **Canada Mortgage and Housing Corporation** data
- **Statistics Canada** housing data

## 🎯 API Endpoints

### POST `/api/analyze-rent`
Analyzes a rental listing for fairness.

**Request Body:**
```json
{
  "price": 2400,
  "bedrooms": 2,
  "bathrooms": 1,
  "location": "Mississauga",
  "sqft": 850,
  "address": "123 Queen St E"
}
```

**Response:**
```json
{
  "user_listing": {...},
  "fairness_result": {
    "score": -5.2,
    "label": "Fair",
    "color": "#10B981",
    "z_score": -0.3,
    "mean_price": 2350,
    "median_price": 2300,
    "std_dev": 150,
    "comparable_count": 8
  },
  "comparables": [...],
  "ai_explanation": {...},
  "price_distribution": {...}
}
```

### GET `/api/market-stats`
Returns general market statistics.

## 🏗️ Project Structure

```
FraserHacks/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── data/
    └── listings.json     # Sample rental data (future)
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Price distribution visualization
- **Live Maps**: Location-based comparable listings
- **Smooth Animations**: Modern, polished user experience
- **Loading States**: User-friendly feedback during analysis
- **Glass Morphism**: Modern UI design patterns

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production:
```
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=production
```

### Sample Data Expansion
To add more sample listings, modify the `SAMPLE_LISTINGS` array in `app.py`:

```python
{
  "price": 2500,
  "bedrooms": 2,
  "bathrooms": 2,
  "location": "Toronto",
  "sqft": 900,
  "address": "456 King St W"
}
```

## 🚀 Deployment

### Heroku
1. Install Heroku CLI
2. Create a `Procfile`:
   ```
   web: python app.py
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🧪 Testing

Run the application locally and test with sample data:
- Price: $2400
- Bedrooms: 2
- Bathrooms: 1
- Location: Mississauga

## 📈 Future Enhancements

- [ ] Real-time API integration with rental platforms
- [ ] Historical price trends
- [ ] Neighborhood insights
- [ ] Advanced filtering options
- [ ] User accounts and saved searches
- [ ] Mobile app development
- [ ] Machine learning price predictions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🏆 Hackathon Pitch

**"Renters are making one of the biggest financial decisions of their lives without market transparency. RentFair uses real market data to instantly evaluate whether a listing is fair, overpriced, or a hidden deal."**

### What Makes This Win
- ✅ **Universal Problem**: Everyone understands the rent affordability challenge
- ✅ **Clear Impact**: Instant before/after value proposition
- ✅ **Strong Visuals**: Data-driven charts and maps
- ✅ **Technical Depth**: Z-score calculations, AI integration
- ✅ **Demo-Ready**: Polished UI with smooth interactions

---

**Built with ❤️ for FraserHacks 2024**
