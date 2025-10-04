set shell := ["bash", "-uc"]

serve:
  cd ui ; bun run dev -- --open

serve-backend:
  cd backend ; uv run fastapi dev main.py

build:
  cd ui ; bun run build

release:
  rsync -avz \
    --delete \
    --exclude=.DS_Store \
    ui/dist/ \
    tools:~/gtsf-ui

release-backend:
  rsync -avz \
    --delete \
    --exclude=__pycache__ \
    --exclude=.DS_Store \
    --exclude=.venv \
    backend/ \
    tools:~/gtsf-backend
