
    const passwordInput = document.getElementById('password1');
    const confirmPasswordInput = document.getElementById('password2');
    confirmPasswordInput.disabled = true;
    passwordInput.addEventListener('input', updatePasswordStrength);
    confirmPasswordInput.addEventListener('mouseover', displayHoverMessage);
    confirmPasswordInput.addEventListener('mouseout', clearHoverMessage);
  
    function updatePasswordStrength() {
        const password = passwordInput.value;
        const strength = zxcvbn(password).score; // Using zxcvbn to calculate password strength
        const strengthMeter = document.getElementById('password-strength-meter');
        const strengthText = document.getElementById('password-strength-text');
  
        // Update the strength meter and text based on the password strength
        strengthMeter.value = strength;
        strengthText.textContent = ['Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong'][strength];

        // Disable/enable confirm password field based on password strength
        
        if (strength < 3) {
            confirmPasswordInput.disabled = true;
            confirmPasswordInput.title = "Password must be either strong or very strong";
        } else {
            confirmPasswordInput.disabled = false;
            confirmPasswordInput.title = "";
        }
    }

    function displayHoverMessage() {
        if (confirmPasswordInput.disabled) {
            confirmPasswordInput.title = "Password must be either strong or very strong";
        }
    }

    function clearHoverMessage() {
        confirmPasswordInput.title = "";
    }
