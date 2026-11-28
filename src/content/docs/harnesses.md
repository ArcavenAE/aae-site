---
title: claude, codex and opencode as managed services
description: One team manifest names a harness per role. marvel starts, replaces and scales them with the same commands, and support differs in places.
---

marvel, an ArcavenAE part, runs claude, codex and opencode as roles of one team, each in its own tmux pane. This is the harness story in Dark Atelier.

## The need

You use more than one coding agent, and each one starts, crashes and runs out of quota in its own way.

## One manifest, one role per harness

A role names its harness in its runtime block. This is marvel's [mixed adapters example](https://github.com/ArcavenAE/marvel/blob/b379ca6543dbfb7191d3bf5680c653215b5e10df/examples/mixed-adapters.toml) without its comments:

```toml
[workspace]
name = "mixed"

[[team]]
name = "matrix"

  [[team.role]]
  name = "analyst-p"
  replicas = 1
  permissions = "plan"

    [team.role.runtime]
    image = "claude"
    command = "claude"
    mode = "headless"
    prompt = "Summarize what a marvel adapter does in one sentence."

  [[team.role]]
  name = "builder-p"
  replicas = 1

    [team.role.runtime]
    image = "codex"
    command = "codex"
    mode = "headless"
    prompt = "Reply with the single word: ok"

  [[team.role]]
  name = "scout-p"
  replicas = 1

    [team.role.runtime]
    image = "opencode"
    command = "opencode"
    mode = "headless"
    args = ["-m", "opencode/deepseek-v4-flash-free"]
    prompt = "Reply with the single word: ok"

  [[team.role]]
  name = "analyst-t"
  replicas = 1
  permissions = "plan"

    [team.role.runtime]
    image = "claude"
    command = "claude"
    args = ["--model", "haiku"]
    context_feed = "statusline"
```

Install the three harnesses and sign in where one asks for it. Then, from a marvel source checkout with the daemon running, apply the example:

```sh
marvel work examples/mixed-adapters.toml
```

See [marvel work](/reference/marvel_work/), and the [two-minute page](/e1-tour/) for the daemon. The first three roles are headless: each takes one prompt and exits. For a codex or opencode seat that stays open, leave out `mode` and `prompt`.

## What is the same

- Every role is applied, scaled and shifted by the same commands, whatever its harness.
- `restart_policy` is `always` unless you set `on-failure` or `never`, and `max_restarts` caps the replacements. [marvel reset-health](/reference/marvel_reset-health/) clears a role that reached the cap.
- A headless run that exits 0 reads `succeeded` and is not run again.
- A team budget's `max_sessions` counts every seat. `max_tokens` counts headless runs only.
- Memory and CPU are read for every seat on macOS and Linux.

## Where support differs

This page was written from marvel's code and docs at commit `b379ca65`. It is read, not measured: no marvel command was run for it. The table starts from marvel's [feature matrix](https://github.com/ArcavenAE/marvel/blob/b379ca6543dbfb7191d3bf5680c653215b5e10df/docs/feature-matrix.md), which says it is current as of an older commit, so where the code has moved the table follows the code.

| Capability | claude | codex | opencode |
|---|---|---|---|
| Context reading, interactive | with `context_feed = "statusline"` | through hooks marvel writes | not built |
| Context reading, headless | built | not built | partial: needs a window from the manifest or opencode's model catalog |
| Account usage windows, and the `limited` state | with the statusline feed | through the hooks; not checked headless | not built |
| Heartbeat health check | with the statusline feed | through the hooks; not checked headless | not built |
| Context-low handoff condition | with a context reading | partial: interactive only | partial: headless only |
| Age handoff condition, interactive roles | built; not measured end to end | partial: the seat may be unable to write the file | partial: the seat may be unable to write the file |
| Successor's first message names the handoff | interactive, bare `claude` command | not built | not built |
| Role `permissions` applied as launch flags | built | `plan`, `auto` and `workspaceNetwork` | not applied |
| `(logged-out)` note in HEALTH | for screens marvel has a pattern for | not built | not built |
| Sign-in expiry, from `marvel get account-logins` | when the cluster turns it on | not built | not built |

About permissions:

- On codex, any other `permissions` value is refused at apply, and so is `dangerous_permissions`.
- On opencode, a role's `permissions = "plan"` or `"auto"` is accepted and changes nothing. Set what opencode may do through opencode's own settings or `runtime.args`.

About handoffs: marvel types the request into the seat's pane, and a headless run is not waiting at a prompt. Read a headless entry on the context-low row as the condition holding, not as a handoff that has been seen to work. A codex role can hand off through a tool instead of writing the file, with `handoff_via = "tool"`. See the [handoff page](/handoff/) for how a handoff works.

## The view

```sh
marvel get sessions --columns team,role,runtime,backend,login,state,health,context,llm
```

Add `-w` to keep it live. See [marvel get](/reference/marvel_get/).

| Column | Header | What it shows |
|---|---|---|
| `team` | TEAM | the seat's team |
| `role` | ROLE | the seat's role |
| `runtime` | RUNTIME | the harness the role names |
| `backend` | BACKEND | the model backend the seat's environment selects. marvel reads it from Claude Code's backend variables and `ANTHROPIC_BASE_URL`, so on a codex or opencode row it does not describe that harness's provider |
| `login` | LOGIN | the label the role or team declares as `account_label`. marvel does not check it against the sign-in |
| `state` | STATE | where the session is, for example `running`, `limited`, `succeeded` or `crashed` |
| `health` | HEALTH | `unknown`, `alive`, `healthy` or `unhealthy`, sometimes with a note such as `(stalled)` |
| `context` | CTX% | how full the model's context window is |
| `llm` | LLM | the model, when the seat's context reading names one |

`alive` means the process is running in its pane and no further check ran. `healthy` means a check passed. A `-` means there is no reading, which is not the same as zero. A `?` in CTX% means the reading cannot be turned into a percentage.

An interactive opencode seat has no context reading, so its CTX% and LLM cells show `-`. A headless codex seat shows `-` in CTX%.

## Other harnesses

marvel also has a goose adapter. Any other command runs as a generic seat, which marvel starts, replaces and stops without reading its context.

## Not built

- opencode seats report no account windows and no heartbeat.
- Nothing pauses or moves a seat because an account window is full.
- marvel has no sign-in check for codex or opencode, and the `login` column is a label, not a check.

## Your exit

Each harness is the one you installed, running in a plain tmux pane. marvel adds launch arguments and environment variables. A codex seat also gets a private home with a config file marvel writes and a link to your `auth.json`, with codex's startup update check turned off.
