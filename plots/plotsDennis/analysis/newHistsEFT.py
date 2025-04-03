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
args = argParser.parse_args()

logger.info("Plot EFT effects")
###############################################################################
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
    # hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    return hist
################################################################################
ROOT.gROOT.SetBatch(ROOT.kTRUE)
WCnames = [
    "cHqMRe1122",
    "cHqMRe33",
    "cHq3MRe1122",
    "cHq3MRe33",
    "cHuRe1122",
    "cHuRe33",
    "cHdRe1122",
    "cHdRe33",
    "cW",
    "cWtil",
]

histnames = {
    "Z1_pt": "Z p_{T} [GeV]",
    "deltaPhiZs": "#Delta #phi(Z_{1}, Z_{2})",
    "deltaPhiLeptons": "#Delta #phi(l_{1}^{Z2}, l_{2}^{Z2})",
}

infile = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/UL2018/all/qualepT-minDLmass12-onZ1-onZ2/Results.root"

outdir = plot_directory+"/NewHists/"
if not os.path.exists( outdir ): os.makedirs( outdir )

for histname in histnames.keys():
    altbinning = True
    h_sm = getHist(infile, histname+"__ZZ", altbinning)
    ymax = h_sm.GetMaximum()
    for wc in WCnames:
        h_plus = getHist(infile, histname+"__ZZ__"+wc+"=1.0000", altbinning)
        h_minus = getHist(infile, histname+"__ZZ__"+wc+"=-1.0000", altbinning)
        p = Plotter("UL2018__ZZ__"+histname+"__"+wc)
        p.plot_dir = outdir
        p.lumi = "60"
        p.xtitle = histnames[histname]
        p.drawRatio = True
        p.ratiotitle = "#frac{EFT+SM}{SM}"
        p.NcolumnsLegend = 1
        if wc == "cHq3MRe1122":
            p.ratiorange = 0.0, 2.0
            p.setCustomYRange(0, ymax*2.5)
        else:
            p.ratiorange = 0.85, 1.15
            p.setCustomYRange(0, ymax*1.7)
        p.addBackground(h_sm, "ZZ (SM)", 15)
        p.addSignal(h_plus,  "ZZ ("+wc+" = +1)", ROOT.kAzure+7, 1)
        p.addSignal(h_minus, "ZZ ("+wc+" = -1)", ROOT.kRed, 2)
        p.draw()
