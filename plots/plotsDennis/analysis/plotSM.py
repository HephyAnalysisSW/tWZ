#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter


def adjustHistogram(hist):
    hist.Rebin(2)
    hist.GetXaxis().SetRangeUser(0, 500)
    return hist


ROOT.gROOT.SetBatch(ROOT.kTRUE)
path_ZZ  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3/UL2018/all/qualepT-minDLmass12-onZ1-onZ2/Results.root"
path_WZ  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3/UL2018/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
path_ttZ = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3/UL2018/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
# path_ttZ_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v3/ULRunII/all/trilepTCR-minDLmass12-offZ1-njet3p-btag1p/Results.root"

files = {
    "ZZ" : path_ZZ,
    "WZ" : path_WZ,
    "ttZ": path_ttZ, 
    # "ttZ_CR" : path_ttZ_CR,
}

histname = "Z1_pt"

backgrounds = [
    ("tWZ", "tWZ", color.TWZ),
    ("ttZ", "ttZ", color.TTZ),
    ("ttX", "ttX", color.TTX_rare),
    ("tZq", "tZq", color.TZQ),
    ("WZ",  "WZ",  color.WZ),
    ("triBoson", "Triboson", color.triBoson),
    ("ZZ", "ZZ", color.ZZ),
    ("nonprompt", "Nonprompt", color.nonprompt),
]

for region in files.keys():
    print "Plotting region", region
    p = Plotter(region)
    p.plot_dir = plot_directory+"/SMplots/"
    p.lumi = "138"
    p.xtitle = "Z p_{T}"
    for (bkg, legname, color) in backgrounds:
        hist = getObjFromFile(files[region], histname+"__"+bkg)
        hist = adjustHistogram(hist)
        p.addBackground(hist, legname, color)
    p.draw()
