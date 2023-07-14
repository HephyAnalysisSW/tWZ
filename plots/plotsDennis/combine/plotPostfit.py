#!/usr/bin/env python

import ROOT
import array
import os
import Analysis.Tools.syncer

from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)


def getHist(fname, hname, altbinning=False):
    bins  = [0, 60, 120, 180, 240, 300, 400, 1000]
    if altbinning:
        bins  = [0, 60, 120, 180, 1000]
    Nbins = len(bins)-1
    hist_oldbins = getObjFromFile(fname, hname)
    hist_newbins = ROOT.TH1F(hist_oldbins.GetName()+"_rebin", hist_oldbins.GetTitle()+"_rebin", Nbins, array.array('d',bins))
    for i in range(Nbins):
        bin = i+1
        hist_newbins.SetBinContent( bin, hist_oldbins.GetBinContent(bin) )
        hist_newbins.SetBinError( bin, hist_oldbins.GetBinError(bin) )
    return hist_newbins


import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--wc',               action='store', type=str, default="cHq1Re11")
args = argParser.parse_args()

processes = ["sm", "tWZ", "ttX", "tZq", "triBoson", "nonprompt"]

processinfo = {
    "sm":        ("ttZ+WZ+ZZ", ROOT.kAzure+7),
    "tWZ":       ("tWZ", color.TWZ),
    "ttX":       ("ttX", color.TTX_rare),
    "tZq":       ("tZq", color.TZQ),
    "triBoson":  ("Triboson", color.triBoson),
    "nonprompt": ("Nonprompt", color.nonprompt),
}

lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}

fname = "DataCards_threePoint_light/"+args.year+"/fitDiagnostics.topEFT_ULRunII_REGION_13TeV_"+args.year+"_1D-"+args.wc+"_margin_SHAPES.root"


plotdir = plot_directory+"/PostFit_threePoint/"+args.year+"/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

for region in ["ttZ", "WZ", "ZZ"]:
    p = Plotter(region+"__"+args.wc)
    p.plot_dir = plotdir
    p.lumi = lumi[args.year]
    p.xtitle = "Z p_{T} [GeV]"
    p.drawRatio = True
    p.ratiorange = (0.2, 1.8)
    for process in processinfo.keys():
        if region == "ZZ" and process == "nonprompt":
            continue
        dir = ""
        if region == "ttZ":
            dir = "ch3"
        elif region == "WZ":
            dir = "ch2"
        elif region == "ZZ":
            dir = "ch1"

        ZZbinning = True if region == "ZZ" else False
        hist = getHist(fname, "shapes_fit_s/"+dir+"/"+process, ZZbinning)
        p.addBackground(hist, processinfo[process][0], processinfo[process][1])
    p.draw()
    histtot = getHist(fname, "shapes_fit_s/"+dir+"/total", ZZbinning)
