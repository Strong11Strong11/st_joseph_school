// Back to top button
const backToTopButton = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.classList.add('show');
    } else {
        backToTopButton.classList.remove('show');
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Active nav link highlighting
document.addEventListener('DOMContentLoaded', () => {
    const currentUrl = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// WhatsApp tooltip
const whatsappFloat = document.querySelector('.whatsapp-float');

if (whatsappFloat) {
    whatsappFloat.addEventListener('mouseenter', function() {
        const tooltip = this.querySelector('.whatsapp-tooltip');
        if (tooltip) {
            tooltip.style.opacity = '1';
            tooltip.style.visibility = 'visible';
        }
    });
    
    whatsappFloat.addEventListener('mouseleave', function() {
        const tooltip = this.querySelector('.whatsapp-tooltip');
        if (tooltip) {
            tooltip.style.opacity = '0';
            tooltip.style.visibility = 'hidden';
        }
    });
    
    // Add click animation
    whatsappFloat.addEventListener('click', function() {
        this.style.transform = 'scale(0.9)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 200);
    });
}

// Testimonial Carousel for Mobile
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize on mobile
    if (window.innerWidth >= 768) return;
    
    const testimonialCarousel = document.getElementById('testimonialCarousel');
    const testimonialPrev = document.getElementById('testimonialPrev');
    const testimonialNext = document.getElementById('testimonialNext');
    const indicators = document.querySelectorAll('.indicator');
    const slides = document.querySelectorAll('.testimonial-slide');
    
    if (!testimonialCarousel || slides.length === 0) return;
    
    let currentSlide = 0;
    const totalSlides = slides.length;
    let isAutoScrolling = true;
    let autoScrollInterval;
    
    // Function to update carousel
    function updateCarousel() {
        // Remove active class from all slides
        slides.forEach(slide => {
            slide.classList.remove('active');
        });
        
        // Add active class to current slide
        slides[currentSlide].classList.add('active');
        
        // Update indicators
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentSlide);
        });
        
        // Scroll to current slide
        const slideWidth = slides[0].offsetWidth + 20; 
        testimonialCarousel.scrollTo({
            left: currentSlide * slideWidth,
            behavior: 'smooth'
        });
    }
    
    // Next slide
    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateCarousel();
    }
    
    // Previous slide
    function prevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        updateCarousel();
    }
    
    // Go to specific slide
    function goToSlide(slideIndex) {
        currentSlide = slideIndex;
        updateCarousel();
    }
    
    // Event listeners for buttons
    if (testimonialPrev) {
        testimonialPrev.addEventListener('click', function() {
            isAutoScrolling = false;
            clearInterval(autoScrollInterval);
            prevSlide();
        });
    }
    
    if (testimonialNext) {
        testimonialNext.addEventListener('click', function() {
            isAutoScrolling = false;
            clearInterval(autoScrollInterval);
            nextSlide();
        });
    }
    
    // Event listeners for indicators
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', function() {
            isAutoScrolling = false;
            clearInterval(autoScrollInterval);
            goToSlide(index);
        });
    });
    
    // Handle scroll events to update active slide
    let scrollTimeout;
    testimonialCarousel.addEventListener('scroll', function() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function() {
            const scrollPosition = testimonialCarousel.scrollLeft;
            const slideWidth = slides[0].offsetWidth + 20;
            const newSlide = Math.round(scrollPosition / slideWidth);
            
            if (newSlide !== currentSlide && newSlide >= 0 && newSlide < totalSlides) {
                currentSlide = newSlide;
                
                // Update active class
                slides.forEach(slide => {
                    slide.classList.remove('active');
                });
                slides[currentSlide].classList.add('active');
                
                // Update indicators
                indicators.forEach((indicator, index) => {
                    indicator.classList.toggle('active', index === currentSlide);
                });
            }
        }, 100);
    });
    
    // Auto-scroll functionality
    function startAutoScroll() {
        if (isAutoScrolling) {
            autoScrollInterval = setInterval(function() {
                nextSlide();
            }, 4000);
        }
    }
    
    function stopAutoScroll() {
        clearInterval(autoScrollInterval);
    }
    
    // Start auto-scroll
    startAutoScroll();
    
    // Pause auto-scroll on interaction
    testimonialCarousel.addEventListener('mouseenter', stopAutoScroll);
    testimonialCarousel.addEventListener('mouseleave', function() {
        if (isAutoScrolling) {
            startAutoScroll();
        }
    });
    
    testimonialCarousel.addEventListener('touchstart', stopAutoScroll);
    testimonialCarousel.addEventListener('touchend', function() {
        if (isAutoScrolling) {
            startAutoScroll();
        }
    });
    
    // Re-initialize on window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {

            stopAutoScroll();
        } else {

            updateCarousel();
            if (isAutoScrolling) {
                startAutoScroll();
            }
        }
    });
    
    // Initialize
    updateCarousel();
});