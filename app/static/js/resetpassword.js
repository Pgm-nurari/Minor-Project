function navigateToHome() {
    window.location.href = "{{url_for('home.index')}}"; // Adjust with your actual home URL if needed
  }

  function validateForm(event) {
    let valid = true;

    const newPassword = document.getElementById("new-password");
    const newPasswordError = document.getElementById("newPasswordError");
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;

    if (newPassword.value === "") {
      newPasswordError.innerText = "New password is required.";
      valid = false;
    } else if (!passwordPattern.test(newPassword.value)) {
      newPasswordError.innerText =
        "Password must be at least 8 characters and include an uppercase letter, a lowercase letter, a number, and a special character.";
      valid = false;
    } else {
      newPasswordError.innerText = "";
    }

    const confirmPassword = document.getElementById("confirm-password");
    const confirmPasswordError = document.getElementById("confirmPasswordError");

    if (confirmPassword.value === "") {
      confirmPasswordError.innerText = "Please confirm your password.";
      valid = false;
    } else if (confirmPassword.value !== newPassword.value) {
      confirmPasswordError.innerText = "Passwords do not match.";
      valid = false;
    } else {
      confirmPasswordError.innerText = "";
    }

    if (valid) {
      event.preventDefault();
      alert("Password has been successfully reset!");
      navigateToHome();
    } else {
      event.preventDefault();
    }
  }