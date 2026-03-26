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

function showExploitationAlert(alertMessage) {
    // Create or update exploitation alert notification
    let alertDiv = document.getElementById('exploitationAlert');
    if (!alertDiv) {
        alertDiv = document.createElement('div');
        alertDiv.id = 'exploitationAlert';
        alertDiv.className = 'fixed top-4 right-4 bg-red-600 text-white px-6 py-4 rounded-lg shadow-xl z-50 transform translate-x-full transition-transform duration-300 max-w-md';
        document.body.appendChild(alertDiv);
    }
    
    alertDiv.innerHTML = `
        <div class="flex items-start">
            <div class="flex-shrink-0">
                <i class="fas fa-exclamation-triangle text-2xl text-yellow-300"></i>
            </div>
            <div class="ml-3 flex-1">
                <h3 class="text-lg font-bold text-white">⚠️ EXPLOITATION ALERT</h3>
                <p class="mt-1 text-sm text-red-100">${alertMessage}</p>
                <div class="mt-2">
                    <button onclick="this.closest('#exploitationAlert').remove()" 
                            class="bg-red-700 hover:bg-red-800 text-white text-xs font-medium px-3 py-1 rounded transition-colors">
                        Dismiss
                    </button>
                </div>
            </div>
            <button onclick="this.closest('#exploitationAlert').remove()" 
                    class="ml-3 text-red-200 hover:text-white transition-colors">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Show alert with slide-in animation and pulse effect
    setTimeout(() => {
        alertDiv.style.transform = 'translateX(0)';
        alertDiv.classList.add('animate-pulse');
    }, 100);
    
    // Auto-hide after 10 seconds (longer than regular errors)
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 300);
        }
    }, 10000);
    
    // Add red border to results section to indicate warning
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.classList.add('border-4', 'border-red-500');
        // Remove border after 15 seconds
        setTimeout(() => {
            resultsSection.classList.remove('border-4', 'border-red-500');
        }, 15000);
    }
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
    const { user_listing, fairness_result, comparables, ai_explanation, price_distribution, warnings, data_quality, currency_info } = data;
    
    // Check for exploitation detection FIRST
    if (ai_explanation && ai_explanation.exploitation_detected) {
        showExploitationAlert(ai_explanation.exploitation_alert);
        // Still show results but with prominent warning
    }
    
    // Display currency info if available
    if (currency_info) {
        displayCurrencyInfo(currency_info);
    }
    
    // Display warnings if any
    if (warnings && warnings.length > 0) {
        displayWarnings(warnings);
    }
    
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
    displayComparableListings(comparables, currency_info);
    
    // Show results section
    document.getElementById('resultsSection').classList.remove('hidden');
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function displayCurrencyInfo(currency_info) {
    const currencyContainer = document.getElementById('currencyInfoContainer');
    if (!currencyContainer) {
        // Create currency info container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'currencyInfoContainer';
        container.className = 'mb-4';
        container.innerHTML = `
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="flex items-center justify-between">
                    <div>
                        <h3 class="text-lg font-semibold text-blue-800">
                            <i class="fas fa-globe mr-2"></i>
                            International Market Analysis
                        </h3>
                        <p class="text-sm text-blue-600 mt-1">
                            Analyzing property in <span id="countryName" class="font-medium"></span> using <span id="currencySymbol" class="font-medium"></span> currency
                        </p>
                    </div>
                    <div class="text-right">
                        <span id="currencyCode" class="text-2xl font-bold text-blue-800"></span>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('resultsSection').insertBefore(container, document.getElementById('resultsSection').firstChild);
    }
    
    // Update currency info
    document.getElementById('countryName').textContent = currency_info.country;
    document.getElementById('currencySymbol').textContent = currency_info.symbol;
    document.getElementById('currencyCode').textContent = currency_info.currency;
}

