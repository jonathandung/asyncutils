@echo off
:: cspell:disable-next-line
setlocal enabledelayedexpansion
if "%AUTILSTESTMAXFAIL%" == "" set AUTILSTESTMAXFAIL=3
if "%1"=="" goto help
goto %1

:.prek-stamp
if exist .prek-stamp goto :eof
where prek >nul 2>nul
if %errorlevel% neq 0 (powershell -ExecutionPolicy ByPass -c "irm https://github.com/j178/prek/releases/download/v0.4.10/prek-installer.ps1 | iex")
prek install
type nul > .prek-stamp
goto :eof

:.uv-stamp
if exist .uv-stamp goto :eof
where uv >nul 2>nul
if %errorlevel% neq 0 (powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex")
uv tool install ruff 2>nul
uv tool install ty 2>nul
type nul > .uv-stamp
goto :eof

:audit
call :.uv-stamp
uv audit --preview-features audit-command
goto :eof

:badges
pytest -p asyncio-cooperative -p no:asyncio --no-cov --local-badge-output-dir badges --local-badge-duration-max 10 --local-badge-generate duration skipped status xfailed
pytest -p asyncio -p no:asyncio-cooperative --local-badge-output-dir badges --local-badge-generate last-run warnings
goto :eof

:bug
asyncutils bug --open %O%
goto :eof

:changelog
:: cspell:disable-next-line
git log --graph --pretty=format:"%%Cred%%h%%Creset -%%C(yellow)%%d%%Creset %%s %%Cgreen(%%cr) %%C(bold blue)<%%an>%%Creset" --abbrev-commit
goto :eof

:clean
for %%i in (.pytest_cache .ruff_cache build dist docs\build docs\source\api py_asyncutils.egg-info) do if exist "%%i" rmdir /s /q "%%i"
for %%i in (.coverage .cspellcache .prek-stamp .uv-stamp docs\source\bug-help.rst docs\source\help.rst docs\source\makefile-usage.rst docs\source\ai-use.md docs\source\changelog.md docs\source\compat.rst docs\source\conduct.md docs\source\contributing.md docs\source\examples.rst docs\source\roadmap.md docs\source\security.md docs\source\support.md) do if exist "%%i" del /q "%%i"
for /d /r . %%d in (__pycache__) do if exist "%%d" rmdir /s /q "%%d"
del /s /q *.pyc *.pyo *.pyz 2>nul
goto :eof

:docs
powershell -ExecutionPolicy ByPass -File ".\scripts\generate.ps1" 2>nul
cd docs
shift
set "__O=%O%"
set "REST_ARGS="
:__loop
if "%~1"=="" goto __done
set "REST_ARGS=!REST_ARGS! %1"
shift
goto __loop
:__done
if defined REST_ARGS set "REST_ARGS=%REST_ARGS:~1%"
set "O=-W %REST_ARGS% %__O%"
set "__O="
set "REST_ARGS="
make html
goto :eof

:help
type assets\mkhelp.txt
goto :eof

:install
call :.prek-stamp
call :.uv-stamp
uv pip install -Ue .[dev]
goto :eof

:lint
call :.uv-stamp
ruff check
ty check
goto :eof

:lock
call :.uv-stamp
uv lock -U
goto :eof

:pc
call :.prek-stamp
prek run
goto :eof

:release
choice /m "You are about to create a release. Are you sure?"
if errorlevel 2 exit /b 1
if errorlevel 1 gh release create
goto :eof

:test
pytest -p asyncio-cooperative -p no:asyncio --no-cov --no-local-badge --maxfail %AUTILSTESTMAXFAIL%
goto :eof

:venv
call :.uv-stamp
uv venv
goto :eof
