<!-- src/Modal.svelte -->

<script>
    export let openModal = false;
    export let onClose;

    const handleClose = () => {
        if (onClose) onClose();
    };
</script>

<style>
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .modal-container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        max-width: 600px;
        width: 100%;
        max-height: 80vh; /* Set a maximum height */
        overflow-y: auto; /* Enable vertical scrolling */
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        position: relative;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .close-button {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
    }
</style>

{#if openModal}
    <div class="modal-overlay" on:click={handleClose}>
        <div class="modal-container" on:click|stopPropagation>
            <div class="modal-header">
                <h2>Event Creation</h2>
                <button class="close-button" on:click={handleClose}>&times;</button>
            </div>

            <!-- Your Event Form Goes Here -->
            <slot></slot>
        </div>
    </div>
{/if}
