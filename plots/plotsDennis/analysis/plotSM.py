#!/usr/bin/env python

import os
import ROOT
import array

import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter


def getHist(fname, hname, altbinning=False):
    bins  = [0, 60, 120, 180, 240, 300, 400, 1000]
    if altbinning:
        bins  = [0, 60, 120, 180, 1000]
    if "ULRunII" in fname:
        # Get histograms from each era
        hist_18 = getObjFromFile(fname.replace("/ULRunII/", "/UL2018/"), hname)
        hist_17 = getObjFromFile(fname.replace("/ULRunII/", "/UL2017/"), hname)
        hist_16 = getObjFromFile(fname.replace("/ULRunII/", "/UL2016/"), hname)
        hist_16preVFP = getObjFromFile(fname.replace("/ULRunII/", "/UL2016preVFP/"), hname)
        # add them
        hist = hist_18.Clone(hist_18.GetName()+"_RunIIcombination")
        hist.Add(hist_17)
        hist.Add(hist_16)
        hist.Add(hist_16preVFP)
    else:
        hist = getObjFromFile(fname, hname)
    # hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    return hist

ROOT.gROOT.SetBatch(ROOT.kTRUE)


path_ZZ     = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/qualepT-minDLmass12-onZ1-onZ2/Results.root"
path_WZ     = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
path_ttZ    = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
path_WZ_CR  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/Results.root"
path_ttZ_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
# path_WZ_offZ  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-offZ1-btag0-met60/Results.root"
# path_ttZ_offZ = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-offZ1-njet3p-btag1p/Results.root"
# path_WZ_CR_offZ  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepFOnoT-minDLmass12-offZ1-btag0-met60/Results.root"
# path_ttZ_CR_offZ = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepFOnoT-minDLmass12-offZ1-njet3p-btag1p/Results.root"

files = {
    "ZZ" : path_ZZ,
    "WZ" : path_WZ,
    "ttZ": path_ttZ,
    # "WZ_CR" : path_WZ_CR,
    # "ttZ_CR": path_ttZ_CR,
    # "WZ_offZ" : path_WZ_offZ,
    # "ttZ_offZ": path_ttZ_offZ,
    # "WZ_CR_offZ" : path_WZ_CR_offZ,
    # "ttZ_CR_offZ": path_ttZ_CR_offZ,
}

histnames = {
    "N_jets": ("Number of jets", 1, 10.5),
    "Z1_pt": ("Z p_{T} [GeV]", 2, 300),
    "l1_pt": ("Leading lepton p_{T} [GeV]", 2, 300),
    "l2_pt": ("Sub-leading lepton p_{T} [GeV]", 2, 200),
    "l3_pt": ("Trailing lepton p_{T} [GeV]", 2, 150),
    "yield": ("", 1, 4.0),
}





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

for histname in histnames:
    for region in files:
        print "Plotting region", region
        p = Plotter(region+"__"+histname)
        (xtitle, rebin, xmax) = histnames[histname]
        p.plot_dir = plot_directory+"/SMplots/"
        p.lumi = "138"
        p.xtitle = xtitle
        p.rebin = rebin
        p.setCustomXRange(0,xmax)
        p.NcolumnsLegend = 2
        p.legshift = (-0.1, 0.3, 0.15, 0.)
        for (bkg, legname, color) in backgrounds:
            altbinning = True if region == "ZZ" else False
            hist = getHist(files[region], histname+"__"+bkg, altbinning)
            p.addBackground(hist, legname, color)
        # if "offZ" in region:
        #     p.drawRatio = True
        #     p.ratiorange = (0.2, 1.8)
        #     h_data = getObjFromFile(files[region], histname+"__data")
        #     p.addData(h_data)
        p.draw()
