#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Configura Windows Task Scheduler para el cierre contable diario de Token Analytics.

.DESCRIPTION
    Registra una tarea programada que ejecuta daily_close.py a las 12:00am
    hora Colombia (COT = UTC-5) todos los dias.

.PREREQUISITES
    - Python 3.x instalado y disponible en PATH
    - Variable de entorno GITHUB_TOKEN configurada
    - Repositorio clonado localmente
    - Ejecutar como Administrador

.USAGE
    # Ejecucion basica (detecta rutas automaticamente)
    .\setup_scheduler.ps1

    # Especificando rutas manualmente
    .\setup_scheduler.ps1 -PythonPath "C:\Python311\python.exe" -RepoPath "C:\Users\user\repos\ibm-data-science-portfolio"

    # Verificar tarea creada
    Get-ScheduledTask -TaskName "TokenAnalyticsDailyClose"

    # Ejecutar manualmente
    Start-ScheduledTask -TaskName "TokenAnalyticsDailyClose"

    # Eliminar tarea
    Unregister-ScheduledTask -TaskName "TokenAnalyticsDailyClose" -Confirm:$false
#>

param(
    [string]$PythonPath = "",
    [string]$RepoPath   = ""
)

$TASK_NAME = "TokenAnalyticsDailyClose"
$TASK_DESC = "Cierre contable diario automatico - Token Analytics / Hipocrates MCP"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Token Analytics - Setup Task Scheduler   " -ForegroundColor Cyan
Write-Host "  Hipocrates MCP / CardioRisk Portfolio     " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# -- DETECTAR PYTHON ----------------------------------------------------------
if (-not $PythonPath) {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) { $PythonPath = $cmd.Source }

    if (-not $PythonPath) {
        $cmd = Get-Command python3 -ErrorAction SilentlyContinue
        if ($cmd) { $PythonPath = $cmd.Source }
    }

    if (-not $PythonPath) {
        $candidates = @(
            "$env:LOCALAPPDATA\Programs\Python\Python3*\python.exe",
            "$env:ProgramFiles\Python3*\python.exe"
        )
        foreach ($c in $candidates) {
            $found = Get-Item $c -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) { $PythonPath = $found.FullName; break }
        }
    }
}

if (-not $PythonPath -or -not (Test-Path $PythonPath)) {
    Write-Host "ERROR: Python no encontrado. Especifica la ruta:" -ForegroundColor Red
    Write-Host "  .\setup_scheduler.ps1 -PythonPath 'C:\Python311\python.exe'" -ForegroundColor Yellow
    exit 1
}

# -- DETECTAR RUTA DEL REPO ---------------------------------------------------
if (-not $RepoPath) {
    $RepoPath = Split-Path $PSScriptRoot -Parent
    if (-not (Test-Path (Join-Path $RepoPath "TOKEN_LOG.md"))) {
        Write-Host "ERROR: No se encontro TOKEN_LOG.md en: $RepoPath" -ForegroundColor Red
        Write-Host "Especifica la ruta del repo:" -ForegroundColor Yellow
        Write-Host "  .\setup_scheduler.ps1 -RepoPath 'C:\ruta\al\repo'" -ForegroundColor Yellow
        exit 1
    }
}

$ScriptPath = Join-Path $RepoPath "token_analytics\daily_close.py"

if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: daily_close.py no encontrado en:" -ForegroundColor Red
    Write-Host "  $ScriptPath" -ForegroundColor Red
    exit 1
}

# -- VERIFICAR GITHUB_TOKEN ---------------------------------------------------
$ghToken = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
if (-not $ghToken) {
    $ghToken = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "Machine")
}
if (-not $ghToken) {
    Write-Host "ADVERTENCIA: GITHUB_TOKEN no encontrado en variables de entorno." -ForegroundColor Yellow
    Write-Host "El cierre diario no podra commitear a GitHub sin este token." -ForegroundColor Yellow
    Write-Host "Configuralo con:" -ForegroundColor Cyan
    Write-Host "  [System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN','TU_TOKEN','User')" -ForegroundColor White
    Write-Host ""
}

# -- MOSTRAR CONFIGURACION ----------------------------------------------------
Write-Host "Configuracion detectada:" -ForegroundColor Green
Write-Host "  Python:            $PythonPath"
Write-Host "  Script:            $ScriptPath"
Write-Host "  Directorio repo:   $RepoPath"
Write-Host "  Hora ejecucion:    12:00am (hora local Colombia)"
Write-Host ""

# -- CREAR TAREA PROGRAMADA ---------------------------------------------------
try {
    $trigger   = New-ScheduledTaskTrigger -Daily -At "12:00AM"
    $action    = New-ScheduledTaskAction `
                     -Execute $PythonPath `
                     -Argument "`"$ScriptPath`"" `
                     -WorkingDirectory $RepoPath
    $settings  = New-ScheduledTaskSettingsSet `
                     -AllowStartIfOnBatteries `
                     -DontStopIfGoingOnBatteries `
                     -StartWhenAvailable `
                     -WakeToRun `
                     -MultipleInstances IgnoreNew `
                     -RestartCount 3 `
                     -RestartInterval (New-TimeSpan -Minutes 5)
    $principal = New-ScheduledTaskPrincipal `
                     -UserId "SYSTEM" `
                     -LogonType ServiceAccount `
                     -RunLevel Highest

    $existing = Get-ScheduledTask -TaskName $TASK_NAME -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "Actualizando tarea existente: $TASK_NAME" -ForegroundColor Yellow
        Set-ScheduledTask -TaskName $TASK_NAME `
            -Action $action -Trigger $trigger `
            -Settings $settings -Principal $principal | Out-Null
    } else {
        Write-Host "Creando tarea: $TASK_NAME" -ForegroundColor Green
        Register-ScheduledTask `
            -TaskName    $TASK_NAME `
            -Description $TASK_DESC `
            -Action      $action `
            -Trigger     $trigger `
            -Settings    $settings `
            -Principal   $principal | Out-Null
    }

    $task = Get-ScheduledTask    -TaskName $TASK_NAME
    $info = Get-ScheduledTaskInfo -TaskName $TASK_NAME

    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  TAREA PROGRAMADA CREADA EXITOSAMENTE      " -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  Nombre:            $($task.TaskName)"
    Write-Host "  Estado:            $($task.State)"
    Write-Host "  Proxima ejecucion: $($info.NextRunTime)"
    Write-Host ""
    Write-Host "Comandos utiles:" -ForegroundColor Cyan
    Write-Host "  Ejecutar ahora:  Start-ScheduledTask -TaskName '$TASK_NAME'"
    Write-Host "  Ver estado:      Get-ScheduledTaskInfo -TaskName '$TASK_NAME'"
    Write-Host "  Eliminar:        Unregister-ScheduledTask -TaskName '$TASK_NAME' -Confirm:`$false"
    Write-Host ""

    $test = Read-Host "Ejecutar prueba inmediata? (S/N)"
    if ($test -match '^[Ss]') {
        Start-ScheduledTask -TaskName $TASK_NAME
        Write-Host "Tarea iniciada. Revisa: $RepoPath\token_analytics\daily_close.log" -ForegroundColor Green
    }

} catch {
    Write-Host "ERROR configurando la tarea:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
