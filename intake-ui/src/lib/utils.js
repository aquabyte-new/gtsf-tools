export function generateID() {
    const template = 'xxxxxx';
    return template.replace(/[x]/g, c => (
        (Math.random() * 16 | 0).toString(16))
    );
}