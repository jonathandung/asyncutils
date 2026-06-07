from sphinx.directives.code import CodeBlock
def setup(app, f=__import__('_operator').methodcaller('replace', '|version|', release := '0.9.11')): app.add_config_value('py313', __import__('sys').version_info >= (3, 13), 'env', 'whether to include Python 3.13-only features in the docs'); app.add_directive('sub-code-block', type('SubCodeBlock', (CodeBlock,), {'run': lambda self: setattr(self, 'content', tuple(map(f, self.content))) or CodeBlock.run(self)}))
project = 'asyncutils'
author = 'Jonathan Dung'
version = '0.9'
copyright = '2026 Jonathan Dung'
need_sphinx = '9.1.0'
extensions = ['autoapi.extension', 'notfound.extension', 'sphinx_copybutton', 'sphinx.ext.ifconfig', 'sphinx.ext.intersphinx', 'sphinx.ext.viewcode']
default_role = 'py:obj'
suppress_warnings = ['autoapi.python_import_resolution']
if __import__('os').getenv('READTHEDOCS') == 'True':
    html_theme = 'furo'
    html_theme_options = {'top_of_page_buttons': ['view', 'edit'], 'source_repository': f'https://github.com/jonathandung/{project}', 'source_branch': 'main', 'source_directory': 'docs/source/'}
    source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}
    extensions += ('myst_parser', 'sphinxext.opengraph')
    ogp_canonical_url = f'https://{project}.readthedocs.io/en/stable/'
else:
    html_theme = 'sphinx_book_theme'
    suppress_warnings += ('ref.doc', 'toc.not_readable')
html_short_title = f'{project} {release} docs'
autoapi_dirs = [f'../../{project}']
autoapi_file_patterns = ['*.pyi']
autoapi_ignore = ['*/_internal/compat.pyi', '*/_internal/initialize.pyi', '*/_internal/log.pyi', '*/_internal/py312.pyi', '*/_internal/py313.pyi', '*/_internal/running_console.pyi', '*/_internal/submodules.pyi']
autoapi_keep_files = True
autoapi_member_order = 'groupwise'
autoapi_options = ['members', 'undoc-members', 'private-members', 'show-inheritance', 'show-module-summary', 'special-members']
autoapi_python_class_content = 'both'
autoapi_root = 'api'
copybutton_exclude = '.linenos, .gp, .go'
copybutton_prompt_text = '>>> '
intersphinx_mapping = {'python': ('https://docs.python.org/3', None), 'anyio': ('https://anyio.readthedocs.io/en/stable', None), 'more-itertools': ('https://more-itertools.readthedocs.io/en/stable', None)}
viewcode_line_numbers = True
maximum_signature_line_length = 120
manpage_url = 'https://manpages.debian.org/{path}'
