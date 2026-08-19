# status/

Nightly machine + human snapshot of the whole ecosystem, written by
`.github/workflows/ecosystem-status.yml` (script: `.github/scripts/ecosystem_status.py`).

- `ecosystem.json` — per repo: open PRs (age/idle), open + stale-unassigned issues,
  latest conclusion per default-branch workflow, releases with asset counts and
  newest-asset timestamp, last push. `totals` at the top level.
- `ecosystem.md` — the same as tables: red workflows, idle PRs, stale issues,
  release-asset freshness for `-data` / `-raw` producers, package latest releases.

Consumers: the chief-of-staff routines (saiemgilani/ClaudeCowork) read these because
the cloud sandbox cannot reach api.github.com. Regenerate locally with `gh auth login`
then `python .github/scripts/ecosystem_status.py`.
