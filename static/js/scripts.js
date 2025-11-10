// Custom JavaScript for Flask app
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask app loaded successfully!');
    
    // Add click animation to buttons
    const buttons = document.querySelectorAll('.btn-custom');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 300);
        });
    });
    
    // Show welcome message
    const userName = document.querySelector('.user-name');
    if (userName) {
        setTimeout(() => {
            alert(`Welcome, ${userName.textContent}!`);
        }, 1000);
    }
});