param(
    [Parameter(Mandatory = $true)][string]$AdminEmail,
    [Parameter(Mandatory = $true)][string]$AdminPassword
)

$ErrorActionPreference = 'Stop'
$mysqlCommand = Get-Command mysql.exe -ErrorAction SilentlyContinue
$mysqlExe = if ($mysqlCommand) { $mysqlCommand.Source } else { 'D:\tools\mysql-8.0.36-winx64\bin\mysql.exe' }
$dotnetCommand = Get-Command dotnet.exe -ErrorAction SilentlyContinue
$dotnetExe = if ($dotnetCommand) { $dotnetCommand.Source } else { Join-Path $env:USERPROFILE '.dotnet\dotnet.exe' }

if (-not (Test-Path -LiteralPath $mysqlExe)) { throw 'mysql.exe was not found. Add MySQL bin to PATH or update this script.' }
if (-not (Test-Path -LiteralPath $dotnetExe)) { throw '.NET SDK was not found. Install .NET 8 SDK and add dotnet.exe to PATH.' }
if ([string]::IsNullOrWhiteSpace($AdminEmail) -or [string]::IsNullOrWhiteSpace($AdminPassword)) { throw 'Provide a staff email and a strong admin password.' }

$dbPassword = [Guid]::NewGuid().ToString('N')
$sql = "CREATE USER IF NOT EXISTS 'ccn_app'@'localhost' IDENTIFIED BY '$dbPassword'; ALTER USER 'ccn_app'@'localhost' IDENTIFIED BY '$dbPassword'; GRANT SELECT, INSERT, UPDATE, DELETE ON ccn_portal.* TO 'ccn_app'@'localhost';"
& $mysqlExe -u root -e $sql
if ($LASTEXITCODE -ne 0) { throw 'Could not configure the local MySQL application user. Check the local MySQL root account.' }

$env:ConnectionStrings__DefaultConnection = "Server=localhost;Port=3306;Database=ccn_portal;User=ccn_app;Password=$dbPassword;CharSet=utf8mb4;SslMode=None;AllowPublicKeyRetrieval=True;"
$env:Admin__Email = $AdminEmail
$env:Admin__Password = $AdminPassword
$env:ASPNETCORE_ENVIRONMENT = 'Development'

Write-Host 'Starting CCN portal at http://127.0.0.1:5080'
& $dotnetExe run --project (Join-Path $PSScriptRoot 'CcnPortal.csproj') --urls http://127.0.0.1:5080
