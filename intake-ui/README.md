# Intake UI

<img width="2551" height="1669" alt="Capture-2025-10-07-210513" src="https://github.com/user-attachments/assets/fb6f74ec-49ae-43e8-908f-e50aab4e9ffb" />

# Developing
This repo uses [Svelte](https://svelte.dev/docs/svelte/overview) and [SvelteKit](https://svelte.dev/docs/kit/introduction) to create a reactive static website that can interface with our FastAPI backend.

> [!NOTE]
> This project uses Svelte, a JavaScript framework that compiles declarative UI components into efficient JavaScript code. SvelteKit is used to provide file-based routing, server-side rendering, and static site generation, as well as development tooling and project structure. Together, they allow us to build the web application as a set of modular components with clear routing and deployment options.
>
> This repo uses Svelte 5 with runes.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Svelte](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode).

# Deployment
Run `just release` to deploy the latest static app to the `internal-tools` EC2.