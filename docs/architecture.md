# Architecture

field-sidekick is organized around a small typed core and explicit workstation modules.

```text
CLI
 ├─ profile loader (desired state)
 ├─ module registry
 ├─ doctor aggregator
 └─ inventory
      │
      ├─ system module
      ├─ dev module
      ├─ network module
      └─ wireless module
           │
           ├─ PlatformInfo
           └─ CommandRunner
```

## Core principles

1. **Desired state is data.** A profile describes which capabilities belong on the workstation.
2. **Modules own domain knowledge.** CLI code does not know how Docker, Wi-Fi or routing are inspected.
3. **External commands cross one boundary.** `CommandRunner` makes probes deterministic and mockable.
4. **Checks are typed.** Every probe returns `PASS`, `WARN`, `FAIL` or `SKIP` with a useful detail.
5. **Target Kali, develop anywhere.** macOS can run the project/tests; Linux-specific checks degrade to SKIP/WARN.
6. **Mutations are future explicit operations.** Install/apply behavior will be idempotent and opt-in; Iteration 2 remains non-destructive.

The architecture deliberately avoids plugin entry points, event buses and other framework machinery until a real use case requires them.
