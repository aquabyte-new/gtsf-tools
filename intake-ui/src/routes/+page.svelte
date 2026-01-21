<script>
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { clearAppState, samplingInfo } from "$lib/state.svelte.js";
    import IntakeModal from "./collect/IntakeModal.svelte";

    let collections = $state([]);
    let showModal = $state(false);
    const apiUrl = `${import.meta.env.VITE_API_URL}/api`;

    onMount(async () => {
        try {
            const response = await fetch(`${apiUrl}/collections`);
            collections = await response.json();
        } catch (error) {
            console.error("Failed to load collections:", error);
        }
    });

    function openCollection(collectionId) {
        goto(`/collect/${collectionId}`);
    }

    function newCollection() {
        clearAppState();
        showModal = true;
    }

    async function createCollection() {
        const response = await fetch(`${apiUrl}/collections/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(samplingInfo),
        });

        if (!response.ok) {
            throw new Error("Failed to create collection. Please try again.");
        }

        const result = await response.json();
        samplingInfo.collectionId = result.collectionId;

        goto(`/collect/${result.collectionId}`);
    }
</script>

<main>
    <div class="header">
        <h1>Collection history</h1>
        <button class="new-collection-btn" onclick={newCollection}
            >New Collection</button
        >
    </div>

    <div class="collections-grid">
        {#each collections as collection}
            <div
                class="collection-card"
                role="button"
                tabindex="0"
                onclick={() => openCollection(collection.id)}
                onkeydown={(e) => e.key === "Enter" && openCollection(collection.id)}
            >
                <h2>{collection.name}</h2>

                <div class="times">
                    <div>
                        Created at: {new Date(
                            collection.createdAt,
                        ).toDateString()}
                    </div>
                    <div>
                        Updated at: {new Date(
                            collection.updatedAt,
                        ).toDateString()}
                    </div>
                </div>

                <div class="stats">
                    <div class="stat">
                        <span class="label">Fish</span>
                        <span class="value">{collection.numFish}</span>
                    </div>
                    <div class="stat">
                        <span class="label">Avg Weight</span>
                        <span class="value"
                            >{collection.avgWeight
                                ? collection.avgWeight.toFixed(1) + "g"
                                : "-"}</span
                        >
                    </div>
                </div>
            </div>
        {/each}
    </div>
</main>

{#if showModal}
    <IntakeModal
        bind:showModal
        title="New Collection"
        submitLabel="Create Collection"
        onSubmit={createCollection}
    />
{/if}

<style>
    main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
    }

    h1 {
        margin: 0;
    }

    .new-collection-btn {
        padding: 0.5rem 1rem;
        cursor: pointer;
        border: 1px solid #333;
        background-color: transparent;
        border-radius: 4px;
        font-size: 1rem;
    }

    .new-collection-btn:hover {
        background-color: #eaeaea;
    }

    .collections-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
    }

    .collection-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1.5rem;
        cursor: pointer;
        transition: box-shadow 0.2s;
    }

    .collection-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .collection-card h2 {
        margin: 0 0 1rem 0;
        font-size: 1.25rem;
    }

    .times {
        margin-bottom: 1rem;
        margin-top: -0.5rem;
    }

    .stats {
        display: flex;
        gap: 1.5rem;
    }

    .stat {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .label {
        font-size: 0.875rem;
        opacity: 0.7;
    }

    .value {
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
