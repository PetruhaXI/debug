#!/usr/bin/env python
# encoding: utf-8
"""
import debug: https://github.com/narfdotpl/debug
"""

try:
    import builtins
except ImportError:
    import __builtin__ as builtins
from sys import _getframe

from ipdb import set_trace


# do not forget
old_import = builtins.__import__

def debug():
    # get frame
    frame = _getframe(2)

    # inject see (`from see import see`)
    ns = frame.f_globals
    if 'see' not in ns:
        ns['see'] = old_import('see', fromlist=['see']).see

    # start ipdb
    set_trace(frame)

# run on first import
debug()

# monkeypatch `import` so `import debug` will work every time
def new_import(*args, **kwargs):
    if args[0] == 'debug':
        debug()
    else:
        return old_import(*args, **kwargs)

builtins.__import__ = new_import
