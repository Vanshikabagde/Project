// Main JavaScript for Health Assessment App

// Enhanced BMI calculation with real-time updates
function calculateBMI() {
    const height = parseFloat(document.getElementById('height')?.value || 0);
    const weight = parseFloat(document.getElementById('weight')?.value || 0);
    const bmiDisplay = document.getElementById('bmiDisplay');
    const bmiValue = document.getElementById('bmiValue');
    const bmiCategory = document.getElementById('bmiCategory');

    if (height && weight && height > 0) {
        const bmi = weight / ((height / 100) ** 2);
        let category = '';
        let color = '';
        let bgColor = '';

        if (bmi < 18.5) {
            category = 'Underweight';
            color = '#6b7280';
            bgColor = 'rgba(107, 114, 128, 0.1)';
        } else if (bmi < 25) {
            category = 'Normal weight';
            color = '#10b981';
            bgColor = 'rgba(16, 185, 129, 0.1)';
        } else if (bmi < 30) {
            category = 'Overweight';
            color = '#f59e0b';
            bgColor = 'rgba(245, 158, 11, 0.1)';
        } else {
            category = 'Obese';
            color = '#ef4444';
            bgColor = 'rgba(239, 68, 68, 0.1)';
        }

        if (bmiDisplay) {
            bmiDisplay.innerHTML = `<div style="background: ${bgColor}; color: ${color}; padding: 8px 12px; border-radius: 8px; font-weight: 600;">BMI: ${bmi.toFixed(1)} (${category})</div>`;
            bmiDisplay.style.display = 'block';
            bmiDisplay.style.animation = 'fadeIn 0.3s ease-out';
        }

        if (bmiValue) {
            bmiValue.textContent = bmi.toFixed(1);
            bmiValue.style.color = color;
            bmiValue.style.animation = 'pulse 0.3s ease-out';
        }

        if (bmiCategory) {
            bmiCategory.textContent = category;
            bmiCategory.style.color = color;
            bmiCategory.style.background = bgColor;
            bmiCategory.style.padding = '4px 8px';
            bmiCategory.style.borderRadius = '12px';
            bmiCategory.style.fontSize = '0.9rem';
            bmiCategory.style.fontWeight = '500';
        }
    } else {
        if (bmiDisplay) {
            bmiDisplay.style.display = 'none';
        }
        if (bmiValue) {
            bmiValue.textContent = '--';
            bmiValue.style.color = '#6b7280';
        }
        if (bmiCategory) {
            bmiCategory.textContent = '--';
            bmiCategory.style.color = '#6b7280';
            bmiCategory.style.background = 'transparent';
        }
    }
}

// Enhanced form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    const errorMessages = form.querySelectorAll('.error-message');

    // Clear previous errors
    errorMessages.forEach(msg => msg.remove());

    requiredFields.forEach(field => {
        const fieldGroup = field.closest('.form-group');
        if (!field.value.trim()) {
            isValid = false;
            fieldGroup.classList.add('error');
            fieldGroup.classList.remove('success');

            const errorMsg = document.createElement('div');
            errorMsg.className = 'error-message';
            errorMsg.textContent = `${field.previousElementSibling?.textContent || 'This field'} is required`;
            fieldGroup.appendChild(errorMsg);

            // Shake animation
            field.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => field.style.animation = '', 500);
        } else {
            fieldGroup.classList.remove('error');
            fieldGroup.classList.add('success');
        }
    });

    return isValid;
}

