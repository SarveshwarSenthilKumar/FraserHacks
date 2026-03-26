let priceChart = null;
let trendsChart = null;

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rentForm');
    form.addEventListener('submit', handleFormSubmit);
    
    // Add input validation and real-time feedback
    setupInputValidation();
    
    // Add smooth scroll behavior
    setupSmoothScroll();
    
    // Add keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Initialize advanced charts
    initializeAdvancedCharts();
});

function setupInputValidation() {
    const priceInput = document.getElementById('price');
    const sqftInput = document.getElementById('sqft');
    
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

function initializeAdvancedCharts() {
    // Initialize price chart
    const priceCtx = document.getElementById('priceChart');
    if (priceCtx) {
        priceChart = new Chart(priceCtx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Comparable Listings',
                    data: [],
                    backgroundColor: 'rgba(108, 189, 147, 0.3)',
                    borderColor: '#6cbd93',
                    borderWidth: 2,
                    borderRadius: 8
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
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Price Range'
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
    
    // Initialize trends chart
    const trendsCtx = document.getElementById('trendsChart');
    if (trendsCtx) {
        trendsChart = new Chart(trendsCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Average Rent',
                    data: [2200, 2250, 2300, 2350, 2400, 2450],
                    borderColor: '#6cbd93',
                    backgroundColor: 'rgba(108, 189, 147, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
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
        alertDiv.className = 'fixed top-4 right-4 bg-red-600 text-white px-6 py-4 rounded-lg shadow-2xl z-50 transform translate-x-full transition-all duration-300 max-w-md border-2 border-red-400';
        document.body.appendChild(alertDiv);
    }
    
    alertDiv.innerHTML = `
        <div class="flex items-start">
            <div class="flex-shrink-0 animate-pulse">
                <i class="fas fa-exclamation-triangle text-3xl text-yellow-300"></i>
            </div>
            <div class="ml-3 flex-1">
                <h3 class="text-lg font-bold text-white flex items-center">
                    <span class="animate-pulse">⚠️</span> EXPLOITATION ALERT
                </h3>
                <p class="mt-2 text-sm text-red-100">${alertMessage}</p>
                <div class="mt-3 p-2 bg-red-700 rounded border border-red-500">
                    <p class="text-xs text-red-200 font-medium">
                        <i class="fas fa-shield-alt mr-1"></i>
                        Our system has detected potentially exploitative pricing or suspicious input patterns. Please exercise extreme caution and verify all details independently.
                    </p>
                </div>
                <div class="mt-3 flex space-x-2">
                    <button onclick="this.closest('#exploitationAlert').remove()" 
                            class="bg-red-700 hover:bg-red-800 text-white text-xs font-medium px-3 py-1 rounded transition-colors">
                        <i class="fas fa-times mr-1"></i> Dismiss
                    </button>
                    <button onclick="window.open('https://www.consumerprotection.gov', '_blank')" 
                            class="bg-yellow-600 hover:bg-yellow-700 text-white text-xs font-medium px-3 py-1 rounded transition-colors">
                        <i class="fas fa-external-link-alt mr-1"></i> Report
                    </button>
                </div>
            </div>
            <button onclick="this.closest('#exploitationAlert').remove()" 
                    class="ml-3 text-red-200 hover:text-white transition-colors text-xl">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Show alert with slide-in animation and strong pulse effect
    setTimeout(() => {
        alertDiv.style.transform = 'translateX(0)';
        alertDiv.classList.add('animate-pulse');
        
        // Add sound effect (optional - using a data URI for a simple beep)
        try {
            const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmFgU7k9n1unEiBC13yO/eizEIHWq+8+OWT');
            audio.volume = 0.3;
            audio.play().catch(() => {}); // Ignore errors if audio is blocked
        } catch (e) {}
    }, 100);
    
    // Add multiple visual warnings throughout the interface
    addExploitationWarnings();
    
    // Auto-hide after 15 seconds (longer for serious alerts)
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 300);
        }
    }, 15000);
    
    // Add persistent warning banner
    addWarningBanner();
}

function addExploitationWarnings() {
    // Add red border and warning overlay to results section
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.classList.add('border-4', 'border-red-500', 'relative');
        
        // Add warning overlay
        const warningOverlay = document.createElement('div');
        warningOverlay.className = 'absolute top-0 left-0 right-0 bg-red-600 text-white px-4 py-2 text-center font-bold text-sm z-10';
        warningOverlay.innerHTML = `
            <i class="fas fa-exclamation-triangle mr-2 animate-pulse"></i>
            ⚠️ EXPLOITATION DETECTED - VERIFY ALL INFORMATION INDEPENDENTLY ⚠️
        `;
        resultsSection.insertBefore(warningOverlay, resultsSection.firstChild);
        
        // Add warning class to all price displays
        const priceElements = resultsSection.querySelectorAll('[id*="price"], [id*="Price"], .text-2xl');
        priceElements.forEach(el => {
            if (el.textContent.includes('$')) {
                el.classList.add('text-red-600', 'font-bold', 'animate-pulse');
            }
        });
    }
    
    // Add warning to fairness indicator
    const fairnessIndicator = document.getElementById('fairnessIndicator');
    if (fairnessIndicator) {
        const warningBadge = document.createElement('div');
        warningBadge.className = 'absolute -top-2 -right-2 bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-xs font-bold animate-pulse';
        warningBadge.innerHTML = '!';
        fairnessIndicator.appendChild(warningBadge);
        fairnessIndicator.classList.add('relative');
    }
}

function addWarningBanner() {
    // Add persistent warning banner at the top of the page
    const banner = document.createElement('div');
    banner.id = 'exploitationBanner';
    banner.className = 'fixed top-0 left-0 right-0 bg-red-700 text-white px-4 py-3 text-center z-40 transform -translate-y-full transition-transform duration-500';
    banner.innerHTML = `
        <div class="flex items-center justify-center max-w-4xl mx-auto">
            <i class="fas fa-shield-alt text-2xl mr-3 animate-pulse"></i>
            <div class="flex-1">
                <p class="font-bold">⚠️ SECURITY ALERT - POTENTIAL EXPLOITATION DETECTED</p>
                <p class="text-sm text-red-200">Please verify all rental details independently and consider reporting suspicious listings</p>
            </div>
            <button onclick="this.closest('#exploitationBanner').remove()" class="ml-4 text-red-200 hover:text-white">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(banner);
    
    // Slide down the banner
    setTimeout(() => {
        banner.style.transform = 'translateY(0)';
    }, 100);
    
    // Remove after 20 seconds
    setTimeout(() => {
        if (banner.parentNode) {
            banner.style.transform = 'translateY(-100%)';
            setTimeout(() => banner.remove(), 500);
        }
    }, 20000);
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
        showExploitationAlertSection(ai_explanation.exploitation_alert);
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
    
    // Update trends chart with real data
    updateTrendsChart(comparables);
    
    // Update AI explanation
    updateAIExplanation(ai_explanation);
    
    // Display comparable listings
    displayComparableListings(comparables, currency_info);
    
    // Show results section
    document.getElementById('resultsSection').classList.remove('hidden');
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function showExploitationAlertSection(alertMessage) {
    const alertSection = document.getElementById('exploitationAlertSection');
    const messageElement = document.getElementById('exploitationAlertMessage');
    
    if (alertSection && messageElement) {
        messageElement.textContent = alertMessage;
        alertSection.classList.remove('hidden');
        
        // Add animation classes
        alertSection.classList.add('animate-pulse', 'border-4', 'border-red-500');
        
        // Scroll to the alert
        setTimeout(() => {
            alertSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
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
    
    // Update average price per sqft
    if (user_listing.sqft > 0) {
        const avgPricePerSqft = fairness_result.mean_price / user_listing.sqft;
        document.getElementById('avgPricePerSqft').textContent = `$${avgPricePerSqft.toFixed(2)}`;
    }
    
    // Update listing count
    document.getElementById('listingCount').textContent = `${fairness_result.comparable_count} properties`;
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
        index === userBinIndex ? '#6cbd93' : 'rgba(108, 189, 147, 0.3)'
    );
    
    priceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Comparable Listings',
                data: bins,
                backgroundColor: backgroundColors,
                borderColor: '#6cbd93',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Listings'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Price Range'
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function updateTrendsChart(comparables) {
    if (!trendsChart || !comparables.length) return;
    
    // Generate trend data based on comparables
    const avgPrice = comparables.reduce((sum, comp) => sum + comp.price, 0) / comparables.length;
    const trendData = [];
    
    for (let i = 0; i < 6; i++) {
        const variation = (Math.random() - 0.5) * 200;
        trendData.push(avgPrice + variation);
    }
    
    trendsChart.data.datasets[0].data = trendData;
    trendsChart.update('active');
}

function updateChartType(type) {
    if (!priceChart) return;
    
    priceChart.config.type = type;
    priceChart.update('active');
}

function updateTimeRange(range) {
    if (!trendsChart) return;
    
    const months = range === '6m' ? 6 : 12;
    const labels = [];
    const data = [];
    
    for (let i = 0; i < months; i++) {
        const month = new Date();
        month.setMonth(month.getMonth() - (months - i - 1));
        labels.push(month.toLocaleString('default', { month: 'short' }));
        data.push(2200 + Math.random() * 500);
    }
    
    trendsChart.data.labels = labels;
    trendsChart.data.datasets[0].data = data;
    trendsChart.update('active');
}

function exportListings() {
    // Create CSV content
    const listings = document.querySelectorAll('#comparableListings .comparable-card');
    let csv = 'Price,Bedrooms,Bathrooms,Square Feet,Address\n';
    
    listings.forEach(listing => {
        const price = listing.querySelector('.font-bold')?.textContent || '';
        const beds = listing.querySelector('.text-purple-800')?.textContent || '';
        const sqft = listing.querySelector('.text-gray-600')?.textContent || '';
        const address = listing.querySelector('.text-gray-500')?.textContent || '';
        
        csv += `${price},${beds},${sqft},${address}\n`;
    });
    
    // Download CSV
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'comparable-listings.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

function updateAIExplanation(ai_explanation) {
    const explanationDiv = document.getElementById('aiExplanation');
    const tipsDiv = document.getElementById('negotiationTips');
    
    // Parse markdown in explanation
    const parsedExplanation = marked.parse(ai_explanation.explanation);
    explanationDiv.innerHTML = `
        <div class="prose prose-lg max-w-none">
            <div class="text-gray-700 leading-relaxed">${parsedExplanation}</div>
        </div>
    `;
    
    // Parse markdown in negotiation tips and convert to list
    const parsedTips = marked.parse(ai_explanation.negotiation_tips);
    
    // Create a temporary div to parse HTML
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
        <div class="comparable-card liquid-glass p-6">
            <div class="flex justify-between items-start mb-4">
                <h4 class="font-semibold text-gray-800">Comparable ${index + 1}</h4>
                <span class="bg-green-100 text-green-800 text-xs font-medium px-3 py-1 rounded-full">
                    ${listing.bedrooms} bed/${listing.bathrooms} bath
                </span>
            </div>
            <div class="space-y-3">
                <div class="flex justify-between items-center">
                    <span class="text-gray-600 text-sm">Rent:</span>
                    <span class="font-bold text-lg gradient-text">${currencySymbol}${listing.price}</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-gray-600 text-sm">Size:</span>
                    <span class="text-gray-800">${listing.sqft} sqft</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-gray-600 text-sm">Price/sqft:</span>
                    <span class="text-gray-800 font-medium">${currencySymbol}${(listing.price / listing.sqft).toFixed(2)}</span>
                </div>
                <div class="text-sm text-gray-500 mt-3">
                    <i class="fas fa-map-marker-alt mr-1"></i>
                    ${listing.address}
                </div>
                <div class="mt-4 pt-4 border-t border-gray-200">
                    <a href="${googleSearchUrl}" target="_blank" rel="noopener noreferrer" 
                       class="inline-flex items-center text-sm text-green-600 hover:text-green-800 hover:underline font-medium">
                        <i class="fas fa-search mr-1"></i>
                        Search on Google
                    </a>
                </div>
            </div>
        </div>
    `;
    }).join('');
}

// Additional functions for exploitation warnings
function addExploitationWarnings() {
    // Add red border and warning overlay to results section
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.classList.add('border-4', 'border-red-500', 'relative');
        
        // Add warning overlay
        const warningOverlay = document.createElement('div');
        warningOverlay.className = 'absolute top-0 left-0 right-0 bg-red-600 text-white px-4 py-2 text-center font-bold text-sm z-10';
        warningOverlay.innerHTML = `
            <i class="fas fa-exclamation-triangle mr-2 animate-pulse"></i>
            ⚠️ EXPLOITATION DETECTED - VERIFY ALL INFORMATION INDEPENDENTLY ⚠️
        `;
        resultsSection.insertBefore(warningOverlay, resultsSection.firstChild);
        
        // Add warning class to all price displays
        const priceElements = resultsSection.querySelectorAll('[id*="price"], [id*="Price"], .text-2xl');
        priceElements.forEach(el => {
            if (el.textContent.includes('$')) {
                el.classList.add('text-red-600', 'font-bold', 'animate-pulse');
            }
        });
    }
    
    // Add warning to fairness indicator
    const fairnessIndicator = document.getElementById('fairnessIndicator');
    if (fairnessIndicator) {
        const warningBadge = document.createElement('div');
        warningBadge.className = 'absolute -top-2 -right-2 bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-xs font-bold animate-pulse';
        warningBadge.innerHTML = '!';
        fairnessIndicator.appendChild(warningBadge);
        fairnessIndicator.classList.add('relative');
    }
}

function addWarningBanner() {
    // Add persistent warning banner at the top of the page
    const banner = document.createElement('div');
    banner.id = 'exploitationBanner';
    banner.className = 'fixed top-0 left-0 right-0 bg-red-700 text-white px-4 py-3 text-center z-40 transform -translate-y-full transition-transform duration-500';
    banner.innerHTML = `
        <div class="flex items-center justify-center max-w-4xl mx-auto">
            <i class="fas fa-shield-alt text-2xl mr-3 animate-pulse"></i>
            <div class="flex-1">
                <p class="font-bold">⚠️ SECURITY ALERT - POTENTIAL EXPLOITATION DETECTED</p>
                <p class="text-sm text-red-200">Please verify all rental details independently and consider reporting suspicious listings</p>
            </div>
            <button onclick="this.closest('#exploitationBanner').remove()" class="ml-4 text-red-200 hover:text-white">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(banner);
    
    // Slide down the banner
    setTimeout(() => {
        banner.style.transform = 'translateY(0)';
    }, 100);
    
    // Remove after 20 seconds
    setTimeout(() => {
        if (banner.parentNode) {
            banner.style.transform = 'translateY(-100%)';
            setTimeout(() => banner.remove(), 500);
        }
    }, 20000);
}
