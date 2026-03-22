from pytest import fixture
from asyncutils.tools import *
dec = fixture(scope='module')
@dec
def argstr(): return '-p -VV'
@dec
def argv(argstr): return argstr.split(' ')
def test_json_argv_conv(cfgjson, argv):
    assert json_to_argv(cfgjson) == argv
    argv_to_json(argv, cfgjson)
def test_json_argstr_conv(cfgjson, argstr):
    assert json_to_argstr(cfgjson) == argstr
    argstr_to_json(argstr, cfgjson)