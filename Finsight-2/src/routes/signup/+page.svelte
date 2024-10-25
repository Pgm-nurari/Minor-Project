<script>
	import { goto } from '$app/navigation';

	let username = '';
	let email = '';
	let department = '';
	let password = '';
	let role = '';

	let usernameError = '';
	let emailError = '';
	let departmentError = '';
	let passwordError = '';
	let roleError = '';

	function validateForm() {
		let valid = true;

		// Username validation
		if (username.trim().length < 3) {
			usernameError = 'Username must be at least 3 characters long.';
			valid = false;
		} else {
			usernameError = '';
		}

		// Email validation
		const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if (!emailPattern.test(email)) {
			emailError = 'Please enter a valid email address.';
			valid = false;
		} else {
			emailError = '';
		}

		// Department validation
		if (department.trim() === '') {
			departmentError = 'Department cannot be empty.';
			valid = false;
		} else {
			departmentError = '';
		}

		// Password validation
		const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
		if (!passwordPattern.test(password)) {
			passwordError = 'Password must be at least 8 characters long, contain uppercase, lowercase, a number, and a special character.';
			valid = false;
		} else {
			passwordError = '';
		}

		// Role validation
		if (role.trim() === '') {
			roleError = 'Role cannot be empty.';
			valid = false;
		} else {
			roleError = '';
		}

		return valid;
	}

	function handleSubmit(event) {
		event.preventDefault(); 

		if (validateForm()) {
			console.log({ username, email, department, password, role });
			goto('/login');
		}
	}
</script>

<body>
	<div class="container">
		<div class="inner-container">
			<div class="form-container">
				<h2>Sign Up</h2>
				<form on:submit={handleSubmit}>
					<label for="username">Username</label>
					<input type="text" id="username" bind:value={username} placeholder="Value" required />
					<span class="error">{usernameError}</span>

					<label for="email">Email</label>
					<input type="email" id="email" bind:value={email} placeholder="Value" required />
					<span class="error">{emailError}</span>

					<label for="department">Department</label>
					<input type="text" id="department" bind:value={department} placeholder="Value" required />
					<span class="error">{departmentError}</span>

					<label for="password">Password</label>
					<input type="password" id="password" bind:value={password} placeholder="Value" required />
					<span class="error">{passwordError}</span>

					<label for="role">Role</label>
					<input type="text" id="role" bind:value={role} placeholder="Value" required />
					<span class="error">{roleError}</span>

					<button type="submit">Sign Up</button>
				</form>
			</div>
			<div class="image-container">
				<img src="signupillustration.jpg" alt="Signup Illustration" />
			</div>
		</div>
	</div>
</body>

<style>
	* {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
		font-family: Arial, sans-serif;
	}

	body {
		background-color: #f0f0f0;
	}

	.container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
		background-color: #52b8b7;
		padding: 40px;
	}

	.inner-container {
		display: flex;
		background-color: white;
		border-radius: 12px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		max-width: 800px;
		width: 100%;
	}

	.form-container {
		padding: 20px;
		width: 400px;
	}

	.form-container h2 {
		font-size: 18px;
		color: #333;
		margin-bottom: 20px;
		text-align: center;
	}

	form {
		display: flex;
		flex-direction: column;
	}

	label {
		margin: 10px 0 5px;
		font-size: 14px;
	}

	input {
		padding: 8px;
		font-size: 14px;
		border-radius: 6px;
		border: 1px solid #ccc;
		margin-bottom: 15px;
	}

	.error {
		color: red;
		font-size: 12px;
		margin-bottom: 10px;
		display: block;
	}

	button {
		background-color: #000;
		color: white;
		padding: 10px;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-size: 16px;
	}

	button:hover {
		background-color: #555;
	}

	.image-container {
		display: flex;
		align-items: center;
		margin-left: 20px;
	}

	.image-container img {
		width: 250px;
	}
</style>
