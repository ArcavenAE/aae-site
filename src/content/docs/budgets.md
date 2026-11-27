---
title: See what your agents spend, and cap it
description: Account limit windows and estimated cost beside each seat, a warning near a limit, and a team budget that refuses a spawn.
---

marvel, an ArcavenAE part, shows how much of each account's rate limit your agents have used, and refuses to start more of them past a ceiling you declare. This is the budgets story in Dark Atelier.

## The need

You do not know how close your agents are to a plan limit, or what they cost, until they stop.

## What is built

| Capability | State |
|---|---|
| One session view with account windows, estimated cost and context | built |
| History of account readings | built |
| Event when an account window nears its limit | built, report only |
| Team caps on sessions and tokens, refused at spawn | built |
| Replacing a seat that is running low on context | built, once the role declares it |
| A dollar cap | not built |
| Pausing or refusing work because of an account window | not built |

## The view

```sh
marvel get sessions --columns team,role,account,5h,7d,7d-reset,cost,context,llm
```

Add `-w` to keep it live. See [marvel get](/reference/marvel_get/).

| Column | Header | What it shows |
|---|---|---|
| `team` | TEAM | the seat's team |
| `role` | ROLE | the seat's role |
| `account` | ACCOUNT | the account the reading belongs to: the display name set in `display.account_names`, else the label the role declared, else a short key |
| `5h` | 5H% | percent used of the five-hour window |
| `7d` | 7D% | percent used of the seven-day window |
| `7d-reset` | 7D-RESET | time until the seven-day window resets, as `+2d3h` or `+47m`; `now` once it has passed |
| `cost` | COST | Claude Code's own running cost total, marked `~`: a list-price estimate and not a bill. Under a subscription it measures usage, not money |
| `context` | CTX% | how full the model's context window is |
| `llm` | LLM | the model the seat is talking to |

A `-` means there is no reading, which is not the same as zero. A `?` after a window percentage means the reading is stale and the number is the last one seen. A `?` in CTX% means the model's window size is unknown. Add the `read` column to see how old each account reading is.

The account windows and the cost come from the harness. An interactive claude seat reports them once its runtime sets `context_feed = "statusline"`, when Claude Code includes them in its status data. A codex seat reports account windows through marvel's codex hook. COST is filled for claude seats on that feed only. Seats that share an account repeat the same window figures, so do not add them up.

## Reading history

```sh
marvel get account-readings
marvel get account-readings --since 1h -o json
```

Each reading carries the account, the window, the percent used, the reset time, when it was observed and the session that reported it. The daemon keeps readings for eight days, across restarts. `--account` filters by account key. Your provider's own usage page stays the authority.

## A warning near the limit

marvel records an `account.window-near-limit` event when an account window reaches the cluster's warning level, once per window. The level is `account_warn_percent` on the cluster's entry in the daemon host's `~/.marvel/config.yaml`. It defaults to 80, and 0 turns it off. A daemon restart can report the same window again. The event is a report: nothing pauses or refuses because of it.

```sh
marvel events --kind account.window-near-limit
```

## A ceiling on what a team starts

A team with a `budget` block is refused a spawn that would cross it. A team without one has no gate. This is marvel's [budget example](https://github.com/ArcavenAE/marvel/blob/main/examples/demo-act4-budget.toml) without its comments. It runs `sleep` in place of an agent, so it needs no model login:

```toml
[workspace]
name = "fanout"

[[team]]
name = "crew"

  [team.budget]
  max_sessions = 6

  [[team.role]]
  name = "crew"
  replicas = 3

    [team.role.runtime]
    image = "generic"
    command = "sleep"
    args = ["3600"]
```

From a marvel source checkout, apply it, then ask for more than the ceiling allows:

```sh
marvel work examples/demo-act4-budget.toml
marvel scale fanout/crew --role crew --replicas 40
marvel get budgets
marvel events --kind admission.refused
```

The scale asks for 40 replicas under a ceiling of 6, so marvel refuses it, names the arithmetic and leaves the team as it was.

Two ceilings are enforced:

- `max_sessions` counts every live session of the team, including ones started with `marvel run`. A manifest that declares more replicas than the ceiling is refused when it is read. A shift is exempt, so a role can run up to twice its replicas while the new generation starts.
- `max_tokens` counts prompt, output and reasoning tokens, and only from seats marvel can meter: headless claude, codex and opencode runs. An interactive seat does not count toward it. A team where no role can report is refused at apply time. The count lives in the daemon's memory, so it starts over when the daemon restarts. `on_unmeasured` says what happens while the meter has no answer yet: `admit` (the default, recorded as an event) or `refuse`.

Scaling down is never refused, and neither is replacing a crashed replica.

## Acting before the context limit

A role can replace a seat that is running low on context. marvel asks the seat to write a handoff, waits for the marker, and then starts the successor. A seat that has not written its handoff keeps running.

```toml
[team.role.shift]
handoff = "~/.marvel-handoffs/{session}.md"
handoff_marker = "END HANDOFF"
handoff_window = "5m"
any = [
  { on = "context-pressure", headroom_tokens = 120000 },
]
```

The condition needs a context reading for the seat, so an interactive claude seat needs the statusline feed here too. It watches the context window, not the account window. See [marvel shift](/reference/marvel_shift/) for the same replacement by hand.

## Not built

- There is no dollar cap. A manifest that sets `max_cost_usd`, `max_team_rss_bytes` or `max_session_ctx_percent` is refused when it is read, because those ceilings are not enforced.
- Nothing acts on an account window. marvel reports it, and a person or a supervisor decides.