// Enhanced progress tracking with visual feedback
function updateProgress() {
    const requiredFields = ['age', 'height', 'weight', 'smoking_status', 'exercise_frequency'];
    const optionalFields = ['blood_type', 'family_history', 'medical_conditions', 'medications', 'symptoms'];
    let filledRequired = 0;
    let filledOptional = 0;

    requiredFields.forEach(field => {
        const element = document.getElementById(field);
        if (element && element.value.trim()) filledRequired++;
    });

    optionalFields.forEach(field => {
        const element = document.getElementById(field);
        if (element && element.value.trim()) filledOptional++;
    });

    const totalFields = requiredFields.length + optionalFields.length;
    const filledFields = filledRequired + filledOptional;
    const progressPercent = Math.min((filledFields / totalFields) * 100, 100);

    // Update progress bar with smooth animation
    const progressBar = document.querySelector('.progress-fill');
    if (progressBar) {
        progressBar.style.width = progressPercent + '%';
        progressBar.style.transition = 'width 0.3s ease-out';

        // Color based on completion
        if (progressPercent < 50) {
            progressBar.style.background = 'linear-gradient(90deg, #ef4444, #f87171)';
        } else if (progressPercent < 80) {
            progressBar.style.background = 'linear-gradient(90deg, #f59e0b, #fbbf24)';
        } else {
            progressBar.style.background = 'linear-gradient(90deg, #10b981, #34d399)';
        }
    }

    // Update progress text with more detail
    const progressText = document.getElementById('progressText');
    if (progressText) {
        const requiredComplete = filledRequired === requiredFields.length;
        progressText.textContent = requiredComplete ?
            `Complete! ${filledOptional}/${optionalFields.length} optional filled` :
            `Required: ${filledRequired}/${requiredFields.length}, Optional: ${filledOptional}/${optionalFields.length}`;
        progressText.style.color = requiredComplete ? '#10b981' : '#6b7280';
    }
}

// Enhanced auto-save with visual feedback
function autoSave() {
    const formData = {};
    document.querySelectorAll('input, select, textarea').forEach(element => {
        if (element.id && element.name) {
            formData[element.name] = element.value;
        }
    });

    // Save to localStorage
    localStorage.setItem('assessmentFormData', JSON.stringify(formData));

    // Visual feedback
    showSaveIndicator();

    // Send to server for progress tracking (if endpoint exists)
    fetch('/api/progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ formData: formData })
    })
    .then(response => response.json())
    .then(data => {
        // Update progress bar with server data
        const progressBar = document.querySelector('.progress-fill');
        if (progressBar && data.progress !== undefined) {
            progressBar.style.width = data.progress + '%';
        }
    })
    .catch(error => {
        // Silently fail - auto-save is not critical
        console.log('Progress update failed:', error);
    });
}

