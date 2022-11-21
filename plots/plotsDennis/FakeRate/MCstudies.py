#!/usr/bin/env python

import os
import ROOT
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
argParser.add_argument('--splitnonprompt', action='store_true', default=False)
argParser.add_argument('--noLooseSel',     action='store_true')
argParser.add_argument('--noLooseWP',      action='store_true')
args = argParser.parse_args()

logger.info("Apply fake rate to control region and compare with signal region")
if args.splitnonprompt:
    logger.info("Splitting non-prompt into Top and DY")
    
################################################################################
# Some functions
def adjustHistogram(hist, nrebin, xmax):
    hist.Rebin(nrebin)
    hist.GetXaxis().SetRangeUser(0, xmax)
    return hist
    
def makeDummySys(hist, variation):
    sys = hist.Clone()
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1 
        sys.SetBinContent(bin, hist.GetBinContent(bin)*(1.0+variation))
    return sys
################################################################################    
ROOT.gROOT.SetBatch(ROOT.kTRUE)

path_SR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3_noData_nonpromptOnly/"
path_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3_noData_nonpromptOnly_FakeRateSF/"
if args.splitnonprompt:
    path_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3_noData_nonpromptOnly_splitnonprompt_FakeRateSF/"
    path_SR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3_noData_nonpromptOnly_splitnonprompt/"

suffix = ""
if args.noLooseSel:
    path_CR = path_CR.replace("_FakeRateSF", "_FakeRateSF_noLooseSel")
    suffix = "__noLooseSel"
if args.noLooseWP:
    path_CR = path_CR.replace("_FakeRateSF", "_FakeRateSF_noLooseWP")
    suffix = "__noLooseWP"
    

prefix_CR = "trilepL-trilepTCR-"
if args.noLooseWP:
    prefix_CR = prefix_CR.replace("trilepL", "trilepVL")

prefix_SR = "trilepT-"


selections = [
    # "minDLmass12/",
    # "minDLmass12-btag0-met60/",
    # "minDLmass12-njet3p-btag1p/",
    # "minDLmass12-onZ1/",
    "minDLmass12-onZ1-btag0-met60/",
    "minDLmass12-onZ1-njet3p-btag1p/",
]

years = ["UL2018"]
channels = ["all"]

histnames = ["N_jets", "Z1_pt", "l1_pt", "l2_pt", "l3_pt"]
object = {
    "N_jets": "Number of jets",
    "Z1_pt": "Z", 
    "l1_pt": "Leading lepton", 
    "l2_pt": "Sub-leading lepton", 
    "l3_pt": "Trailing lepton",
}

rebin = {
    "N_jets": 1,
    "Z1_pt": 4, 
    "l1_pt": 1, 
    "l2_pt": 1, 
    "l3_pt": 1,
}

xmax = {
    "N_jets": 10.5, 
    "Z1_pt": 300, 
    "l1_pt": 200, 
    "l2_pt": 150, 
    "l3_pt": 100,
}

processes = ["nonprompt"]
if args.splitnonprompt:
    processes = ["tt+ST", "DY"]


plotters = {}

for year in years: 
    logger.info("Running year %s", year)
    for selection in selections:
        logger.info("Selection = %s", selection)
        for channel in channels:
            for process in processes:
                logger.info("Process = %s", process)
                for histname in histnames:            
                    filename_SR = path_SR+year+"/"+channel+"/"+prefix_SR+selection+"/Results.root"
                    filename_CR = path_CR+year+"/"+channel+"/"+prefix_CR+selection+"/Results.root"
                    # logger.info("Reading SR from %s", filename_SR)
                    # logger.info("Reading CR from %s", filename_CR)
                    hist_SR = getObjFromFile(filename_SR, histname+"__"+process) 
                    hist_CR = getObjFromFile(filename_CR, histname+"__"+process)
                    hist_SR = adjustHistogram(hist_SR, rebin[histname], xmax[histname])
                    hist_CR = adjustHistogram(hist_CR, rebin[histname], xmax[histname])  
                    plotdir = plot_directory+"/FakeRate/ClosureTest/"+selection
                    if not os.path.exists( plotdir ): os.makedirs( plotdir )
                    p = Plotter(year+"__"+channel+"__"+process+"__"+histname+suffix)
                    p.plot_dir = plotdir
                    p.drawRatio = True
                    p.ratiorange = (0.2, 1.8)
                    p.xtitle = object[histname]+" p_{T} [GeV]"
                    if "N_jets" in histname: p.xtitle = object[histname]
                    p.addData(hist_SR, process+" [SR]")
                    p.addBackground(hist_CR, process+" [CR*fakerate]", 15)
                    plotters[year+selection+channel+process+histname] = p

for name in plotters:
    plotters[name].draw()

del plotters
