#!/usr/bin/env python

import ROOT
import array
import Analysis.Tools.syncer
import os
import numpy as np

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)



def getHist(fname, hname, bins):
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

def getNonpromptFromCR(fname, histname, bins, backgrounds):
    # Get prompt backgrounds in CR
    firstbkg = True
    for bkg in backgrounds:
        # print fname, histname+"__"+bkg
        h_bkg = getHist(fname, histname+"__"+bkg, bins)
        if firstbkg:
            h_bkg_CR = h_bkg.Clone()
            firstbkg = False
        else:
            h_bkg_CR.Add(h_bkg)
    # Get nonprompt = Data in CR * fakerate and subtract backgrounds
    h_nonprompt = getHist(fname, histname+"__data", bins)
    h_nonprompt.Add(h_bkg_CR, -1)
    return h_nonprompt

def getCombinedSignal_SM(fname, hname, bins, rate=None, rate_process=None, sys_processes=[], fname_sys=None):
    signals = ["ttZ_sm", "WZTo3LNu_powheg", "ZZ_powheg"]
    for i_sig, sig in enumerate(signals):
        # If one of the signals should be varied, use alternative file
        filename = fname
        if sig in sys_processes:
            filename = fname_sys
        # If this is the first in the loop clone, otherwise Add to cloned
        if i_sig==0:
            hist = getHist(filename, hname.replace("sm", sig), bins)
            if sig == rate_process:
                hist.Scale(rate)
        else:
            tmp = getHist(filename, hname.replace("sm", sig), bins)
            if sig == rate_process:
                tmp.Scale(rate)
            hist.Add(tmp)
    return hist


bins_ttZ  = [0, 40, 80, 120, 160, 200, 260, 340, 1000]
bins_WZ  = [0, 20, 40, 60, 80, 100, 120, 140, 180, 220, 260, 300, 340, 380, 420, 500, 1000]
bins_ZZ  = [0, 20, 40, 60, 80, 120, 200, 1000]

histname = "Z1_pt"
version = "v15"
dataTag = "_noData"
year = "ULRunII"

dirs = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+year+"/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+year+"/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+year+"/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
    "WZ_CR":  "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_threePoint_FakeRateSF_useDataSF/"+year+"/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/",
    "ttZ_CR": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_threePoint_FakeRateSF_useDataSF/"+year+"/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/",
}
inname = 'Results.root'

plotdir = plot_directory+"/BinningStudies/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

# Define backgrounds
processes = ["sm", "tWZ", "ttX", "tZq", "triBoson", "ggToZZ", "nonprompt"]
processes_CR = ["ttZ_sm", "WZTo3LNu_powheg", "ZZ_powheg", "tWZ", "ttX", "tZq", "triBoson", "ggToZZ"]

processinfo = {
    "sm":        ("ttZ+WZ+ZZ", ROOT.kAzure+7),
    "ttZ":       ("ttZ", color.TTZ),
    "WZ":        ("WZ",  color.WZ),
    "ZZ":        ("ZZ", color.ZZ),
    "tWZ":       ("tWZ", color.TWZ),
    "ttX":       ("ttX", color.TTX_rare),
    "tZq":       ("tZq", color.TZQ),
    "triBoson":  ("Triboson", color.triBoson),
    "ggToZZ":    ("gg #rightarrow ZZ", color.ZZ),
    "nonprompt": ("Nonprompt", color.nonprompt),
}

for region in ["ttZ", "WZ", "ZZ"]:
    bins = []
    if region == "ttZ" or region == "ttZ_CR":
        bins = bins_ttZ
    elif region == "WZ" or region == "WZ_CR":
        bins = bins_WZ
    elif region == "ZZ":
        bins = bins_ZZ


    logger.info( 'Filling region %s', region )
    p = Plotter(region+"__"+histname)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.drawRatio = True
    # p.divideByWidth = True
    # p.ytitle = "Events / GeV [GeV^{-1}]"

    for process in processes:
        logger.info( '  %s', process )
        ########################################################################
        ## First get the nominal processes.
        ## Nonprompt needs special treatment because it is constructed from
        ## a control region
        if process == "nonprompt" and region in ["ttZ", "WZ"]:
            # Get prompt backgrounds in CR
            logger.info( '    (estimate from CR)')
            h_nonprompt = getNonpromptFromCR(dirs[region+"_CR"]+inname, histname, bins, processes_CR)
            p.addBackground(h_nonprompt, processinfo[process][0], processinfo[process][1])
        else:
            logger.info( '    read nominal')
            # The SM also needs special treatment because we need to sum ttZ, WZ and ZZ
            # Also, we construct the lin and quad histograms for the EFT fit
            if process == "sm":
                h_sm = getCombinedSignal_SM(dirs[region]+inname, histname+"__"+process, bins)
                p.addBackground(h_sm, processinfo[process][0], processinfo[process][1])
            else:
                name = histname+"__"+process
                h_bkg = getHist(dirs[region]+inname, name, bins)
                p.addBackground(h_bkg, processinfo[process][0], processinfo[process][1])

    logger.info( '  DATA' )
    filename = dirs[region]+inname
    filename = filename.replace("_noData", "_onlyData")
    observed = getHist(filename, histname+"__data", bins)
    p.addData(observed, "Data")
    p.draw()
