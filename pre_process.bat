@echo off

where uv >nul 2>&1
if %errorlevel% neq 0 goto :check_scoop_for_uv
goto :check_git

:check_scoop_for_uv
where scoop >nul 2>&1
if %errorlevel% == 0 goto :install_uv

echo 正在安裝 scoop...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression"

:install_uv
echo 正在用 scoop 安裝 uv...
scoop install uv

:check_git
where git >nul 2>&1
if %errorlevel% == 0 goto :end

where scoop >nul 2>&1
if %errorlevel% == 0 goto :install_git

echo 正在安裝 scoop...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression"

:install_git
echo 正在用 scoop 安裝 git...
scoop install git

:git_pull
git pull

:end
