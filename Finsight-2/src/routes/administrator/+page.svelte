<!-- src/routes/admin.svelte -->
<script>
	// Importing components from the lib folder
	import EventCard from '$lib/eventcard.svelte';
	import Modal from '$lib/modal.svelte'; // For modals for new event/user forms
	import Userauthcard from '$lib/userauthcard.svelte';
	import EventForm from '$lib/eventform.svelte';
    import UserReqForm from '$lib/userreqform.svelte';
	import DynamicTable from '$lib/dynamictable.svelte';

	let showNewEventModal = false; // To track if new event modal is open
	let showNewUserModal = false; // To track if new user modal is open

	// Example user data for UserAuthCards
	const users = [
		{
			userName: 'John Doe',
			department: 'Finance',
			role: 'Admin',
			email: 'john@example.com',
			password: 'secret123',
			event: 'Annual Report',
			phone: '123-456-7890',
			subEvents: ['Budget Review', 'Forecasting'] // Example sub events
		},
		{
			userName: 'Jane Smith',
			department: 'HR',
			role: 'Manager',
			email: 'jane@example.com',
			password: 'password456',
			event: 'Employee Training',
			phone: '987-654-3210',
			subEvents: ['Training Session 1', 'Training Session 2'] // Example sub events
		},
		{
			userName: 'Bob Brown',
			department: 'IT',
			role: 'Engineer',
			email: 'bob@example.com',
			password: 'tech789',
			event: 'System Upgrade',
			phone: '555-444-3333',
			subEvents: ['Initial Setup', 'Testing Phase'] // Example sub events
		}
	];

	// Example event data for EventCards
	const events = [
		{
			eventName: 'Annual Budget Review',
			status: 'Ongoing',
			department: 'Finance',
			date: '2024-11-15',
			type: 'Meeting'
		},
		{
			eventName: 'Team Building Workshop',
			status: 'Completed',
			department: 'HR',
			date: '2024-09-20',
			type: 'Workshop'
		},
		{
			eventName: 'Product Launch',
			status: 'Upcoming',
			department: 'Marketing',
			date: '2024-12-01',
			type: 'Event'
		},
		{
			eventName: 'Security Audit',
			status: 'Ongoing',
			department: 'IT',
			date: '2024-10-22',
			type: 'Audit'
		}
	];

	// Dummy dataset for Users Table
	const users_table = [
		{
			username: 'John Doe',
			department: 'Finance',
			role: 'Finance Manager',
			email: 'john.doe@finance.com',
			event: 'Annual Report',
			phone: '123-456-7890'
		},
		{
			username: 'Jane Smith',
			department: 'Event Planning',
			role: 'Event Manager',
			email: 'jane.smith@events.com',
			event: 'Team Building Workshop',
			phone: '987-654-3210'
		},
		{
			username: 'Bob Brown',
			department: 'Finance',
			role: 'Finance Manager',
			email: 'bob.brown@finance.com',
			event: 'Budget Planning',
			phone: '555-444-3333'
		}
	];

	const openNewEventModal = () => {
		showNewEventModal = true;
		document.addEventListener('keydown', handleModalKeydown);
	};

	const openNewUserModal = () => {
		showNewUserModal = true;
		document.addEventListener('keydown', handleModalKeydown);
	};

	const closeModal = () => {
		showNewEventModal = false;
		showNewUserModal = false;
		document.removeEventListener('keydown', handleModalKeydown);
	};

	// @ts-ignore
	const handleModalKeydown = (event) => {
		if (event.key === 'Escape') {
			closeModal();
		}
	};

	// Define the viewAllEvents function
	function viewAllEvents() {
		alert('Redirecting to the all events page.');
	}
</script>

