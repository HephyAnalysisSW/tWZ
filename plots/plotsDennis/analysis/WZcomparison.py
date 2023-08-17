#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from MyRootTools.plotter.Plotter                 import Plotter


ROOT.gROOT.SetBatch(ROOT.kTRUE)

path = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint"
year = "ULRunII"
channel = "all"

selections_WZ = {
    "SRonZ": "trilepT-minDLmass12-onZ1-btag0-met60",
    "CRonZ": "trilepFOnoT-minDLmass12-onZ1-btag0-met60",
    "SRoffZ": "trilepT-minDLmass12-offZ1-btag0-met60",
    "CRoffZ": "trilepFOnoT-minDLmass12-offZ1-btag0-met60",
}

for sel in selections_WZ.keys():
    filename = path+"/"+year+"/"+channel+"/"+selections_WZ[sel]+"/Results.root"
    if "SRonZ" in sel:
        filename = filename.replace("_threePoint","_threePoint_noData")
    h_WZ = getObjFromFile(filename,"Z1_pt__WZTo3LNu")
    h_WZ_NLO = getObjFromFile(filename,"Z1_pt__WZTo3LNu_powheg")
    h_WZ_EFT = getObjFromFile(filename,"Z1_pt__WZ__cHq1Re11=0.0000")
    p = Plotter(sel)
    p.plot_dir = plot_directory+"/WZcomparison/"
    p.lumi = "138"
    p.xtitle = "Z p_{T} [GeV]"
    p.rebin = 2
    p.drawRatio = True
    p.ratiorange = (0.2, 1.8)
    # p.setCustomXRange(0,xmax)
    p.addBackground(h_WZ, "WZ LO", 15)
    p.addSignal(h_WZ_NLO, "WZ NLO", ROOT.kAzure+7)
    p.addSignal(h_WZ_EFT, "WZ EFT", ROOT.kRed-2)
    p.draw()
