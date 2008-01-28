#!/usr/bin/env python

import sys
import pdbparse
from pefile import PE

def cstring(str):
    for i in range(len(str)):
        if str[i] == '\0': return str[:i]
    return str

pdb = pdbparse.parse(sys.argv[1])
pe = PE(sys.argv[2])
gsyms = pdb.streams[pdb.streams[3].gsym_file]

#for k in sorted(gsyms.vars.keys()):
#    off = gsyms.vars[k].offset
#    try:
#        virt_base = pe.sections[gsyms.vars[k].segment-1].VirtualAddress
#        print "%-60s: %#08x" % (k, off+virt_base)
#    except IndexError:
#        print "Skipping %s, segment %d does not exist" % (k,gsyms.vars[k].segment-1)

for sym in gsyms.globals:
    off = sym.offset
    try:
        virt_base = pe.sections[sym.segment-1].VirtualAddress
        nm = cstring(pe.sections[sym.segment-1].Name)
        print "%-40s: (%s+%x) = (%x+%x) = %x" % (sym.name,nm,off,virt_base,off,off+virt_base)
    except IndexError:
        print "Skipping %s, segment %d does not exist" % (sym.name,sym.segment-1)