<header class="header">
	<div class="header-content">
		<h1>FINSIGHT</h1>
		<div class="auth-links">
			<button
				on:click={openNewEventModal}
				on:keydown={(event) => {
					if (event.key === 'Enter' || event.key === ' ') {
						// Handle both 'Enter' and 'Space' for accessibility
						openNewEventModal();
					}
				}}
                class="nav-button"
			>
				Create Event
			</button>
			<button class="nav-button" on:click={openNewUserModal}>New User</button>
			<a href="/" class="nav-button">
                <button class="nav-button">Logout</button>
            </a>
		</div>
	</div>
</header>

<nav>
	<a href="#dashboard">
		<button class="nav-button active">Dashboard</button>
	</a>
	<a href="#events">
		<button class="nav-button">Events</button>
	</a>
	<a href="#users">
		<button class="nav-button">Users</button>
	</a>
</nav>

<main>
	<Modal openModal={showNewEventModal} onClose={closeModal}>
		<EventForm />
	</Modal>

	<section id="dashboard">
        <h2>Dashboard</h2>
        <p>Welcome to the <strong>Administrator Dashboard!</strong> Manage your events and transactions seamlessly.</p>
    </section>

	<!-- Users Section -->
	<section id="users">
		<h2>Users Authentication</h2>
		<div class="user-list">
			{#each users as user}
				<Userauthcard
					userName={user.userName}
					department={user.department}
					role={user.role}
					email={user.email}
					password={user.password}
					event={user.event}
					phone={user.phone}
					subEvents={user.subEvents}
					onAuthorize={() => console.log(`${user.userName} authorized!`)}
				/>
			{/each}
		</div>
	</section>

	<!-- Pre-existing Events Section -->
	<section class="events-section" id="events">
		<div class="section-header">
			<h2>Events</h2>
			<div class="view-all">
				<button class="view-all-button" on:click={viewAllEvents}>View All Events</button>
			</div>
		</div>
		<div class="events-container">
			{#each events as event}
				<EventCard
					eventName={event.eventName}
					status={event.status}
					department={event.department}
					date={event.date}
					type={event.type}
				/>
			{/each}
		</div>
	</section>

	<!-- Users Table Section -->
	<section id="users">
		<h2>Users Table</h2>
		<DynamicTable data={users_table} /> <!-- Dynamic Table Component with Users Data -->
	</section>
</main>

{#if showNewEventModal}
	<Modal openModal={showNewEventModal} onClose={closeModal}>
		<EventForm />
	</Modal>
{/if}

<!-- New User Modal -->
{#if showNewUserModal}
	<Modal openModal={showNewUserModal} onClose={closeModal}>
		<UserReqForm /> <!-- Replace placeholder with the user request form component -->
	</Modal>
{/if}

<style>
	/* Styling for the main admin page */
	main {
		padding: 20px;
	}

	section {
		margin-bottom: 40px;
	}

	h2 {
		color: #22543d;
		margin-bottom: 10px;
	}

	.user-list {
		display: flex;
		flex-wrap: wrap;
		justify-content: start; /* Align to the start */
		gap: 20px; /* Space between cards */
		max-width: 100%; /* Prevent overflow */
		overflow-x: auto; /* Enable horizontal scrolling */
	}

	.header {
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

	.auth-links {
		display: flex;
		gap: 15px;
	}

	nav {
		display: flex;
		justify-content: center; /* Center the navigation items */
		background-color: #22543d; /* Background color */
		padding: 10px; /* Padding around the nav */
		border-radius: 5px; /* Rounded corners */
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2); /* Shadow for depth */
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

	.events-section {
		margin: 30px 0;
	}

	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 10px;
	}

	.view-all {
		display: flex;
		align-items: center;
	}

	.view-all-button {
		padding: 5px 10px;
		background-color: #48bb78;
		color: white;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	.view-all-button:hover {
		background-color: #38a169;
	}

	.events-container {
		display: flex;
		flex-wrap: wrap;
		justify-content: start; /* Align to the start */
		gap: 20px; /* Space between cards */
		max-width: 100%; /* Prevent overflow */
		overflow-x: auto; /* Enable horizontal scrolling */
	}
	section#users {
		margin-top: 50px;
	}
</style>
