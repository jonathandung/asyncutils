from asyncutils.tools import *
@(dec := __import__('pytest').fixture(scope='module'))
def argstr(): return '-p -VV'
@dec
def argv(argstr): return argstr.split(' ')
def test_json_argv_conv(cfgjson, argv):
    assert json_to_argv(cfgjson) == argv
    argv_to_json(argv, cfgjson)
def test_json_argstr_conv(cfgjson, argstr):
    assert json_to_argstr(cfgjson) == argstr
    argstr_to_json(argstr, cfgjson)
def test_cmd_help():
    print_cmd_help(s := __import__('_io').StringIO())
    assert s.getvalue().removesuffix('\n') == get_cmd_help()