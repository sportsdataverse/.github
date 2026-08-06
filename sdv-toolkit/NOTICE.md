# Third-Party Notices

The 10 skills listed below are third-party Claude Code skills vendored into
this plugin from a local skills collection (`~/.claude/skills` /
`~/.agents/skills`, not a public git repository). They were renamed to the
`sdv-` prefix for namespace consistency with the rest of the toolkit and are
otherwise unmodified, except for internal cross-references
(`dependsOn` / `@ref` / bare prose mentions of sibling skill names) rewritten
to point at their new `sdv-` names — see `skills/*/SKILL.md` for the current
content. Licence/author fields below are recorded exactly as declared in each
skill's original frontmatter (or their absence, if none was declared) —
nothing here is upgraded or guessed.

| Original name | Vendored as | Original source path | Licence | Author | Version |
|---|---|---|---|---|---|
| `ml-pipeline` | `sdv-ml-pipeline` | `~/.claude/skills/ml-pipeline` | MIT | https://github.com/Jeffallan | 1.1.0 |
| `polars` | `sdv-polars` | `~/.claude/skills/polars` | See note below | K-Dense Inc. (skill author) | 1.1 |
| `evaluating-ml-models` | `sdv-evaluating-ml-models` | `~/.claude/skills/evaluating-ml-models` | None declared | None declared | — |
| `engineering-ml-features` | `sdv-engineering-ml-features` | `~/.claude/skills/engineering-ml-features` | None declared | None declared | — |
| `data-scientist` | `sdv-data-scientist` | `~/.claude/skills/data-scientist` | None declared | None declared | — |
| `assuring-data-pipelines` | `sdv-assuring-data-pipelines` | `~/.claude/skills/assuring-data-pipelines` | None declared | None declared | — |
| `python-performance-optimization` | `sdv-python-performance-optimization` | `~/.claude/skills/python-performance-optimization` | None declared | None declared | — |
| `working-in-notebooks` | `sdv-working-in-notebooks` | `~/.claude/skills/working-in-notebooks` | None declared | None declared | — |
| `analyzing-data` | `sdv-analyzing-data` | `~/.claude/skills/analyzing-data` | None declared | None declared | — |
| `building-data-pipelines` | `sdv-building-data-pipelines` | `~/.claude/skills/building-data-pipelines` | None declared | None declared | — |

**Note on `polars`'s licence field**: the skill's frontmatter `license:` key is
set to `https://github.com/pola-rs/polars/blob/main/LICENSE`, i.e. it points
at the licence of the *polars project* (the DataFrame library the skill
documents), not necessarily a stated licence for the skill's own text. It is
recorded verbatim; we make no claim about what licence covers the skill
content itself.

**The other 8 skills** (all except `ml-pipeline` and `polars`) ship no
`license:` or author metadata in their upstream frontmatter. They are vendored
as installed, with no licence claim made or implied.
