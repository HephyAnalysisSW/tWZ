#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os
import array

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from tWZ.Tools.histogramHelper                   import WClatexNames
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)


import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
args = argParser.parse_args()

def getHist(fname, hname, rebin, altbinning=False):
    # print fname, hname
    bins  = [0, 60, 120, 180, 240, 300, 400, 1000]
    if altbinning:
        bins  = [0, 60, 120, 180, 1000]
    if "ULRunII" in fname:
        # Get histograms from each era
        hist_18 = getObjFromFile(fname.replace("/ULRunII/", "/UL2018/"), hname)
        hist_17 = getObjFromFile(fname.replace("/ULRunII/", "/UL2017/"), hname)
        hist_16 = getObjFromFile(fname.replace("/ULRunII/", "/UL2016/"), hname)
        hist_16preVFP = getObjFromFile(fname.replace("/ULRunII/", "/UL2016preVFP/"), hname)
        # add them
        hist = hist_18.Clone(hist_18.GetName()+"_RunIIcombination")
        hist.Add(hist_17)
        hist.Add(hist_16)
        hist.Add(hist_16preVFP)
    else:
        hist = getObjFromFile(fname, hname)
    if rebin:
        hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    return hist


files = {
    "ttZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_minorProcesses_v1_reduceEFT_noData/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root",
    "WZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_minorProcesses_v1_reduceEFT_noData/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root",
    "ZZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_minorProcesses_v1_reduceEFT_noData/ULRunII/all/qualepT-minDLmass12-onZ1-onZ2/Results.root",
}

plotdir = plot_directory+"/MinorProcesses/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

histname = "Z1_pt"
backgrounds = ["TTGamma", "ZGamma", "ggToZZ", "HToZZ", "ttW", "ttW_EWK"]


processinfo = {
    "TTGamma":       ("t#bar{t}#gamma", color.TTG),
    "ZGamma":        ("Z#gamma",  ROOT.kAzure+7),
    "ggToZZ":        ("gg #rightarrow ZZ", color.ZZ),
    "HToZZ":         ("H #rightarrow ZZ", color.TTX_rare),
    "ttW":           ("t#bar{t}W", ROOT.kGreen-2),
    "ttW_EWK":       ("t#bar{t}W (EWK)", ROOT.kGreen-6),    
}

for region in ["ttZ", "WZ", "ZZ"]:
    altbinning = True if region in ["ZZ"] else False
    # Setup plotter
    p = Plotter("MinorProcesses_ULRunII__"+region+"__"+histname)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z #it{p}_{T} [GeV]"
    p.drawRatio = True
    p.subtext = "Preliminary"
    p.legshift = (-0.1, -0.1, 0.0, 0.0)
    regiontext = "SR"
    if region == "ttZ":
        regiontext+="_{t#bar{t}Z}"
    elif region == "WZ":
        regiontext+="_{WZ}"
    elif region == "ZZ":
        regiontext+="_{ZZ}"
    p.addText(0.22, 0.7, regiontext, font=43, size=16)
    for process in backgrounds:
        h_bkg = getHist(files[region], histname+"__"+process, True, altbinning)
        p.addBackground(h_bkg, processinfo[process][0], processinfo[process][1])
    p.draw()
