
---

## Part B — Team Composition & Culture Note

Save this as `docs/planning/team.md`. The brief asks you to discuss "team composition being mindful of the requirements" and "the ideal team culture with justification and how collaboration will be handled." This file answers both in one place.

```markdown
# Team Composition & Collaboration Model — Ipswich Books PoC

**Version:** 1.0

## 1. Assumed Team Composition

The PoC is built by a single developer, but the reporting team is modelled on
the composition a mid-sized retailer would realistically need to operate and
evolve the solution. This is the composition referenced throughout the report.

| Role | FTE | Responsibility |
|------|-----|----------------|
| Product Owner | 0.5 | Backlog prioritisation; stakeholder liaison (Ipswich Retail business) |
| Django Developer | 2.0 | MVT feature delivery: Book, Order, Profile models; views; templates; tests |
| DevOps Engineer | 1.0 | CI/CD pipeline, Docker, Render deployment, Prometheus/Grafana, repo hygiene |
| QA Engineer | 0.5 | Test strategy, E2E scenarios, sign-off on release candidates |
| UX Designer | 0.25 | Wireframes, frontend styling, accessibility review |

**Total:** 4.25 FTE. For a company of Ipswich Retail's size, the two
Distinct engineering roles — developer and DevOps — reflect the
cross-functional "you build it, you run it" model that DevOps adoption
requires. Splitting DevOps into its own role for a PoC is a pragmatic choice
while the platform matures; on a full-scale team the responsibility would be
distributed across the developer group.

## 2. Ideal Team Culture (and Why)

The following cultural principles are adopted, each justified against a
concrete pain point observed in Ipswich Retail's current monolith:

### 2.1 Blameless post-mortems
**Justification:** The brief notes frequent downtime. A blameless
post-mortem culture encourages the team to surface root causes rather than
hide incidents, which is the only reliable way to reduce repeat outages. The
PoC supports this via structured Render log review after each deploy
failure — captured in the report's reflection section.

### 2.2 Small, reversible changes
**Justification:** The monolithic deployment process is described as slow and
manual. Trunk-based development with short-lived feature branches and small
PRs forces smaller diffs, faster review, and lower-risk deploys. The
branching strategy (`feature/* → develop → main`) implements this
mechanically.

### 2.3 "You build it, you run it"
**Justification:** The brief explicitly identifies dev/ops silos as a source
of friction and delay. Shared on-call and shared deployment responsibility
removes the "throw over the wall" handoff. In the PoC this is visible in the
pipeline: the same team writes tests, merges to `main`, and owns the Render
deploy that the tests gate.

### 2.4 Automate everything repeatable
**Justification:** The brief notes "considerable manual work" in the current
deployment cycle. Anything performed twice manually becomes a script or a
pipeline step. Concretely: tests, image build, deployment, and monitoring
scrape configuration are all automated, leaving humans to focus on judgement
rather than toil.

### 2.5 Continuous feedback over phase gates
**Justification:** Feedback loops in the current system are described as slow
— bug fixes take a long time to reach production, and complaints arrive after
release. Short loops (CI on every PR, deploy on merge, live Grafana
dashboards) surface problems in minutes rather than weeks.

## 3. Collaboration Mechanisms

| Concern | Mechanism |
|---|---|
| Backlog & planning | GitHub Issues (labels: `feat`, `bug`, `ci`, `infra`) organised into a GitHub Projects board |
| Real-time chat | Slack — channels: `#dev`, `#deploys`, `#alerts` |
| Async standup | Slack thread each morning: "yesterday / today / blockers" |
| Code review | Pull request required before merge to `main`; at least one approving review; CI green required |
| Deploy visibility | GitHub Actions → Slack notification on deploy success/failure |
| Incident flow | Render log link + Slack alert; blameless retrospective comment posted to the corresponding GitHub Issue |
| Documentation | Versioned in-repo under `docs/` (this file, scope.md, toolchain.md, and diagrams) — docs-as-code |

## 4. Branching & Release Strategy

- `main` — protected; every commit deployable; auto-deploys via Render.
- `develop` — integration branch; may occasionally be red while a feature
  is in progress.
- `feature/<short-name>` — short-lived; one feature or fix per branch;
  opened as a PR to `develop`.
- `hotfix/<name>` — branched from `main`, PR back to both `main` and
  `develop`.

Commit messages follow Conventional Commits (`feat:`, `fix:`, `ci:`,
`docs:`, `chore:`). This is not ceremony for its own sake — CI can later
branch on commit type if needed (e.g. skip deploy on `docs:`).

## 5. Decision-Making & Escalation

- Two-reviewer rule for changes to `.github/workflows/`, `Dockerfile`, or
  production configuration.
- The DevOps Engineer has final say on infrastructure changes; the Product
  Owner has final say on scope.
- Escalation path: Developer → DevOps Engineer → Product Owner.

---

*End of Team document — v1.0*