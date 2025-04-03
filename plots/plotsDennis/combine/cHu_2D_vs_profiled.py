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
fname_1d = "DataCards_threePoint_light_minus_UNBLINDED_binning-A_SMZero/ULRunII/higgsCombine.topEFT_ULRunII_combined_13TeV_ULRunII_1D-cHuRe33_float_random_13.MultiDimFit.mH125.123456.root"
fname_2d = "DataCards_threePoint_light_minus_UNBLINDED_binning-A_SMZero/ULRunII/higgsCombine.topEFT_ULRunII_combined_13TeV_ULRunII_1D-cHuRe33_float_from2D.MultiDimFit.mH125.123456.root"

g_1d = getGraphFromTree(fname_1d, "cHuRe33")
g_2d = getGraphFromTree(fname_2d, "cHuRe33")
g_2d.SetLineColor(ROOT.kRed)

plotdir = plot_directory+"/Limits_UL_threePoint_Random/"
c = ROOT.TCanvas("", "", 600, 600)
ROOT.gPad.SetTopMargin(0.02)
leg = ROOT.TLegend(.65, .25, .9, .5)
isFirst = True
g_1d.Draw("AL")
g_2d.Draw("L SAME")

leg = ROOT.TLegend(.4, .7, .8, .9)
leg.AddEntry(g_1d, "1D scan", "l")
leg.AddEntry(g_2d, "Minimum from 2D scan", "l")
leg.Draw()

ROOT.gPad.RedrawAxis()
c.Print(plotdir+"cHuRe33_1Dvs2D.pdf")
