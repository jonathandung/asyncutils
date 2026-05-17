#!/usr/bin/env python3
if __name__ != '__main__': raise ImportError('asyncutils: cannot import __main__ submodule')
raise SystemExit(__import__('asyncutils.cli', fromlist=('',)).run())