#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.histogramHelper                   import WClatexNames
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger

def getEFTatWCpoint(file, region, histname, wcname, wcvalue):
    sm = getObjFromFile(file, region+"__"+histname+"/sm")
    sm_lin_quad = getObjFromFile(file, region+"__"+histname+"/sm_lin_quad_"+wcname)
    quad = getObjFromFile(file, region+"__"+histname+"/quad_"+wcname)
    # This is the formula:
    # signal = (1 - k)* sm + k* sm_lin_quad + (k^2 - k) quad
    h_eft = sm.Clone(region+"__"+histname+"__"+wcname+"__"+str(wcvalue))
    h_eft.Add(sm, -wcvalue)
    h_eft.Add(sm_lin_quad, wcvalue)
    h_eft.Add(quad, wcvalue*wcvalue-wcvalue)
    return h_eft


logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--noData',           action='store_true', default=False)
args = argParser.parse_args()


dataTag = "_noData" if args.noData else ""
dirname_suffix = "_light"
combineInput = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint"+dataTag+dirname_suffix+"/ULRunII/CombineInput.root"

plotdir = plot_directory+"/PaperPlots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

sys = [
    "muF_ttZ", "muF_WZ", "muF_ZZ",
    "muR_ttZ", "muR_WZ", "muR_ZZ",
]
histname = "Z1_pt"
for region in ["ttZ", "WZ", "ZZ"]:
    for wc in ["cHq1Re1122", "cHq1Re33", "cHq3Re1122", "cHq3Re33"]:
        h_sm = getObjFromFile(combineInput, region+"__"+histname+"/sm")
        wcvalueUp = 1
        wcvalueDown = -1
        if region == "WZ" and wc == "cHq3Re1122":
            wcvalueUp = 0.2
            wcvalueDown = -0.2
        h_eftUp   = getEFTatWCpoint(combineInput, region, histname, wc, wcvalueUp)
        h_eftDown = getEFTatWCpoint(combineInput, region, histname, wc, wcvalueDown)
        p = Plotter("EFT_ULRunII__"+region+"__"+histname+"__"+wc)
        p.plot_dir = plotdir
        p.lumi = "138"
        p.xtitle = "Z #it{p}_{T} [GeV]"
        p.drawRatio = True
        p.ratiotitle = "#splitline{Ratio}{to SM}"
        p.simtext = "Simulation"
        p.subtext = "Preliminary"
        p.legshift = (0.1, -0.3, 0.0, 0.0)
        p.ratiorange = 0.7, 1.3
        p.NcolumnsLegend = 1
        regiontext = "SR"
        if region == "ttZ":
            regiontext+="_{t#bar{t}Z}"
        elif region == "WZ":
            regiontext+="_{WZ}"
        elif region == "ZZ":
            regiontext+="_{ZZ}"
        p.addText(0.22, 0.65, regiontext, font=43, size=16)
        signalName = region.replace("ttZ", "t#bar{t}Z")+" (SM)"
        p.addBackground(h_sm, signalName, 15)
        for s in sys:
            h_up = getObjFromFile(combineInput, region+"__"+histname+"/sm__"+s+"Up")
            h_down = getObjFromFile(combineInput, region+"__"+histname+"/sm__"+s+"Down")
            p.addSystematic(h_up, h_down, s, signalName)
        p.addSignal(h_eftUp,   signalName.replace("(SM)", "")+"("+WClatexNames[wc].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = "+str(wcvalueUp)+")", ROOT.kRed-2, 2)
        p.addSignal(h_eftDown, signalName.replace("(SM)", "")+"("+WClatexNames[wc].replace("/#Lambda^{2} [TeV^{-2}]", "")+" = "+str(wcvalueDown)+")", ROOT.kAzure+7)
        p.draw()
