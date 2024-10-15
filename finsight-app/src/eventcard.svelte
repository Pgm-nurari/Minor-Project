<!-- EventCard.svelte -->

<script>
    export let eventName;
    export let status;
    export let department;
    export let date;
    export let type;
</script>

<style>
    .eventcard {
        width: 240px;
        height: 331px;
        background: white;
        box-shadow: 4px 10px 4px rgba(0, 0, 0, 0.25);
        border-radius: 15px;
        overflow: hidden;
        border: 3px #AFD46E solid;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 24px;
    }

    .eventcard:hover {
        transform: translateY(-5px);
        transition: transform 0.3s ease;
    }

    .topbox {
        width: 100%;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: center;
        gap: 16px;
    }

    .cardheadingbox {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .cardheading {
        font-size: 24px;
        font-weight: 600;
        color: #1E1E1E;
    }

    .cardlist {
        align-self: stretch;
        height: 158px;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 12px;
        display: flex;
    }

    .cardlistitem {
        width: 100%;
        height: 22px;
        padding-left: 2px;
        padding-right: 2px;
        justify-content: center;
        align-items: center;
        display: inline-flex;
    }

    .cardlistitemtext {
        color: #757575;
        font-size: 16px;
        font-family: Inter;
        font-weight: 400;
        line-height: 22.40px;
        word-wrap: break-word;
    }

    .cardbutton {
        width: 176px;
        height: 40px;
        background: #AFD46E;
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #2C2C2C;
    }

    .cardbutton:hover {
        background-color: #8bc34a;
        cursor: pointer;
    }

    .cardbuttontext {
        color: white;
        font-size: 16px;
        text-align: center;
    }
</style>

<div class="eventcard">
    <div class="topbox">
        <h3 class="cardheadingbox">
            <span class="cardheading">{eventName}</span>
        </h3>
        <ul class="cardlist">
            <li class="cardlistitem"><span class="cardlistitemtext">Status: {status}</span></li>
            <li class="cardlistitem"><span class="cardlistitemtext">Department: {department}</span></li>
            <li class="cardlistitem"><span class="cardlistitemtext">Date: {date}</span></li>
            <li class="cardlistitem"><span class="cardlistitemtext">Type: {type}</span></li>
        </ul>
    </div>
    <div>
        <button class="cardbutton">
            <span class="cardbuttontext">View Event</span>
        </button>
    </div>
</div>
