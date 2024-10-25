<script>
    import { goto } from '$app/navigation';

    function navigateToResetPassword(event) {
        event.preventDefault();

        const email = document.getElementById('email');
        const emailError = document.getElementById('emailError');
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        let valid = true;

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
            goto('/reset_password');
        }
    }

    function navigateToHome() {
        goto('/');
    }
</script>

<div class="container">
    <div class="inner-container">
        <div class="illustration-container">
            <img src="/forgotillustration.jpg" alt="Reset Password Illustration" class="illustration" />
        </div>

        <div class="form-container">
            <h2 class="form-heading">RESET YOUR PASSWORD HERE</h2>

            <form id="resetPasswordForm" method="POST">
                <div>
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="Value" required />
                    <span id="emailError" class="error-message"></span>
                </div>

                <div class="button-container">
                    <button type="button" on:click={navigateToHome}>Cancel</button>
                    <button type="submit" on:click={navigateToResetPassword}>Reset Password</button>
                </div>
            </form>
        </div>
    </div>
</div>

<style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #52B8B7;
        padding: 40px;
        margin: 0 25%;
    }

    .inner-container {
        background-color: #ffffff;
        border-radius: 12px;
        max-width: 500px;
        width: 100%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }

    .illustration-container {
        text-align: center;
        margin-bottom: 20px;
    }

    .illustration {
        width: auto;
        max-width: 350px;
        height: auto;
    }

    .form-container {
        text-align: center;
    }

    .form-heading {
        font-size: 16px;
        color: #333333;
        margin-bottom: 20px;
    }

    label {
        display: block;
        font-size: 14px;
        color: #555;
        margin-bottom: 5px;
    }

    input {
        width: 70%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 14px;
        margin-bottom: 5px;
    }

    button {
        background-color: #000000;
        color: #ffffff;
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
    }

    .button-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .error-message {
        color: red; 
        font-size: 12px; 
        margin-top: 5px;
    }
</style>
