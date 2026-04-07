$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

if (Test-Path ".\.env") {
  # Minimal .env loader (KEY=VALUE, ignores comments/blank lines)
  Get-Content ".\.env" | ForEach-Object {
    $line = $_.Trim()
    if ($line.Length -eq 0) { return }
    if ($line.StartsWith("#")) { return }
    $idx = $line.IndexOf("=")
    if ($idx -lt 1) { return }
    $key = $line.Substring(0, $idx).Trim()
    $val = $line.Substring($idx + 1).Trim()
    [Environment]::SetEnvironmentVariable($key, $val, "Process")
  }
}

python .\scripts\update_iran_timer.py

