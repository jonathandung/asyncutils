@echo off
:: cspell:disable-next-line
setlocal enabledelayedexpansion
if "%AUTESTMAXFAIL%" == "" set AUTESTMAXFAIL=3
if "%1"=="" goto help
goto %1

:.prek-stamp
if exist .prek-stamp goto :eof
where prek >nul 2>nul
set PREK_UV_SOURCE=none
if not defined PREK_INSTALL_DIR set PREK_INSTALL_DIR=%USERPROFILE%\.local\bin
if %errorlevel% neq 0 (powershell -ExecutionPolicy ByPass -c "irm https://github.com/j178/prek/releases/download/v0.5.7/prek-installer.ps1 | iex")
%PREK_INSTALL_DIR%\prek.exe install
type nul >.prek-stamp
goto :eof

:.uv-stamp
if exist .uv-stamp goto :eof
where uv >nul 2>nul
if not defined UV_INSTALL_DIR set UV_INSTALL_DIR=%USERPROFILE%\.local\bin
if %errorlevel% neq 0 (powershell -ExecutionPolicy ByPass -c "irm https://releases.astral.sh/installers/uv/latest/uv-installer.ps1 | iex")
%UV_INSTALL_DIR%\uv.exe tool install ruff 2>nul
%UV_INSTALL_DIR%\uv.exe tool install ty 2>nul
type nul >.uv-stamp
goto :eof

:badges
pytest -p asyncio-cooperative -p no:asyncio --no-cov --local-badge-output-dir badges --local-badge-duration-max 10 --local-badge-generate duration skipped status xfailed
pytest -p asyncio -p no:asyncio-cooperative --local-badge-output-dir badges --local-badge-generate last-run warnings
goto :eof

:bug
asyncutils bug --open %O%
goto :eof

:build
docker build -t jonathandung/asyncutils:latest .
goto :eof

:clean
for %%i in (.pytest_cache .ruff_cache build dist docs\build docs\source\api py_asyncutils.egg-info) do if exist "%%i" rmdir /s /q "%%i"
for %%i in (.coverage .cspellcache .prek-stamp .uv-stamp docs\source\bug-help.rst docs\source\help.rst docs\source\makefile-usage.rst docs\source\ai-use.md docs\source\changelog.md docs\source\conduct.md docs\source\contributing.md docs\source\governance.md docs\source\roadmap.md docs\source\security.md docs\source\support.md) do if exist "%%i" del /q "%%i"
for /d /r . %%d in (__pycache__) do if exist "%%d" rmdir /s /q "%%d"
del /s /q *.pyc *.pyo 2>nul
goto :eof

:dclean
git clean -dxf
goto :eof

:docs
powershell -ExecutionPolicy ByPass -File ".\scripts\generate.ps1"
cd docs
shift
set "__O=%O%"
set "REST_ARGS="
if not defined __B set "__B=html"
:__l
if "%~1"=="" goto __d
set "REST_ARGS=!REST_ARGS! %1"
shift
goto __l
:__d
if defined REST_ARGS set "REST_ARGS=%REST_ARGS:~1%"
set "O=%REST_ARGS% %__O%"
set "__O="
set "REST_ARGS="
make "%__B%"
goto :eof

:help
type assets\mkhelp.txt
goto :eof

:links
set __B=linkcheck
call :docs
goto :eof

:lint
call :.uv-stamp
echo Running ruff...
ruff check
echo Running ty...
ty check
where cspell >nul 2>nul
if %errorlevel% equ 0 (
    echo Running cspell... && cspell .
)
goto :eof

:lock
call :.uv-stamp
uv lock -U
goto :eof

:log
:: cspell:disable-next-line
git log --graph --pretty=format:"%%Cred%%h%%Creset -%%C(yellow)%%d%%Creset %%s %%Cgreen(%%cr) %%C(bold blue)<%%an>%%Creset" --abbrev-commit
goto :eof

:pc
call :.prek-stamp
prek run -a
goto :eof

:release
choice /m "You are about to create a release. Are you sure?"
if errorlevel 2 exit /b 1
if errorlevel 1 gh release create
goto :eof

:run
docker run --rm -it jonathandung/asyncutils:latest
goto :eof

:setup
call :.uv-stamp
call :.prek-stamp
uv sync
goto :eof

:test
pytest -p asyncio-cooperative -p no:asyncio --no-cov --no-local-badge --maxfail %AUTESTMAXFAIL%
goto :eof
