__import__('sys').path.insert(0, __import__('os').path.abspath('../..'))
project = 'asyncutils'
author = 'Jonathan Dung'
copyright = '2026-%Y Jonathan Dung'
version = '0.8'
release = '0.8.20'
need_sphinx = '9.1.0'
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
autodoc_typehints = 'none'
extensions = ['sphinx.ext.napoleon', 'sphinx.ext.viewcode', 'autoapi.extension']
autoapi_dirs = ['../../asyncutils']
autoapi_file_patterns = ['*.pyi']
autoapi_root = 'api'
autoapi_ignore = ['../../asyncutils/_internal/__init__.pyi', '../../asyncutils/_internal/helpers.pyi', '../../asyncutils/_internal/initialize.pyi', '../../asyncutils/_internal/log.pyi', '../../asyncutils/_internal/compat.pyi', '../../asyncutils/_internal/py312.pyi', '../../asyncutils/_internal/py313.pyi', '../../asyncutils/_internal/log.pyi', '../../asyncutils/_internal/compat.pyi', '../../asyncutils/_internal/py312.pyi', '../../asyncutils/_internal/running_console.pyi', '../../asyncutils/_internal/submodules.pyi', '../../asyncutils/__init__.pyi']