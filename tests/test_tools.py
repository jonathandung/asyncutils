from _io import StringIO
import asyncutils as au, pytest as pt
from asyncutils.tools import *
@(dec := __import__('pytest').fixture(scope='module'))
def argstr(): return '-pVVm 5'
@dec
def argv(argstr): return argstr.split(' ')
def test_json_argv_conv(config_json, argv):
    assert json_to_argv(config_json) == argv
    argv_to_json(argv, config_json)
def test_json_argstr_conv(config_json, argstr):
    assert json_to_argstr(config_json) == argstr
    argstr_to_json(argstr, config_json)
def test_cmd_help():
    print_cmd_help(s := StringIO())
    assert s.getvalue() == get_cmd_help()
def test_json_fmt(contents):
    print_cfg_json_format(s := StringIO())
    fmt = get_cfg_json_format()
    assert s.getvalue() == fmt
    from pyjson5 import loads
    assert loads(contents).keys() <= loads(fmt).keys()
def test_loadf(tmp_path):
    p = tmp_path/'test.toml'
    p.write_text('[sec1]\nkey1 = "value"\n"key 2" = [{a = true, b = [42]}]\n')
    assert loadf(p) == {'sec1': {'key1': 'value', 'key 2': [{'a': True, 'b': [42]}]}}
    with pt.raises(TypeError, match='did not expect extension'): loadf(p, 'ini')
@pt.mark.parametrize(('obj', 'expected'), ((au.queues.SmartQueue, 'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/queues/index.html#asyncutils.queues.SmartQueue'), ('properties', 'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/properties/index.html#module-asyncutils.properties'), (au.util, 'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/util/index.html#module-asyncutils.util')))
def test_help(obj, expected): assert find_help_url(obj) == expected
