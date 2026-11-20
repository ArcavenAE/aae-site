---
title: "marvel credential"
description: "Manage bus credentials the daemon holds (transient, never persisted)"
---

Manage bus credentials the daemon holds (transient, never persisted)

## Synopsis

Manage bus credentials the daemon holds (transient, never persisted)

## Options inherited from parent commands

```
      --cluster string       named cluster from ~/.marvel/config.yaml
  -i, --identity string      private key file for SSH auth (overrides cluster identity)
      --marvel-home string   marvel's state root, an absolute path (default ~/.marvel); sets $MARVEL_HOME, and the flag wins over the variable
      --socket string        explicit daemon address (overrides --cluster)
```

## SEE ALSO

* [marvel](/reference/marvel/)	 - Agent orchestration control plane
* [marvel credential delete](/reference/marvel_credential_delete/)	 - Delete a credential (its value is zeroed)
* [marvel credential get](/reference/marvel_credential_get/)	 - Show a credential's metadata, or its value with --reveal (local socket only, and only when this cluster's config entry sets allow_credential_reveal: true)
* [marvel credential list](/reference/marvel_credential_list/)	 - List credentials (metadata only)
* [marvel credential put](/reference/marvel_credential_put/)	 - Push a bus credential to the daemon (value from --value-file, or - for stdin)