// Show save indicator
function showSaveIndicator() {
    let indicator = document.getElementById('save-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'save-indicator';
        indicator.textContent = '💾 Saved';
        indicator.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1001;
            animation: slideInRight 0.3s ease-out;
        `;
        document.body.appendChild(indicator);
    }

    clearTimeout(indicator.timeout);
    indicator.timeout = setTimeout(() => {
        indicator.style.animation = 'slideOutRight 0.3s ease-in forwards';
        setTimeout(() => indicator.remove(), 300);
    }, 2000);
}

// Load saved form data with animation
function loadSavedData() {
    const savedData = localStorage.getItem('assessmentFormData');
    if (savedData) {
        const formData = JSON.parse(savedData);
        let loadedCount = 0;

        Object.keys(formData).forEach(key => {
            const element = document.querySelector(`[name="${key}"]`);
            if (element && formData[key]) {
                element.value = formData[key];
                loadedCount++;

                // Add fade-in animation
                element.style.animation = 'fadeIn 0.3s ease-out';
            }
        });

        if (loadedCount > 0) {
            setTimeout(() => {
                calculateBMI();
                updateProgress();
                showAlert('📁 Previous data loaded successfully!', 'success');
            }, 100);
        }
    }
}

// Enhanced form submission with validation and loading states
function handleFormSubmit(formId, submitButtonText = 'Submit') {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        if (!validateForm(formId)) {
            e.preventDefault();
            showAlert('⚠️ Please fill in all required fields', 'warning');
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalHTML = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.7';

            // Clear localStorage on successful submission
            localStorage.removeItem('assessmentFormData');

            // Re-enable after timeout (in case of error)
            setTimeout(() => {
                submitBtn.innerHTML = originalHTML;
                submitBtn.disabled = false;
                submitBtn.style.opacity = '1';
            }, 5000);
        }
    });
}

// Enhanced alert system
function showAlert(message, type = 'info', duration = 5000) {
    // Remove existing alerts of same type
    const existingAlerts = document.querySelectorAll(`.alert-${type}`);
    existingAlerts.forEach(alert => alert.remove());

    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible`;
    alertDiv.innerHTML = `
        <i class="fas fa-${getAlertIcon(type)}"></i>
        <span>${message}</span>
        <button class="btn-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    // Add to flash messages container or create one
    let container = document.querySelector('.flash-messages');
    if (!container) {
        container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.insertBefore(container, document.body.firstChild);
    }

    container.appendChild(alertDiv);

    // Auto-remove after duration
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.style.animation = 'slideOutRight 0.3s ease-in forwards';
            setTimeout(() => alertDiv.remove(), 300);
        }
    }, duration);
}

function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
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

// Enhanced keyboard navigation
function initializeKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        // ESC to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => modal.classList.remove('show'));
        }

        // Ctrl/Cmd + S to save (if form exists)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const form = document.querySelector('form');
            if (form) {
                autoSave();
                showAlert('💾 Data saved!', 'success');
            }
        }
    });
}

// Initialize tooltips
function initializeTooltips() {
    const tooltips = document.querySelectorAll('.tooltip');
    tooltips.forEach(tooltip => {
        const text = tooltip.getAttribute('data-tooltip');
        if (text) {
            const tooltipElement = document.createElement('span');
            tooltipElement.className = 'tooltip-text';
            tooltipElement.textContent = text;
            tooltip.appendChild(tooltipElement);
        }
    });
}

// Enhanced animations for page elements
function initializeAnimations() {
    // Animate cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe cards and sections
    document.querySelectorAll('.card, .action-card, .stat-card, .form-section').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        observer.observe(el);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize BMI calculator
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');

    if (heightInput && weightInput) {
        heightInput.addEventListener('input', calculateBMI);
        weightInput.addEventListener('input', calculateBMI);
    }

    // Initialize progress tracking
    document.querySelectorAll('input, select, textarea').forEach(element => {
        element.addEventListener('input', updateProgress);
        element.addEventListener('change', updateProgress);
        element.addEventListener('input', debounce(autoSave, 1000));
        element.addEventListener('change', autoSave);
    });

    // Load saved data
    loadSavedData();

    // Set up form submissions with validation
    handleFormSubmit('personalForm', 'Save Information');
    handleFormSubmit('assessmentForm', 'Get Risk Assessment');

    // Initialize additional features
    initializeSmoothScrolling();
    initializeKeyboardNavigation();
    initializeTooltips();
    initializeAnimations();

    // Update progress on page load
    updateProgress();

    // Calculate BMI on page load
    calculateBMI();
});

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced print functionality
function printResults() {
    // Add print-specific styles
    const printStyles = document.createElement('style');
    printStyles.textContent = `
        @media print {
            .navbar, .footer, .btn, .flash-messages, .progress-bar {
                display: none !important;
            }
            body {
                background: white !important;
                font-size: 12pt;
            }
            .card, .form-container {
                box-shadow: none !important;
                border: 1px solid #ddd !important;
                break-inside: avoid;
            }
            h1, h2, h3 {
                page-break-after: avoid;
            }
        }
    `;
    document.head.appendChild(printStyles);

    window.print();

    // Remove print styles after printing
    setTimeout(() => document.head.removeChild(printStyles), 1000);
}

// Enhanced export functionality
function exportResults(format = 'pdf') {
    showAlert(`📄 Exporting as ${format.toUpperCase()}...`, 'info');

    // Simulate export process
    setTimeout(() => {
        showAlert(`✅ Results exported as ${format.toUpperCase()}!`, 'success');
    }, 2000);
}

// Modal functionality
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    @keyframes slideOutRight {
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
`;
document.head.appendChild(style);
        if (bmiCategory) {
            bmiCategory.textContent = '--';
        }
    }
}

