---
title: "marvel config"
description: "Manage marvel cluster configuration"
---

Manage marvel cluster configuration

## Synopsis

Manage marvel cluster configuration

## Options inherited from parent commands

```
      --cluster string       named cluster from ~/.marvel/config.yaml
  -i, --identity string      private key file for SSH auth (overrides cluster identity)
      --marvel-home string   marvel's state root, an absolute path (default ~/.marvel); sets $MARVEL_HOME, and the flag wins over the variable
      --socket string        explicit daemon address (overrides --cluster)
```

## SEE ALSO

* [marvel](/reference/marvel/)	 - Agent orchestration control plane
* [marvel config add-cluster](/reference/marvel_config_add-cluster/)	 - Add or update a cluster
* [marvel config current](/reference/marvel_config_current/)	 - Show the current cluster
* [marvel config list](/reference/marvel_config_list/)	 - List configured clusters
* [marvel config remove-cluster](/reference/marvel_config_remove-cluster/)	 - Remove a cluster
* [marvel config repoint](/reference/marvel_config_repoint/)	 - Move a cluster to a new address, carrying its host key trust over when the key matches
* [marvel config tmux-server](/reference/marvel_config_tmux-server/)	 - Print the tmux server name this HOME's daemon uses
* [marvel config use-cluster](/reference/marvel_config_use-cluster/)	 - Set the current cluster
