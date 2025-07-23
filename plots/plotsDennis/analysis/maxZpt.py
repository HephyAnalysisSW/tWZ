import ROOT
from RootTools.core.standard             import *


r = sample.treeReader( variables = read_variables, sequence = sequence, selectionString = cutInterpreter.cutString(args.selection_rec))
r.start()
while r.run():
    event = r.event
