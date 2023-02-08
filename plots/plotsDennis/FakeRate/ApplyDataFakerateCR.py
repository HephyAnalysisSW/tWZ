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
args = argParser.parse_args()

logger.info("Apply fake rate to control region and compare with signal region")
    
################################################################################
# Some functions
def adjustHistogram(hist, nrebin, xmax):
    hist.Rebin(nrebin)
    hist.GetXaxis().SetRangeUser(0, xmax)
    return hist
    
def getSumOfHistograms(filename, names):
    if len(names) < 1:
        raise Exception("Legth of names is 0")
    hist = getObjFromFile(filename, names[0])
    for i, name in enumerate(names):
        if i==0:
            continue
        else:
            hist_tmp = getObjFromFile(filename, name)
            hist.Add(hist_tmp)
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

path_SR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v5/"
path_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v5_FakeRateSF_useDataSF/"

prefix_SR = "trilepT-"
prefix_CR = "trilepFOnoT-"

selections = [
    "minDLmass12-offZ1/",
    "minDLmass12-offZ1-njet3p-btag1p/",
    "minDLmass12-offZ1-btag0-met60/",
]

years = ["UL2017", "UL2018"]
channels = ["all"]

histnames = ["N_jets", "Z1_pt", "l1_pt", "l2_pt", "l3_pt"]
# histnames = ["N_jets", "Z1_pt", "l1_pt", "l2_pt", "l3_pt"]
object = {
    "N_jets": "Number of jets",
    "Z1_pt": "Z", 
    "l1_pt": "Leading lepton", 
    "l2_pt": "Sub-leading lepton", 
    "l3_pt": "Trailing lepton",
}

rebin = {
    "N_jets": 1,
    "Z1_pt": 2, 
    "l1_pt": 4, 
    "l2_pt": 4, 
    "l3_pt": 4,
}

xmax = {
    "N_jets": 10.5, 
    "Z1_pt": 300, 
    "l1_pt": 200, 
    "l2_pt": 150, 
    "l3_pt": 100,
}

prompt_processes = [
    ("tWZ", "tWZ", color.TWZ),
    ("ttZ", "ttZ", color.TTZ),
    ("ttX", "ttX", color.TTX_rare),
    ("tZq", "tZq", color.TZQ),
    ("WZ",  "WZ",  color.WZ),
    ("triBoson", "Triboson", color.triBoson),
    ("ZZ", "ZZ", color.ZZ),
]

plotters = {}

for year in years: 
    logger.info("Running year %s", year)
    for selection in selections:
        logger.info("Selection = %s", selection)
        for channel in channels:
            for histname in histnames:
                plotdir = plot_directory+"/FakeRate/ClosureTest_data/"+selection
                if not os.path.exists( plotdir ): os.makedirs( plotdir )
                p = Plotter(year+"__"+channel+"__"+histname)
                p.plot_dir = plotdir
                p.drawRatio = True
                p.ratiorange = (0.2, 1.8)
                p.xtitle = object[histname]+" p_{T} [GeV]"
                if "N_jets" in histname: p.xtitle = object[histname]
                # Get File names
                filename_SR = path_SR+year+"/"+channel+"/"+prefix_SR+selection+"/Results.root"
                filename_CR = path_CR+year+"/"+channel+"/"+prefix_CR+selection+"/Results.root"
                # Get Data in SR
                h_data_SR = getObjFromFile(filename_SR, histname+"__data") 
                h_data_SR = adjustHistogram(h_data_SR, rebin[histname], xmax[histname])
                p.addData(h_data_SR, "Data")
                # Get nonpromt = Data in CR * fakerate
                # h_nonpromt = getObjFromFile(filename_SR, histname+"__nonprompt")
                h_nonpromt = getObjFromFile(filename_CR, histname+"__data")
                h_nonpromt = adjustHistogram(h_nonpromt, rebin[histname], xmax[histname]) 
                p.addBackground(h_nonpromt, "Nonprompt", 15)
                # Get uncertainty 
                h_nonpromt_up = getObjFromFile(filename_CR.replace("FakeRateSF_useDataSF", "FakeRateSF_useDataSF_Fakerate_UP"), histname+"__data")
                h_nonpromt_up = adjustHistogram(h_nonpromt_up, rebin[histname], xmax[histname]) 
                h_nonpromt_down = getObjFromFile(filename_CR.replace("FakeRateSF_useDataSF", "FakeRateSF_useDataSF_Fakerate_DOWN"), histname+"__data")
                h_nonpromt_down = adjustHistogram(h_nonpromt_down, rebin[histname], xmax[histname]) 
                p.addSystematic(h_nonpromt_up, h_nonpromt_down, "Fakerate", "Nonprompt")
                p.addNormSystematic("Nonprompt", 0.3)
                # Get all prompt backgrounds
                for (process,legname,color) in prompt_processes:
                    h_bkg = getObjFromFile(filename_SR, histname+"__"+process) 
                    h_bkg = adjustHistogram(h_bkg, rebin[histname], xmax[histname]) 
                    p.addBackground(h_bkg, legname, color)
                plotters[year+selection+channel+histname] = p

for name in plotters:
    plotters[name].draw()

del plotters
