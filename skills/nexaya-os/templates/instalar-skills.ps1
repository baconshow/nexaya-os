<#
.SYNOPSIS
    Links the skills of your agentic OS into Claude Code on this machine.

.DESCRIPTION
    For every subfolder of the source folder that contains a SKILL.md, creates a
    junction at <Destination>\<name> pointing to it. Editing a skill in the OS
    folder (which syncs between your machines) then works in Claude Code right
    away, with nothing copied.

    Safe to run any number of times:
    - a junction that already points here is left as it is;
    - anything else with the same name (a regular folder, an old copy, a junction
      to another place) is reported and skipped. Nothing is ever deleted.

    No fixed paths: the source defaults to the folder of this script and the
    destination to $HOME\.claude\skills, so the same file works on every machine
    and every user profile. Junctions need no administrator rights.

    Copy this file to <OS root>\Sistema\skills\instalar.ps1 and run it on each
    machine, and again whenever a new skill folder appears. Then open a new
    Claude Code session so it loads the skills.

.PARAMETER Source
    Folder that holds one subfolder per skill. Default: the folder of this script.

.PARAMETER Destination
    Claude Code's user skills folder. Default: $HOME\.claude\skills.

.PARAMETER DryRun
    Only report what would be linked; change nothing.

.EXAMPLE
    pwsh -NoProfile -File "<OS root>\Sistema\skills\instalar.ps1"

.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File "<OS root>\Sistema\skills\instalar.ps1" -DryRun
#>

[CmdletBinding()]
param(
    [string]$Source = $PSScriptRoot,
    [string]$Destination = (Join-Path $HOME '.claude\skills'),
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Get-NormalPath {
    param([string]$Path)
    if ([string]::IsNullOrWhiteSpace($Path)) { return '' }
    # Some junction targets carry the \\?\ prefix; drop it before comparing.
    $plain = $Path -replace '^\\\\\?\\', ''
    return [System.IO.Path]::GetFullPath($plain).TrimEnd('\').ToLowerInvariant()
}

if (-not (Test-Path -LiteralPath $Source -PathType Container)) {
    Write-Error ('Source folder not found: {0}' -f $Source)
    exit 1
}

if (-not (Test-Path -LiteralPath $Destination)) {
    if ($DryRun) {
        Write-Host ('Would create folder: {0}' -f $Destination)
    }
    else {
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        Write-Host ('Folder created: {0}' -f $Destination)
    }
}

$skills = @(Get-ChildItem -LiteralPath $Source -Directory |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') } |
    Sort-Object Name)

if ($skills.Count -eq 0) {
    Write-Warning ('No subfolder with a SKILL.md in {0}.' -f $Source)
    exit 0
}

Write-Host ('Source:      {0}' -f $Source)
Write-Host ('Destination: {0}' -f $Destination)
if ($DryRun) { Write-Host 'Dry run: nothing will be changed.' }
Write-Host ''

$linked = 0
$already = 0
$skipped = 0

foreach ($skill in $skills) {
    $name = $skill.Name
    $target = $skill.FullName
    $link = Join-Path $Destination $name

    # Get-Item -Force also sees a broken junction, which Test-Path does not.
    $existing = Get-Item -LiteralPath $link -Force -ErrorAction SilentlyContinue

    if ($null -eq $existing) {
        if ($DryRun) {
            Write-Host ('  would link   {0}' -f $name)
        }
        else {
            New-Item -ItemType Junction -Path $link -Target $target | Out-Null
            Write-Host ('  linked       {0}' -f $name)
        }
        $linked++
        continue
    }

    $currentTarget = @($existing.Target)[0]
    $pointsHere = ($existing.LinkType -eq 'Junction') -and
        ((Get-NormalPath $currentTarget) -eq (Get-NormalPath $target))

    if ($pointsHere) {
        Write-Host ('  already ok   {0}' -f $name)
        $already++
    }
    else {
        $what = if ($existing.LinkType) {
            '{0} to {1}' -f $existing.LinkType, $currentTarget
        }
        else {
            'a regular folder or file'
        }
        Write-Warning ('{0}: {1} already exists ({2}). Skipped; resolve it by hand if you want this one linked.' -f $name, $link, $what)
        $skipped++
    }
}

Write-Host ''
$verb = if ($DryRun) { 'would be linked' } else { 'linked now' }
Write-Host ('Summary: {0} {1}, {2} already linked, {3} skipped.' -f $linked, $verb, $already, $skipped)
if (-not $DryRun -and $linked -gt 0) {
    Write-Host 'Open a new Claude Code session so it loads the skills.'
}
