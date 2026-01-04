// animations.js - UPDATED VERSION
// Scroll animation handler
document.addEventListener('DOMContentLoaded', function() {
    
    const fadeElements = document.querySelectorAll('.section-title, .feature-highlight, .stat-item, .news-card, .team-card');
    
    fadeElements.forEach(element => {
        element.classList.add('fade-on-scroll');
    });
    
    // Check if elements are in viewport
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    fadeElements.forEach(element => {
        observer.observe(element);
    });
    
    // Page load animation
    setTimeout(() => {
        document.querySelectorAll('.fade-on-scroll').forEach(el => {
            el.classList.add('visible');
        });
    }, 1000);
});

// Motivational quotes for loading screen
const loadingQuotes = [
    "Preparing your educational experience...",
    "Building knowledge foundations...",
    "Loading school resources...",
    "Creating learning pathways...",
    "Connecting to educational excellence...",
    "Initializing school systems...",
    "Preparing academic materials...",
    "Loading student resources...",
    "Connecting to school network...",
    "Finalizing setup..."
];

// Initialize loading - FIXED VERSION
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded - starting fixed spinner");
    
    const loadingSpinner = document.getElementById('loadingSpinner');
    const progressBar = document.getElementById('progressBar');
    const loadingTime = document.getElementById('loadingTime');
    const loadingQuote = document.getElementById('loadingQuote');
    
    // If no spinner exists, exit
    if (!loadingSpinner) {
        console.log("No loading spinner found");
        return;
    }
    
    let startTime = Date.now();
    let progress = 0;
    let quoteIndex = 0;
    
    // Show the spinner
    loadingSpinner.style.display = 'flex';
    loadingSpinner.classList.remove('loading-complete');
    
    // Start progress animation
    const progressInterval = setInterval(function() {
        const elapsed = Date.now() - startTime;
        const totalTime = 2000; // 2 seconds minimum
        
        // Calculate progress (max 90% until 2 seconds)
        progress = Math.min(90, Math.floor((elapsed / totalTime) * 90));
        if (progressBar) progressBar.style.width = progress + '%';
        if (loadingTime) loadingTime.textContent = 'Loading: ' + progress + '%';
        
        // Change quote every second
        if (Math.floor(elapsed / 1000) > quoteIndex) {
            quoteIndex = Math.floor(elapsed / 1000);
            if (loadingQuote) {
                loadingQuote.textContent = loadingQuotes[quoteIndex % loadingQuotes.length];
            }
        }
        
        // After 2 seconds, complete the loading
        if (elapsed >= totalTime) {
            clearInterval(progressInterval);
            
            // Animate to 100%
            let finalProgress = 90;
            const finalInterval = setInterval(function() {
                finalProgress += 5;
                if (finalProgress >= 100) {
                    finalProgress = 100;
                    clearInterval(finalInterval);
                    
                    // Complete loading
                    if (progressBar) progressBar.style.width = '100%';
                    if (loadingTime) loadingTime.textContent = 'Loading: 100%';
                    if (loadingQuote) loadingQuote.textContent = 'Welcome to St. Joseph Mission School!';
                    
                    // Fade out the spinner (DO NOT REMOVE FROM DOM)
                    setTimeout(function() {
                        loadingSpinner.classList.add('loading-complete');
                        
                        // IMPORTANT: Keep it in DOM but hidden
                        setTimeout(function() {
                            loadingSpinner.style.pointerEvents = 'none';
                        }, 800);
                    }, 500);
                } else {
                    if (progressBar) progressBar.style.width = finalProgress + '%';
                    if (loadingTime) loadingTime.textContent = 'Loading: ' + finalProgress + '%';
                }
            }, 30);
        }
    }, 50);
    
    // Force hide after 5 seconds maximum (safety fallback)
    setTimeout(function() {
        if (loadingSpinner && !loadingSpinner.classList.contains('loading-complete')) {
            console.log("Safety timeout - fading out spinner");
            loadingSpinner.classList.add('loading-complete');
        }
    }, 5000);
});

// Optional: Show spinner during form submissions
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // For regular forms (not AJAX), don't show spinner
            if (!this.classList.contains('ajax-form')) {
                return;
            }
            
            e.preventDefault();
            const loadingSpinner = document.getElementById('loadingSpinner');
            loadingSpinner.classList.remove('loading-complete');
            loadingSpinner.style.display = 'flex';
            
            // Submit the form after showing spinner
            setTimeout(() => {
                this.submit();
            }, 500);
        });
    });
});