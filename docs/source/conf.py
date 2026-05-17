import sys, os
sys.path.insert(0, os.path.abspath('../..'))
def setup(app): app.add_config_value('py313', sys.version_info >= (3, 13), 'env', 'whether to include Python 3.13-only features in the docs')
project = 'asyncutils'
author = 'Jonathan Dung'
copyright = '2026-%Y Jonathan Dung'
version = '0.9'
release = '0.9.5'
need_sphinx = '9.1.0'
default_role = 'py:obj'
extensions = ['autoapi.extension', 'myst_parser', 'notfound.extension', 'sphinx_copybutton', 'sphinx.ext.ifconfig', 'sphinx.ext.intersphinx', 'sphinx.ext.viewcode']
source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}
suppress_warnings = ['autoapi.python_import_resolution']
html_theme = 'furo'
html_theme_options = {'top_of_page_buttons': ['view', 'edit'], 'source_repository': 'https://github.com/jonathandung/asyncutils', 'source_branch': 'main', 'source_directory': 'docs/source/'}
pygments_style = 'sphinx'
autoapi_dirs = ['../../asyncutils']
autoapi_file_patterns = ['*.pyi']
autoapi_ignore = ['*/_internal/helpers.pyi', '*/_internal/initialize.pyi', '*/_internal/log.pyi', '*/_internal/compat.pyi', '*/_internal/py312.pyi', '*/_internal/py313.pyi', '*/_internal/log.pyi', '*/_internal/compat.pyi', '*/_internal/py312.pyi', '*/_internal/running_console.pyi', '*/_internal/submodules.pyi']
autoapi_member_order = 'groupwise'
autoapi_options = ['members', 'undoc-members', 'private-members', 'show-inheritance', 'show-module-summary', 'special-members']
autoapi_python_class_content = 'both'
autoapi_root = 'api'
copybutton_exclude = '.linenos, .gp, .go'
copybutton_prompt_text = '>>> '
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
viewcode_line_numbers = True