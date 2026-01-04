class NotificationSystem {
    constructor() {
        this.container = document.getElementById('notificationsContainer');
        if (!this.container) {
            this.createContainer();
        }
        this.notificationCount = 0;
        this.maxNotifications = 5;
        this.init();
    }
    
    createContainer() {
        this.container = document.createElement('div');
        this.container.className = 'notifications-container';
        this.container.id = 'notificationsContainer';
        document.body.insertBefore(this.container, document.body.firstChild);
    }
    
    init() {
        // Load any existing messages from Django messages framework
        this.loadDjangoMessages();
        
        // Listen for new messages
        document.addEventListener('newNotification', (e) => {
            this.show(e.detail.type, e.detail.message, e.detail.title);
        });
        
        // Auto-cleanup every minute
        setInterval(() => this.cleanup(), 60000);
    }
    
    loadDjangoMessages() {
        // This would be populated by Django template context
        // In practice, you'll need to pass messages to JavaScript
        // For now, we'll handle messages through the template
    }
    
    show(type, message, title = null) {
        // Limit number of notifications
        if (this.notificationCount >= this.maxNotifications) {
            this.removeOldest();
        }
        
        this.notificationCount++;
        const notificationId = 'notification-' + Date.now();
        
        // Default titles based on type
        if (!title) {
            const titles = {
                'success': 'Success',
                'error': 'Error',
                'warning': 'Warning',
                'info': 'Information'
            };
            title = titles[type] || 'Notification';
        }
        
        // Icons based on type
        const icons = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-circle',
            'warning': 'fas fa-exclamation-triangle',
            'info': 'fas fa-info-circle'
        };
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.id = notificationId;
        notification.setAttribute('role', 'alert');
        notification.setAttribute('aria-live', 'polite');
        
        const icon = icons[type] || 'fas fa-bell';
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        notification.innerHTML = `
            <i class="${icon} notification-icon"></i>
            <div class="notification-content">
                <div class="notification-title">
                    <span>${title}</span>
                    <button class="notification-close" aria-label="Close notification">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <p class="notification-message">${message}</p>
                <div class="notification-time">
                    <i class="far fa-clock"></i>
                    ${time}
                </div>
                <div class="notification-progress"></div>
            </div>
        `;
        
        // Add to container
        this.container.appendChild(notification);
        
        // Add click event to close button
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => this.remove(notificationId));
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (document.getElementById(notificationId)) {
                this.remove(notificationId);
            }
        }, 5000);
        
        // Add sound for important notifications
        if (type === 'error' || type === 'warning') {
            this.playSound(type);
        }
        
        return notificationId;
    }
    
    remove(notificationId) {
        const notification = document.getElementById(notificationId);
        if (notification) {
            notification.style.animation = 'slideOutRight 0.4s ease forwards';
            notification.addEventListener('animationend', () => {
                notification.remove();
                this.notificationCount = Math.max(0, this.notificationCount - 1);
            });
        }
    }
    
    removeOldest() {
        const notifications = this.container.querySelectorAll('.notification');
        if (notifications.length > 0) {
            this.remove(notifications[0].id);
        }
    }
    
    cleanup() {
        // Remove any notifications that might have been missed
        const notifications = this.container.querySelectorAll('.notification');
        const now = Date.now();
        
        notifications.forEach(notification => {
            const id = notification.id;
            const time = parseInt(id.split('-')[1]);
            if (now - time > 10000) {
                notification.remove();
                this.notificationCount = Math.max(0, this.notificationCount - 1);
            }
        });
    }
    
    playSound(type) {
        // Create a subtle notification sound
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            // Different sounds for different notification types
            if (type === 'error') {
                oscillator.frequency.setValueAtTime(300, audioContext.currentTime);
                oscillator.frequency.setValueAtTime(200, audioContext.currentTime + 0.1);
            } else if (type === 'warning') {
                oscillator.frequency.setValueAtTime(400, audioContext.currentTime);
                oscillator.frequency.setValueAtTime(350, audioContext.currentTime + 0.1);
            }
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
            
            oscillator.start();
            oscillator.stop(audioContext.currentTime + 0.3);
        } catch (e) {
            // Audio not supported or blocked
            console.log('Audio notification not supported');
        }
    }
    
    // Convenience methods
    success(message, title = null) {
        return this.show('success', message, title);
    }
    
    error(message, title = null) {
        return this.show('error', message, title);
    }
    
    warning(message, title = null) {
        return this.show('warning', message, title);
    }
    
    info(message, title = null) {
        return this.show('info', message, title);
    }
    
    // Show multiple messages at once
    showMultiple(messages) {
        messages.forEach(msg => {
            setTimeout(() => {
                this.show(msg.type, msg.message, msg.title);
            }, messages.indexOf(msg) * 300);
        });
    }
}

// Initialize notification system when DOM is loaded
let notificationSystem;

document.addEventListener('DOMContentLoaded', function() {
    notificationSystem = new NotificationSystem();
    
    // Expose to global scope for easy access
    window.showNotification = function(type, message, title = null) {
        if (notificationSystem) {
            return notificationSystem.show(type, message, title);
        }
        return null;
    };
    
    // Shortcut methods
    window.showSuccess = (message, title) => notificationSystem.success(message, title);
    window.showError = (message, title) => notificationSystem.error(message, title);
    window.showWarning = (message, title) => notificationSystem.warning(message, title);
    window.showInfo = (message, title) => notificationSystem.info(message, title);
    
    // Load Django messages if they exist in the template
    loadTemplateMessages();
});

// Function to load messages from Django template context
function loadTemplateMessages() {
    // Check if there are messages in the template
    const messageContainer = document.querySelector('[data-django-messages]');
    if (messageContainer) {
        try {
            const messages = JSON.parse(messageContainer.dataset.djangoMessages);
            if (messages && messages.length > 0) {
                // Show messages with a slight delay
                setTimeout(() => {
                    messages.forEach(msg => {
                        notificationSystem.show(msg.tags, msg.message);
                    });
                }, 1000);
            }
        } catch (e) {
            console.log('Could not parse Django messages');
        }
    }
}

// Function to trigger notifications from Django messages
function showDjangoMessage(type, message) {
    if (notificationSystem) {
        notificationSystem.show(type, message);
    } else {
        // Queue message if notification system not ready
        document.addEventListener('notificationSystemReady', () => {
            notificationSystem.show(type, message);
        });
    }
}

// Custom event for triggering notifications
function triggerNotification(type, message, title = null) {
    const event = new CustomEvent('newNotification', {
        detail: { type, message, title }
    });
    document.dispatchEvent(event);
}

// Make functions available globally
window.triggerNotification = triggerNotification;
window.showDjangoMessage = showDjangoMessage;