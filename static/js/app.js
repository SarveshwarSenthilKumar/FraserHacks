let priceChart = null;
let map = null;

// Simple coordinate generation function
function getSimpleCoordinates(address, location) {
    const cityCenters = {
        'mississauga': {lat: 43.5890, lng: -79.6441},
        'toronto': {lat: 43.6532, lng: -79.3832},
        'vancouver': {lat: 49.2827, lng: -123.1207},
        'montreal': {lat: 45.5017, lng: -73.5673},
        'calgary': {lat: 51.0447, lng: -114.0719},
        'ottawa': {lat: 45.4215, lng: -75.6972}
    };
    
    const center = cityCenters[location.toLowerCase()] || cityCenters['mississauga'];
    
    // Add small random offset
    const latOffset = (Math.random() - 0.5) * 0.1;
    const lngOffset = (Math.random() - 0.5) * 0.1;
    
    return {
        lat: center.lat + latOffset,
        lng: center.lng + lngOffset
    };
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rentForm');
    form.addEventListener('submit', handleFormSubmit);
    
    // Add input validation and real-time feedback
    setupInputValidation();
    
    // Add smooth scroll behavior
    setupSmoothScroll();
    
    // Add keyboard shortcuts
    setupKeyboardShortcuts();
});

function setupInputValidation() {
    const priceInput = document.getElementById('price');
    const sqftInput = document.getElementById('sqft');
    
    // Remove automatic formatting to prevent interference with typing
    // Only validate that it's a valid number
    
    // Validate sqft input
    sqftInput.addEventListener('input', function(e) {
        let value = parseInt(e.target.value);
        if (value && (value < 100 || value > 10000)) {
            e.target.setCustomValidity('Square footage should be between 100 and 10,000');
        } else {
            e.target.setCustomValidity('');
        }
    });
}

