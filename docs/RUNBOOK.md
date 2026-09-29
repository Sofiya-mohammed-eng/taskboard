# Taskboard runbook

## Services

| Service  | What it is         | Port | Notes                                   |
|----------|--------------------|------|-----------------------------------------|
| frontend | Nginx, static page | 8080 | Proxies `/api/` to the API              |
| api      | FastAPI            | 8000 | Health check at `/health`               |
| db       | Postgres 16        | none | Not exposed to the host; named volume   |

## Run the current source (development)

    docker compose up --build -d

## Deploy a released version

Released images are published to GHCR by the release workflow when a
version tag (for example `v0.1.0`) is pushed.

    docker compose down
    TAG=v0.1.0 docker compose -f docker-compose.release.yml up -d
    docker compose -f docker-compose.release.yml ps
    curl http://localhost:8000/health

Stop the development stack first: both use ports 8000 and 8080.

## Roll back to the previous version

1. Find the last known-good version: `git tag` or the GitHub Releases page.
2. Redeploy that tag:

       TAG=<previous-version> docker compose -f docker-compose.release.yml up -d

3. Verify: `curl http://localhost:8000/health` returns `{"status":"ok"}`
   and the page at http://localhost:8080 loads and lists tasks.
4. Record what failed and why (a short note in the incident or PR).

Rollback is safe because every version is an immutable image stored in
GHCR. The database is not rolled back: the API only creates its table if
it is missing. If a future release changes the schema, add a migration
plan to this section before shipping it.

## Health checks and logs

    curl http://localhost:8000/health
    docker compose -f docker-compose.release.yml ps
    docker compose -f docker-compose.release.yml logs api --tail 50

## Common failures

- **API cannot reach the database:** check that `db` is `healthy` in `ps`
  and that `.env` has the same values the database was created with.
- **Port already in use:** another stack is running. Run `docker compose down`
  in the other stack.
- **Image pull denied:** the GHCR packages are private. Make them public in
  the package settings.
