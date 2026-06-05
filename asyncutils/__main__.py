#!/usr/bin/env python3
if __name__ != '__main__': raise ImportError('asyncutils: import of __main__ submodule not allowed')
raise SystemExit(__import__('asyncutils.cli', fromlist=('',)).run())
