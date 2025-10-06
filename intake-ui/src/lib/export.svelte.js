import { entries, samplingInfo } from "./state.svelte.js";

// This is configured in .env.development and .env.production
const apiUrl = import.meta.env.VITE_API_URL;


const columns = [
    "id",
    'penId',
    'species',
    'location',
    'weight',
    'length',
    'width',
    'breadth',
    'cameraStartTime',
    'cameraEndTime',
    'sedationEndTime',
    'measurementEndTime',
    'notes',
    "collectionName",
]

const columnMap = {
    "weight": "weightG",
    "length": "lengthMm",
    "width": "widthMm",
    "breadth": "breadthMm",
    "cameraStartTime": "intakeStart",
    "cameraEndTime": "intakeEnd",
    "sedationEndTime": "sedationEnd",
    "measurementEndTime": "measurementEnd",
    "id": "fishId",
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

export async function saveToBackend(quiet = false) {
    if (entries.length === 0) {
        alert("No data to save");
        return;
    }

    // Prepare fish data with sampling info
    const fish = entries.map((entry) => ({
        ...entry,
        penId: samplingInfo.penId,
        location: samplingInfo.location,
        species: samplingInfo.species
    }));

    try {
        const response = await fetch(`${apiUrl}/save`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                collectionName: samplingInfo.name,
                fish: fish,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        if (!quiet) {
            alert(`Successfully saved ${entries.length} fish to backend`);
        }
    } catch (error) {
        console.error('Failed to save to backend:', error);
        alert(`Failed to save to backend: ${error.message}`);
    }
}