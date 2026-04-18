# ============================================
# setup-venv.ps1 — Managed-PC Safe Version
# No activation. No blocked scripts. 100% VS Code driven.
# Run using terminal:
# powershell -ExecutionPolicy Bypass -File .\powershell\setup-venv.ps1
# ============================================

# 1. Detect project root
$ProjectRoot = Get-Location
$ProjectName = Split-Path $ProjectRoot -Leaf

Write-Host "Project: $ProjectName"
Write-Host "Root:    $ProjectRoot"

# 2. Build venv path
$VenvRoot = Join-Path $env:LOCALAPPDATA "venvs"
$VenvPath = Join-Path $VenvRoot $ProjectName

Write-Host "`nCreating venv in:"
Write-Host "  $VenvPath"

New-Item -ItemType Directory -Force -Path $VenvRoot | Out-Null

# 3. Create venv
python -m venv $VenvPath

if (-not (Test-Path (Join-Path $VenvPath "Scripts/python.exe"))) {
    Write-Host "`nERROR: Venv creation failed." -ForegroundColor Red
    exit 1
}

Write-Host "`nVenv created successfully."

# 4. Configure VS Code
$VSCodeDir = Join-Path $ProjectRoot ".vscode"
New-Item -ItemType Directory -Force -Path $VSCodeDir | Out-Null

$SettingsFile = Join-Path $VSCodeDir "settings.json"
$Interpreter = Join-Path $VenvPath "Scripts/python.exe"

$Settings = @{
    "python.defaultInterpreterPath" = $Interpreter
}

$Settings | ConvertTo-Json | Set-Content $SettingsFile -Encoding UTF8

Write-Host "`nVS Code interpreter set to:"
Write-Host "  $Interpreter"

# 5. Final message
Write-Host "`nSetup complete!"
Write-Host "Open VS Code and everything will automatically use the venv."
Write-Host "No activation required."