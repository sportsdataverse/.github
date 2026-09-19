#!/usr/bin/env bash
# Read-only audit of the sportsdataverse GitHub org: settings, members by role, 2FA gaps,
# teams, private repos, outside collaborators, installed apps, fine-grained PAT state.
# Needs `gh` authenticated as an org OWNER (member-level auth hides most of it).
#
#   scripts/org-audit.sh > audit-$(date +%F).md
#
# Nothing here writes. The switches are flipped by a human following
# docs/runbooks/github-org-permissions.md.
set -euo pipefail
ORG="${ORG:-sportsdataverse}"
api() { gh api "$@" 2>&1 || true; }
echo "# $ORG GitHub org audit (read-only) — $(date -u +%Y-%m-%dT%H:%MZ)"; echo
echo "## Org settings"
api "orgs/$ORG" --jq '"- plan: \(.plan.name)\n- default_repository_permission: **\(.default_repository_permission)**  (target: none)\n- two_factor_requirement_enabled: **\(.two_factor_requirement_enabled)**  (target: true)\n- members_can_create_repositories: \(.members_can_create_repositories) (private: \(.members_can_create_private_repositories), public: \(.members_can_create_public_repositories))  (target: false)\n- members_can_fork_private_repositories: \(.members_can_fork_private_repositories)  (target: false)\n- web_commit_signoff_required: \(.web_commit_signoff_required)"'
echo; echo "## Members by role"
for role in admin member; do echo "### $role"; api "orgs/$ORG/members?role=$role&per_page=100" --paginate --jq '.[] | "- \(.login)"'; done
echo; echo "## Members WITHOUT 2FA"
api "orgs/$ORG/members?filter=2fa_disabled&per_page=100" --paginate --jq '.[] | "- \(.login)"'
echo; echo "## Teams"
api "orgs/$ORG/teams?per_page=100" --paginate --jq '.[] | "- \(.slug) (privacy=\(.privacy), perm=\(.permission))"'
echo; echo "## Private repos, with who can reach them beyond org-wide default"
api "orgs/$ORG/repos?type=private&per_page=100" --paginate --jq '.[] | .name' | while read -r r; do
  teams=$(api "repos/$ORG/$r/teams" --jq '[.[] | "\(.slug):\(.permission)"] | join(", ")')
  direct=$(api "repos/$ORG/$r/collaborators?affiliation=direct&per_page=100" --paginate --jq '[.[] | "\(.login):\(.role_name)"] | join(", ")')
  echo "- $r — teams: ${teams:-none}; direct: ${direct:-none}"
done
echo; echo "## Outside collaborators"
api "orgs/$ORG/outside_collaborators?per_page=100" --paginate --jq '.[] | "- \(.login)"'
echo; echo "## Installed GitHub Apps (administration/members permissions are the ones to justify)"
api "orgs/$ORG/installations" --jq '.installations[] | "- \(.app_slug) (repos=\(.repository_selection), perms=\(.permissions | keys | join(",")))"'
echo; echo "## Fine-grained PAT policy"
echo "- pending requests: $(api "orgs/$ORG/personal-access-token-requests?per_page=1" --jq 'if type=="array" then length else .message end')"
echo "- active grants: $(api "orgs/$ORG/personal-access-tokens?per_page=1" --jq 'if type=="array" then length else .message end')"
echo "  (\"Not Found\" on both = the org has never enabled fine-grained PAT access / approval; see runbook step 5)"
