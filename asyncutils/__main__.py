#!/usr/bin/env python3
if __name__ != '__main__': raise ImportError('asyncutils.__main__ is not meant to be imported')
raise SystemExit(__import__('asyncutils.cli', fromlist=('',)).run())
