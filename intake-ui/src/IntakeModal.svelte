<script>
    import { samplingInfo } from "./lib/state.svelte.js";

    let { showModal = $bindable() } = $props();

    function closeModal() {
        showModal = false;
    }
</script>

<div
    class="modal-backdrop"
    onclick={closeModal}
    role="button"
    tabindex="-1"
    onkeydown={(e) => e.key === "Escape" && closeModal()}
>
    <div
        class="modal"
        onclick={(e) => e.stopPropagation()}
        onkeydown={(e) => e.stopPropagation()}
        role="dialog"
        tabindex="-1"
    >
        <h2>Edit Sampling Info</h2>

        <form
            onsubmit={(e) => {
                e.preventDefault();
                closeModal();
            }}
        >
            <div class="form-group">
                <label for="penId">Pen ID:</label>
                <input type="text" id="penId" bind:value={samplingInfo.penId} />
            </div>

            <div class="form-group">
                <label for="species">Species:</label>
                <select id="species" bind:value={samplingInfo.species}>
                    <option value="atlantic_salmon">Atlantic Salmon</option>
                    <option value="rainbow_trout">Rainbow Trout</option>
                    <option value="coho_salmon">Coho </option>
                    <option value="toy_fish">Toy Fish</option>
                </select>
            </div>

            <div class="form-group">
                <label for="location">Location:</label>
                <input
                    type="text"
                    id="location"
                    bind:value={samplingInfo.location}
                />
            </div>

            <div class="form-group">
                <label for="notes">Notes:</label>
                <textarea id="notes" bind:value={samplingInfo.notes} rows="4"
                ></textarea>
            </div>

            <div class="button-group">
                <button type="submit">Done</button>
                <button type="button" onclick={closeModal}>Cancel</button>
            </div>
        </form>
    </div>
</div>

<style>
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .modal {
        background-color: white;
        padding: 2rem;
        border-radius: 8px;
        max-width: 500px;
        width: 90%;
        max-height: 90vh;
        overflow-y: auto;
    }

    .modal h2 {
        margin-top: 0;
        margin-bottom: 1.5rem;
    }

    .form-group {
        margin-bottom: 1.25rem;
    }

    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    .form-group input[type="text"],
    .form-group select,
    .form-group textarea {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-family: inherit;
        font-size: 1rem;
    }

    .form-group input:focus,
    .form-group select:focus,
    .form-group textarea:focus {
        outline: none;
        border-color: #4a90e2;
    }

    .form-group textarea {
        resize: vertical;
    }

    .button-group {
        display: flex;
        gap: 0.75rem;
        margin-top: 1.5rem;
    }

    button {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 4px;
        font-size: 1rem;
        cursor: pointer;
    }

    button[type="submit"] {
        background-color: #4a90e2;
        color: white;
    }

    button[type="submit"]:hover {
        background-color: #357abd;
    }

    button[type="button"] {
        background-color: #e0e0e0;
        color: #333;
    }

    button[type="button"]:hover {
        background-color: #d0d0d0;
    }
</style>
