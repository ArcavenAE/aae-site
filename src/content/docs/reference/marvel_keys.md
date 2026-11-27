---
title: "marvel keys"
description: "Manage SSH keys for marvel clients and the daemon"
---

Manage SSH keys for marvel clients and the daemon

## Synopsis

Manage marvel SSH key material.

Client-side (on your machine, for connecting to a daemon):
  marvel keys generate          # create ~/.marvel/keys/client_ed25519
  marvel keys show              # print your public key (to send to the admin)
  marvel keys list              # list keys under ~/.marvel/keys/
  marvel keys doctor            # audit and fix ~/.marvel/ permissions

Daemon-side (on the machine running marvel daemon):
  marvel keys authorize <file>  # add a client's pubkey (--scope admin|credential-push)
  marvel keys authorized        # list authorized clients and their scope
  marvel keys revoke <fp>       # remove a client by fingerprint
  marvel keys host-fingerprint  # print this daemon's host key fingerprint

## Options inherited from parent commands

```
      --cluster string       named cluster from ~/.marvel/config.yaml
  -i, --identity string      private key file for SSH auth (overrides cluster identity)
      --marvel-home string   marvel's state root, an absolute path (default ~/.marvel); sets $MARVEL_HOME, and the flag wins over the variable
      --socket string        explicit daemon address (overrides --cluster)
```

## SEE ALSO

* [marvel](/reference/marvel/)	 - Agent orchestration control plane
* [marvel keys authorize](/reference/marvel_keys_authorize/)	 - Authorize a client's public key on this daemon
* [marvel keys authorized](/reference/marvel_keys_authorized/)	 - List clients authorized on this daemon
* [marvel keys doctor](/reference/marvel_keys_doctor/)	 - Audit (and optionally fix) permissions under ~/.marvel/
* [marvel keys generate](/reference/marvel_keys_generate/)	 - Generate a new client keypair under ~/.marvel/keys/
* [marvel keys host-fingerprint](/reference/marvel_keys_host-fingerprint/)	 - Print this daemon's SSH host key fingerprint
* [marvel keys list](/reference/marvel_keys_list/)	 - List client keypairs under ~/.marvel/keys/
* [marvel keys revoke](/reference/marvel_keys_revoke/)	 - Revoke a client by fingerprint
* [marvel keys show](/reference/marvel_keys_show/)	 - Print a client public key (to share with the daemon admin)
* [marvel keys trust](/reference/marvel_keys_trust/)	 - Trust and record a cluster's host key in ~/.marvel/known_hosts
