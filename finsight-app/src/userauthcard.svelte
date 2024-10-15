<!-- src/UserAuthCard.svelte -->

<script>
    export let userName;
    export let department;
    export let role;
    export let email;
    export let password;
    export let event;
    export let subEvents = [];
    export let phone;
    export let onAuthorize;

    let isAuthorized = false; // Boolean to track authorization state

    const togglePassword = (id) => {
        const passwordInput = document.getElementById(id);
        passwordInput.type =
            passwordInput.type === "password" ? "text" : "password";
    };

    const handleAuthorize = () => {
        isAuthorized = true; // Set authorized state to true
        if (onAuthorize) onAuthorize(); // Call the passed authorization function
    };
</script>

<div class="request-card">
    <div class="field-container">
        <b>User Name:</b> <span>{userName}</span>
    </div>
    <div class="field-container">
        <b>Department:</b> <span>{department}</span>
    </div>
    <div class="field-container">
        <b>Role:</b> <span>{role}</span>
    </div>
    <div class="field-container">
        <b>Email:</b> <span>{email}</span>
    </div>
    <div class="field-container password-container">
        <b>Password:</b>
        <input
            type="password"
            value={password}
            class="password-input"
            id="password"
            readonly
        />
        <button class="eye-button" on:click={() => togglePassword("password")}
            >&#128065;</button
        >
    </div>
    <div class="field-container">
        <b>Event:</b> <span>{event}</span>
    </div>
    {#if subEvents.length > 0}
        <div class="field-container">
            <b>Sub Events:</b> <span>{subEvents.join(", ")}</span>
        </div>
    {/if}
    <div class="field-container">
        <b>Phone:</b> <span>{phone}</span>
    </div>

    {#if isAuthorized}
        <div class="field-container authorized">Authorized</div>
    {:else}
        <button class="authorize-btn" on:click={handleAuthorize}
            >Authorize</button
        >
    {/if}
</div>

<style>
    .request-card {
        width: 300px; /* Fixed width */
        height: 300px; /* Reduced height */
        margin: 10px;
        padding: 10px; /* Further reduced padding for smaller card */
        background-color: #fafafa;
        border: 1px solid #e0e0e0; /* Same border thickness as EventCard */
        border-radius: 8px; /* Rounded border */
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* Same shadow level as EventCard */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
    }

    .field-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2px; /* Further reduced margin for smaller line spacing */
        font-size: 14px; /* Smaller font size */
    }

    b {
        color: #1e1e1e;
    }

    span {
        color: #757575;
    }

    .password-container {
        display: flex;
        align-items: center;
    }

    .password-input {
        font-size: 14px; /* Smaller font size for input */
        border: none;
        background: none;
        color: #757575;
        width: 90px; /* Adjust width of password input */
    }

    .eye-button {
        background: none;
        border: none;
        cursor: pointer;
        margin-left: 5px;
        font-size: 14px;
        color: #757575;
    }

    .authorize-btn {
        background-color: #ff6b6b;
        border: none;
        color: white;
        padding: 6px 12px; /* Reduced padding */
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px; /* Smaller font size for button */
        align-self: center;
    }

    .authorize-btn:hover {
        background-color: #e55b5b;
    }

    .authorized {
        color: green; /* Change text color to green for authorized state */
        font-weight: bold; /* Bold text for visibility */
    }
</style>
