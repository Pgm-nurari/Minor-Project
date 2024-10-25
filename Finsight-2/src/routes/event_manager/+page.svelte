<!-- src/routes/event-manager.svelte -->
<script>
    // Importing components from the lib folder
    import EventCard from '$lib/eventcard.svelte';
    import Modal from '$lib/modal.svelte'; // For modals for new transaction form
    import TransactionForm from '$lib/transactionsform.svelte'; // Transaction form component
    import DynamicTable from '$lib/dynamictable.svelte';

    let showNewTransactionModal = false; // To track if new transaction modal is open

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

    // Example transaction data (for demonstration)
    const transactions = [
        {
            BillNumber: 'INV001',
            Date: '2024-10-10',
            Amount: '$500',
            TransactionNature: 'Income',
            TransactionMode: 'Credit Card',
            TransactionCategory: 'Sales',
            PartyName: 'ABC Corp.'
        },
        {
            BillNumber: 'INV002',
            Date: '2024-10-11',
            Amount: '$250',
            TransactionNature: 'Expense',
            TransactionMode: 'Bank Transfer',
            TransactionCategory: 'Office Supplies',
            PartyName: 'XYZ Ltd.'
        },
        {
            BillNumber: 'INV003',
            Date: '2024-10-12',
            Amount: '$1500',
            TransactionNature: 'Income',
            TransactionMode: 'Cash',
            TransactionCategory: 'Consulting',
            PartyName: 'DEF Inc.'
        },
        {
            BillNumber: 'INV004',
            Date: '2024-10-13',
            Amount: '$400',
            TransactionNature: 'Expense',
            TransactionMode: 'Cheque',
            TransactionCategory: 'Marketing',
            PartyName: 'Marketing Solutions'
        }
    ];

    const openNewTransactionModal = () => {
        showNewTransactionModal = true;
        document.addEventListener('keydown', handleModalKeydown);
    };

    const closeModal = () => {
        showNewTransactionModal = false;
        document.removeEventListener('keydown', handleModalKeydown);
    };

    // @ts-ignore
    const handleModalKeydown = (event) => {
        if (event.key === 'Escape') {
            closeModal();
        }
    };

    // Define the viewAllTransactions function
    function viewAllTransactions() {
        alert('Redirecting to the all transactions page.');
    }
    function viewAllEvents() {
		alert('Redirecting to the all events page.');
	}
</script>

<header class="header">
    <div class="header-content">
        <h1>FINSIGHT</h1>
        <div class="auth-links">
           <button class="nav-button" on:click={openNewTransactionModal}>New Transaction</button>
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
    <a href="#transactions">
        <button class="nav-button">Transactions</button>
    </a>
</nav>

<main>
    <!-- Modal for New Transaction -->
    {#if showNewTransactionModal}
        <Modal openModal={showNewTransactionModal} onClose={closeModal}>
            <TransactionForm />
        </Modal>
    {/if}

    <!-- Dashboard Section -->
    <section id="dashboard">
        <h2>Dashboard</h2>
        <p>Welcome to the <strong>Event Manager Dashboard!</strong> Manage your events and transactions seamlessly.</p>
    </section>

    <!-- Events Section -->
    <section class="events-section" id="events">
		<div class="section-header">
			<h2>Pre-existing Events</h2>
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

    <!-- Transactions Section -->
    <section id="transactions">
        <h2>Transactions</h2>
        <!-- Dynamic Table Component with sample transaction data -->
        <DynamicTable data={transactions} />
    </section>
</main>

<style>
    /* Styling for the main event-manager dashboard */
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

    .view-all-button {
        padding: 10px 15px;
        background-color: #48bb78;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .view-all-button:hover {
        background-color: #38a169;
    }.events-section {
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
</style>
