<!-- App.svelte or Dashboard.svelte -->
<script>
	let isLoggedIn = false;

	function logIn() {
		alert('Redirecting to login page...');
		isLoggedIn = true;
	}

	function signUp() {
		alert('Redirecting to sign-up page...');
	}
</script>

<body>
	<header>
		<div class="header-content">
			<h1>FINSIGHT</h1>
			<div class="auth-links">
				<a href="/login">Login</a>
				<a href="/signup">Signup</a>
			</div>
		</div>
	</header>

	<nav>
		<a href="#home">
			<button class="nav-button active">Home</button>
		</a>

		<a href="#about">
			<button class="nav-button">About Us</button>
		</a>

		<a href="#contact">
			<button class="nav-button">Contact Us</button>
		</a>
	</nav>

	<section id="home" class="hero">
		<h1>Event Finance Management Software</h1>
		<p>Streamline your events and manage them with ease.</p>
		<button class="cta-button" on:click={logIn}>Log In To Greatness</button>
	</section>

	<section id="features" class="features">
		<div class="feature">
			<h3>Secure</h3>
			<p>Your data is encrypted using TLS protocols for maximum security.</p>
		</div>
		<div class="feature">
			<h3>Easy-to-use</h3>
			<p>Simplified onboarding and a comprehensive knowledge base.</p>
		</div>
		<div class="feature">
			<h3>All-in-one</h3>
			<p>Manage all event data seamlessly from one platform.</p>
		</div>
		<div class="feature">
			<h3>Customizable</h3>
			<p>Adapt Finsight to meet the needs of your business.</p>
		</div>
	</section>

	<section id="about" class="about">
		<h2>About Us</h2>
		<div class="about-content">
			<div>
				<p>
					Finsight is your go-to solution for efficient event financial management. With our
					platform, you can easily track expenses, monitor transactions, and visualize your
					financial data in real-time.
				</p>
				<p>
					Our goal is to make event management simpler, more secure, and highly effective for all
					users.
				</p>
			</div>
			<!-- svelte-ignore a11y-img-redundant-alt -->
			<img src="/about-us-image.jpg" alt="About Us Image" />
		</div>
	</section>

	<section id="contact" class="contact">
		<h2>Contact Us</h2>
		<p>Follow us on social media or reach out via email:</p>
		<a href="https://www.instagram.com" target="_blank" class="social-link">Instagram</a>
		<a href="https://www.facebook.com" target="_blank" class="social-link">Facebook</a>
		<a href="mailto:info@finsight.com" class="social-link">Gmail</a>
	</section>

	<footer class="footer">
		<p>&copy; 2024 Finsight. All Rights Reserved.</p>
	</footer>
</body>

<style>
	/* Header Styles */
	header {
		background-color: #48bb78;
		padding: 15px;
	}

	.header-content {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.header-content h1 {
		margin: 0;
		color: #fff;
	}

	/* Auth Links (Login & Signup) Styles */
	.auth-links {
		display: flex;
		gap: 15px;
	}

	.auth-links a {
		color: #fff;
		text-decoration: none;
		font-weight: bold;
		padding: 8px 15px;
		border-radius: 5px;
		transition: background-color 0.3s ease;
	}

	.auth-links a:hover {
		background-color: #2f855a;
	}

	/* Navigation Styles */
	nav {
		display: flex;
		justify-content: center;
		background-color: #22543d;
		padding: 10px;
	}

	.nav-button {
		background-color: #48bb78;
		padding: 10px 20px;
		border-radius: 20px;
		margin-right: 10px;
		cursor: pointer;
		border: none;
		color: white;
		transition: background-color 0.3s;
	}

	.nav-button:hover {
		background-color: #38a169;
	}

	.nav-button.active {
		background-color: #2f855a;
	}

	nav a:last-child .nav-button {
		margin-right: 0;
	}
	body {
		font-family: 'Helvetica Neue', sans-serif;
		background-color: #f0fff4;
		margin: 0;
		padding: 0;
		color: #2c3e50;
		scroll-behavior: smooth;
	}
	.hero {
		background: linear-gradient(to right, #48bb78, #22543d);
		background-size: cover;
		background-blend-mode: overlay;
		background-position: center;
		color: white;
		text-align: center;
		padding: 100px 20px;
		transition: all 0.5s;
		opacity: 0.9;
	}
	.hero h1 {
		font-size: 3em;
		margin-bottom: 10px;
		animation: slide-in 1s ease-out;
	}
	.hero p {
		font-size: 1.2em;
		margin-bottom: 20px;
		animation: fade-in 1s ease-in-out;
	}
	.cta-button {
		background-color: #38a169;
		color: white;
		padding: 12px 24px;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		font-size: 1.2em;
		transition: background-color 0.3s;
	}
	.cta-button:hover {
		background-color: #2f855a;
	}
	.features {
		display: flex;
		justify-content: space-around;
		padding: 60px 20px;
		background-color: #f0fff4;
		animation: fade-in 1s ease-out;
	}
	.feature {
		width: 22%;
		text-align: center;
		background-color: #fff;
		padding: 20px;
		border-radius: 10px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		transition: transform 0.3s ease-in-out;
	}
	.feature:hover {
		transform: translateY(-10px);
	}
	.about {
		padding: 100px 20px;
		text-align: center;
		background-color: #48bb78;
		color: white;
		border-radius: 10px;
		margin: 20px;
		animation: fade-in 1.5s ease-in;
	}
	.about-content {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 20px;
		margin-top: 30px;
	}
	.about-content img {
		width: 45%;
		border-radius: 10px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}
	.about-content div {
		width: 50%;
	}
	.contact {
		padding: 60px 20px;
		text-align: center;
		background-color: #48bb78;
		color: white;
		border-radius: 10px;
		margin: 20px;
		animation: fade-in 1.5s ease-in;
	}
	.social-link {
		color: #2c3e50;
		text-decoration: none;
		margin: 0 10px;
		background: #d2f5d2;
		padding: 8px 15px;
		border-radius: 5px;
		transition: background-color 0.3s;
	}
	.social-link:hover {
		background: #2c6e49;
		color: #fff;
	}
	.footer {
		background-color: #22543d;
		color: white;
		text-align: center;
		padding: 10px 20px;
		box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
	}
	@keyframes fade-in {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
	@keyframes slide-in {
		from {
			transform: translateY(-20px);
			opacity: 0;
		}
		to {
			transform: translateY(0);
			opacity: 1;
		}
	}
</style>
