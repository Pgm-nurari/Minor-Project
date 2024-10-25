<!-- src/routes/finance-manager.svelte -->
<script>
    import EventCard from '$lib/eventcard.svelte';
    import DynamicTable from '$lib/dynamictable.svelte';
    import Modal from '$lib/modal.svelte'; // Import modals if needed

    // Dummy event data
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
        }
    ];

    // Dummy transaction data
    const transactions = [
        {
            billNo: '001',
            date: '2024-10-01',
            amount: 15000,
            eventManager: 'John Doe',
            transactionNature: 'Expense',
            transactionMode: 'Cash',
            transactionCategory: 'Rent',
            partyName: 'Office Building'
        },
        {
            billNo: '002',
            date: '2024-10-05',
            amount: 3000,
            eventManager: 'Jane Smith',
            transactionNature: 'Expense',
            transactionMode: 'UPI',
            transactionCategory: 'Food',
            partyName: 'Catering Services'
        },
        {
            billNo: '003',
            date: '2024-10-10',
            amount: 5000,
            eventManager: 'Bob Brown',
            transactionNature: 'Revenue',
            transactionMode: 'Bank',
            transactionCategory: 'Stationary',
            partyName: 'Stationery Store'
        }
    ];
    function viewAllEvents() {
		alert('Redirecting to the all events page.');
	}
</script>

<header class="header">
	<div class="header-content">
		<h1>FINSIGHT</h1>
		<div class="auth-links">
			<a href="/" class="nav-button">
                <button class="nav-button">Logout</button>
            </a>
		</div>
	</div>
</header>

<nav >
    <a href="#dashboard"><button class="nav-button active">Dashboard</button></a>
    <a href="#events"><button class="nav-button">Events</button></a>
    <a href="#transactions"><button class="nav-button">Transactions</button></a>
    <a href="#statistics"><button class="nav-button">Statistics</button></a>
    <a href="#reports"><button class="nav-button">Reports</button></a>
</nav>

<main>
    <section id="dashboard">
        <h2>Dashboard</h2>
        <p>Welcome to the <strong>Finance Manager Dashboard!</strong> Manage your finances and events efficiently.</p>
    </section>

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

    <section id="transactions">
        <h2>Transactions</h2>
        <DynamicTable data={transactions} />
    </section>

    <section id="statistics">
        <h2>Statistics</h2>
        <p>Statistics content goes here.</p>
    </section>

    <section id="reports">
        <h2>Reports</h2>
        <p>Reports content goes here.</p>
    </section>
</main>

<style>
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
    /* Add your styles here */
    main {
        padding: 20px;
    }
    .events-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: start;
        gap: 20px;
        max-width: 100%;
        overflow-x: auto;
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
</style>
