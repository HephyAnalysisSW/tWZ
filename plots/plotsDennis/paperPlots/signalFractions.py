#!/usr/bin/env python

import ROOT
import array
import Analysis.Tools.syncer
import os

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--noData',           action='store_true', default=False)
argParser.add_argument('--year',             action='store', type=str, default="UL2018")
argParser.add_argument('--light',            action='store_true', default=False)
args = argParser.parse_args()

# histname
histname = "Z1_pt"

version = "v11"
logger.info( "Version = %s", version )

if args.noData:
    logger.info( "Use Asimov data (blind)" )
else:
    logger.info( "Use data (unblinded)" )

dataTag = "_noData" if args.noData else ""

dirs = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+args.year+"/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+args.year+"/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+args.year+"/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
}


signals = ["ttZ", "WZ", "ZZ"]
backgrounds = ["tWZ", "ttX", "tZq", "triBoson", "nonprompt"]

for region in ["ZZ", "WZ", "ttZ"]:
    print(region)
    Numbers = {}
    Nall = 0
    for process in signals+backgrounds:
        h = getObjFromFile(dirs[region]+"Results.root", histname+"__"+process)
        Numbers[process] = h.Integral()
        Nall += h.Integral()
    for process in signals+backgrounds:
        print(process,": %.2f"%(100.*Numbers[process]/Nall))
