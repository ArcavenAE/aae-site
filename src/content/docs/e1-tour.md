---
title: marvel in two minutes
description: Declare a team, let marvel make it true, lose a session, scale a role and shift the team.
---

This page is a placeholder for the step-through of marvel's core loop. It runs
on the simulator, so it needs no model login. The steps below are the main
commands the recorded tour types, in the order it types them, with one
exception noted at step 3; the text each step prints will come from the tour's
plain-text transcript once the page reads it.

The tour needs a marvel source checkout for `examples/tour.toml`. See the
[marvel repository](https://github.com/ArcavenAE/marvel) for the tour and its
recording.

1. Start the daemon: `marvel daemon`. See [marvel daemon](/reference/marvel_daemon/).
2. Make the manifest true: `marvel work examples/tour.toml`. See [marvel work](/reference/marvel_work/).
3. Watch the team: `marvel get sessions -w 1`. The recording starts this in its top pane before the daemon, so the pane is ready; it runs alongside the steps below. See [marvel get](/reference/marvel_get/).
4. Lose a session: `marvel kill demo/crew-worker-g1-1`. See [marvel kill](/reference/marvel_kill/).
5. Scale a role: `marvel scale demo/crew --role worker --replicas 5`. See [marvel scale](/reference/marvel_scale/).
6. Shift to a new generation: `marvel shift demo/crew`. See [marvel shift](/reference/marvel_shift/).
7. Read the record: `marvel events`. See [marvel events](/reference/marvel_events/).
8. Start a one-off session: `marvel run claude`. See [marvel run](/reference/marvel_run/).
9. Print the command that opens its pane: `marvel attach --print <desk>`. See [marvel attach](/reference/marvel_attach/).
10. Tear down: `marvel stop --teardown`. See [marvel stop](/reference/marvel_stop/).