function displayWarnings(warnings) {
    const warningsContainer = document.getElementById('warningsContainer');
    if (!warningsContainer) {
        // Create warnings container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'warningsContainer';
        container.className = 'mb-6';
        container.innerHTML = `
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h3 class="text-lg font-semibold text-yellow-800 mb-2">
                    <i class="fas fa-exclamation-triangle mr-2"></i>
                    Data Quality Warnings
                </h3>
                <div id="warningsList" class="space-y-1"></div>
            </div>
        `;
        document.getElementById('resultsSection').insertBefore(container, document.getElementById('resultsSection').firstChild);
    }
    
    const warningsList = document.getElementById('warningsList');
    warningsList.innerHTML = warnings.map(warning => `
        <div class="flex items-start">
            <i class="fas fa-exclamation-circle text-yellow-600 mt-0.5 mr-2 flex-shrink-0"></i>
            <span class="text-sm text-yellow-800">${warning}</span>
        </div>
    `).join('');
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
    console.log('Creating map with comparables:', comparables.length, 'listings');
    
    // Wait for DOM to be ready
    setTimeout(() => {
        const mapContainer = document.getElementById('map');
        if (!mapContainer) {
            console.error('Map container not found');
            return;
        }
        
        console.log('Map container found:', mapContainer);
        console.log('Map container dimensions:', mapContainer.offsetWidth, 'x', mapContainer.offsetHeight);
        
        // Ensure container has proper dimensions
        if (mapContainer.offsetHeight === 0) {
            mapContainer.style.height = '400px';
            mapContainer.style.width = '100%';
        }
        
        // Initialize map if it doesn't exist
        if (!map) {
            try {
                console.log('Initializing new map...');
                // Center on Mississauga by default
                map = L.map('map').setView([43.5890, -79.6441], 12);
                
                // Use CartoDB tiles as backup (more reliable)
                const tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                    attribution: '© OpenStreetMap contributors © CARTO',
                    subdomains: 'abcd',
                    maxZoom: 19,
                    minZoom: 1,
                    tileSize: 256,
                    detectRetina: true
                });
                
                tileLayer.addTo(map);
                
                // Listen for tile load events
                tileLayer.on('tileload', function(e) {
                    console.log('Map tile loaded successfully');
                });
                
                tileLayer.on('tileerror', function(e) {
                    console.error('Map tile failed to load:', e);
                    // Try fallback tile server
                    try {
                        const fallbackLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                            attribution: '© OpenStreetMap contributors',
                            maxZoom: 19
                        });
                        map.removeLayer(tileLayer);
                        fallbackLayer.addTo(map);
                        console.log('Switched to fallback tile server');
                    } catch (fallbackError) {
                        console.error('Fallback also failed:', fallbackError);
                    }
                });
                
                console.log('Map initialized successfully');
            } catch (error) {
                console.error('Error initializing map:', error);
                // Show error message in map container
                mapContainer.innerHTML = `
                    <div class="flex items-center justify-center h-full bg-gray-100 rounded-lg p-4">
                        <div class="text-center">
                            <i class="fas fa-map-marked-alt text-4xl text-gray-400 mb-2"></i>
                            <p class="text-gray-600">Map unavailable</p>
                            <p class="text-sm text-gray-500">Showing property locations in list below</p>
                        </div>
                    </div>
                `;
                return;
            }
        } else {
            console.log('Using existing map, clearing markers...');
            // Clear existing markers
            map.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });
        }
        
        // Add markers for comparable listings
        comparables.forEach((listing, index) => {
            console.log(`Adding marker ${index + 1} for:`, listing.address);
            
            // Use coordinates from server or generate simple ones
            const lat = listing.lat || 43.5890 + (Math.random() - 0.5) * 0.1;
            const lng = listing.lng || -79.6441 + (Math.random() - 0.5) * 0.1;
            
            const marker = L.marker([lat, lng]).addTo(map);
            
            // Create Google search URL instead of direct listing link
            const searchQuery = encodeURIComponent(`${listing.address} ${listing.location} rental $${listing.price}`);
            const googleSearchUrl = `https://www.google.com/search?q=${searchQuery}`;
            
            const popupContent = `
                <div class="p-2" style="min-width: 200px;">
                    <h4 class="font-bold mb-2">Comparable ${index + 1}</h4>
                    <p class="text-sm mb-1"><strong>$${listing.price}/month</strong></p>
                    <p class="text-sm mb-1">${listing.bedrooms} bed, ${listing.bathrooms} bath</p>
                    <p class="text-sm mb-2">${listing.address}</p>
                    <a href="${googleSearchUrl}" target="_blank" class="text-blue-600 hover:underline text-sm font-medium">
                        <i class="fas fa-search mr-1"></i>
                        Search on Google →
                    </a>
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
            <div class="p-2" style="min-width: 200px;">
                <h4 class="font-bold text-red-600 mb-2">Your Listing</h4>
                <p class="text-sm mb-1"><strong>$${user_listing.price}/month</strong></p>
                <p class="text-sm mb-1">${user_listing.bedrooms} bed, ${user_listing.bathrooms} bath</p>
                <p class="text-sm">${user_listing.address || 'Address not provided'}</p>
            </div>
        `);
        
        // Force map to redraw and invalidate size
        setTimeout(() => {
            if (map) {
                console.log('Invalidating map size and fitting bounds...');
                map.invalidateSize();
                
                // Fit all markers in view
                const group = new L.featureGroup([userMarker]);
                comparables.forEach((listing, index) => {
                    const lat = listing.lat || 43.5890 + (Math.random() - 0.5) * 0.1;
                    const lng = listing.lng || -79.6441 + (Math.random() - 0.5) * 0.1;
                    const marker = L.marker([lat, lng]);
                    group.addLayer(marker);
                });
                
                map.fitBounds(group.getBounds().extend(userMarker.getLatLng()), { 
                    padding: [50, 50],
                    maxZoom: 15 
                });
            }
        }, 500);
        
    }, 500); // Increased delay to ensure DOM is fully ready
}

