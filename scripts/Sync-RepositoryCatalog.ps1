[CmdletBinding()]
param(
    [string]$Root,
    [switch]$Pull,
    [string]$JsonPath,
    [switch]$IncludeHidden
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Root)) {
    $Root = Split-Path -Parent $PSScriptRoot
}

function Invoke-RepoGit {
    param(
        [Parameter(Mandatory)] [string]$RepositoryPath,
        [Parameter(Mandatory)] [string[]]$GitArguments
    )

    $normalizedPath = $RepositoryPath.Replace('\', '/')
    $previousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $lines = @(& git -c "safe.directory=$normalizedPath" -C $normalizedPath @GitArguments 2>&1)
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
    }

    $safeText = ((($lines | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine).Trim()) -replace '(?i)(https?://)[^/\s@]+@', '$1***@'

    [pscustomobject]@{
        ExitCode = $exitCode
        Text     = $safeText
    }
}

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$repositories = Get-ChildItem -LiteralPath $resolvedRoot -Directory -Force |
    Where-Object {
        (Test-Path -LiteralPath (Join-Path $_.FullName '.git')) -and
        ($IncludeHidden -or -not $_.Name.StartsWith('.'))
    } |
    Sort-Object Name

$results = foreach ($repository in $repositories) {
    $repositoryPath = $repository.FullName
    $status = Invoke-RepoGit -RepositoryPath $repositoryPath -GitArguments @('status', '--porcelain')
    $branch = Invoke-RepoGit -RepositoryPath $repositoryPath -GitArguments @('branch', '--show-current')
    $upstream = Invoke-RepoGit -RepositoryPath $repositoryPath -GitArguments @('rev-parse', '--abbrev-ref', '@{upstream}')
    $origin = Invoke-RepoGit -RepositoryPath $repositoryPath -GitArguments @('remote', 'get-url', 'origin')
    $headBefore = Invoke-RepoGit -RepositoryPath $repositoryPath -GitArguments @('rev-parse', 'HEAD')
    $shallow = Invoke-RepoGit -RepositoryPath $repositoryPath -GitArguments @('rev-parse', '--is-shallow-repository')

    $dirtyFiles = if ($status.Text) {
        @($status.Text -split '\r?\n')
    }
    else {
        @()
    }

    $action = 'inspected'
    $message = ''
    $headAfter = $headBefore.Text

    if ($Pull) {
        if ($status.ExitCode -ne 0) {
            $action = 'failed'
            $message = $status.Text
        }
        elseif ($dirtyFiles.Count -gt 0) {
            $action = 'skipped-dirty'
            $message = "$($dirtyFiles.Count) local change(s)"
        }
        elseif ($upstream.ExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($upstream.Text)) {
            $action = 'skipped-no-upstream'
            $message = 'current branch has no upstream'
        }
        else {
            Write-Host "[$($repository.Name)] git pull --ff-only --prune"
            $pullResult = Invoke-RepoGit -RepositoryPath $repositoryPath -GitArguments @('pull', '--ff-only', '--prune')
            $headAfterResult = Invoke-RepoGit -RepositoryPath $repositoryPath -GitArguments @('rev-parse', 'HEAD')
            $headAfter = $headAfterResult.Text
            $message = $pullResult.Text

            if ($pullResult.ExitCode -ne 0) {
                $action = 'failed'
            }
            elseif ($headBefore.Text -eq $headAfter) {
                $action = 'current'
            }
            else {
                $action = 'updated'
            }
        }
    }

    [pscustomobject]@{
        Repository  = $repository.Name
        Path        = $repositoryPath
        Origin      = $origin.Text
        Branch      = $branch.Text
        Upstream    = if ($upstream.ExitCode -eq 0) { $upstream.Text } else { '' }
        Shallow     = ($shallow.Text -eq 'true')
        DirtyFiles  = $dirtyFiles.Count
        HeadBefore  = $headBefore.Text
        HeadAfter   = $headAfter
        Action      = $action
        Message     = $message
    }
}

$summary = $results | Group-Object Action | Sort-Object Name
Write-Output "Repositories: $($results.Count)"
$summary | ForEach-Object { Write-Output ("{0}: {1}" -f $_.Name, $_.Count) }

$notable = @($results | Where-Object { $_.Action -in @('updated', 'failed', 'skipped-dirty', 'skipped-no-upstream') })
if ($notable.Count -gt 0) {
    Write-Output ''
    $notable |
        Select-Object Repository, Action, Branch, DirtyFiles, HeadBefore, HeadAfter |
        Format-Table -AutoSize
}

if ($JsonPath) {
    $resolvedJsonPath = if ([System.IO.Path]::IsPathRooted($JsonPath)) {
        $JsonPath
    }
    else {
        Join-Path $resolvedRoot $JsonPath
    }

    $jsonDirectory = Split-Path -Parent $resolvedJsonPath
    if ($jsonDirectory -and -not (Test-Path -LiteralPath $jsonDirectory)) {
        New-Item -ItemType Directory -Path $jsonDirectory -Force | Out-Null
    }

    $results | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $resolvedJsonPath -Encoding UTF8
    Write-Output "JSON: $resolvedJsonPath"
}
