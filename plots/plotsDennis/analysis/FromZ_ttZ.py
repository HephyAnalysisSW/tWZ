#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from MyRootTools.plotter.Plotter                 import Plotter

plotdir = plot_directory+"/FromZ/"
if not os.path.exists( plotdir ): os.makedirs( plotdir )

file = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_noData/UL2018/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/FromZ.root"

canvas = getObjFromFile(file, "8ade0052_28df_479c_8a74_4818030cdba3")

ttZ = canvas.GetPrimitive("FromZ_TTZ_ced4027b_5e9c_474f_8a1d_78cbe5ddd185")
ttZ_EFT = canvas.GetPrimitive("FromZ_TTZ_EFT_e1247fb0_bf0c_4393_8f6b_cab1593fcade")

noZ = ttZ.GetBinContent(1)
fromZ = ttZ.GetBinContent(3)
print("ttZ SM:", noZ/(ttZ.Integral()))


noZ = ttZ_EFT.GetBinContent(1)
fromZ = ttZ_EFT.GetBinContent(3)
print("ttZ EFT:", noZ/(ttZ_EFT.Integral()))
    # p = Plotter(sel)
    # p.plot_dir = plot_directory+"/WZcomparison/"
    # p.lumi = "138"
    # p.xtitle = "Z p_{T} [GeV]"
    # p.rebin = 2
    # p.drawRatio = True
    # p.ratiorange = (0.2, 1.8)
    # # p.setCustomXRange(0,xmax)
    # p.addBackground(h_WZ, "WZ LO", 15)
    # p.addSignal(h_WZ_NLO, "WZ NLO", ROOT.kAzure+7)
    # p.addSignal(h_WZ_EFT, "WZ EFT", ROOT.kRed-2)
    # p.draw()
