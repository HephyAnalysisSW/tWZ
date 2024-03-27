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


f_addCorr = {
    "ZZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v13_reduceEFT_noData/ULRunII/all/qualepT-minDLmass12-onZ1-onZ2/Results.root",
    "WZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v13_reduceEFT_noData/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
}

f_mulCorr = {
    "ZZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v13_reduceEFT_noData_EWK_mul/ULRunII/all/qualepT-minDLmass12-onZ1-onZ2/Results.root",
    "WZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v13_reduceEFT_noData_EWK_mul/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
}

f_noCorr = {
    "ZZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v13_reduceEFT_noData_noEWK/ULRunII/all/qualepT-minDLmass12-onZ1-onZ2/Results.root",
    "WZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v13_reduceEFT_noData_noEWK/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
}

plotdir = plot_directory+"/EWKcorrections/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

for region in ["ZZ", "WZ"]:
    alternativeBinnig = False
    histname = "Z1_pt__WZTo3LNu_powheg"
    if region == "ZZ":
        alternativeBinnig = True
        histname = "Z1_pt__ZZ_powheg"

    h_noCorr = getHist(f_noCorr[region], histname, True, alternativeBinnig)
    h_addCorr = getHist(f_addCorr[region], histname, True, alternativeBinnig)
    h_mulCorr = getHist(f_mulCorr[region], histname, True, alternativeBinnig)

    systematics = []
    for (sys, sysUp, sysDown) in [ ("muR", "Scale_UPNONE", "Scale_DOWNNONE"), ("muF","Scale_NONEUP", "Scale_NONEDOWN") ]:
        h_up = getHist(f_noCorr[region].replace("noEWK", "noEWK_"+sysUp), histname, True, alternativeBinnig)
        h_down = getHist(f_noCorr[region].replace("noEWK", "noEWK_"+sysDown), histname, True, alternativeBinnig)
        systematics.append( (sys, h_up, h_down) )


    p = Plotter("ULRunII__"+region)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z #it{p}_{T} [GeV]"
    p.drawRatio = True
    p.ratiotitle = "#splitline{Ratio to}{add. EWK}"
    p.subtext = "Preliminary"
    p.legshift = (-0.1, 0.0, 0.0, 0.0)
    p.addBackground(h_noCorr, region+" (no EWK)", 15)
    p.addSignal(h_addCorr, region+" (add. EWK)", ROOT.kAzure+7)
    p.addSignal(h_mulCorr, region+" (mul. EWK)", ROOT.kRed)
    for (sysname, hUp, hDown) in systematics:
        p.addSystematic(hUp, hDown, sysname, region+" (no EWK)")
    p.draw()
