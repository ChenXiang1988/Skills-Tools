# CLI Lifecycle

Read this file only when the task depends on local CLI availability, version, install, or update.

## Version Check

Check current CLI version:

```bash
calicat -V
```

Check whether a new version exists:

```bash
calicat update --check
```

Interpretation:

- if `hasUpdate` is `false`, continue with the current CLI
- if `hasUpdate` is `true`, prefer updating before debugging strange CLI behavior

## Update

Preferred update command:

```bash
calicat update
```

This uses the official installer path behind the scenes.

The CLI may also print a reminder during common commands like:

- `calicat login`
- `calicat status`
- `calicat tools-list`
- `calicat tools-call`

The reminder is informational. It does not silently auto-upgrade.

## Install

If the user does not have `calicat` installed, guide them by platform.

### macOS / Linux

```bash
curl -fsSL https://www.calicat.cn/cli/install.sh | bash
```

### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://www.calicat.cn/cli/install.ps1 | iex"
```

After install, verify:

```bash
calicat --help
calicat -V
```

## Uninstall

### macOS / Linux

```bash
rm -f ~/.local/bin/calicat
rm -rf ~/.calicat-cli
```

### Windows PowerShell

```powershell
Remove-Item "$HOME\\.calicat-cli" -Recurse -Force
Remove-Item "$HOME\\.calicat-cli\\bin\\calicat.exe" -Force -ErrorAction SilentlyContinue
```

If the user only wants to clear auth state:

```bash
calicat logout
```

## Minimal Troubleshooting

If `calicat` exists but behaves unexpectedly:

1. check `calicat -V`
2. run `calicat update --check`
3. if a newer version exists, update first
4. run `calicat status`
5. if auth is stale, run `calicat logout` then `calicat login`
