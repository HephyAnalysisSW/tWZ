#!/usr/bin/env python

import os
import ROOT
import array

import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter

from tWZ.Tools.CMScolors import CMScolors


def getHist(fname, hname, bins):
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
    if bins is not None:
        hist = hist.Rebin(len(bins)-1, hist.GetName()+"_rebin", array.array('d',bins))
    return hist

ROOT.gROOT.SetBatch(ROOT.kTRUE)
plotdir = plot_directory+"/PaperPlots/"


path_ZZ     = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/qualepT-minDLmass12-onZ1-onZ2/Results.root"
path_WZ     = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-btag0-met60/Results.root"
path_ttZ    = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_reduceEFT_threePoint_noData/ULRunII/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/Results.root"
path_WZ_CR  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_threePoint/ULRunII/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/Results.root"
path_ttZ_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_threePoint/ULRunII/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/Results.root"

processinfo = {
    "ttZ":       ("t#bar{t}Z", CMScolors["ttZ"]),
    "ttZ_sm":    ("t#bar{t}Z", CMScolors["ttZ"]),
    "WZTo3LNu":  ("WZ",  CMScolors["WZ"]),
    "WZ":        ("WZ",  CMScolors["WZ"]),
    "ZZ":        ("ZZ", CMScolors["ZZ"]),
    "ZZ_powheg": ("ZZ", CMScolors["ZZ"]),
    "tWZ":       ("tWZ", CMScolors["tWZ"]),
    "ttX":       ("t#bar{t}X", CMScolors["ttX"]),
    "tZq":       ("tZq", CMScolors["tZq"]),
    "triBoson":  ("Triboson", CMScolors["triboson"]),
    "nonprompt": ("Nonprompt", CMScolors["nonprompt"]),
    "ggToZZ":    ("gg #rightarrow ZZ", CMScolors["ggZZ"]),
}

histnames = ["Z1_pt", "yield", "N_jets", "l1_pt", "l2_pt", "l3_pt"]



xtitles = {
    "Z1_pt": "Z boson candidate #it{p}_{T} [GeV]",
    "yield": "",
    "N_jets": "Number of jets",
    "l1_pt": "Leading lepton #it{p}_{T} [GeV]",
    "l2_pt": "Sub-leading lepton #it{p}_{T} [GeV]",
    "l3_pt": "Trailing lepton #it{p}_{T} [GeV]",
}

# signals = ["ttZ", "WZ", "ZZ"]
signals = ["ttZ_sm", "WZTo3LNu", "ZZ_powheg"]
backgrounds = ["tWZ", "ttX", "tZq", "triBoson", "ggToZZ", "nonprompt"]
processes_CR = ["nonprompt", "ttZ_sm", "WZTo3LNu", "ZZ_powheg", "tWZ", "ttX", "tZq", "triBoson", "ggToZZ"]

regions = {
    ("ttZ", path_ttZ, "SR_{t#bar{t}Z}"),
    ("WZ", path_WZ, "SR_{WZ}"),
    ("ZZ", path_ZZ, "SR_{ZZ}"),
    ("ttZ_CR", path_ttZ_CR, "CR_{t#bar{t}Z}"),
    ("WZ_CR", path_WZ_CR, "CR_{WZ}"),
}

bins_ttZ  = [40, 80, 120, 160, 200, 260, 340, 1000]
bins_WZ  = [40, 60, 80, 100, 120, 140, 180, 220, 260, 300, 340, 380, 420, 500, 1000]
bins_ZZ  = [40, 60, 80, 120, 200, 1000]


for (regionname, path, regiontext) in regions:
    for histname in histnames:
        # print histname, path
        bins = None
        if histname == "Z1_pt":
            if regionname in ["ttZ", "ttZ_CR"]:
                bins = bins_ttZ
                if regionname == "ttZ_CR":
                    bins = [40, 80, 120, 160, 200, 260, 340] # adjust range for showing the CR
            elif regionname in ["WZ", "WZ_CR"]:
                bins = bins_WZ
                if regionname == "WZ_CR":
                    bins = [40, 60, 80, 100, 120, 140, 180, 220, 260, 300, 340] # adjust range for showing the CR
            else:
                bins = bins_ZZ
        for log in [False, True]:
            suffix = ""
            if log:
                suffix+="_log"
            p = Plotter("ULRunII__"+regionname+"__"+histname+suffix)
            p.plot_dir = plotdir
            p.lumi = "138"
            p.xtitle = xtitles[histname]
            p.ytitle = "Events / GeV"
            p.divideByWidth = True
            p.legshift = (-0.1, 0.1, 0.0, 0.0)
            p.yfactor = 1.4
            p.legtextsize = 0.04
            p.horizontalErrors = True
            p.logoAbovePlot = True
            p.subtext = ""
            # p.simtext = "Simulation"

            if histname == "yield" and not log:
                p.yfactor = 3.0
                p.legshift = (-0.1, 0.1, 0.0, 0.0)
            if log:
                p.log = True
                if regionname == "WZ_CR":
                    p.setCustomYRange(0.001, 400)
                elif regionname == "ttZ_CR":
                    p.setCustomYRange(0.001, 40)
            else:
                if regionname == "WZ_CR":
                    p.setCustomYRange(0.0, 45)
                elif regionname == "ttZ_CR":
                    p.setCustomYRange(0.0, 5.5)
            p.addText(0.25, 0.8, regiontext, font=63, size=24) #20
            processes = signals+backgrounds
            if regionname in ["ttZ_CR", "WZ_CR"]:
                processes = processes_CR
            for process in processes:
                hist = getHist(path, histname+"__"+process, bins)
                p.addBackground(hist, processinfo[process][0], processinfo[process][1])
            if "_CR" in regionname:
                h_data = getHist(path, histname+"__data", bins)
                p.addData(h_data)
            else:
                h_data = getHist(path.replace("noData", "onlyData"), histname+"__data", bins)
                p.addData(h_data)
            p.draw()
