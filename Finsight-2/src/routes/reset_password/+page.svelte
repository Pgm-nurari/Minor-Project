<script>
    import { goto } from '$app/navigation';

    function navigateToHome() {
        goto('/');
    }

    function validateForm(event) {
        let valid = true;

        const newPassword = document.getElementById('new-password');
        const newPasswordError = document.getElementById('newPasswordError');
        const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;

        if (newPassword.value === '') {
            newPasswordError.innerText = 'New password is required.';
            valid = false;
        } else if (!passwordPattern.test(newPassword.value)) {
            newPasswordError.innerText = 'Password must be at least 8 characters and include an uppercase letter, a lowercase letter, a number, and a special character.';
            valid = false;
        } else {
            newPasswordError.innerText = '';
        }

        const confirmPassword = document.getElementById('confirm-password');
        const confirmPasswordError = document.getElementById('confirmPasswordError');

        if (confirmPassword.value === '') {
            confirmPasswordError.innerText = 'Please confirm your password.';
            valid = false;
        } else if (confirmPassword.value !== newPassword.value) {
            confirmPasswordError.innerText = 'Passwords do not match.';
            valid = false;
        } else {
            confirmPasswordError.innerText = '';
        }

        if (!valid) {
            event.preventDefault();
        } else {
            navigateToHome();
        }
    }
</script>

<div class="container">
    <div class="login-wrapper">
        <h2 class="login-heading">RESET YOUR PASSWORD HERE</h2>

        <div class="illustration-container">
            <img src="/resetpasswordillustration.jpg" alt="Reset Password Illustration" class="illustration" />
        </div>

        <form class="login-form" on:submit|preventDefault={validateForm} action="#" method="POST">
            <div>
                <label for="new-password" class="label">New Password</label>
                <input type="password" id="new-password" name="new-password" placeholder="Value" required />
                <span id="newPasswordError" class="error-message"></span>
            </div>

            <div>
                <label for="confirm-password" class="label">Confirm Password</label>
                <input type="password" id="confirm-password" name="confirm-password" placeholder="Value" required />
                <span id="confirmPasswordError" class="error-message"></span>
            </div>

            <div>
                <button type="button" class="reset-button" on:click={navigateToHome}>Cancel</button>
                <button type="submit" class="reset-button">Reset Password</button>
            </div>
        </form>
    </div>
</div>

<style>
    .container {
        margin: 0 25%;
        padding: 0;
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #52B8B7;
    }

    .login-wrapper {
        text-align: center;
        background-color: #ffffff;
        padding: 40px 50px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .login-heading {
        margin-bottom: 20px;
        color: #2d6832;
    }

    .login-form {
        width: 300px;
        margin: 0 auto;
    }

    .label {
        display: block;
        font-size: 14px;
        color: #555;
        margin-bottom: 5px;
    }

    input {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .reset-button {
        background-color: #FF6B6B;
        color: #FFFFFF;
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        margin-right: 10px;
    }

    .illustration {
        width: auto;
        max-width: 300px;
        height: auto;
    }

    .error-message {
        color: red;
        font-size: 12px;
        margin-top: 5px;
        display: block;
    }
</style>
