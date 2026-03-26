let currentChart = null;

// Form submission handler
document.getElementById('rentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Show loading state
    setLoading(true);
    hideResults();
    hideError();
    
    try {
        const response = await fetch('/analyze-rent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResults(result);
        } else {
            showError(result.error || 'An error occurred during analysis');
        }
    } catch (error) {
        showError('Network error. Please try again.');
    } finally {
        setLoading(false);
    }
});

function setLoading(isLoading) {
    const button = document.querySelector('.analyze-btn');
    const btnText = document.querySelector('.btn-text');
    const btnLoading = document.querySelector('.btn-loading');
    
    button.disabled = isLoading;
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline-flex';
    } else {
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

function displayResults(data) {
    const { user_listing, comparables, market_stats, fairness_result, explanation } = data;
    
    // Update fairness badge
    updateFairnessBadge(fairness_result);
    
    // Update explanation
    document.getElementById('explanationText').textContent = explanation;
    
    // Update market stats
    updateMarketStats(market_stats, comparables);
    
    // Create price distribution chart
    createPriceChart(user_listing.price, comparables);
    
    // Display comparable listings
    displayComparableListings(comparables);
    
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

function updateFairnessBadge(fairnessResult) {
    const badge = document.getElementById('fairnessBadge');
    const badgeIcon = document.getElementById('badgeIcon');
    const badgeText = document.getElementById('badgeText');
    const fairnessTitle = document.getElementById('fairnessTitle');
    const priceDifference = document.getElementById('priceDifference');
    
    // Remove existing classes
    badge.className = 'fairness-badge';
    
    // Add appropriate class and content
    if (fairnessResult.classification === 'Fair') {
        badge.classList.add('fair');
        badgeIcon.textContent = '✓';
        badgeText.textContent = 'Fair Price';
        fairnessTitle.textContent = 'This listing is fairly priced';
    } else if (fairnessResult.classification === 'Overpriced') {
        badge.classList.add('overpriced');
        badgeIcon.textContent = '▲';
        badgeText.textContent = 'Overpriced';
        fairnessTitle.textContent = 'This listing is overpriced';
    } else {
        badge.classList.add('underpriced');
        badgeIcon.textContent = '▼';
        badgeText.textContent = 'Underpriced';
        fairnessTitle.textContent = 'This listing is underpriced';
    }
    
    // Update price difference
    const percentDiff = Math.abs(fairnessResult.percent_difference);
    const direction = fairnessResult.percent_difference > 0 ? 'above' : 'below';
    priceDifference.textContent = `${percentDiff.toFixed(1)}% ${direction} market average`;
}

function updateMarketStats(marketStats, comparables) {
    document.getElementById('avgRent').textContent = `$${marketStats.mean.toLocaleString()}`;
    document.getElementById('medianRent').textContent = `$${marketStats.median.toLocaleString()}`;
    document.getElementById('priceRange').textContent = `$${marketStats.min.toLocaleString()} - $${marketStats.max.toLocaleString()}`;
    document.getElementById('comparableCount').textContent = comparables.length;
}

function createPriceChart(userPrice, comparables) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (currentChart) {
        currentChart.destroy();
    }
    
    // Prepare data
    const comparablePrices = comparables.map(c => c.price);
    const labels = comparables.map((c, index) => `Unit ${index + 1}`);
    
    // Create histogram bins
    const minPrice = Math.min(...comparablePrices, userPrice);
    const maxPrice = Math.max(...comparablePrices, userPrice);
    const binCount = 8;
    const binWidth = (maxPrice - minPrice) / binCount;
    
    const bins = [];
    const binLabels = [];
    
    for (let i = 0; i < binCount; i++) {
        const binMin = minPrice + i * binWidth;
        const binMax = binMin + binWidth;
        binLabels.push(`$${Math.round(binMin).toLocaleString()} - $${Math.round(binMax).toLocaleString()}`);
        
        // Count comparable prices in this bin
        const count = comparablePrices.filter(price => 
            price >= binMin && price < binMax
        ).length;
        bins.push(count);
    }
    
    // Find which bin the user price falls into
    const userBinIndex = Math.min(
        Math.floor((userPrice - minPrice) / binWidth),
        binCount - 1
    );
    
    currentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: binLabels,
            datasets: [
                {
                    label: 'Comparable Listings',
                    data: bins,
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    borderRadius: 8
                },
                {
                    label: 'Your Listing',
                    data: new Array(binCount).fill(0).map((_, index) => 
                        index === userBinIndex ? 1 : 0
                    ),
                    backgroundColor: 'rgba(239, 68, 68, 0.8)',
                    borderColor: 'rgba(239, 68, 68, 1)',
                    borderWidth: 2,
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (context.datasetIndex === 0) {
                                return `${context.dataset.label}: ${context.parsed.y} listings`;
                            } else if (context.parsed.y > 0) {
                                return `Your listing: $${userPrice.toLocaleString()}`;
                            }
                            return null;
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

function displayComparableListings(comparables) {
    const listingsGrid = document.getElementById('listingsGrid');
    listingsGrid.innerHTML = '';
    
    comparables.forEach(listing => {
        const listingElement = document.createElement('div');
        listingElement.className = 'listing-item';
        
        listingElement.innerHTML = `
            <div class="listing-price">$${listing.price.toLocaleString()}/month</div>
            <div class="listing-details">${listing.bedrooms} bed, ${listing.bathrooms} bath</div>
            <div class="listing-details">${listing.sqft ? listing.sqft.toLocaleString() + ' sqft' : 'Size not specified'}</div>
            <div class="listing-address">${listing.address}</div>
        `;
        
        listingsGrid.appendChild(listingElement);
    });
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('errorSection').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

function hideError() {
    document.getElementById('errorSection').style.display = 'none';
}

function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

function resetForm() {
    document.getElementById('rentForm').reset();
    hideResults();
    hideError();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Add some interactivity to form inputs
document.querySelectorAll('input, select').forEach(element => {
    element.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });
    
    element.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Add input validation
document.getElementById('price').addEventListener('input', function() {
    if (this.value < 0) {
        this.value = 0;
    }
});

document.getElementById('sqft').addEventListener('input', function() {
    if (this.value < 0) {
        this.value = 0;
    }
});