function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const form = document.getElementById('rentForm');
            if (form) {
                form.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to clear results
        if (e.key === 'Escape') {
            const resultsSection = document.getElementById('resultsSection');
            if (resultsSection && !resultsSection.classList.contains('hidden')) {
                resultsSection.classList.add('hidden');
                document.getElementById('rentForm').scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    // Clean and validate form data
    const priceValue = document.getElementById('price').value.replace(/,/g, '');
    const formData = {
        price: parseFloat(priceValue),
        bedrooms: parseInt(document.getElementById('bedrooms').value),
        bathrooms: parseInt(document.getElementById('bathrooms').value),
        location: document.getElementById('location').value.trim(),
        sqft: parseInt(document.getElementById('sqft').value) || 0,
        address: document.getElementById('address').value.trim()
    };
    
    // Validate required fields
    if (!formData.price || formData.price <= 0) {
        showError('Please enter a valid rent price');
        return;
    }
    
    if (!formData.location) {
        showError('Please enter a location');
        return;
    }
    
    // Show loading state with animation
    showLoadingState();
    
    // Make API call with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
    
    fetch('/api/analyze-rent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
        signal: controller.signal
    })
    .then(response => {
        clearTimeout(timeoutId);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        displayResults(data);
        // Add success animation
        animateSuccess();
    })
    .catch(error => {
        clearTimeout(timeoutId);
        console.error('Error:', error);
        if (error.name === 'AbortError') {
            showError('Request timed out. Please try again.');
        } else {
            showError('An error occurred while analyzing the rent. Please try again.');
        }
    })
    .finally(() => {
        hideLoadingState();
    });
}

function showLoadingState() {
    const loadingState = document.getElementById('loadingState');
    const resultsSection = document.getElementById('resultsSection');
    
    loadingState.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    
    // Add loading animation to form
    const form = document.getElementById('rentForm');
    form.style.opacity = '0.6';
    form.style.pointerEvents = 'none';
}

function hideLoadingState() {
    const loadingState = document.getElementById('loadingState');
    const form = document.getElementById('rentForm');
    
    loadingState.classList.add('hidden');
    form.style.opacity = '1';
    form.style.pointerEvents = 'auto';
}

function showError(message) {
    // Create or update error notification
    let errorDiv = document.getElementById('errorNotification');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'errorNotification';
        errorDiv.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300';
        document.body.appendChild(errorDiv);
    }
    
    errorDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-exclamation-circle mr-2"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Show error with slide-in animation
    setTimeout(() => {
        errorDiv.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorDiv.style.transform = 'translateX(100%)';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

function animateSuccess() {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.classList.add('fade-in-up');
    
    // Remove animation class after animation completes
    setTimeout(() => {
        resultsSection.classList.remove('fade-in-up');
    }, 600);
}

function displayResults(data) {
    const { user_listing, fairness_result, comparables, ai_explanation, price_distribution } = data;
    
    // Update fairness indicator
    updateFairnessIndicator(fairness_result);
    
    // Update statistics
    updateStatistics(user_listing, fairness_result);
    
    // Create price distribution chart
    createPriceChart(price_distribution, user_listing.price);
    
    // Create map (now synchronous)
    createMap(comparables, user_listing);
    
    // Update AI explanation
    updateAIExplanation(ai_explanation);
    
    // Display comparable listings
    displayComparableListings(comparables);
    
    // Show results section
    document.getElementById('resultsSection').classList.remove('hidden');
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function updateFairnessIndicator(fairness_result) {
    const indicator = document.getElementById('fairnessIndicator');
    const label = document.getElementById('fairnessLabel');
    const description = document.getElementById('fairnessDescription');
    
    const colors = {
        'Underpriced': { bg: '#3B82F6', icon: 'fa-arrow-down' },
        'Fair': { bg: '#10B981', icon: 'fa-check' },
        'Overpriced': { bg: '#EF4444', icon: 'fa-arrow-up' },
        'Insufficient Data': { bg: '#6B7280', icon: 'fa-question' }
    };
    
    const color = colors[fairness_result.label] || colors['Insufficient Data'];
    
    indicator.innerHTML = `
        <div style="background-color: ${color.bg};" class="w-24 h-24 rounded-full flex items-center justify-center text-white">
            <i class="fas ${color.icon} text-4xl"></i>
        </div>
    `;
    
    label.textContent = fairness_result.label;
    label.style.color = color.bg;
    
    if (fairness_result.label === 'Insufficient Data') {
        description.textContent = 'Not enough comparable data available for analysis.';
    } else {
        const absScore = Math.abs(fairness_result.score);
        const direction = fairness_result.score > 0 ? 'above' : 'below';
        description.textContent = `This listing is ${absScore.toFixed(1)}% ${direction} the market average.`;
    }
}

function updateStatistics(user_listing, fairness_result) {
    document.getElementById('marketAvg').textContent = `$${fairness_result.mean_price.toFixed(0)}`;
    document.getElementById('yourRent').textContent = `$${user_listing.price.toFixed(0)}`;
    
    const difference = document.getElementById('difference');
    const score = fairness_result.score;
    difference.textContent = `${score > 0 ? '+' : ''}${score.toFixed(1)}%`;
    difference.style.color = score > 10 ? '#EF4444' : score < -10 ? '#3B82F6' : '#10B981';
    
    document.getElementById('comparableCount').textContent = fairness_result.comparable_count;
}

function createPriceChart(price_distribution, userPrice) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (priceChart) {
        priceChart.destroy();
    }
    
    // Create price bins for histogram
    const prices = price_distribution.prices;
    const minPrice = Math.min(...prices, userPrice);
    const maxPrice = Math.max(...prices, userPrice);
    const binWidth = (maxPrice - minPrice) / 10;
    
    const bins = [];
    const labels = [];
    
    for (let i = 0; i < 10; i++) {
        const binMin = minPrice + (i * binWidth);
        const binMax = binMin + binWidth;
        labels.push(`$${binMin.toFixed(0)}-$${binMax.toFixed(0)}`);
        
        const count = prices.filter(price => price >= binMin && price < binMax).length;
        bins.push(count);
    }
    
    // Find which bin the user price falls into
    const userBinIndex = Math.min(Math.floor((userPrice - minPrice) / binWidth), 9);
    const backgroundColors = bins.map((_, index) => 
        index === userBinIndex ? '#FF6384' : 'rgba(102, 126, 234, 0.6)'
    );
    
    priceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Comparable Listings',
                data: bins,
                backgroundColor: backgroundColors,
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.y} listings`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Listings'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Price Range'
                    }
                }
            }
        }
    });
}

function createMap(comparables, user_listing) {
    // Initialize map if it doesn't exist
    if (!map) {
        // Center on Mississauga by default
        map = L.map('map').setView([43.5890, -79.6441], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
    } else {
        map.eachLayer(layer => {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });
    }
    
    // Add markers for comparable listings
    comparables.forEach((listing, index) => {
        // Use coordinates from server or generate simple ones
        const lat = listing.lat || 43.5890 + (Math.random() - 0.5) * 0.1;
        const lng = listing.lng || -79.6441 + (Math.random() - 0.5) * 0.1;
        
        const marker = L.marker([lat, lng]).addTo(map);
        
        const popupContent = listing.listing_url ? 
            `<div class="p-2">
                <h4 class="font-bold">Comparable ${index + 1}</h4>
                <p class="text-sm">$${listing.price}/month</p>
                <p class="text-sm">${listing.bedrooms} bed, ${listing.bathrooms} bath</p>
                <p class="text-sm">${listing.address}</p>
                <a href="${listing.listing_url}" target="_blank" class="text-blue-600 hover:underline text-sm">View Listing</a>
            </div>` :
            `<div class="p-2">
                <h4 class="font-bold">Comparable ${index + 1}</h4>
                <p class="text-sm">$${listing.price}/month</p>
                <p class="text-sm">${listing.bedrooms} bed, ${listing.bathrooms} bath</p>
                <p class="text-sm">${listing.address}</p>
            </div>`;
        
        marker.bindPopup(popupContent);
    });
    
    // Add marker for user listing
    const userCoords = getSimpleCoordinates(user_listing.address || 'Downtown', user_listing.location);
    const userMarker = L.marker([userCoords.lat, userCoords.lng], {
        icon: L.divIcon({
            className: 'custom-div-icon',
            html: `<div style="background-color: #FF6384; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        })
    }).addTo(map);
    
    userMarker.bindPopup(`
        <div class="p-2">
            <h4 class="font-bold text-red-600">Your Listing</h4>
            <p class="text-sm">$${user_listing.price}/month</p>
            <p class="text-sm">${user_listing.bedrooms} bed, ${user_listing.bathrooms} bath</p>
            <p class="text-sm">${user_listing.address || 'Address not provided'}</p>
        </div>
    `);
}

