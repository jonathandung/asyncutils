@echo off
rem cspell:disable-next-line
setlocal enabledelayedexpansion

if "%AUTILSTESTMAXFAIL%" == "" set AUTILSTESTMAXFAIL=3
if "%1"=="" goto help
goto %1

:.uv-stamp
if exist .uv-stamp goto :eof
where uv >nul 2>nul
if %errorlevel% neq 0 (
  where curl >nul 2>nul
  if %errorlevel% equ 0 (curl -LsSf https://astral.sh/uv/install.sh | sh) else (
    where wget >nul 2>nul
    if %errorlevel% equ 0 (wget -qO- https://astral.sh/uv/install.sh | sh) else (
      echo curl or wget required to install uv >&2
      exit /b 1)))
(uv tool install -U ruff & uv tool install -U ty) 2>nul
type nul > .uv-stamp
goto :eof

:build-docs
pwsh .\scripts\win\genhelp.ps1
pwsh .\scripts\win\genmakefileusage.ps1
sphinx-build -W docs/source docs/build
goto :eof

:changelog
rem cspell:disable-next-line
git log --graph --pretty=format:"%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset" --abbrev-commit
goto :eof

:clean
for %%i in (build dist py_asyncutils.egg-info .cspellcache .ruff_cache .pytest_cache docs\build docs\source\api) do if exist "%%i" rmdir /s /q "%%i"
for %%i in (.coverage .uv-stamp docs\source\help.rst docs\source\makefile-usage.rst) do if exist "%%i" del /q "%%i"
for /d /r . %%d in (__pycache__) do if exist "%%d" rmdir /s /q "%%d"
del /s /q *.pyc *.pyo *.so 2>nul
goto :eof

:gen-badges
pytest -p asyncio-cooperative -p no:asyncio --no-cov --local-badge-output-dir badges --local-badge-duration-max 10 --local-badge-generate duration skipped status xfailed
pytest -p asyncio -p no:asyncio-cooperative --local-badge-output-dir badges --local-badge-generate cov last-run warnings
goto :eof

:gen-baseline
detect-secrets scan > .secrets.baseline
goto :eof

:help
type assets\mkhelp.txt
goto :eof

:install
call :.uv-stamp
uv pip install -Ue .[dev]
goto :eof

:install-system
call :.uv-stamp
uv pip install --system -Ue .[dev]
goto :eof

:install-silent
call :install > nul
goto :eof

:pre-commit
pre-commit run --all-files
goto :eof

:regen-trie
cspell-tools compile-trie ./assets/words.txt -o ./assets
goto :eof

:release
gh release create
goto :eof

:ruff
call :.uv-stamp
ruff check
goto :eof

:spellcheck
cspell lint .
goto :eof

:test
pytest -p asyncio-cooperative -p no:asyncio --no-cov --no-local-badge --maxfail %AUTILSTESTMAXFAIL%
goto :eof

:type-check
call :.uv-stamp
ty check
goto :eof

:venv
call :.uv-stamp
uv venv
goto :eof

:watch
ptw --runner "pytest" --onfail "echo 'Tests failed!'"
goto :eof
