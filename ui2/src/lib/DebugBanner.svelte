<div class="banner">
    <div class="banner-title">VITE MODE: {import.meta.env.MODE}</div>
    <div class="banner-title">VITE SSR: {import.meta.env.SSR}</div>
    <div>
        Backend API: <a
            href="{import.meta.env.VITE_API_URL}/docs"
            target="_blank"
        >
            {import.meta.env.VITE_API_URL}
        </a>
    </div>
</div>

<style>
    .banner {
        background-color: #56abff;
        color: rgb(0, 0, 0);
        padding: 0.5rem;
        text-align: center;
        margin: 0rem;
    }

    .banner-title {
        text-transform: uppercase;
        font-weight: bold;
    }
</style>
