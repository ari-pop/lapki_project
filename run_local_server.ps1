$projectRoot = $PSScriptRoot
$envFile = Join-Path $projectRoot ".env.local.ps1"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "Не найдено окружение .venv. Сначала создайте его и установите зависимости." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $envFile)) {
    Write-Host "Не найден локальный файл почтовых настроек .env.local.ps1" -ForegroundColor Yellow
    Write-Host "Сначала выполните .\setup_local_mail.ps1" -ForegroundColor Yellow
    exit 1
}

. $envFile

Write-Host "Почтовые настройки загружены. Запускаю сервер..." -ForegroundColor Cyan
& $pythonExe manage.py runserver
