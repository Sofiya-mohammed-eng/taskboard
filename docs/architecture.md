# Taskboard architecture

```mermaid
flowchart LR
  user["Browser"] -->|":8080"| fe["Nginx frontend"]
  fe -->|"/api/ proxy"| api["FastAPI API"]
  api -->|"SQL"| db[("Postgres")]

  dev["Developer"] -->|"pull request"| gh["GitHub"]
  gh --> ci["CI: tests + image builds"]
  gh -->|"tag vX.Y.Z"| rel["Release workflow"]
  rel --> ghcr[("GHCR images")]
  rel --> gr["GitHub Release + notes"]
  ghcr -->|"TAG=vX.Y.Z"| deploy["docker-compose.release.yml"]
```

- `main` is protected: changes arrive by pull request, and `test` and `build` must pass.
- Releases are immutable version tags. Rolling back means redeploying an older tag.
