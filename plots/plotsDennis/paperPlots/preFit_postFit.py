#!/usr/bin/env python

import ROOT
import array
import os
import Analysis.Tools.syncer
import ctypes

from math import sqrt

from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
from tWZ.Tools.CMScolors                         import CMScolors

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

ROOT.gROOT.SetBatch(ROOT.kTRUE)

def getHistRunII(fname, hname, bins):
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
    if bins is not None:
        hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    return hist

def getEnvelop(sigtotal, central):
    up = sigtotal.Clone("total_up")
    down = sigtotal.Clone("total_down")
    up.Reset()
    down.Reset()
    Nbins = sigtotal.GetSize()-2
    for i in range(Nbins):
        bin = i+1
        c = central.GetBinContent(bin)
        e = sigtotal.GetBinError(bin)
        up.SetBinContent(bin, c+e)
        down.SetBinContent(bin, c-e)
    return up, down


def getHist(fname, hname, bins, isGraph=False):
    # print("-----------------------")
    # print(fname)
    # print(hname)
    Nbins = len(bins)-1
    hist_oldbins = getObjFromFile(fname, hname)
    hist_newbins = ROOT.TH1F(hist_oldbins.GetName()+"_rebin", hist_oldbins.GetTitle()+"_rebin", Nbins, array.array('d',bins))
    for i in range(Nbins):
        bin = i+1
        if isGraph:
            x = ctypes.c_double(0.)
            y = ctypes.c_double(0.)
            hist_oldbins.GetPoint(i, x, y)
            error = hist_oldbins.GetErrorY(i)
            hist_newbins.SetBinContent( bin, y.value )
            hist_newbins.SetBinError( bin, error )
        else:
            hist_newbins.SetBinContent( bin, hist_oldbins.GetBinContent(bin) )
            hist_newbins.SetBinError( bin, hist_oldbins.GetBinError(bin) )
    return hist_newbins

def getSumOfSignals(fname, dirname, bins):
    histnames = []
    file = ROOT.TFile(fname, "READ")
    dir = file.Get(dirname)
    for key in dir.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, ROOT.TH1):
            hname = obj.GetName()
            if "sm" == hname or "sm_" in hname or "quad_" in hname:
                histnames.append(hname)
    file.Close()
    hists = []
    for hname in histnames:
        hists.append( getHist(fname, dirname+"/"+hname, bins) )
    histsum = sumHistsCorrelated(hists, bins)
    return histsum

def sumHistsCorrelated(hists, bins):
    histsum = hists[0].Clone("sumOfSignals")
    histsum.Reset()
    Nbins = len(bins)-1
    for i in range(Nbins):
        bin = i+1
        binContent = 0
        binError = 0
        for h in hists:
            c = h.GetBinContent(bin)
            e = h.GetBinError(bin)
            binContent += c
            binError += e*e
        histsum.SetBinContent(bin, binContent)
        histsum.SetBinError(bin, sqrt(binError))
    return histsum


################################################################################
################################################################################
################################################################################
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--binning', action='store', default="A")
args = argParser.parse_args()

logger.info( "Make PostFit plot")

dir = "/users/dennis.schwarz/CMSSW_10_6_28/src/tWZ/plots/plotsDennis/combine/DataCards_threePoint_light_minus_UNBLINDED_binning-A_SMZero/ULRunII"
filename = "POSTFITSHAPES.topEFT_ULRunII_combined_13TeV_ULRunII_fullFit_noScan.root"
# filename = "POSTFITSHAPES.topEFT_ULRunII_combined_13TeV_ULRunII_1D-cHqMRe33_float_noScan.root"
# filename = "POSTFITSHAPES.topEFT_ULRunII_combined_13TeV_ULRunII_1D-cHqMRe33_margin_noScan.root"
postFitFile = os.path.join(dir, filename)
postFitFile = "PostFitShapes.root"


plotdir = plot_directory+"/PaperPlots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )


################################################################################
bins_ttZ  = [0, 40, 80, 120, 160, 200, 260, 340, 1000]
bins_WZ  = [0, 20, 40, 60, 80, 100, 120, 140, 180, 220, 260, 300, 340, 380, 420, 500, 1000]
bins_ZZ  = [0, 20, 40, 60, 80, 120, 200, 1000]
if args.binning == "A":
    bins_ttZ  = [40, 80, 120, 160, 200, 260, 340, 1000]
    bins_WZ  = [40, 60, 80, 100, 120, 140, 180, 220, 260, 300, 340, 380, 420, 500, 1000]
    bins_ZZ  = [40, 60, 80, 120, 200, 1000]
################################################################################

path_ZZ     = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/qualepT-minDLmass12-onZ1-onZ2/Results.root"
path_WZ     = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
path_ttZ    = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"

processinfo = {
    "Signal":  ("t#bar{t}Z + WZ + ZZ", CMScolors["sm"]),
    # "SignalSum":  ("t#bar{t}Z + WZ + ZZ", CMScolors["sm"]),
    "tWZ":       ("tWZ", CMScolors["tWZ"]),
    "ttX":       ("t#bar{t}X", CMScolors["ttX"]),
    "tZq":       ("tZq", CMScolors["tZq"]),
    "triBoson":  ("Triboson", CMScolors["triboson"]),
    "nonprompt": ("Nonprompt", CMScolors["nonprompt"]),
    "ggToZZ":    ("gg #rightarrow ZZ", CMScolors["ggZZ"]),
}

lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}

regions = ["ttZ", "WZ", "ZZ"]
rootDir = {
    "ttZ": "ch3_prefit",
    "WZ" : "ch2_prefit",
    "ZZ" : "ch1_prefit",
}

rates = {
        "tWZ":       0.20,
        "ttX":       0.20,
        "tZq":       0.10,
        "triBoson":  0.20,
        "ggToZZ":    0.2,
}

for region in regions:
    for doLog in [True,False]:
        bins=[]
        prefitfile = None
        mainprocess = None
        if region in ["ttZ", "topEFT_ULRunII_3_13TeV"]:
            bins = bins_ttZ
            prefitfile = path_ttZ
            mainprocess = "t#bar{t}Z"
        elif region in ["WZ", "topEFT_ULRunII_2_13TeV"]:
            bins = bins_WZ
            prefitfile = path_WZ
            mainprocess = "WZ"
        elif region in ["ZZ", "topEFT_ULRunII_1_13TeV"]:
            bins = bins_ZZ
            prefitfile = path_ZZ
            mainprocess = "ZZ"

        plotname = "PrePostFit__"+region

        if doLog:
            plotname+="__log"
        p = Plotter(plotname)
        p.plot_dir = plotdir
        p.lumi = lumi["ULRunII"]
        p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
        p.ytitle = "Events / GeV"
        p.ratiotitle = "#splitline{Ratio to}{PreFit}"
        p.drawRatio = True
        p.ratiorange = (0.7, 1.3)
        if region == "WZ":
            p.ratiorange = (0.55, 1.15)
        p.divideByWidth = True
        p.legshift = (-0.1, 0., 0., 0.)
        p.legtextsize = 0.045
        p.horizontalErrors = True
        p.logoAbovePlot = True
        p.subtext = ""


        if doLog:
            p.log = True
            if region in ["WZ", "topEFT_ULRunII_2_13TeV"]:
                p.setCustomYRange(0.0008, 50000)
            elif region in ["ZZ", "topEFT_ULRunII_1_13TeV"]:
                p.setCustomYRange(0.0008, 1000)
            elif region in ["ttZ", "topEFT_ULRunII_3_13TeV"]:
                p.setCustomYRange(0.0008, 5000)
        for process in processinfo.keys():
            # print(process)
            if region in ["ZZ", "topEFT_ULRunII_1_13TeV"] and process == "nonprompt":
                continue
            dir = region
            if region == "ttZ":
                dir = "ch3"
            elif region == "WZ":
                dir = "ch2"
            elif region == "ZZ":
                dir = "ch1"
            if process == "Signal":
                hist_ZZ = getHistRunII(prefitfile, "Z1_pt__ZZ_powheg", bins)
                hist_WZ = getHistRunII(prefitfile, "Z1_pt__WZTo3LNu", bins)
                hist_ttZ = getHistRunII(prefitfile, "Z1_pt__ttZ_sm", bins)
                p.addBackground(hist_ZZ, "ZZ", CMScolors["ZZ"])
                p.addBackground(hist_WZ, "WZ", CMScolors["WZ"])
                p.addBackground(hist_ttZ, "t#bar{t}Z", CMScolors["ttZ"])
                # Also get SM hist prefit for uncertainties
                sigtotal = getHist(postFitFile, rootDir[region]+"/TotalSig", bins)
                if region == "ttZ":
                    up, down = getEnvelop(sigtotal, hist_ttZ)
                    p.addSystematic(up, down, "total_sig_sys", "t#bar{t}Z")
                elif region == "WZ":
                    up, down = getEnvelop(sigtotal, hist_WZ)
                    p.addSystematic(up, down, "total_sig_sys", "WZ")
                elif region == "ZZ":
                    up, down = getEnvelop(sigtotal, hist_ZZ)
                    p.addSystematic(up, down, "total_sig_sys", "ZZ")
                # p.addNormSystematic(self, bkgname, size)

            else:
                hist = getHist(postFitFile, rootDir[region]+"/"+process, bins)
                p.addBackground(hist, processinfo[process][0], processinfo[process][1])
                if process in rates.keys():
                    p.addNormSystematic(processinfo[process][0], rates[process])
        h_data = getHist(postFitFile, rootDir[region]+"/data_obs", bins, False)
        p.addData(h_data)
        h_post_total = getHist(postFitFile, rootDir[region].replace("prefit", "postfit")+"/TotalProcs", bins)
        p.addSignal(h_post_total, "PostFit", ROOT.kRed)
        regiontext = "SR"
        if region == "ttZ":
            regiontext+="_{t#bar{t}Z}"
        elif region == "WZ":
            regiontext+="_{WZ}"
        elif region == "ZZ":
            regiontext+="_{ZZ}"
        # regiontext+=", PostFit"
        p.addText(0.25, 0.8, regiontext, font=43, size=20)
        p.draw()
