@echo off
setlocal enabledelayedexpansion

if "%1"=="" goto help
goto %1

:test
pytest -p asyncio-cooperative -p no:asyncio --no-cov --no-local-badge --maxfail 5
goto :eof

:test-with-badges
pytest -p asyncio-cooperative -p no:asyncio --no-cov --maxfail 0 --local-badge-output-dir assets --local-badge-duration-max 10 --local-badge-generate duration skipped status warnings xfailed
pytest -p asyncio -p no:asyncio-cooperative --maxfail 0 --local-badge-output-dir assets --local-badge-generate cov
goto :eof

:clean
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist py_asyncutils.egg-info rmdir /s /q py_asyncutils.egg-info
if exist .ruff_cache rmdir /s /q .ruff_cache
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist docs\build rmdir /s /q docs\build
if exist docs\source\api rmdir /s /q docs\source\api
if exist .coverage del /q .coverage
if exist .uv-stamp del /q .uv-stamp
if exist docs\source\help.rst del /q docs\source\help.rst
if exist docs\source\makefile-usage.rst del /q docs\source\makefile-usage.rst
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
del /s /q *.pyc *.pyo *.so 2>nul
goto :eof

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

:venv
call :.uv-stamp
uv venv
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

:ruff
call :.uv-stamp
ruff check
goto :eof

:watch
ptw --runner "pytest" --onfail "echo 'Tests failed!'"
goto :eof

:type-check
call :.uv-stamp
ty check
goto :eof

:rmclog
if exist ChangeLog del /q ChangeLog
goto :eof

:clog
call :rmclog
git log --pretty --numstat --summary > ChangeLog
goto :eof

:publish
call :.uv-stamp
uv build && uv publish
goto :eof

:pre-commit
call :.uv-stamp
pre-commit run --all-files
goto :eof

:help
type make.help
goto :eof
