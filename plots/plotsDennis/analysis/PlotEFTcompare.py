#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

files = {
    "ttZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/CompareEFTsamples_v4_noData/YEAR/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root",
    "WZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/CompareEFTsamples_v4_noData/YEAR/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root",
    "ZZ": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/CompareEFTsamples_v4_noData/YEAR/all/qualepT-minDLmass12-onZ1-onZ2/Results.root",
}

colors = {
    "ttZ": color.TTZ,
    "WZ": color.WZ,
    "ZZ": color.ZZ,
}

lumi = {
    "UL2016preVFP": "19.5",
    "UL2016":       "16.5",
    "UL2017":       "41.5",
    "UL2018":       "60",
}


eftpoints = [
    ("c_{#phi q}^{(1)(11)}=+2",   "__cHq1Re11=2.0000", ROOT.kRed, 1),
    ("c_{#phi q}^{(1)(11)}=-2",   "__cHq1Re11=-2.0000", ROOT.kRed, 2),
    ("c_{#phi q}^{(1)(22)}=+2",   "__cHq1Re22=2.0000", ROOT.kGreen, 1),
    ("c_{#phi q}^{(1)(22)}=-2",   "__cHq1Re22=-2.0000", ROOT.kGreen, 2),
    ("c_{#phi q}^{(1)(33)}=+2",   "__cHq1Re33=2.0000", ROOT.kBlue, 1),
    ("c_{#phi q}^{(1)(33)}=-2",   "__cHq1Re33=-2.0000", ROOT.kBlue, 2),
    ("c_{#phi q}^{(3)(11)}=+0.2", "__cHq3Re11=0.2000", ROOT.kMagenta, 1),
    ("c_{#phi q}^{(3)(11)}=-0.2", "__cHq3Re11=-0.2000", ROOT.kMagenta, 2),
    ("c_{#phi q}^{(3)(22)}=+2",   "__cHq3Re22=2.0000", ROOT.kAzure+7, 1),
    ("c_{#phi q}^{(3)(22)}=-2",   "__cHq3Re22=-2.0000", ROOT.kAzure+7, 2),
    ("c_{#phi q}^{(3)(33)}=+2",   "__cHq3Re33=2.0000", 798, 1),
    ("c_{#phi q}^{(3)(33)}=-2",   "__cHq3Re33=-2.0000", 798, 2),
]


histname = "Z1_pt"
xtitle = "Z p_{T} [GeV]"

for year in ["UL2016preVFP", "UL2016", "UL2018"]:
    for region in ["ttZ", "WZ", "ZZ"]:
        h_SM = getObjFromFile(files[region].replace("YEAR", year), histname+"__"+region)
        h_EFT = getObjFromFile(files[region].replace("YEAR", year), histname+"__"+region+"_EFT")
        SF = h_SM.Integral()/h_EFT.Integral()
        h_EFT.Scale(SF)
        print "Factor =", SF
        p = Plotter(year+"__"+region+"__"+histname)
        p.plot_dir = plot_directory+"/EFTcompare/"
        p.lumi = lumi[year]
        p.xtitle = xtitle
        p.drawRatio = True
        p.rebin = 2
        # p.setCustomXRange(0,xmax)
        p.addBackground(h_SM, region, colors[region])
        p.addSignal(h_EFT, region+" EFT sample", ROOT.kRed)
        p.draw()

for year in ["UL2016preVFP", "UL2016", "UL2018"]:
    for region in ["ttZ", "WZ", "ZZ"]:
        h_EFT = getObjFromFile(files[region].replace("YEAR", year), histname+"__"+region+"_EFT")
        p = Plotter(year+"__EFT__"+region+"__"+histname)
        p.plot_dir = plot_directory+"/EFTcompare/"
        p.lumi = lumi[year]
        p.xtitle = xtitle
        p.drawRatio = True
        p.rebin = 4
        p.setCustomXRange(0,600)
        p.addBackground(h_EFT, region+" SM", 15)
        for (legname, suffix, color, linestyle) in eftpoints:
            hist = getObjFromFile(files[region].replace("YEAR", year), histname+"__"+region+"_EFT"+suffix)
            p.addSignal(hist, legname, color, linestyle)
        p.draw()
