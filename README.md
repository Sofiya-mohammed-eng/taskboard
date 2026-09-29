# Taskboard

A small three-tier app (Nginx frontend, FastAPI API, Postgres) used to practice
a production-style CI/CD workflow.

## Run locally

    cp .env.example .env        # then set a real POSTGRES_PASSWORD in .env
    docker compose up --build -d
    open http://localhost:8080

## Run the tests

    docker build --target test -t taskboard-api:test ./api
    docker run --rm taskboard-api:test

## Branching strategy

- `main` is always releasable and protected: no direct pushes.
- All work happens on short-lived branches: `feature/<name>` or `fix/<name>`.
- Changes reach `main` only through a pull request. CI must pass before merging.
- Pull requests are squash-merged to keep history readable.
- Releases are version tags on `main`, e.g. `v0.1.0`.

## Documentation

- [Architecture diagram](docs/architecture.md)
- [Runbook: deploy, roll back, troubleshoot](docs/RUNBOOK.md)
