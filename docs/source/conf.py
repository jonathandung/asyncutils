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
autoapi_ignore = ['*/_internal/__init__.pyi', '*/_internal/helpers.pyi', '*/_internal/initialize.pyi', '*/_internal/log.pyi', '*/_internal/compat.pyi', '*/_internal/py312.pyi', '*/_internal/py313.pyi', '*/_internal/log.pyi', '*/_internal/compat.pyi', '*/_internal/py312.pyi', '*/_internal/running_console.pyi', '*/_internal/submodules.pyi']