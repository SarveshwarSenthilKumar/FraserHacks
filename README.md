# 🏠 RentFair

**Know if your rent is fair, overpriced, or a hidden deal**

RentFair is a web application that analyzes rental listings to determine if they're fairly priced compared to the market. Using real market data and statistical analysis, it provides instant feedback on rental fairness with clear explanations and visualizations.

## 🚀 Features

- **Fairness Scoring**: Get instant analysis of whether a rental is overpriced, fair, or underpriced
- **Market Comparison**: Compare listings against similar properties in the same area
- **Statistical Analysis**: Z-score calculations and market statistics for data-driven insights
- **Interactive Visualizations**: Price distribution charts showing where your listing stands
- **Comparable Listings**: View similar properties with detailed information
- **Responsive Design**: Works beautifully on desktop and mobile devices

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Visualization**: Chart.js
- **Styling**: Modern CSS with gradients and animations
- **Data**: Sample rental listings (easily replaceable with real APIs)

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FraserHacks
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## 🧮 Algorithm

The fairness scoring algorithm uses statistical analysis to determine market positioning:

1. **Find Comparables**: Filter listings by location and bedroom count (±1 bedroom)
2. **Calculate Market Stats**: Compute mean, median, standard deviation, and price range
3. **Fairness Score**: `(user_rent - avg_rent) / avg_rent`
4. **Z-Score**: `(user_rent - mean) / standard_deviation`
5. **Classification**:
   - Underpriced: < -10% below market
   - Fair: ±10% of market
   - Overpriced: > +10% above market

## 📊 Data Structure

Each rental listing contains:
```json
{
  "price": 2400,
  "bedrooms": 2,
  "bathrooms": 1,
  "location": "Mississauga",
  "sqft": 850,
  "address": "123 Main St"
}
```

## 🔧 API Endpoints

### POST /analyze-rent
Analyzes a rental listing for fairness.

**Request Body:**
```json
{
  "address": "123 Main St",
  "location": "Mississauga",
  "price": 2400,
  "bedrooms": 2,
  "bathrooms": 1,
  "sqft": 850
}
```

**Response:**
```json
{
  "user_listing": {...},
  "comparables": [...],
  "market_stats": {
    "mean": 2250,
    "median": 2300,
    "std_dev": 200,
    "min": 1950,
    "max": 2600,
    "count": 10
  },
  "fairness_result": {
    "fairness_score": 0.067,
    "z_score": 0.75,
    "classification": "Fair",
    "color": "green",
    "percent_difference": 6.7
  },
  "explanation": "This 2-bedroom listing in Mississauga is fairly priced..."
}
```

### GET /market-stats/<location>/<bedrooms>
Returns market statistics for a specific location and bedroom count.

## 🎨 Design Features

- **Modern UI**: Gradient backgrounds, smooth animations, and card-based layouts
- **Responsive Design**: Mobile-first approach with breakpoints for tablets and desktops
- **Interactive Elements**: Hover effects, loading states, and smooth transitions
- **Accessibility**: Semantic HTML5, proper form labels, and keyboard navigation
- **Visual Feedback**: Color-coded fairness badges and progress indicators

## 🔮 Future Enhancements

- **Real API Integration**: Connect to Zillow, Realtor.com, or local rental APIs
- **Location Intelligence**: Geocoding and distance-based clustering
- **AI Explanations**: OpenAI integration for personalized negotiation tips
- **Historical Data**: Track price trends over time
- **User Accounts**: Save analyses and get price alerts
- **Mobile App**: React Native or Flutter application

## 🏆 Pitch Positioning

"Renters are making one of the biggest financial decisions of their lives without market transparency. RentFair uses real market data to instantly evaluate whether a listing is fair, overpriced, or a hidden deal."

## 📈 What Makes This Win

- **Universal Problem**: Everyone understands the rent affordability challenge
- **Clear Impact**: Immediate before/after value proposition
- **Strong Visuals**: Data-driven charts and clear metrics
- **Scalable Solution**: Can expand to multiple cities and data sources
- **Demo-Ready**: Polished UI that looks impressive in presentations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for the FraserHacks competition**
