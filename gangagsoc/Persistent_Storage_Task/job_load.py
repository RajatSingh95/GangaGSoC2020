import ganga.ganga
from ganga import *
from GangaCore.GPIDev.Base.Proxy import *
import json
import re,ast

def full_print(obj, out=None, interactive=False):
    """Print the full contents of a GPI object without abbreviation."""
    
    from io import StringIO
    import sys
    if out is None:
        out = sys.stdout

    from GangaCore.GPIDev.Lib.GangaList.GangaList import GangaList

    _obj = stripProxy(obj)

    if isType(_obj, GangaList):
        obj_len = len(_obj)
        if obj_len == 0:
            #print('[]', end=' ', file=out)
            return '[]'
        else:
            outString = '['
            outStringList = []
            for x in _obj:
                if isType(x, GangaObject):
                    sio = StringIO()
                    stripProxy(x).printTree(sio, interactive)
                    result = sio.getvalue()
                    # remove trailing whitespace and newlines
                    outStringList.append(result.rstrip())
                else:
                    # remove trailing whitespace and newlines
                    outStringList.append(str(x).rstrip())
            outString += ', '.join(outStringList)
            outString += ']'
            return outString
            #print(outString, end=' ', file=out)
        return

    if isProxy(obj) and isinstance(_obj, GangaObject):
        sio = StringIO()
        runProxyMethod(obj, 'printTree', sio, interactive)
        
        return sio.getvalue()
        #from ast import literal_eval
        #l = literal_eval(sio.getvalue())
        
        #print(sio.getvalue(), end=' ', file=out)
    else:
        #print(str(_obj), end=' ', file=out)
        return str(_obj)



