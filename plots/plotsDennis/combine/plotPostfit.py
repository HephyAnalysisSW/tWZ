#!/usr/bin/env python

import ROOT
import array
import os
import Analysis.Tools.syncer
import ctypes

from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
from tWZ.Tools.CMScolors                         import CMScolors

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

ROOT.gROOT.SetBatch(ROOT.kTRUE)


def getHist(fname, hname, altbinning=False, isData=False):
    # print("-----------------------")
    # print(fname)
    # print(hname)
    bins  = [0, 60, 120, 180, 240, 300, 400, 1000]
    if altbinning:
        bins  = [0, 60, 120, 180, 1000]
    Nbins = len(bins)-1
    hist_oldbins = getObjFromFile(fname, hname)
    hist_newbins = ROOT.TH1F(hist_oldbins.GetName()+"_rebin", hist_oldbins.GetTitle()+"_rebin", Nbins, array.array('d',bins))
    for i in range(Nbins):
        bin = i+1
        if isData:
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


################################################################################
################################################################################
################################################################################
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--wc',               action='store', type=str, default="cHq1Re11-cHq1Re33")
argParser.add_argument('--light',            action='store_true', default=False)
argParser.add_argument('--minus',            action='store_true', default=False)
argParser.add_argument('--unblind',          action='store_true', default=False)
argParser.add_argument('--noBB',             action='store_true', default=False)
argParser.add_argument('--SM',               action='store_true', default=False)
argParser.add_argument('--region',           action='store', type=str, default="combined")
args = argParser.parse_args()

logger.info( "Make PostFit plot")

dirname_suffix = ""
if args.light:               dirname_suffix+="_light"
if args.minus:               dirname_suffix+="_minus"
if args.unblind:             dirname_suffix+="_UNBLINDED"
if args.noBB:                dirname_suffix+="_noBB"
if args.SM:                  dirname_suffix+="_SM"

this_dir = os.getcwd()
dataCard_dir = this_dir+"/DataCards_threePoint"+dirname_suffix+"/"+args.year+"/"
plotdir = plot_directory+"/PostFit_UL_threePoint"+dirname_suffix+"/"+args.year+"/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

processinfo = {
    "total_signal":("t#bar{t}Z + WZ + ZZ", CMScolors["sm"]),
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

if args.SM:
    fname = dataCard_dir+"/fitDiagnostics.topEFT_ULRunII_"+args.region+"_13TeV_"+args.year+"_SHAPES.root"
else:
    fname = dataCard_dir+"/fitDiagnostics.topEFT_ULRunII_"+args.region+"_13TeV_"+args.year+"_1D-"+args.wc+"_margin_SHAPES.root"

if args.region == "combined":
    regions = ["ttZ", "WZ", "ZZ"]
else:
    regions = ["topEFT_ULRunII_"+args.region+"_13TeV"]

for region in regions:
    if args.SM:
        plotname = "PostFit__"+region
    else:
        plotname = "PostFit__"+region+"__"+args.wc
    p = Plotter(plotname)
    p.plot_dir = plotdir
    p.lumi = lumi[args.year]
    p.xtitle = "Z boson candidate #it{p}_{T} [GeV]"
    p.drawRatio = True
    p.ratiorange = (0.2, 1.8)
    for process in processinfo.keys():
        if region in ["ZZ", "topEFT_ULRunII_1_13TeV"] and process == "nonprompt":
            continue
        dir = region
        if region == "ttZ":
            dir = "ch3"
        elif region == "WZ":
            dir = "ch2"
        elif region == "ZZ":
            dir = "ch1"

        ZZbinning = True if region in ["ZZ", "topEFT_ULRunII_1_13TeV"] else False
        hist = getHist(fname, "shapes_fit_s/"+dir+"/"+process, ZZbinning)
        p.addBackground(hist, processinfo[process][0], processinfo[process][1])
    h_data = getHist(fname, "shapes_fit_s/"+dir+"/data", ZZbinning, True)
    p.addData(h_data)
    p.draw()
