$projectRoot = $PSScriptRoot
$envFile = Join-Path $projectRoot ".env.local.ps1"

Write-Host "Настройка локальной почты для проекта Лапки" -ForegroundColor Cyan
Write-Host "Файл будет сохранен только локально: $envFile" -ForegroundColor DarkGray

$email = Read-Host "Введите почту Mail.ru для отправки писем"
$securePassword = Read-Host "Введите пароль приложения Mail.ru" -AsSecureString

$bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

$content = @"
`$env:DJANGO_EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
`$env:DJANGO_EMAIL_HOST="smtp.mail.ru"
`$env:DJANGO_EMAIL_PORT="465"
`$env:DJANGO_EMAIL_HOST_USER="$email"
`$env:DJANGO_EMAIL_HOST_PASSWORD="$plainPassword"
`$env:DJANGO_EMAIL_USE_TLS="False"
`$env:DJANGO_EMAIL_USE_SSL="True"
`$env:DJANGO_DEFAULT_FROM_EMAIL="$email"
"@

Set-Content -Path $envFile -Value $content -Encoding UTF8

Write-Host "Локальный файл настроек сохранен." -ForegroundColor Green
Write-Host "Теперь можно запускать проект через .\run_local_server.ps1" -ForegroundColor Green
