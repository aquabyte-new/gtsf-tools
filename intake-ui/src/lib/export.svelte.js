import { entries, samplingInfo } from "./state.svelte.js";

// This is configured in .env.development and .env.production
const apiUrl = `${import.meta.env.VITE_API_URL}/api`;


const columns = [
    "fishId",
    'penId',
    'species',
    'location',
    'weight',
    'length',
    'width',
    'breadth',
    'captureStart',
    'captureEnd',
    'sedationEnd',
    'measurementEnd',
    'notes',
    "collectionName",
]

const columnMap = {
    "weight": "weightG",
    "length": "lengthMm",
    "width": "widthMm",
    "breadth": "breadthMm",
}

// Helper to escape CSV values
function escapeCSV(value) {
    if (value === null || value === undefined) return '';

    let str = (typeof value === 'object') ? JSON.stringify(value) : String(value);
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
        return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
}

function toCSV() {
    if (entries.length === 0) {
        return null;
    }

    const header = columns.map(col => columnMap[col] || col).join(',');
    const rows = entries.map((entry) => {
        const fullEntry = {
            ...entry,
            penId: samplingInfo.penId,
            location: samplingInfo.location,
            species: samplingInfo.species,
            collectionName: samplingInfo.name,
        };
        return columns.map(col => escapeCSV(fullEntry[col])).join(',');
    });
    return [header, ...rows].join('\n');
}

export function exportCSV() {
    // Create filename with timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const filename = `gtsf-entries-${timestamp}.csv`;

    // Generate CSV
    const csv = toCSV();

    if (csv === null) {
        alert("No data to export");
        return;
    }

    // Trigger download
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

/**
 * Save a single fish to the backend.
 * @param {Object} fish - The fish data from the measurement stage
 * @returns {Promise<boolean>} - True if save succeeded
 */
export async function saveFishToBackend(fish) {
    const collectionId = samplingInfo.collectionId;
    if (!collectionId) {
        console.error('No collection ID set - cannot save fish');
        alert('No collection selected. Please start a collection first.');
        return false;
    }

    const payload = {
        fishId: fish.fishId,
        weightG: parseFloat(fish.weightG),
        lengthMm: parseFloat(fish.lengthMm),
        widthMm: fish.widthMm ? parseFloat(fish.widthMm) : null,
        breadthMm: fish.breadthMm ? parseFloat(fish.breadthMm) : null,
        circumferenceMm: fish.circumferenceMm ? parseFloat(fish.circumferenceMm) : null,
        captureStart: new Date(fish.captureStart).toISOString(),
        captureEnd: new Date(fish.captureEnd).toISOString(),
        sedationEnd: new Date(fish.sedationEnd).toISOString(),
        measurementEnd: new Date(fish.measurementEnd).toISOString(),
        notes: fish.notes || null,
    };

    try {
        const response = await fetch(`${apiUrl}/samples/${collectionId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const text = await response.text();
            throw new Error(`HTTP ${response.status}: ${text}`);
        }

        console.log(`Saved fish ${fish.fishId} to collection ${collectionId}`);
        return true;
    } catch (error) {
        console.error('Failed to save fish:', error);
        alert(`Failed to save fish: ${error.message}`);
        return false;
    }
}