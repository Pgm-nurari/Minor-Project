<script>
    document.addEventListener('DOMContentLoaded', function () {
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const form = document.querySelector('form');

        const emailError = document.getElementById('emailError');
        const passwordError = document.getElementById('passwordError');

        function validateEmail(email) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailPattern.test(email);
        }

        function validatePassword(password) {
            const lengthCriteria = password.length >= 8;
            const uppercaseCriteria = /[A-Z]/.test(password);
            const lowercaseCriteria = /[a-z]/.test(password);
            const numberCriteria = /\d/.test(password);
            const specialCharCriteria = /[!@#$%^&*(),.?":{}|<>]/.test(password);

            return lengthCriteria && uppercaseCriteria && lowercaseCriteria && numberCriteria && specialCharCriteria;
        }

        emailInput.addEventListener('input', function () {
            if (!validateEmail(emailInput.value)) {
                emailError.textContent = 'Please enter a valid email address.';
            } else {
                emailError.textContent = '';
            }
        });

        passwordInput.addEventListener('input', function () {
            if (!validatePassword(passwordInput.value)) {
                passwordError.textContent = 'Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.';
            } else {
                passwordError.textContent = '';
            }
        });

        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent default form submission

            const isEmailValid = validateEmail(emailInput.value);
            const isPasswordValid = validatePassword(passwordInput.value);

            if (!isEmailValid) {
                emailError.textContent = 'Please enter a valid email address.';
            }

            if (!isPasswordValid) {
                passwordError.textContent = 'Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.';
            }

            if (isEmailValid && isPasswordValid) {
                // Simulate form submission or make an API call
                console.log('Form submitted');
                alert('Form submitted successfully!');

                // Here, you can make a fetch request or redirect the user
                // fetch('/api/submit', { method: 'POST', body: new FormData(form) })
            }
        });
    });
</script>

<div class="container">
    <div class="login-wrapper">
        <h2 class="login-heading">Login</h2>
        <div style="margin-bottom: 20px;">
            <img src="/loginillsutration.jpg" alt="Login Illustration" style="max-width: 400px; width: 100%;" />
        </div>

        <div class="login-form">
            <form action="#" method="POST">
                <div>
                    <label for="email" style="display: block; font-size: 14px; color: #555; margin-bottom: 5px;">Email</label>
                    <input type="email" id="email" name="email" placeholder="Value" required />
                    <span id="emailError" class="error"></span>
                </div>

                <div>
                    <label for="password" style="display: block; font-size: 14px; color: #555; margin-bottom: 5px;">Password</label>
                    <input type="password" id="password" name="password" placeholder="Value" required />
                    <span id="passwordError" class="error"></span>
                </div>

                <div>
                    <button type="submit">Log In</button>
                </div>

                <div>
                    <a href="/forgot_password" class="forgot-password">Forgot password?</a>
                </div>
            </form>
        </div>
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

    input {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 14px;
        margin-bottom: 15px;
    }

    .error {
        color: red;
        font-size: 12px;
        margin-top: -10px;
        margin-bottom: 15px;
        display: block;
    }

    button {
        width: 100%;
        background-color: #ff6b6b;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
    }

    .forgot-password {
        color: #757575;
        font-size: 14px;
        text-decoration: none;
    }
</style>
