<script>
    import { onMount } from "svelte";

    let eventDetails = {
        eventName: '',
        eventType: '',
        eventDuration: '',
        eventDate: '',
        FinMan: '',
        EveMan: '',
        department: '',
        subEventYesNo: 'No',
        subEvents: []
    };
    let subEventCount = 0;
    let subEvents = [];

    function addSubEvents() {
        subEvents = Array.from({ length: subEventCount }, (_, i) => ({
            name: "",
            type: "",
            duration: "",
            date: "",
            FinMan: "",
            manager: ""
        }));
    }

    function submitForm() {
        console.log(eventDetails);
        alert("Event Created Successfully!");
        eventDetails = { eventName: '', eventType: '', eventDuration: '', eventDate: '', FinMan: '', EveMan: '', department: '', subEventYesNo: 'No', subEvents: [] };
        subEvents = [];
        subEventCount = 0;
    }
</script>

<style>
    .container {
        max-width: 600px;
        margin: auto;
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    h2 {
        text-align: center;
        color: #6cba5e;
        margin-bottom: 20px;
    }
    .form-group {
        margin-bottom: 15px;
    }
    .form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .form-group input,
    .form-group select {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    button[type="submit"],
    button[type="button"] {
        width: 100%;
        padding: 10px;
        background-color: #6cba5e;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
    }
    button[type="submit"]:hover,
    button[type="button"]:hover {
        background-color: #5aa850;
    }
    .sub-event-form {
        background-color: #f9f9f9;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .sub-event-form h4 {
        margin-bottom: 10px;
        color: #6cba5e;
    }
</style>

<div class="container">
    <h2>Event Creation</h2>
    <form on:submit|preventDefault={submitForm}>
        <!-- Event Details -->
        <div class="form-group">
            <label for="eventName">Event Name</label>
            <input type="text" id="eventName" bind:value={eventDetails.eventName} placeholder="Enter Event Name" required />
        </div>

        <div class="form-group">
            <label for="eventType">Event Type</label>
            <select id="eventType" bind:value={eventDetails.eventType}>
                <option value="training seminars">Training Seminars</option>
                <option value="workshops">Workshops</option>
                <option value="techfest">Tech-Fest</option>
                <option value="charity">Charity & Causes</option>
                <option value="infoseminar">Informative Seminar</option>
                <option value="busmeetup">Business Meetup</option>
                <option value="competitions">Competitions</option>
            </select>
        </div>

        <div class="form-group">
            <label for="eventDuration">Event Duration (Days/Weeks/Months)</label>
            <input type="text" id="eventDuration" bind:value={eventDetails.eventDuration} placeholder="Enter Duration" required />
        </div>

        <div class="form-group">
            <label for="eventDate">Event Date</label>
            <input type="date" id="eventDate" bind:value={eventDetails.eventDate} required />
        </div>

        <div class="form-group">
            <label for="FinMan">Finance Manager</label>
            <input type="text" id="FinMan" bind:value={eventDetails.FinMan} placeholder="Enter Finance Manager" required />
        </div>

        <div class="form-group">
            <label for="EveMan">Event Manager</label>
            <input type="text" id="EveMan" bind:value={eventDetails.EveMan} placeholder="Enter Event Manager" required />
        </div>

        <div class="form-group">
            <label for="department">Department</label>
            <select id="department" bind:value={eventDetails.department}>
                <option value="CS">Computer Science</option>
                <option value="Science">Science</option>
                <option value="Maths">Maths</option>
                <option value="VM">Visual Media</option>
                <option value="Commerce">Commerce</option>
            </select>
        </div>

        <!-- Sub-Events -->
        <div class="form-group">
            <label>Sub-Events?</label>
            <div>
                <input type="radio" id="subEventYes" name="subEventYesNo" bind:group={eventDetails.subEventYesNo} value="Yes" />
                <label for="subEventYes">Yes</label>
                <input type="radio" id="subEventNo" name="subEventYesNo" bind:group={eventDetails.subEventYesNo} value="No" />
                <label for="subEventNo">No</label>
            </div>
        </div>

        {#if eventDetails.subEventYesNo === 'Yes'}
            <div class="form-group">
                <label for="subEventCount">Number of Sub-Events</label>
                <input type="number" id="subEventCount" bind:value={subEventCount} min="1" />
                <button type="button" on:click={addSubEvents} style="margin-top: 10px;">Add Sub-Events</button>
            </div>

            <!-- Sub-Event Forms -->
            {#each subEvents as subEvent, i}
                <div class="sub-event-form">
                    <h4>Sub-Event {i + 1}</h4>
                    <div class="form-group">
                        <label for="subEventName{i}">Sub-Event Name</label>
                        <input type="text" id="subEventName{i}" bind:value={subEvent.name} placeholder="Enter Sub-Event Name" required />
                    </div>
                    <div class="form-group">
                        <label for="subEventType{i}">Sub-Event Type</label>
                        <select id="subEventType{i}" bind:value={subEvent.type}>
                            <option value="training seminars">Training Seminars</option>
                            <option value="workshops">Workshops</option>
                            <option value="techfest">Tech-Fest</option>
                            <option value="charity">Charity & Causes</option>
                            <option value="infoseminar">Informative Seminar</option>
                            <option value="busmeetup">Business Meetup</option>
                            <option value="competitions">Competitions</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="subEventDuration{i}">Duration</label>
                        <input type="text" id="subEventDuration{i}" bind:value={subEvent.duration} placeholder="Days/Weeks/Months" required />
                    </div>
                    <div class="form-group">
                        <label for="subEventDate{i}">Sub-Event Date</label>
                        <input type="date" id="subEventDate{i}" bind:value={subEvent.date} required />
                    </div>
                    <div class="form-group">
                        <label for="subEventFinMan{i}">Sub-Event Finance Manager</label>
                        <input type="text" id="subEventFinMan{i}" bind:value={subEvent.FinMan} placeholder="Enter Sub-Event Finance Manager" required />
                    </div>
                    <div class="form-group">
                        <label for="subEventManager{i}">Sub-Event Manager</label>
                        <input type="text" id="subEventManager{i}" bind:value={subEvent.manager} placeholder="Enter Sub-Event Manager" required />
                    </div>
                </div>
            {/each}
        {/if}

        <button type="submit">Add Event</button>
    </form>
</div>
