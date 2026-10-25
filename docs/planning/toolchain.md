# Toolchain Decisions — Ipswich Books PoC

**Version:** 1.0

## Purpose

This document records the tool selected for each DevOps concern, the
justification for that choice, and the alternative considered. Every decision
is justified against the PoC's constraints: **zero budget**, **single
developer**, **five-week timeline**, and **required DevOps coverage** (CI,
containerization, CD, monitoring).

## Decisions

| Concern | Tool selected | Justification | Alternative considered |
|---|---|---|---|
| Version control | GitHub (public repo) | Free, integrates natively with GitHub Actions, public repo is an assessment requirement | GitLab, Bitbucket |
| CI | GitHub Actions | Co-located with the repository — no separate server to provision or maintain. YAML workflow lives in the repo, making pipeline-as-code a natural by-product | Jenkins (powerful but requires server + plugin maintenance); GitLab CI (viable but creates a second platform to manage for a GitHub-hosted repo) |
| Containerization | Docker + Docker Compose | Industry standard; Compose simplifies local dev with PostgreSQL + app in one command | Podman (rootless; less familiar to employers) |
| Container registry | GitHub Container Registry (GHCR) | Free for public packages; same platform as the code | Docker Hub (rate limits on free tier) |
| Deployment (CD) | Render.com | Native Python/Docker support; free tier; auto-deploy from GitHub; managed Postgres available on free tier | Railway (free tier recently reduced); PythonAnywhere (no Docker support); DigitalOcean (requires credit card) |
| Production database | Render Postgres (free tier) | Same provider as the app = one bill, one dashboard, internal networking | Supabase (separate platform to manage); ElephantSQL (retired) |
| Monitoring — metrics | Prometheus + Grafana | Brief explicitly requires these tools; runs locally via Docker Compose, so no paid cloud tier needed | Datadog / New Relic (paid, overkill for PoC) |
| Monitoring — logs | Render log stream + Slack webhook | Free, no additional tooling | Sentry (paid tier for meaningful usage) |
| Planning / diagrams | Draw.io | Free, browser-based, exports PNG + editable `.drawio` source that can be versioned | Lucidchart (free tier limited), Visio (paid) |
| Backlog | GitHub Issues + Projects | Free, co-located with code and PRs; no separate Jira licence needed | Trello, Jira |

## Deliberate non-choices (and why)

- **No Kubernetes.** The PoC runs a single container on Render. Introducing
  Kubernetes would demonstrate orchestration skill but at the cost of the
  pipeline, deployment, and monitoring work that the assessment explicitly
  requires. Kubernetes is noted as a full-scale migration path in the report's
  future-work section.
- **No Terraform.** The Render configuration is a single YAML blueprint
  (`render.yaml`). Terraform would add state management overhead with no
  benefit at this scale, but is noted as a future improvement if infrastructure
  grows.
- **No Jenkins.** Jenkins would demonstrate deeper pipeline customisation, but
  it requires a hosted server and ongoing plugin maintenance — an unjustifiable
  cost for a solo PoC. GitHub Actions provides equivalent pipeline semantics
  with zero infrastructure.

## Free-tier limitations to acknowledge in the report

- **Render free web service** sleeps after 15 minutes of inactivity → first
  request after idle takes 30–60s. This is documented as a limitation.
- **Render free Postgres** expires after 90 days of inactivity (not an issue
  for the PoC's lifetime).
- **GitHub Actions** free tier: 2,000 minutes/month for private repos; unlimited
  for public repos — our repo is public, so no practical limit.
- **Prometheus/Grafana** run locally in Docker; the deployed app exposes
  `/metrics`, but scraping happens from the developer's machine during the
  PoC. In production, this would move to a persistent monitoring host.