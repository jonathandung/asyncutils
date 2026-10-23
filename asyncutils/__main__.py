#!/usr/bin/env python3
raise SystemExit(__import__('asyncutils.cli', fromlist=('',)).run()) if __name__ == '__main__' else ImportError('asyncutils.__main__ is not meant to be imported')
