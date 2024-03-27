#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os

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

def convertBinning(h_dummy, h_combineOutput):
    hist = h_dummy.Clone()
    hist.Reset()
    Nbins = h_combineOutput.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        hist.SetBinContent(bin, h_combineOutput.GetBinContent(bin))
        hist.SetBinError(bin, h_combineOutput.GetBinError(bin))
    return hist

# def getVariations(hist):
#     up = hist.Clone()
#     down = hist.Clone()
#     Nbins = h_combineOutput.GetSize()-2
#     for i in range(Nbins):



dirname_suffix = "_light"
dataTag = "_noData"
nRegions = 3
directory = "/users/dennis.schwarz/CMSSW_10_6_28/src/tWZ/plots/plotsDennis/combine/DataCards_threePoint"+dirname_suffix+"/ULRunII/"
combineInput = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint"+dataTag+dirname_suffix+"/ULRunII/CombineInput.root"

plotdir = plot_directory+"/PaperPlots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

regions = {
    1: "ZZ",
    2: "WZ",
    3: "ttZ",
}
histname = "Z1_pt"
signals = ["total_signal"]
backgrounds = ["tWZ", "ttX", "tZq", "triBoson", "ggToZZ", "nonprompt"]


processinfo = {
    "total_signal": ("t#bar{t}Z + WZ + ZZ", ROOT.kAzure+7),
    "sm":        ("t#bar{t}Z + WZ + ZZ", ROOT.kAzure+7),
    "ttZ":       ("t#bar{t}Z", color.TTZ),
    "WZ":        ("WZ",  color.WZ),
    "ZZ":        ("ZZ", color.ZZ),
    "tWZ":       ("tWZ", color.TWZ),
    "ttX":       ("t#bar{t}X", color.TTX_rare),
    "tZq":       ("tZq", color.TZQ),
    "triBoson":  ("Triboson", color.triBoson),
    "ggToZZ":    ("gg #rightarrow ZZ", color.ZZ),
    "nonprompt": ("Nonprompt", color.nonprompt),
}


for r in range(1, nRegions+1):
    region = regions[r]
    WCname = "cHq1Re1122" if region in ["ZZ", "WZ"] else "cHq1Re33"
    h_data_prefit = getObjFromFile(combineInput, region+"__"+histname+"/data_obs")
    additionalOption = ""
    if region in ["WZ"]:
        # additionalOption = "ignoreCovWarning_"
        additionalOption = "minimizerStrategy_"
    filename = directory+"fitDiagnostics.topEFT_ULRunII_"+str(r)+"_13TeV_ULRunII_1D-"+WCname+"_margin_"+additionalOption+"SHAPES.root"
    # Setup plotter
    p = Plotter("PostFit_ULRunII__"+region+"__"+histname)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z #it{p}_{T} [GeV]"
    p.drawRatio = True
    # p.ratiotitle = "#splitline{Ratio}{to SM}"
    p.subtext = "Preliminary"
    p.legshift = (-0.1, -0.1, 0.0, 0.0)
    regiontext = "SR"
    if region == "ttZ":
        regiontext+="_{t#bar{t}Z}"
    elif region == "WZ":
        regiontext+="_{WZ}"
    elif region == "ZZ":
        regiontext+="_{ZZ}"
    regiontext+=", PostFit"
    p.addText(0.22, 0.7, regiontext, font=43, size=16)
    for process in signals+backgrounds:
        h_bkg = getObjFromFile(filename, "shapes_fit_s/topEFT_ULRunII_"+str(r)+"_13TeV/"+process)
        h_bkg_converted = convertBinning(h_data_prefit, h_bkg)
        p.addBackground(h_bkg_converted, processinfo[process][0], processinfo[process][1])
    p.addData(h_data_prefit)
    p.draw()
