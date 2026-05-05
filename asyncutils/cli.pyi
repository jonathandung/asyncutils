__all__ = 'run',
def run() -> int:
    '''| Run the command-line interface (this module's REPL) and return the integer return code.
    | See :func:`tools.get_cmd_help()` for detailed usage.
    | If an error somehow escapes the console and the pdb option is enabled, 1 will be returned after calling the post-mortem debugger on its traceback.'''