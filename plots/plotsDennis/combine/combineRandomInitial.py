import ROOT
import os
import array
import Analysis.Tools.syncer
from tWZ.Tools.helpers                   import getObjFromFile
from tWZ.Tools.user                      import plot_directory
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--files',             action='store', type=str, default=None)
args = argParser.parse_args()

def getGraphFromTree(filename, wcname):
    wcvalues, twodeltaNLLs = array.array( 'd' ), array.array( 'd' )
    branchname = "k_"+wcname
    rf = ROOT.TFile.Open(filename)
    tree = getattr(rf, "limit")
    if tree.GetEntry(0)<=0:
        raise RuntimeError( "Tree of file %s is empty", filename)
    minDelta = 1000000000
    for point in tree:
        if point.deltaNLL > 0.000000001:
            # first value is the best fit with deltaNLL=0, jump this one
            wcvalues.append(eval("point."+branchname))
            twodeltaNLLs.append(2*point.deltaNLL)
            if 2*point.deltaNLL < minDelta:
                minDelta = 2*point.deltaNLL
    rf.Close()
    # print len(wcvalues)
    if len(wcvalues) == 0:
        wcvalues.append(0)
        twodeltaNLLs.append(0)
    # for i in range(len(twodeltaNLLs)):
    #     twodeltaNLLs[i] = twodeltaNLLs[i]-minDelta

    graph = ROOT.TGraph(len(wcvalues), wcvalues, twodeltaNLLs)
    graph = setDrawStyle(graph, wcname)
    return graph

def setDrawStyle(g, wcname):
    from tWZ.Tools.histogramHelper import WClatexNames
    g.GetYaxis().SetRangeUser(0, 8)
    g.SetTitle('')
    g.GetXaxis().SetTitle(WClatexNames[wcname])
    g.GetYaxis().SetTitle('-2 #Delta ln L')
    g.SetLineWidth(2)
    return g

# List of input ROOT files
dummy_name = "DataCards_threePoint_light_minus_UNBLINDED_binning-A_SMZero/ULRunII/higgsCombine.topEFT_ULRunII_combined_13TeV_ULRunII_1D-cHuRe33_float_<RANDSTR>.MultiDimFit.mH125.123456.root"

file_names = [ dummy_name.replace("<RANDSTR>", "random_%i"%i) for i in range(50)]
vetos = ["random_5"]
vetos += ["random_11", "random_22", "random_23", "random_24", "random_27", "random_28", "random_29", "random_61"]


for i in range(len(file_names) - 1, -1, -1):
    if "ULRunII_combined_" in file_names[i]:
        for veto in vetos:
            if veto in file_names[i]:
                del file_names[i]
                break

file_names = ["myFile.root"]

graphs = []
for fname in file_names:
    g = getGraphFromTree(fname, "cHuRe33")
    graphs.append(g)


plotdir = plot_directory+"/Limits_UL_threePoint_Random/"
c = ROOT.TCanvas("", "", 600, 600)
ROOT.gPad.SetTopMargin(0.02)
leg = ROOT.TLegend(.65, .25, .9, .5)
isFirst = True
for g in graphs:
    if isFirst:
        isFirst = False
        g.Draw("AL")
    else:
        g.Draw("L SAME")

ROOT.gPad.RedrawAxis()
c.Print(plotdir+"cHuRe33.pdf")