// Initialize BMI calculator helpers
function initializeBMICalculator() {
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');

    if (heightInput && weightInput) {
        heightInput.addEventListener('input', calculateBMI);
        weightInput.addEventListener('input', calculateBMI);
    }

    calculateBMI();
}

function initializeProgressTracking() {
    updateProgress();
    document.querySelectorAll('input, select, textarea').forEach(element => {
        element.addEventListener('input', updateProgress);
        element.addEventListener('change', updateProgress);
    });
}

// Form progress tracking
function updateProgress() {
    const requiredFields = ['height', 'weight', 'smoking_status', 'exercise_frequency'];
    const optionalFields = ['blood_type', 'family_history', 'medical_conditions', 'medications', 'symptoms'];
    let filledRequired = 0;
    let filledOptional = 0;

    requiredFields.forEach(field => {
        const element = document.getElementById(field);
        if (element && element.value.trim()) filledRequired++;
    });

    optionalFields.forEach(field => {
        const element = document.getElementById(field);
        if (element && element.value.trim()) filledOptional++;
    });

    const totalFields = requiredFields.length + optionalFields.length;
    const filledFields = filledRequired + filledOptional;
    const progressPercent = (filledFields / totalFields) * 100;

    // Update progress bar if it exists
    const progressBar = document.querySelector('.progress-fill');
    if (progressBar) {
        progressBar.style.width = progressPercent + '%';
    }

    // Update progress text if it exists
    const progressText = document.getElementById('progressText');
    if (progressText) {
        progressText.textContent = `Required: ${filledRequired}/${requiredFields.length}, Optional: ${filledOptional}/${optionalFields.length}`;
    }
}

// Auto-save functionality
function autoSave() {
    const formData = {};
    document.querySelectorAll('input, select, textarea').forEach(element => {
        if (element.id && element.name) {
            formData[element.name] = element.value;
        }
    });

    // Save to localStorage as backup
    localStorage.setItem('assessmentFormData', JSON.stringify(formData));

    // Send to server for progress tracking
    fetch('/api/progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ formData: formData })
    })
    .then(response => response.json())
    .then(data => {
        // Update progress bar with server data
        const progressBar = document.querySelector('.progress-fill');
        if (progressBar && data.progress !== undefined) {
            progressBar.style.width = data.progress + '%';
        }
    })
    .catch(error => console.log('Progress update failed:', error));
}

// Load saved form data
function loadSavedData() {
    const savedData = localStorage.getItem('assessmentFormData');
    if (savedData) {
        const formData = JSON.parse(savedData);
        Object.keys(formData).forEach(key => {
            const element = document.querySelector(`[name="${key}"]`);
            if (element) {
                element.value = formData[key];
            }
        });
        calculateBMI();
        updateProgress();
    }
}

// Form submission with loading state
function handleFormSubmit(formId, submitButtonText = 'Submit') {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.textContent;
            submitBtn.textContent = '⏳ Processing...';
            submitBtn.disabled = true;

            // Re-enable after 2 seconds if not redirected
            setTimeout(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        }
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set up BMI calculation
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');

    if (heightInput && weightInput) {
        heightInput.addEventListener('input', calculateBMI);
        weightInput.addEventListener('input', calculateBMI);
    }

    // Set up progress tracking
    document.querySelectorAll('input, select, textarea').forEach(element => {
        element.addEventListener('input', updateProgress);
        element.addEventListener('change', updateProgress);
        element.addEventListener('input', autoSave);
        element.addEventListener('change', autoSave);
    });

    // Load saved data
    loadSavedData();

    // Set up form submissions
    handleFormSubmit('personalForm', 'Save Information');
    handleFormSubmit('assessmentForm', 'Get Risk Assessment');

    // Update progress on page load
    updateProgress();
});

// Utility functions
function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    // Add to page
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    // Remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Print functionality
function printResults() {
    window.print();
}

// Export functionality (placeholder)
function exportResults() {
    showAlert('Export functionality coming soon!', 'info');
}