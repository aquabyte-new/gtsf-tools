<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { entries, samplingInfo } from "$lib/state.svelte.js";
  import CollectPage from "../CollectPage.svelte";

  const apiUrl = `${import.meta.env.VITE_API_URL}/api`;

  // Convert API datetime strings to timestamps and add iconIdx
  function transformApiFish(apiFish) {
    return {
      ...apiFish,
      iconIdx: Math.floor(Math.random() * 13) + 1,
      captureStart: new Date(apiFish.captureStart).getTime(),
      captureEnd: new Date(apiFish.captureEnd).getTime(),
      sedationEnd: new Date(apiFish.sedationEnd).getTime(),
      measurementEnd: new Date(apiFish.measurementEnd).getTime(),
    };
  }

  onMount(async () => {
    const collectionId = $page.params.collectionId;
    if (!collectionId) {
      return;
    }

    try {
      const [collectionRes, samplesRes] = await Promise.all([
        fetch(`${apiUrl}/collections/${collectionId}`),
        fetch(`${apiUrl}/samples/${collectionId}`),
      ]);

      if (!collectionRes.ok || !samplesRes.ok) {
        throw new Error("Failed to load collection data.");
      }

      const [collection, samples] = await Promise.all([
        collectionRes.json(),
        samplesRes.json(),
      ]);

      const transformedSamples = samples.map(transformApiFish);
      entries.splice(0, entries.length, ...transformedSamples);
      samplingInfo.collectionId = collection.id;
      samplingInfo.name = collection.name ?? "";
      samplingInfo.penId = collection.penId ?? "";
      samplingInfo.species = collection.species ?? "";
      samplingInfo.location = collection.location ?? "";
      samplingInfo.notes = collection.notes ?? null;
    } catch (error) {
      console.error("Failed to load collection:", error);
      alert("Failed to load collection. Please try again.");
    }
  });
</script>

<CollectPage />
