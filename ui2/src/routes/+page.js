import { error } from '@sveltejs/kit';

const apiUrl = import.meta.env.VITE_API_URL;

export const load = async ({ params }) => {
    const response = await fetch(`${apiUrl}/collections`);
    return { collections: await response.json() };
};