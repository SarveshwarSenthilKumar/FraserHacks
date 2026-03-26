# RentFair - Smart Rent Analysis System

**RentFair** is a comprehensive rent fairness analysis platform that helps renters determine if a rental listing is fairly priced compared to the market. Built with advanced statistical analysis and AI-powered insights, RentFair provides transparent, data-driven rental market intelligence.

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Algorithm](#-algorithm)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [UI Features](#-ui-features)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)
- [Team](#-team)

## Features

### Core Functionality
- **Fairness Scoring**: Advanced Z-score based algorithm to determine rent fairness with statistical confidence
- **Data Visualization**: Interactive charts showing price distribution, market trends, and comparative analysis
- **Location Intelligence**: Interactive map view of comparable listings with geographic clustering
- **AI Insights**: Powered by Google Gemini API for intelligent explanations and negotiation tips
- **Comparable Analysis**: Smart filtering of similar listings based on multiple criteria

### Advanced Features
- **Real-time Analysis**: Instant market comparison and fairness assessment
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Advanced Filtering**: Multi-parameter filtering for precise comparable matching
- **Investment Metrics**: Yield estimates, cap rates, and appreciation potential
- **Market Intelligence**: Trend analysis, inventory levels, and days on market
- **Exploitation Detection**: AI-powered alerts for suspiciously overpriced listings

### User Experience
- **Modern UI**: Beautiful, responsive design with smooth animations and glass morphism effects
- **Professional Design**: Cohesive green gradient theme with excellent readability
- **Loading States**: User-friendly feedback during analysis with animated indicators
- **Export Functionality**: Download comparable listings and analysis reports

## Technology Stack

### Backend
- **Flask 2.3+** - Python web framework with robust routing and templating
- **Google Gemini API** - Advanced AI for market insights and negotiation strategies
- **NumPy/Statistics** - Mathematical calculations and statistical analysis
- **JSON** - Data serialization and API communication

### Frontend
- **HTML5/CSS3/JavaScript ES6+** - Modern web technologies with semantic markup
- **Tailwind CSS 2.2+** - Utility-first CSS framework for rapid styling
- **Chart.js** - Interactive data visualization with responsive charts
- **Leaflet 1.9+** - Interactive maps with clustering and markers
- **Font Awesome 6.4+** - Comprehensive icon library
- **Glass Morphism Design** - Modern UI with backdrop filters and transparency

### Development Tools
- **Python 3.8+** - Core programming language
- **pip** - Package management
- **Git** - Version control
- **OnRender** - Deployment

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

### One-Command Setup
```bash
git clone https://github.com/yourusername/FraserHacks.git
cd FraserHacks
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` to start analyzing rental properties!

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/FraserHacks.git
cd FraserHacks
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### 5. Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file or directly in `app.py`

### 6. Run the Application
```bash
python app.py
```

### 7. Access the Application
Open your browser and navigate to `http://localhost:5000`

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

## Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key for AI insights | Yes | - |
| `FLASK_ENV` | Flask environment mode | No | `development` |
| `SECRET_KEY` | Flask secret key for sessions | No | auto-generated |
| `PORT` | Application port | No | `5000` |
| `DEBUG` | Debug mode | No | `True` |

### Customization Options

#### Adding New Locations
Edit the `SAMPLE_LISTINGS` array in `app.py` to add new cities:
```python
{
  "price": 2800,
  "bedrooms": 2,
  "bathrooms": 2,
  "location": "Vancouver",
  "sqft": 950,
  "address": "789 Granville St"
}
```

#### Adjusting Fairness Thresholds
Modify the fairness calculation in `calculate_fairness()`:
```python
# Current thresholds
FAIR_THRESHOLD = 0.1  # 10% variance
OVERPRICED_THRESHOLD = 0.1
UNDERPRICED_THRESHOLD = -0.1
```

#### Custom Styling
Edit `static/css/style.css` to customize:
- Color schemes (CSS variables in `:root`)
- Animation speeds
- Glass morphism effects
- Responsive breakpoints

## Project Structure

```
FraserHacks/
├── app.py                      # Flask backend application
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── Procfile                   # Deployment configuration
├── notes.txt                  # Development notes
├── templates/
│   └── index.html             # Main HTML template with responsive design
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles with glass morphism
│   └── js/
│       └── app.js             # Frontend JavaScript logic
└── data/                      # Future data storage
    └── listings.json          # Sample rental data (planned)
```

### Key Files Explained

- **`app.py`**: Main Flask application with API endpoints and business logic
- **`templates/index.html`**: Single-page application with modern UI components
- **`static/css/style.css`**: Comprehensive styling with animations and responsive design
- **`static/js/app.js`**: Frontend logic for API calls, charts, and user interactions

## 🎨 UI Features

### Design System
- **Color Palette**: Green gradient theme (`#6cbd93` to `#1e6e30`)
- **Typography**: Clean, readable fonts with proper hierarchy
- **Spacing**: Consistent padding and margins using Tailwind classes
- **Animations**: Smooth transitions and micro-interactions

### Responsive Design
- **Desktop (1024px+)**: Full-featured layout with side-by-side charts
- **Tablet (768px-1023px)**: Optimized grid layout and touch interactions
- **Mobile (<768px)**: Stacked layout with simplified navigation

### Interactive Components
- **Glass Morphism Cards**: Modern translucent design with backdrop blur
- **Animated Charts**: Real-time data visualization with Chart.js
- **Interactive Maps**: Location-based property clustering with Leaflet
- **Loading States**: Professional spinners and progress indicators
- **Hover Effects**: Smooth transitions and scale transformations

### Accessibility Features
- **Semantic HTML**: Proper heading structure and landmark elements
- **ARIA Labels**: Screen reader compatibility
- **Keyboard Navigation**: Full keyboard accessibility
- **Color Contrast**: WCAG AA compliant text contrast ratios


### Environment-Specific Configuration

#### Production
```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your_production_secret
GEMINI_API_KEY=your_production_api_key
```

#### Development
```env
FLASK_ENV=development
DEBUG=True
SECRET_KEY=dev_secret_key
GEMINI_API_KEY=your_dev_api_key
```

### Manual Testing Checklist

#### Basic Functionality
- [ ] Application loads correctly at `http://localhost:5000`
- [ ] Header displays with proper styling
- [ ] Footer matches header design
- [ ] Form submission works without errors
- [ ] Loading states appear during analysis

#### Analysis Features
- [ ] Fairness scoring produces accurate results
- [ ] Charts render correctly with sample data
- [ ] Map displays location markers
- [ ] AI insights generate meaningful content
- [ ] Export functionality works

#### Responsive Design
- [ ] Desktop layout (1920x1080)
- [ ] Tablet layout (768x1024)
- [ ] Mobile layout (375x667)
- [ ] Touch interactions on mobile

#### Sample Test Cases
```python
# Test Case 1: Fair Price
{
  "price": 2400,
  "bedrooms": 2,
  "bathrooms": 1,
  "location": "Mississauga",
  "sqft": 850,
  "address": "123 Queen St E"
}
# Expected: Fair (within ±10% of market)

# Test Case 2: Overpriced
{
  "price": 3200,
  "bedrooms": 2,
  "bathrooms": 1,
  "location": "Mississauga",
  "sqft": 850,
  "address": "456 Hurontario St"
}
# Expected: Overpriced (> +10% of market)

# Test Case 3: Underpriced
{
  "price": 1800,
  "bedrooms": 2,
  "bathrooms": 1,
  "location": "Mississauga",
  "sqft": 850,
  "address": "789 Burnhamthorpe Rd"
}
# Expected: Underpriced (< -10% of market)
```

### Automated Testing (Future)
```bash
# Unit tests
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/

# UI tests
python -m pytest tests/ui/
```

## Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow
1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/FraserHacks.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   python app.py
   # Test manually in browser
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style Guidelines
- **Python**: Follow PEP 8, use 4-space indentation
- **JavaScript**: Use ES6+, semicolons, 2-space indentation
- **CSS**: Follow BEM methodology for class names
- **HTML**: Use semantic tags, proper indentation

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [*] Manual testing completed
- [*] All tests pass
- [*] No false data
- [*] No regression issues

```

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 A. Maji and S. Senthil Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👥 Team

**Developers**
- **S. Senthil Kumar** - Backend Development, API Design, Algorithm Implementation, Data Analysis
- **A. Maji** - Frontend Development, UI/UX Design, Testing

**Built for FraserHacks 2026**

---

### 🎯 Problem Statement
**"Renters are making one of the biggest financial decisions of their lives without market transparency. RentFair uses real market data to instantly evaluate whether a listing is fair, overpriced, or a hidden deal."**

###  What Makes This Project Special

#### **Universal Problem**
- Everyone understands the rent affordability challenge
- Addresses a real financial pain point
- Impactful solution for millions of renters

#### **Clear Impact**
- Instant value proposition
- Tangible savings for users
- Empowers renters with data-driven decisions

#### **Strong Visuals**
- Data-driven charts and maps
- Professional, modern UI design
- Engaging user experience

#### **Technical Depth**
- Detailed statistical analysis
- AI integration with Gemini API
- Responsive design and accessibility

#### **Demo-Ready**
- Polished UI with smooth interactions
- Complete end-to-end functionality
- Production-ready deployment options

### Technologies Demonstrated
- **Backend**: Flask, Statistical Analysis
- **Frontend**: Modern JavaScript, Responsive Design, Data Visualization
- **AI/ML**: Google Gemini API, Natural Language Processing
- **DevOps**: OnRender, Environment configuration

### Project Metrics
- **Lines of Code**: 2000+ across frontend and backend
- **API Endpoints**: 3 fully functional endpoints
- **UI Components**: 15+ interactive components
- **Data Points**: 50+ sample rental listings
- **Deployment**: Production-ready on multiple platforms

---

**Thank you for checking out RentFair!**

If you find this project useful, please give us a ⭐ on GitHub and consider contributing to make rental markets more transparent for everyone.
