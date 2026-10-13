---
verb: init
---
Framework first-run (deployment, quickstart distilled for the agent; activates as a staged migration once upgrade-framework lands):

1. Copy `.meta/` and `.agents/skills/` into the target vault root (minimal core variant: `plugins/core/` + protocol + scripts + docs + VERSION + command).
2. Write the target AGENTS.md shell (identity + layout paragraphs; the handwritten region is the user's) with the injection markers verbatim — see `.meta/docs/agents-example.md`.
3. Create the four empty directories: `vault/` · `wiki/notes/` · `wiki/sessions/` · `wiki/vault/`.
4. `python .meta/scripts/wiki_plugin_kernel.py all` — validate green, injection region built, skills in sync.
5. First-run verification: drop any file into `vault/`, say "map", then "check".
