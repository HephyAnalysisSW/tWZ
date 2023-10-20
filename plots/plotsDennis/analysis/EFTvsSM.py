#!/usr/bin/env python

import ROOT
import array
import Analysis.Tools.syncer
import os

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
args = argParser.parse_args()



def getHist(fname, hname, altbinning=False):
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
    hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    return hist

################################################################################
### Setup
logger.info( "Compare EFT and SM files")

# histname
histname = "Z1_pt"

version = "v11"
logger.info( "Version = %s", version )

# Directories
dirs = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint_noData/YEAR/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint_noData/YEAR/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint_noData/YEAR/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
}

processes = {
    "ZZ":  ("ZZ", "ZZ_pythia"),
    "WZ":  ("WZ", "WZTo3LNu_powheg"),
    "ttZ": ("ttZ", "ttZ_sm"),
}

lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}


outdir = plot_directory+"/EFTvsSMv2/"
if not os.path.exists( outdir ): os.makedirs( outdir )

for year in ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]:
    for region in ["WZ", "ZZ", "ttZ"]:
        altbinning = region=="ZZ"
        (process_eft, process_sm) = processes[region]
        file = dirs[region].replace("YEAR", year)+"Results.root"
        h_SM  = getHist(file, histname+"__"+process_sm, altbinning)
        h_EFT = getHist(file, histname+"__"+process_eft, altbinning)
        h_EFT_muR_up   = getHist(file.replace("noData", "noData_Scale_UPNONE"), histname+"__"+process_eft, altbinning)
        h_EFT_muR_down = getHist(file.replace("noData", "noData_Scale_DOWNNONE"), histname+"__"+process_eft, altbinning)
        h_EFT_muF_up   = getHist(file.replace("noData", "noData_Scale_NONEUP"), histname+"__"+process_eft, altbinning)
        h_EFT_muF_down = getHist(file.replace("noData", "noData_Scale_NONEDOWN"), histname+"__"+process_eft, altbinning)

        f_xs = 1.11 if region=="ttZ" else (1.17 if region=="WZ" else 1.02)
        SF = h_EFT.Integral()/h_SM.Integral()
        SF_xscorr = h_EFT.Integral()/(h_SM.Integral()*f_xs)
        h_SM.Scale(SF)

        print SF, 1/SF
        print SF_xscorr, 1/SF_xscorr


        p = Plotter(year+"__"+region+"__"+histname)
        p.plot_dir = outdir
        p.lumi = lumi[year]
        p.xtitle = "Z p_{T} [GeV]"
        p.drawRatio = True
        # p.setCustomXRange(0,600)
        p.addBackground(h_EFT, "EFT sample", 15)
        p.addSignal(h_SM, "SM sample", ROOT.kRed)
        p.addSystematic(h_EFT_muR_up, h_EFT_muR_down, "muR", "EFT sample")
        p.addSystematic(h_EFT_muF_up, h_EFT_muF_down, "muF", "EFT sample")
        p.draw()
