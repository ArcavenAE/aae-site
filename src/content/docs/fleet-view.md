---
title: See every agent on every cluster in one view
description: One command reads the sessions of several marvel clusters and prints them as one table.
---

marvel, an ArcavenAE part, reads the sessions of several clusters in one command and prints them as one table. This is the fleet view story in Dark Atelier.

## The need

Agents spread over several machines get checked one machine at a time, so a stalled or logged-out seat waits until someone looks at its host.

## What is built

| Capability | State |
|---|---|
| One merged session table across clusters, once or live | built |
| Host memory readings across clusters | built, for clusters that turn them on |
| A load rollup per team on one cluster (`get teams --load`) | built |
| A load rollup per team across clusters | [designed](https://github.com/ArcavenAE/marvel/blob/main/docs/design/team-load-rollup.md), not built |

## Name your clusters

Each cluster is one daemon, listed in your `~/.marvel/config.yaml`:

```sh
marvel config add-cluster <name> mrvl://<host>
marvel config list
```

A remote daemon needs its `mrvl://` listener on and your public key authorized. marvel's [keys guide](https://github.com/ArcavenAE/marvel/blob/main/docs/keys.md) has the steps. See also [marvel config add-cluster](/reference/marvel_config_add-cluster/).

A second machine is not required. Two daemons on one machine, each with its own `HOME`, can both be added by their socket paths.

## The view

```sh
marvel get sessions --all-clusters --columns cluster,team,role,state,health,context,active,llm,rss
```

`--cluster a,b` reads only the clusters you name, and `-w` keeps the table live.

| Column | Header | What it shows |
|---|---|---|
| `cluster` | CLUSTER | the cluster the row came from |
| `team` | TEAM | the seat's team |
| `role` | ROLE | the seat's role |
| `state` | STATE | where the session is, for example `running`, `limited` or `crashed` |
| `health` | HEALTH | `unknown`, `alive`, `healthy` or `unhealthy`, with a note such as `(stalled)` or `(logged-out)` when marvel sees one |
| `context` | CTX% | how full the model's context window is |
| `active` | ACTIVE% | the share of the last 15 minutes the seat was not quiet |
| `llm` | LLM | the model the seat is talking to |
| `rss` | RSS | resident memory of the seat's whole process tree, on macOS and Linux |

`alive` means the process is running in its pane and no further check ran. `healthy` means a check passed. A `-` means there is no reading, which is not the same as zero.

For a claude seat on the statusline feed, ACTIVE% is provisional: it is the share of time spent waiting on model responses, so a seat in a long build can read near 0%. A trailing `*` marks a value reported by the statusline or a heartbeat, which is weaker evidence than token flow.

The column list decides what prints, so keep `cluster` in it. Without it the rows do not say where they came from.

## How the read behaves

- It only reads. Every command that changes something still names one cluster.
- Clusters are read in parallel, each under its own 10 second timer. One that fails does not hide the rows of the others.
- Each cluster's outcome is reported, for example `answered`, `unreachable`, `no_answer_in_time` or `auth_refused`. On a terminal, or with `--header`, a summary table above the sessions covers the clusters that answered, with a total row; the rest keep a status line each.
- The exit code is 0 when every cluster answered and 10 when only some did. See [marvel get](/reference/marvel_get/) for the other codes and the `-o json` form.
- Run it from your own shell. It is refused inside a marvel seat, and it cannot be combined with `--socket` or `--identity`.

## Host memory across clusters

```sh
marvel get vitals --all-clusters
```

This prints each host's memory and swap readings, for clusters whose entry in the daemon host's `~/.marvel/config.yaml` sets `host_vitals: true`. marvel reports the readings and does not act on them.

## Not built

- There is no per-team rollup across clusters. `marvel get teams --load` reads the one daemon you reach.
- `--all-clusters` applies to `get sessions` and `get vitals`.
