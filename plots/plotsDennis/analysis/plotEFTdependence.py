#!/usr/bin/env python

import os
import ROOT
import array
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--moreEFToperators',action='store_true', default=False)
args = argParser.parse_args()

logger.info("Plot EFT effects")

################################################################################
# Some functions
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
    # hist = removeNegative(hist)
    # if hist.Integral() < 0.01:
    #     hist = removeZeros(hist)
    return hist
################################################################################
ROOT.gROOT.SetBatch(ROOT.kTRUE)
regions = ["WZ", "ZZ", "ttZ"]
years = ["UL2016preVFP", "UL2016", "UL2017", "UL2018", "ULRunII"]
WCnames = ["cHq1Re11", "cHq1Re22", "cHq1Re33", "cHq3Re11", "cHq3Re22", "cHq3Re33", "cHq1Re1122", "cHq3Re1122"]
version = "v11"
histname = "Z1_pt"
dataTag = "_noData"

dirs = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/YEAR/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/YEAR/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/YEAR/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
}

if args.moreEFToperators:
    dirs = {
        "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"_moreEFToperators/YEAR/all/qualepT-minDLmass12-onZ1-onZ2/",
        "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"_moreEFToperators/YEAR/all/trilepT-minDLmass12-onZ1-btag0-met60/",
        "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"_moreEFToperators/YEAR/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
    }
    regions = ["ZZ", "ttZ", "WZ"]
    years = ["UL2018"]
    WCnames += [
        "cHuRe11",
        "cHuRe22",
        "cHuRe33",
        "cHdRe11",
        "cHdRe22",
        "cHdRe33",
        "cW",
        "cWtil",
    ]


lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}

outdir = plot_directory+"/EFTdependence/"
if not os.path.exists( outdir ): os.makedirs( outdir )


for year in years:
    for region in regions:
        altbinning = True if region == "ZZ" else False
        path = dirs[region].replace("YEAR", year)
        h_sm = getHist(path+"Results.root", histname+"__"+region, altbinning)
        ymax = h_sm.GetMaximum()
        for wc in WCnames:
            h_plus = getHist(path+"Results.root", histname+"__"+region+"__"+wc+"=1.0000", altbinning)
            h_minus = getHist(path+"Results.root", histname+"__"+region+"__"+wc+"=-1.0000", altbinning)
            p = Plotter(year+"__"+region+"__"+wc)
            p.plot_dir = outdir
            p.lumi = lumi[year]
            p.xtitle = "Z p_{T} [GeV]"
            p.drawRatio = True
            p.ratiotitle = "#frac{EFT+SM}{SM}"
            p.ratiorange = 0.85, 1.15
            p.setCustomYRange(0, ymax*1.7)
            p.addBackground(h_sm, region+" (SM)", 15)
            p.addSignal(h_plus,  region+" ("+wc+" = +1)", ROOT.kAzure+7, 1)
            p.addSignal(h_minus, region+" ("+wc+" = -1)", ROOT.kRed, 2)
            p.draw()

























        ######################
