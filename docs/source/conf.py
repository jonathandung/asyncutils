import sys, os
def setup(app): app.add_config_value('py313', sys.version_info >= (3, 13), 'env', 'whether to include Python 3.13-only features in the docs')
project = 'asyncutils'
author = 'Jonathan Dung'
version = '0.9'
release = '0.9.10'
copyright = '2026 Jonathan Dung'
need_sphinx = '9.1.0'
extensions = ['autoapi.extension', 'notfound.extension', 'sphinx_copybutton', 'sphinx.ext.ifconfig', 'sphinx.ext.intersphinx', 'sphinx.ext.viewcode']
default_role = 'py:obj'
suppress_warnings = ['autoapi.python_import_resolution']
if os.getenv('READTHEDOCS') == 'True':
    html_theme = 'furo'
    html_theme_options = {'top_of_page_buttons': ['view', 'edit'], 'source_repository': 'https://github.com/jonathandung/asyncutils', 'source_branch': 'main', 'source_directory': 'docs/source/'}
    source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}
    extensions += ('myst_parser', 'sphinxext.opengraph')
    ogp_canonical_url = 'https://asyncutils.readthedocs.io/en/stable/'
else:
    html_theme = 'sphinx_book_theme'
    suppress_warnings += ('ref.doc', 'toc.not_readable')
html_short_title = 'asyncutils 0.9.10 docs'
autoapi_dirs = ['../../asyncutils']
autoapi_file_patterns = ['*.pyi']
autoapi_ignore = ['*/_internal/helpers.pyi', '*/_internal/initialize.pyi', '*/_internal/log.pyi', '*/_internal/compat.pyi', '*/_internal/py312.pyi', '*/_internal/py313.pyi', '*/_internal/log.pyi', '*/_internal/compat.pyi', '*/_internal/py312.pyi', '*/_internal/running_console.pyi', '*/_internal/submodules.pyi']
autoapi_keep_files = True
autoapi_member_order = 'groupwise'
autoapi_options = ['members', 'undoc-members', 'private-members', 'show-inheritance', 'show-module-summary', 'special-members']
autoapi_python_class_content = 'both'
autoapi_root = 'api'
copybutton_exclude = '.linenos, .gp, .go'
copybutton_prompt_text = '>>> '
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
viewcode_line_numbers = True