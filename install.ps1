param(
  [ValidateSet('generic','claude','claude-skill','copilot','chatgpt','openai','codex','openai-plugin','claude-plugin','release')]
  [string]$HostName = 'generic',
  [string]$Destination = ''
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Build = Join-Path $Root 'dist/marketing-council'
$Release = Join-Path $Root 'dist/release'
$Version = (Get-Content (Join-Path $Root 'manifest.json') -Raw | ConvertFrom-Json).version

if ($HostName -in @('chatgpt','openai','codex','openai-plugin','claude-plugin','release')) {
  python (Join-Path $Root 'scripts/build_host_packages.py') --output-root $Release | Out-Null
  if ($HostName -eq 'claude-plugin') {
    Write-Output (Join-Path $Release ("marketing-council-claude-marketplace-v$Version.zip"))
  } elseif ($HostName -eq 'release') {
    Write-Output $Release
  } else {
    Write-Output (Join-Path $Release ("marketing-council-openai-plugin-v$Version.zip"))
  }
  exit 0
}

python (Join-Path $Root 'scripts/build_dist.py') --output $Build | Out-Null

if (-not $Destination) {
  switch ($HostName) {
    'claude' { $Destination = Join-Path $HOME '.claude/skills' }
    'claude-skill' { $Destination = Join-Path $HOME '.claude/skills' }
    'copilot' { $Destination = Join-Path $HOME '.copilot/skills' }
    default { $Destination = Join-Path $HOME '.agents/skills' }
  }
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$Target = Join-Path $Destination 'marketing-council'
if (Test-Path $Target) { Remove-Item $Target -Recurse -Force }
Copy-Item $Build $Target -Recurse
Write-Output $Target
