# Ipswich Books — DevOps PoC

Proof-of-Concept e-commerce book storefront for Ipswich Retail, built with
Django (MVT) and delivered under DevOps principles.

**Live application:** _(added in Phase 4)_
**Case study report:** _(added in Phase 5)_

## Repository layout

- `docs/planning/` — scope, toolchain decisions, team model, wireframes,
  MVT architecture diagram
- `shop/` — Django app (Book, Order models; storefront views) [Phase 2]
- `accounts/` — Auth & profile views [Phase 2]
- `templates/` — HTML templates [Phase 2]
- `.github/workflows/` — CI pipeline [Phase 3]
- `Dockerfile`, `docker-compose.yml` — Containerization [Phase 2]

## Documentation

- [Scope (v1.1)](docs/planning/scope.md)
- [Toolchain decisions](docs/planning/toolchain.md)
- [Team & culture](docs/planning/team.md)

## Phase status

- [x] Phase 1 — Planning (scope, wireframes, MVT diagram, team model)
- [ ] Phase 2 — Django development & containerization
- [ ] Phase 3 — CI/CD pipeline
- [ ] Phase 4 — Monitoring & observability
- [ ] Phase 5 — Report
