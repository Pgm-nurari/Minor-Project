// JavaScript functions for navigation and validation
function navigateToResetPassword(event) {
    event.preventDefault();

    const email = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    let valid = true;

    // Validate email input
    if (email.value === '') {
        emailError.innerText = 'Email is required.';
        valid = false;
    } else if (!emailPattern.test(email.value)) {
        emailError.innerText = 'Please enter a valid email address.';
        valid = false;
    } else {
        emailError.innerText = '';
    }

    if (valid) {
        alert('Email validation successful!');
        // Redirect to reset password page
        window.location.href = "{{url_for('home.reset_password')}}";
    }
}

function navigateToHome() {
    // Redirect to home page
    window.location.href = "{{url_for('home.index')}}";
}