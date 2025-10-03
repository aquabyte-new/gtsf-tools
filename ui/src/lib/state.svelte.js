// Stages state.
const defaultStages = { camera: null, sedation: null, measurement: null };
function loadStages() {
    if (typeof window === 'undefined') {
        return { ...defaultStages };
    }
    const saved = sessionStorage.getItem('stages');
    return saved ? JSON.parse(saved) : { ...defaultStages };
}

export const stages = $state(loadStages());

// Entries state.
function loadEntries() {
    if (typeof window === 'undefined') {
        return [];
    }
    const saved = sessionStorage.getItem('entries');
    return saved ? JSON.parse(saved) : [];
}
export const entries = $state(loadEntries());

// Sampling info state.
const defaultSamplingInfo = {
    penId: '880',
    species: 'atlantic_salmon',
    location: 'bergen_workshop',
    notes: null,
};
function loadSamplingInfo() {
    if (typeof window === 'undefined') {
        return { ...defaultSamplingInfo };
    }
    const saved = sessionStorage.getItem('samplingInfo');
    return saved ? JSON.parse(saved) : { ...defaultSamplingInfo };
}

export const samplingInfo = $state(loadSamplingInfo());

// State utilities.
export function cameraStageActive() {
    return stages.camera !== null;
}

export function sedationStageActive() {
    return stages.sedation !== null;
}

export function measurementStageActive() {
    return stages.measurement !== null;
}

export function saveFish(fish, weight) {
    if (weight === null || weight < 0) { return null; }

    fish.weight = weight;
    entries.push(fish);
    return entries.length;
}

export function clearAppState() {
    sessionStorage.clear();

    // Reset state (assign defaults to current state objects)
    Object.assign(stages, { ...defaultStages });
    Object.assign(samplingInfo, { ...defaultSamplingInfo });
    entries.splice(0, entries.length);
}