function updateAIExplanation(ai_explanation) {
    const explanationDiv = document.getElementById('aiExplanation');
    const tipsDiv = document.getElementById('negotiationTips');
    
    // Parse markdown in the explanation
    const parsedExplanation = marked.parse(ai_explanation.explanation);
    explanationDiv.innerHTML = `
        <div class="prose prose-lg max-w-none">
            <div class="text-gray-700 leading-relaxed">${parsedExplanation}</div>
        </div>
    `;
    
    // Parse markdown in negotiation tips and convert to list
    const parsedTips = marked.parse(ai_explanation.negotiation_tips);
    
    // Create a temporary div to parse the HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = parsedTips;
    
    // Extract list items or paragraphs
    let listItems = [];
    const listElements = tempDiv.querySelectorAll('li');
    const paragraphs = tempDiv.querySelectorAll('p');
    
    if (listElements.length > 0) {
        listItems = Array.from(listElements).map(li => li.innerHTML);
    } else if (paragraphs.length > 0) {
        listItems = Array.from(paragraphs).map(p => p.innerHTML);
    } else {
        // Fallback to manual parsing with bullet points
        listItems = ai_explanation.negotiation_tips.split('•').filter(tip => tip.trim()).map(tip => tip.trim());
    }
    
    tipsDiv.innerHTML = `
        <ul class="space-y-2">
            ${listItems.map(tip => 
                `<li class="flex items-start">
                    <i class="fas fa-check-circle text-green-500 mt-1 mr-2 flex-shrink-0"></i>
                    <span>${tip}</span>
                </li>`
            ).join('')}
        </ul>
    `;
}

function displayComparableListings(comparables, currency_info = null) {
    const container = document.getElementById('comparableListings');
    const currencySymbol = currency_info ? currency_info.symbol : '$';
    
    container.innerHTML = comparables.map((listing, index) => {
        // Create Google search URL for the property
        const searchQuery = encodeURIComponent(`${listing.address} ${listing.location} rental ${currencySymbol}${listing.price}`);
        const googleSearchUrl = `https://www.google.com/search?q=${searchQuery}`;
        
        return `
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
                    <span class="font-bold text-lg">${currencySymbol}${listing.price}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-600">Size:</span>
                    <span>${listing.sqft} sqft</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-600">Price/sqft:</span>
                    <span>${currencySymbol}${(listing.price / listing.sqft).toFixed(2)}</span>
                </div>
                <div class="text-sm text-gray-500 mt-2">
                    <i class="fas fa-map-marker-alt mr-1"></i>
                    ${listing.address}
                </div>
                <div class="mt-3 pt-3 border-t border-gray-200">
                    <a href="${googleSearchUrl}" target="_blank" rel="noopener noreferrer" 
                       class="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 hover:underline font-medium">
                        <i class="fas fa-search mr-1"></i>
                        Search on Google
                    </a>
                </div>
            </div>
        </div>
    `;
    }).join('');
}
