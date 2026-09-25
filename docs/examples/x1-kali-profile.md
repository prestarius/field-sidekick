# X1/Kali profile walkthrough

[`configs/profiles/x1-kali.yaml`](../../configs/profiles/x1-kali.yaml) is the bundled top-level profile. It names the ThinkPad X1/Kali target, enables the local diagnostic module settings, and composes focused components through `include`.

The package components establish the baseline: `core`, `dev`, `networking`, `wireless`, `security`, and `esp32`. App components then record tool-specific state: AI intent, Tailscale, Syncthing, Firefox, Obsidian, OPSEC notes, Magic Wormhole, and editors.

Composition keeps the top-level profile short and makes scoped planning useful:

```bash
uv run field plan dev
uv run field plan wireless
uv run field plan firefox
```

The profile does not mean every listed capability is automatically installed. Apt package records are actionable on a supported Linux target. The `dev` component can also install PlatformIO through `uv tool` and enable Docker. Syncthing's package and user service are actionable, while folder pairing is manual. The Firefox component can create the dedicated `ai`, `research`, and `burner` profiles and write only its marked preference block.

Tailscale vendor setup/login, AI tools, editor setup, VPNs, hardware setup, and other account- or device-bound tasks stay `MANUAL`. Before adapting this profile, read [configuration](../configuration.md), then copy only the components appropriate to your workstation.
