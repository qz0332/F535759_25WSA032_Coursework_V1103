# powershell -ExecutionPolicy Bypass -File .\powershell\PS_prompt.ps1
function prompt {
    "$(Split-Path -Leaf (Get-Location))> "
}

