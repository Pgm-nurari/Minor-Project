<!-- App.svelte or Dashboard.svelte -->

<script>
    import EventCard from './EventCard.svelte';

    // Sample event data that would typically come from Pocketbase
    let events = [
        {
            id: 1,
            eventName: "Annual Conference",
            status: "Upcoming",
            department: "Marketing",
            date: "10/20/2024",
            type: "Conference"
        },
        {
            id: 2,
            eventName: "Workshop on AI",
            status: "Completed",
            department: "Tech",
            date: "09/15/2024",
            type: "Workshop"
        },
        {
            id: 3,
            eventName: "Fundraiser Gala",
            status: "Ongoing",
            department: "Charity",
            date: "10/30/2024",
            type: "Gala"
        },
        {
            id: 4,
            eventName: "Sports Day",
            status: "Upcoming",
            department: "Sports",
            date: "11/05/2024",
            type: "Sports Event"
        }
    ];

	import Modal from './modal.svelte';
    import EventForm from './eventform.svelte';

    let showModal = false;

    const openModal = () => showModal = true;
    const closeModal = () => showModal = false;

	import UserAuthCard from './UserAuthCard.svelte';

    const userData = {
        userName: 'User 1',
        department: 'CS',
        role: 'Finance Manager',
        email: 'finman001@mail.com',
        password: '********',
        event: 'Biz Blitz',
        subEvents: ['E-Football', 'Market Mania'],
        phone: '67565*****',
    };

    const handleAuthorize = () => {
        // Authorization logic here
        console.log('User authorized:', userData.userName);
    };
</script>

<style>
    .cardscontainer {
        width: 100%;
        max-width: 1512px;
        height: 751px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-gap: 16px;
        padding: 16px;
        overflow-x: auto;
    }

    @media (max-width: 1200px) {
        .cardscontainer {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    @media (max-width: 900px) {
        .cardscontainer {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 600px) {
        .cardscontainer {
            grid-template-columns: 1fr;
        }
    }
</style>

<div class="cardscontainer">
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

<button on:click={openModal}>Create Event</button>

<Modal openModal={showModal} onClose={closeModal}>
    <EventForm />
</Modal>

<UserAuthCard 
    userName={userData.userName}
    department={userData.department}
    role={userData.role}
    email={userData.email}
    password={userData.password}
    event={userData.event}
    subEvents={userData.subEvents}
    phone={userData.phone}
    onAuthorize={handleAuthorize}
/>
