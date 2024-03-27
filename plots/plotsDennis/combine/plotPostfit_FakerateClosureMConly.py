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


def getHist(fname, hname):
    # bins  = [0, 60, 120, 180, 1000]
    bins  = [0, 40, 100, 180, 1000]
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
args = argParser.parse_args()

lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
    "ULRunII":      "138",
}

fname = "DataCards_FakerateClosureMConly/"+args.year+"/fitDiagnostics.FakerateClosureMConly_ULRunII_REGION_13TeV_"+args.year+"_SHAPES.root"
print fname

regions = {
    "WZ":       ["FakerateClosureMConly_ULRunII_1_13TeV"],
    "ttZ":      ["FakerateClosureMConly_ULRunII_2_13TeV"],
    "combined": ["ch1", "ch2"],
}

plotdir = plot_directory+"/PostFit_FakerateClosureMConly/"+args.year+"/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

dataHists = {
    "WZ": getObjFromFile("/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_FakerateClosureMConly/"+args.year+"/CombineInput.root", "WZ__Z1_pt/data_obs"),
    "ttZ": getObjFromFile("/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_FakerateClosureMConly/"+args.year+"/CombineInput.root", "ttZ__Z1_pt/data_obs"),
}


for region in ["ttZ", "WZ", "combined"]:
    for dir in regions[region]:
        p = Plotter(region+"__"+dir)
        p.plot_dir = plotdir
        p.lumi = lumi[args.year]
        p.xtitle = "Z p_{T} [GeV]"
        p.drawRatio = True
        p.ratiorange = (0.2, 1.8)
        p.legshift = (-0.05, -0.27, 0.0, 0.0)
        p.NcolumnsLegend = 1
        filename = fname
        if region == "WZ":
            filename = filename.replace("REGION", "1")
        elif region == "ttZ":
            filename = filename.replace("REGION", "2")
        elif region == "combined":
            filename = filename.replace("REGION", "combined")
        # print filename, "shapes_fit_b/"+dir+"/nonprompt"
        hist = getHist(filename, "shapes_fit_b/"+dir+"/nonprompt")
        p.addBackground(hist, "Nonprompt prediction from CR", 13)
        datastring = region
        if region == "combined":
            datastring = "WZ" if dir == "ch1" else "ttZ"
        h_data = dataHists[datastring].Clone()
        p.addData(h_data, "Nonprompt MC from SR")
        p.draw()
