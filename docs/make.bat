@echo off
pushd %~dp0
if "%SPHINXBUILD%" == "" set SPHINXBUILD=sphinx-build
if "%1" == "" %SPHINXBUILD% -M help source build
%SPHINXBUILD% >nul 2>nul
if errorlevel 9009 (
	echo Command 'sphinx-build' not found. Make sure you have Sphinx installed,
	echo then set the SPHINXBUILD environment variable to point to the full
	echo path of the 'sphinx-build' executable. Alternatively, you may add the
	echo Sphinx directory to PATH.
	echo.
	echo If you don't have Sphinx installed, refer to
    echo https://www.sphinx-doc.org/en/master/usage/installation.html for steps
    echo to take.
	exit /b 1
)
%SPHINXBUILD% -M %1 source build -W %SPHINXOPTS% %O%
popd
