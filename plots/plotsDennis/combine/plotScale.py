#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.CMScolors import CMScolors

from tWZ.samples.color                           import color
from tWZ.Tools.histogramHelper                   import WClatexNames
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger

logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--noData',           action='store_true', default=False)
argParser.add_argument('--addSignal',           action='store_true', default=False)
args = argParser.parse_args()



combineInput = "/groups/hephy/cms/dennis.schwarz/www/tWZ/CombineInput_UL_threePoint_light_minus_binning-B/ULRunII/CombineInput.root"

plotdir = plot_directory+"/ScalePlots/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

regions = ["WZ", "ZZ", "ttZ"]
histname = "Z1_pt"
signals = ["sm"]
backgrounds = ["tWZ", "ttX", "tZq", "triBoson", "ggToZZ", "nonprompt"]


processinfo = {
    "sm":        ("t#bar{t}Z + WZ + ZZ", CMScolors["sm"]),
    "ttZ"  :    ("t#bar{t}Z", CMScolors["ttZ"]),
    "WZ":        ("WZ",  CMScolors["WZ"]),
    "ZZ":        ("ZZ", CMScolors["ZZ"]),
    "tWZ":       ("tWZ", CMScolors["tWZ"]),
    "ttX":       ("t#bar{t}X", CMScolors["ttX"]),
    "tZq":       ("tZq", CMScolors["tZq"]),
    "triBoson":  ("Triboson", CMScolors["triboson"]),
    "nonprompt": ("Nonprompt", CMScolors["nonprompt"]),
    "ggToZZ":    ("gg #rightarrow ZZ", CMScolors["ggZZ"]),
}

scales_muF = ["muF_ttZ", "muF_WZ", "muF_ZZ"]
scales_muR = ["muR_ttZ", "muR_WZ", "muR_ZZ"]

scaleinfo = {
    "muR_ttZ": ROOT.kRed,
    "muR_WZ": ROOT.kAzure+7,
    "muR_ZZ": ROOT.kGreen,
    "muF_ttZ": ROOT.kRed,
    "muF_WZ": ROOT.kAzure+7,
    "muF_ZZ": ROOT.kGreen,
}

for region in regions:
    p = Plotter("Scales_muF__"+region+"__"+histname)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z #it{p}_{T} [GeV]"
    p.drawRatio = True
    p.ratiotitle = "#splitline{Ratio}{to SM}"
    p.subtext = "Preliminary"
    p.legshift = (-0.1, -0.1, 0.0, 0.0)

    h_sm = getObjFromFile(combineInput, region+"__"+histname+"/sm")
    p.addBackground(h_sm, processinfo["sm"][0], processinfo["sm"][1])
    for scale in scales_muF:
        h_up = getObjFromFile(combineInput, region+"__"+histname+"/sm__"+scale+"Up")
        h_down = getObjFromFile(combineInput, region+"__"+histname+"/sm__"+scale+"Down")
        p.addSignal(h_up, scale+" up", scaleinfo[scale], 1)
        p.addSignal(h_down, scale+" down", scaleinfo[scale], 2)
    p.draw()

    p2 = Plotter("Scales_muR__"+region+"__"+histname)
    p2.plot_dir = plotdir
    p2.lumi = "138"
    p2.xtitle = "Z #it{p}_{T} [GeV]"
    p2.drawRatio = True
    p2.ratiotitle = "#splitline{Ratio}{to SM}"
    p2.subtext = "Preliminary"
    p2.legshift = (-0.1, -0.1, 0.0, 0.0)

    p2.addBackground(h_sm, processinfo["sm"][0], processinfo["sm"][1])
    for scale in scales_muR:
        h_up = getObjFromFile(combineInput, region+"__"+histname+"/sm__"+scale+"Up")
        h_down = getObjFromFile(combineInput, region+"__"+histname+"/sm__"+scale+"Down")
        p2.addSignal(h_up, scale+" up", scaleinfo[scale], 1)
        p2.addSignal(h_down, scale+" down", scaleinfo[scale], 2)
    p2.draw()
