---
title: "marvel"
description: "Agent orchestration control plane"
---

Agent orchestration control plane

## Synopsis

Agent orchestration control plane

## Options

```
      --cluster string       named cluster from ~/.marvel/config.yaml
  -i, --identity string      private key file for SSH auth (overrides cluster identity)
      --marvel-home string   marvel's state root, an absolute path (default ~/.marvel); sets $MARVEL_HOME, and the flag wins over the variable
      --socket string        explicit daemon address (overrides --cluster)
```

## SEE ALSO

* [marvel attach](/reference/marvel_attach/)	 - Open a session's tmux pane by desk number, session key or name
* [marvel backend](/reference/marvel_backend/)	 - Inspect the model backend sessions are running on
* [marvel bus](/reference/marvel_bus/)	 - Inspect the cluster's message bus
* [marvel capture](/reference/marvel_capture/)	 - Capture a session's pane content
* [marvel config](/reference/marvel_config/)	 - Manage marvel cluster configuration
* [marvel converge](/reference/marvel_converge/)	 - Release a team (or all teams) from the start-line hold and converge to desired
* [marvel credential](/reference/marvel_credential/)	 - Manage bus credentials the daemon holds (transient, never persisted)
* [marvel daemon](/reference/marvel_daemon/)	 - Start the marvel daemon
* [marvel delete](/reference/marvel_delete/)	 - Delete a resource
* [marvel describe](/reference/marvel_describe/)	 - Show detailed information about a resource, or the daemon that answers
* [marvel doctor](/reference/marvel_doctor/)	 - Check this host for what a first run needs
* [marvel events](/reference/marvel_events/)	 - List recent session/team state-transition events
* [marvel example](/reference/marvel_example/)	 - Print a manifest the binary carries
* [marvel exposure](/reference/marvel_exposure/)	 - Record, end or void the functions a slot has read (the clean-room exposure gate)
* [marvel get](/reference/marvel_get/)	 - List resources (sessions, teams, workspaces, endpoints, policies, credentials, budgets, account-readings, account-logins, vitals)
* [marvel handoff](/reference/marvel_handoff/)	 - Hand a seat's work to its successor through the daemon
* [marvel hibernate](/reference/marvel_hibernate/)	 - Sign off the named teams, end every seat, and hold the teams until a wake
* [marvel inject](/reference/marvel_inject/)	 - Send keystrokes to a session's pane (executive privilege)
* [marvel keys](/reference/marvel_keys/)	 - Manage SSH keys for marvel clients and the daemon
* [marvel kill](/reference/marvel_kill/)	 - Kill a session (alias for delete session)
* [marvel mcp](/reference/marvel_mcp/)	 - MCP servers marvel offers to its seats
* [marvel orphans](/reference/marvel_orphans/)	 - List agents heartbeating against session keys this daemon owns with a stale token
* [marvel plan](/reference/marvel_plan/)	 - Preview the convergence delta per team without spawning (dry run)
* [marvel reap](/reference/marvel_reap/)	 - List (and with --confirm, destroy) marvel tmux state the daemon does not own
* [marvel reset-health](/reference/marvel_reset-health/)	 - Clear a role's crash-loop restart count and backoff without deleting the team
* [marvel resume](/reference/marvel_resume/)	 - Resume a suspended cluster
* [marvel run](/reference/marvel_run/)	 - Run a one-off agent session
* [marvel run-sandboxed](/reference/marvel_run-sandboxed/)	 - Run a command under a sandbox profile the daemon composes, outside this seat's own profile
* [marvel scale](/reference/marvel_scale/)	 - Scale a team role to N replicas
* [marvel shift](/reference/marvel_shift/)	 - Initiate a rolling shift for a team
* [marvel status](/reference/marvel_status/)	 - Say whether the cluster is running or suspended
* [marvel stop](/reference/marvel_stop/)	 - Stop the marvel daemon, leaving agents running
* [marvel suspend](/reference/marvel_suspend/)	 - Freeze every seat and the tmux server in place
* [marvel upgrade](/reference/marvel_upgrade/)	 - Upgrade marvel to the latest version
* [marvel version](/reference/marvel_version/)	 - Print marvel version and channel
* [marvel view](/reference/marvel_view/)	 - Work with a seat's read-only views
* [marvel wait](/reference/marvel_wait/)	 - Wait for a session to finish (experimental)
* [marvel wake](/reference/marvel_wake/)	 - Bring hibernated teams back, supervisors first
* [marvel work](/reference/marvel_work/)	 - Load a manifest and reconcile desired state
