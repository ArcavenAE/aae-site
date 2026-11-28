---
title: Hand off to a fresh agent before the context runs out
description: A role declares a handoff file. marvel asks the seat for it as context runs low or the seat ages, and starts a successor once it is written.
---

marvel, an ArcavenAE part, asks a running agent to write down where it is, waits for that file, and then replaces the agent with a successor. This is the handoff story in Dark Atelier.

## The need

Your agent hits its context limit, or your plan limit, in the middle of the work, and the new session starts from nothing.

## What is built

| Capability | State |
|---|---|
| Asking for a handoff when a seat's context runs low | built, once the role declares it |
| Asking for a handoff when a seat reaches an age | built, for a role with one replica |
| Asking by hand with `marvel shift` | built |
| Replacing the seat only after it writes the handoff | built, once the role declares it; `--no-handoff` skips it |
| Naming the handoff in the successor's first message | built for claude |
| A trigger on a plan's usage limit | not built |
| Replacing one seat of a role that has several | not built |

This page was written from marvel's code and docs at commit `38e5b403`. It is read, not measured: no shift was run for it.

## Declare the handoff

A shift replaces a role's agents with new ones. This is the runtime and shift part of a role, taken from marvel's [max-age example](https://github.com/ArcavenAE/marvel/blob/38e5b4039b76f20176d5cd45a507b0257b23691e/examples/auto-shift-max-age.toml) without its comments:

```toml
    [team.role.runtime]
    image = "claude"
    command = "claude"
    context_window = 1000000
    context_feed = "statusline"

    [team.role.shift]
    handoff = "~/.marvel-handoffs/{session}.md"
    handoff_marker = "END HANDOFF"
    handoff_window = "5m"
    any = [
      { on = "context-pressure", headroom_tokens = 120000 },
      { on = "max-age", max_age = "8h", quiet_for = "5m", max_defer = "30m" },
    ]
```

| Key | What it does |
|---|---|
| `handoff` | the file the seat writes. `{session}` becomes the seat's session name. The path is absolute or starts with `~/` |
| `handoff_marker` | the line that says the file is finished, as its last non-empty line |
| `handoff_window` | how long marvel waits for the file. It defaults to 5 minutes |
| `on = "context-pressure"` | asks when the seat's remaining context falls below `headroom_tokens` |
| `on = "max-age"` | asks when the seat is older than `max_age`, which is at least 15 minutes. It waits for a pause of `quiet_for`, and asks anyway once `max_defer` has also passed |

The context condition needs `handoff` and `handoff_marker`, and a context reading for the seat. An interactive claude seat reports one through `context_feed = "statusline"`. The age condition is refused on a headless role and on a role with more than one replica.

Support differs by harness. marvel's [feature matrix](https://github.com/ArcavenAE/marvel/blob/38e5b4039b76f20176d5cd45a507b0257b23691e/docs/feature-matrix.md) marks the context condition as partial for codex and opencode, and records no end-to-end measurement of the age condition with a claude seat.

The seat normally writes the file itself, so the role's permissions have to allow that write. A seat that cannot write files on the daemon's host, but can run a command, can use [marvel handoff put](/reference/marvel_handoff_put/).

Apply the manifest with [marvel work](/reference/marvel_work/). The [two-minute page](/e1-tour/) shows how to start the daemon.

## What happens

1. A condition holds. marvel creates the handoff's directory, types a request into the seat's pane with the path, the marker and the window, and records `team.shift-handoff-requested`.
2. The seat writes the file. It counts when it is a regular file and not a symlink, was written after the request, has text above the marker, and ends with the marker line.
3. marvel starts the successor, with the old seat's key in `MARVEL_PREDECESSOR`. For an interactive claude role whose `command` is the bare `claude`, the successor also gets a first message that names the predecessor and the handoff path, unless the role sets `successor_prompt = false`.
4. Once the successor is ready, marvel stops the old seat. Ready does not show that the successor has read the handoff: with no health check it means only that the session is running.

If the window ends without the file, the old seat keeps running. marvel records `team.shift-handoff-missing`, repeats it, and leaves the decision to you or the team's supervisor. A handoff written after that does not start the shift. To go ahead anyway, run `marvel shift <workspace/team> --role <role> --no-handoff`.

## By hand

```sh
marvel shift <workspace/team> --role <role>
```

For a role that declares a handoff, this asks for it first and shifts once it is written. A shift of the whole team is refused while a role in it declares a handoff, so name the role or pass `--no-handoff`. A role that declares no handoff shifts at once. See [marvel shift](/reference/marvel_shift/).

## The view

```sh
marvel get sessions --columns team,role,generation,state,context,age,last-active,llm,rss
```

Add `-w` to keep it live. See [marvel get](/reference/marvel_get/).

| Column | Header | What it shows |
|---|---|---|
| `team` | TEAM | the seat's team |
| `role` | ROLE | the seat's role |
| `generation` | GEN | the seat's generation, which a shift raises |
| `state` | STATE | where the session is, for example `running` or `crashed` |
| `context` | CTX% | how full the model's context window is |
| `age` | AGE | time since the session was created |
| `last-active` | LAST-ACTIVE | time since the seat last showed work. A seat in a long tool call reads quiet |
| `llm` | LLM | the model the seat is talking to |
| `rss` | RSS | resident memory of the seat's whole process tree, on macOS and Linux |

A `-` means there is no reading, which is not the same as zero. A trailing `*` on LAST-ACTIVE marks a value reported by the statusline or a heartbeat, which is weaker evidence than token flow.

The record of a shift is in the events:

```sh
marvel events --kind team.shift-handoff-requested
marvel events --kind team.shift-autotriggered
marvel events --kind team.shift-handoff-missing
```

See [marvel events](/reference/marvel_events/).

## At a usage limit

No shift condition watches your plan's limits. marvel reports account windows and records an event when one nears its warning level, as the [budgets page](/budgets/) describes, and nothing shifts on it. If you act on that warning, ask for the shift by hand while the seat still has usage left, because the seat writes the handoff itself. The successor is built from the same role declaration, so a shift does not by itself move the work to another login.

## Not built

- There is no usage-limit trigger, and nothing moves a team to another account on its own.
- On a role with more than one replica, a shift asks one seat for a handoff and then replaces every seat of the role. Replacing only the seat that was asked is not built.

## Your exit

The handoff is a plain file at the path you declared, so any editor, or a new session outside marvel, can read it. A role with no shift table is never shifted automatically.
