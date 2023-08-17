#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

def largestDiff(h1, h2):
    Nbins = h1.GetSize()-2
    largestDiff = 0
    largestDiffBin = -1

    for i in range(Nbins):
        bin = i+1
        c1 = h1.GetBinContent(bin)
        c2 = h2.GetBinContent(bin)
        ratio = 1
        if c2 > 0:
            ratio = c1/c2
            if abs(1.0-ratio) > largestDiff and bin < 25:
                largestDiff = abs(1.0-ratio)
                largestDiffBin = bin
    return largestDiff, largestDiffBin


import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--offZ',           action='store_true', default=False)
args = argParser.parse_args()


file_nominal = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
file_reweight = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData_WZreweight/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
plotname = "ULRunII__WZ_njetReweight_comparison"

if args.offZ:
    file_nominal  = file_nominal.replace("onZ1", "offZ1").replace("_noData", "")
    file_reweight = file_reweight.replace("onZ1", "offZ1").replace("_noData", "")
    plotname += "_offZ"


h_nominal  = getObjFromFile(file_nominal,  "Z1_pt__WZ")
h_reweight = getObjFromFile(file_reweight, "Z1_pt__WZ")

outdir = plot_directory+"/NjetWZreweight/"
if not os.path.exists( outdir ): os.makedirs( outdir )

p = Plotter(plotname)
p.plot_dir = outdir
p.lumi = "138"
p.xtitle = "Z p_{T} [GeV]"
p.drawRatio = True
p.addBackground(h_nominal, "WZ", 15)
p.addSignal(h_reweight, "WZ reweighted", ROOT.kRed)
p.draw()

largestDiff, largestDiffBin = largestDiff(h_nominal, h_reweight)
print "Largest difference is %.3f percent in bin %i" %(100*largestDiff, largestDiffBin)
