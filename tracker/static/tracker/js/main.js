/* main.js - interactive features for mental health tracker */

// initialize interactive elements when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeNavbarHoverEffects();
    initializeCardHoverEffects();
    initializeButtonHoverEffects();
});

// navbar button hover effects
function initializeNavbarHoverEffects() {
    const navButtons = document.querySelectorAll('.nav-btn-primary, .nav-btn-secondary');
    
    navButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (this.classList.contains('nav-btn-primary')) {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 6px 16px rgba(92, 107, 192, 0.35)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            if (this.classList.contains('nav-btn-primary')) {
                this.style.boxShadow = '0 4px 12px rgba(92, 107, 192, 0.25)';
            }
        });
    });
    
    // sign in link hover effect
    const signInLink = document.querySelector('.nav-link-primary');
    if (signInLink) {
        signInLink.addEventListener('mouseenter', function() {
            this.style.color = '#7e57c2';
        });
        
        signInLink.addEventListener('mouseleave', function() {
            this.style.color = '#5c6bc0';
        });
    }
}

// home page feature cards hover effects
function initializeCardHoverEffects() {
    const cards = document.querySelectorAll('.feature-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 12px 24px rgba(92, 107, 192, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.08)';
        });
    });
}

// button hover effects for mood actions
function initializeButtonHoverEffects() {
    const primaryButtons = document.querySelectorAll('.btn-primary-action');
    const secondaryButtons = document.querySelectorAll('.btn-secondary-action');
    
    primaryButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 12px rgba(67, 160, 71, 0.4)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 8px rgba(67, 160, 71, 0.3)';
        });
    });
    
    secondaryButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            if (this.classList.contains('btn-update')) {
                this.style.boxShadow = '0 4px 10px rgba(149, 117, 205, 0.4)';
            } else if (this.classList.contains('btn-archive')) {
                this.style.boxShadow = '0 4px 10px rgba(255, 183, 77, 0.4)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            if (this.classList.contains('btn-update')) {
                this.style.boxShadow = '0 2px 6px rgba(149, 117, 205, 0.3)';
            } else if (this.classList.contains('btn-archive')) {
                this.style.boxShadow = '0 2px 6px rgba(255, 183, 77, 0.3)';
            }
        });
    });
}
