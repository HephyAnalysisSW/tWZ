#!/usr/bin/env python

import ROOT
import Analysis.Tools.syncer
import os
import array

from math                                        import sqrt
from tWZ.Tools.helpers                           import getObjFromFile, writeObjToFile, writeObjToDirInFile
from tWZ.Tools.user                              import plot_directory
from tWZ.samples.color                           import color
from tWZ.Tools.histogramHelper                   import WClatexNames
from MyRootTools.plotter.Plotter                 import Plotter
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import tWZ.Tools.logger as logger


f_nom = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_ttdilep_v1_noData/UL2018/all/trilepFOnoT-minDLmass12-btag1p/Results.root"
f_up = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_ttdilep_v1_noData_ISR_UP/UL2018/all/trilepFOnoT-minDLmass12-btag1p/Results.root"
f_down = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_ttdilep_v1_noData_ISR_DOWN/UL2018/all/trilepFOnoT-minDLmass12-btag1p/Results.root"


plotdir = plot_directory+"/ttdilep_ISR/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

histname = "l1_pt"

h_nom = getObjFromFile(f_nom, histname+"__TTLep")
h_up = getObjFromFile(f_up, histname+"__TTLep")
h_down = getObjFromFile(f_down, histname+"__TTLep")

p = Plotter("TTLep_UL2018")
p.plot_dir = plotdir
p.lumi = "60"
p.xtitle = "Leading lepton #it{p}_{T} [GeV]"
p.drawRatio = True
p.subtext = "Preliminary"
p.ratiorange = 0.8, 1.2
p.NcolumnsLegend = 1
p.addBackground(h_nom, "t#bar{t} dilep", 13)
p.addSignal(h_up, "t#bar{t} dilep (ISR up)", ROOT.kAzure+7)
p.addSignal(h_down, "t#bar{t} dilep (ISR down)", ROOT.kRed-2)
p.draw()
