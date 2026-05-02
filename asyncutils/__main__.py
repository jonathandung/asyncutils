#!/usr/bin/env python3
if __name__ != '__main__': raise ImportError('cannot import asyncutils.__main__')
raise SystemExit(__import__('asyncutils.cli', fromlist=('',)).run())