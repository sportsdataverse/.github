# GitHub org permissions — hardening runbook

Why: as of 2026-09-18 the `sportsdataverse` org's **default repository permission is `admin`**
(every one of 64 non-owner members is admin on every repo, including the 13 private ones),
2FA is not required, any member can create repos, and fine-grained PAT controls have never
been enabled. `/platform/api-key` on sportsdataverse.org issues Data API keys to anyone the
org counts as a member, so org membership is also the API's trust boundary.

Every step below is flipped by a human owner in the GitHub UI. `scripts/org-audit.sh`
(read-only, run as an owner) is the before/after check: run it, do a step, run it again.

## 0. Baseline

```sh
scripts/org-audit.sh > audit-before.md
```

Latest baseline: 7 owners, 64 members, 1 team (`metahockey`, pull), 13 private repos,
8 outside collaborators, 3 members without 2FA, 13 installed apps.

## 1. Teams first (so step 2 removes nothing anyone needs)

Settings → Teams. Create, then grant per repo (Repo → Settings → Collaborators and teams):

| team | members | grants |
|---|---|---|
| `core` | owners + the people who run the droplet/DB/orchestration | `admin` on `sdv-db`, `sdv-orch`, `sdv-internal-refs`, `odds-data`, `.github`; `maintain` elsewhere |
| `maintainers` | package maintainers | `maintain` on their packages' repos (R, Python, JS, `*-raw`, `*-data`) |
| `contributors` | everyone else who should see private work | `read`/`triage` on the specific private repos they need, none by default |
| `metahockey` (exists) | keep | as is |

Rule of thumb: nobody gets `admin` through a team unless they are an owner anyway.

## 2. Base permission `admin` → **No permission**

Settings → Member privileges → Base permissions → **No permission**. Members then see only
public repos plus what their teams grant. Do this immediately after step 1, same sitting.

Expect: a handful of "I can't see X" messages. Answer each by adding the person to the
right team, not by raising the base back.

## 3. Repository creation

Settings → Member privileges → Repository creation → **disable** for members (owners create;
requests go to an owner). Also **disable** "Members can fork private repositories" (already
off) and keep "Repository forking" for public repos on.

## 4. Two-factor authentication

Settings → Authentication security → **Require two-factor authentication**. GitHub removes
members without 2FA from the org at the moment you enable it — message the 3 in the audit
first, wait a week, then flip it. Outside collaborators without 2FA are removed the same way.

## 5. Personal access tokens

Settings → Personal access tokens:
- Fine-grained tokens → **Allow access via fine-grained personal access tokens**, and
  **Require administrator approval**.
- Tokens (classic) → **Restrict access via personal access tokens (classic)**. Classic PATs
  carry `repo` scope across every repo the user can reach; with base = none that is mostly
  harmless, but restricting them forces the fine-grained path.
After this, `scripts/org-audit.sh` reports request/grant counts instead of "Not Found".

## 6. OAuth and GitHub Apps

Settings → Third-party access → OAuth application policy → **Restrict** (then approve the
ones actually used: Vercel, Codecov, r-universe, CodeRabbit, Cloudflare, DigitalOcean, giscus,
utterances). Review the installed-apps list in the audit: any app with `administration` or
`members` on **all repositories** should be narrowed to selected repositories unless it needs
org-wide reach (Vercel and Cloudflare deploy from specific repos; Codecov and CodeRabbit do
not need `administration`).

## 7. Owners and outside collaborators

- Owners: 7 is a lot for the org's size. Anyone who does not need billing/settings/deletion
  becomes a `core` team member instead.
- Outside collaborators (8): confirm each still needs the repos they hold; remove the rest.

## 8. Data API keys (sportsdataverse.org)

No change to who can mint (`isOrgMember`), by decision on 2026-09-18. The control is per-key
rate limits in sdv-db, surfaced on `/platform/api-key`. Steps 1–2 shrink "org member" back to
people you actually admitted, which is the real fix for "API access too permissive".

## 9. Funding button

`FUNDING.yml` in this repo shows the Sponsor button on every org repo. Ko-fi is live;
two lines wait on you:
- publish a GitHub Sponsors listing for the org (Settings → Sponsors) and uncomment `github:`;
- fill the `patreon:` slug.

## After

```sh
scripts/org-audit.sh > audit-after.md && diff audit-before.md audit-after.md
```

Expected diff: base permission `none`, 2FA `true`, repo creation `false`, PAT counts numeric,
teams listed with grants, fewer owners/outside collaborators.
