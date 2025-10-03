// Application state.
export const stages = $state({
    camera: null,
    sedation: null,
    measurement: null,
});
export const entries = $state([]);
export const samplingInfo = $state({
    penId: 880,
    location: null,
    notes: null,
})

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