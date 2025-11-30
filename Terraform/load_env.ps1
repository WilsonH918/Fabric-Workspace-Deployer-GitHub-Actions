# Load environment variables from .env file (PowerShell)
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*#') { return }      # skip comments
    if ($_ -match '^\s*$') { return }      # skip blanks
    $pair = $_ -split '=', 2
    $key = $pair[0].Trim()
    $value = $pair[1].Trim('"').Trim()
    [System.Environment]::SetEnvironmentVariable($key, $value, 'Process')
    Write-Host "Loaded $key"
}
Write-Host "`nEnvironment variables loaded for Terraform (process scope)."