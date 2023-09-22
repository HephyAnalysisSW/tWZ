#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter


ROOT.gROOT.SetBatch(ROOT.kTRUE)
paths = {
    "ttZ" : "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_FakeRateSF_useDataSF/ULRunII/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/Results.root",
    "WZ"  : "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_FakeRateSF_useDataSF/ULRunII/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/Results.root",
}

histname = "FakeCategory"

processes = [
    ("tWZ", "tWZ", color.TWZ),
    ("ttZ", "ttZ", color.TTZ),
    ("ttX", "ttX", color.TTX_rare),
    ("tZq", "tZq", color.TZQ),
    ("WZ",  "WZ",  color.WZ),
    ("triBoson", "Triboson", color.triBoson),
    ("ZZ", "ZZ", color.ZZ),
    ("nonprompt", "Nonprompt", color.nonprompt),
]

plotdir = plot_directory+"/FakeCategory/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )


for region in ["ttZ", "WZ"]:
    print "Plotting region", region
    p = Plotter(region+"__"+histname)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Fake Category"
    p.NcolumnsLegend = 2
    p.setCustomXRange(-0.5, 4.5)
    p.legshift = (0., 0.1, 0.0, 0.)
    for (process, legname, color) in processes:
        hist = getObjFromFile(paths[region], histname+"__"+process)
        p.addBackground(hist, legname, color)
    p.draw()
