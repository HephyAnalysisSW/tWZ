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
    hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    return hist

ROOT.gROOT.SetBatch(ROOT.kTRUE)
plotdir = plot_directory+"/PaperPlots/"


path_ZZ     = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/qualepT-minDLmass12-onZ1-onZ2/Results.root"
path_WZ     = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
path_ttZ    = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
path_WZ_CR  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint/ULRunII/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/Results.root"
path_ttZ_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v11_reduceEFT_threePoint/ULRunII/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/Results.root"

processinfo = {
    "ttZ":       ("t#bar{t}Z", color.TTZ),
    "WZ":        ("WZ",  color.WZ),
    "ZZ":        ("ZZ", color.ZZ),
    "tWZ":       ("tWZ", color.TWZ),
    "ttX":       ("t#bar{t}X", color.TTX_rare),
    "tZq":       ("tZq", color.TZQ),
    "triBoson":  ("Triboson", color.triBoson),
    "nonprompt": ("Nonprompt", color.nonprompt),
}
histname = "Z1_pt"

signals = ["ttZ", "WZ", "ZZ"]
backgrounds = ["tWZ", "ttX", "tZq", "triBoson", "nonprompt"]

regions = {
    ("ttZ", path_ttZ, "SR_{t#bar{t}Z}"),
    ("WZ", path_WZ, "SR_{WZ}"),
    ("ZZ", path_ZZ, "SR_{ZZ}"),
    ("ttZ_CR", path_ttZ_CR, "CR_{t#bar{t}Z}"),
    ("WZ_CR", path_WZ_CR, "CR_{WZ}"),
}



for (regionname, path, regiontext) in regions:
    p = Plotter("ULRunII__"+regionname+"__"+histname)
    p.plot_dir = plotdir
    p.lumi = "138"
    p.xtitle = "Z #it{p}_{T} [GeV]"
    p.subtext = "Preliminary"
    p.legshift = (-0.1, -0.1, 0.0, 0.0)
    p.addText(0.22, 0.75, regiontext, font=43, size=16)
    for process in signals+backgrounds:
        altbinning = True if regionname in ["ZZ", "ttZ_CR", "WZ_CR"] else False
        hist = getHist(path, histname+"__"+process, altbinning)
        p.addBackground(hist, processinfo[process][0], processinfo[process][1])
    p.draw()
