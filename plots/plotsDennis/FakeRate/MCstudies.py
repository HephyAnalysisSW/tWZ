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



def adjustHistogram(hist):
    hist.Rebin(2)
    hist.GetXaxis().SetRangeUser(0, 400)
    return hist
    
def makeDummySys(hist, variation):
    sys = hist.Clone()
    Nbins = hist.GetSize()-2
    for i in range(Nbins):
        bin = i+1 
        sys.SetBinContent(bin, hist.GetBinContent(bin)*(1.0+variation))
    return sys
    
ROOT.gROOT.SetBatch(ROOT.kTRUE)

path_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3_noData_nonpromptOnly_FakeRateSF/"
path_SR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3_noData_nonpromptOnly/"

prefix_CR = "trilepL-trilepTCR-"
prefix_SR = "trilepT-"


selections = [
    "minDLmass12/",
    # "minDLmass12-onZ1-btag0-met60/",
    # "minDLmass12-onZ1-njet3p-btag1p/",
    # "minDLmass12-offZ1-btag0-met60/",
    # "minDLmass12-offZ1-njet3p-btag1p/",
    "minDLmass12-btag0-met60/",
    "minDLmass12-njet3p-btag1p/",
]

years = ["UL2018"]
channels = ["all"]

histname = "Z1_pt__nonprompt"

logger.info("Apply fake rate to control region and compare with signal region")

for year in years: 
    logger.info("Running year %s", year)
    for selection in selections:
        logger.info("Selection = %s", selection)
        for channel in channels:
            filename_SR = path_SR+year+"/"+channel+"/"+prefix_SR+selection+"/Results.root"
            filename_CR = path_CR+year+"/"+channel+"/"+prefix_CR+selection+"/Results.root"
            # print filename_CR, filename_SR
            hist_SR = getObjFromFile(filename_SR, histname) 
            hist_CR = getObjFromFile(filename_CR, histname)
            # hist_CR_up = makeDummySys(hist_CR,  0.3)        
            # hist_CR_dn = makeDummySys(hist_CR, -0.3)        
            hist_SR = adjustHistogram(hist_SR)
            hist_CR = adjustHistogram(hist_CR)  
            # hist_CR_up = adjustHistogram(hist_CR_up)
            # hist_CR_dn = adjustHistogram(hist_CR_dn)
            plotdir = plot_directory+"/FakeRate/"+selection
            if not os.path.exists( plotdir ): os.makedirs( plotdir )
            p = Plotter(year+"__"+channel)
            p.plot_dir = plotdir
            p.drawRatio = True
            p.xtitle = "Z p_{T}"
            p.addData(hist_SR, "SR")
            p.addBackground(hist_CR, "CR*fakerate", 15)
            # p.addSystematic(hist_CR_up, hist_CR_dn, "FakeRateNorm", "CR*fakerate")
            p.draw()
            