function updateAIExplanation(ai_explanation) {
    const explanationDiv = document.getElementById('aiExplanation');
    const tipsDiv = document.getElementById('negotiationTips');
    
    explanationDiv.innerHTML = `
        <div class="prose prose-lg max-w-none">
            <p class="text-gray-700 leading-relaxed">${ai_explanation.explanation}</p>
        </div>
    `;
    
    tipsDiv.innerHTML = `
        <ul class="space-y-2">
            ${ai_explanation.negotiation_tips.split('•').filter(tip => tip.trim()).map(tip => 
                `<li class="flex items-start">
                    <i class="fas fa-check-circle text-green-500 mt-1 mr-2 flex-shrink-0"></i>
                    <span>${tip.trim()}</span>
                </li>`
            ).join('')}
        </ul>
    `;
}

function displayComparableListings(comparables) {
    const container = document.getElementById('comparableListings');
    
    container.innerHTML = comparables.map((listing, index) => `
        <div class="comparable-card bg-white border border-gray-200 rounded-lg p-4 hover:shadow-lg">
            <div class="flex justify-between items-start mb-3">
                <h4 class="font-semibold text-gray-800">Comparable ${index + 1}</h4>
                <span class="bg-purple-100 text-purple-800 text-xs font-medium px-2 py-1 rounded">
                    ${listing.bedrooms} bed/${listing.bathrooms} bath
                </span>
            </div>
            <div class="space-y-2">
                <div class="flex justify-between">
                    <span class="text-gray-600">Rent:</span>
                    <span class="font-bold text-lg">$${listing.price}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-600">Size:</span>
                    <span>${listing.sqft} sqft</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-600">Price/sqft:</span>
                    <span>$${(listing.price / listing.sqft).toFixed(2)}</span>
                </div>
                <div class="text-sm text-gray-500 mt-2">
                    <i class="fas fa-map-marker-alt mr-1"></i>
                    ${listing.address}
                </div>
                ${listing.listing_url ? `
                <div class="mt-3 pt-3 border-t border-gray-200">
                    <a href="${listing.listing_url}" target="_blank" rel="noopener noreferrer" 
                       class="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 hover:underline">
                        <i class="fas fa-external-link-alt mr-1"></i>
                        View Listing
                    </a>
                </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}
