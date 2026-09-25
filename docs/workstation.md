# Workstation notes

The bundled `x1-kali-field` profile targets a ThinkPad X1 running Kali Linux. It is a reviewable starting point, not a universal baseline and not a claim that every listed capability is installed automatically.

On Kali/Debian, the profile can currently plan or apply selected apt packages, `uv tool` CLI tools, Docker's system service, Syncthing's user service, and dedicated Firefox profiles (`ai`, `research`, and `burner`). On other systems, unsupported provider entries show `SKIP`; they are not attempted.

The profile also records intentional manual boundaries: vendor repository setup and login for Tailscale, Syncthing folder pairing, AI and editor installation/login, VPN configuration, Obsidian vaults, Magic Wormhole pairing, secrets, device setup, and network changes. Some security and wireless tools are represented as packages; field-sidekick does not run them or direct traffic at any target.

Firefox changes are limited to a marked block in `user.js` for the named dedicated profiles. The managed preferences disable password saving and address/payment autofill. Existing files are retained and unrelated/default profiles are not modified.

Use `field doctor`, `field inventory`, and `field plan` before applying a profile to a machine. The [X1/Kali walkthrough](examples/x1-kali-profile.md) explains how the bundled configuration is composed.
