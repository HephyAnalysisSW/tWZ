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


def getHist(fname, hname, Nrebin):
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
    hist = hist.Rebin(Nrebin)
    return hist

ROOT.gROOT.SetBatch(ROOT.kTRUE)
plotdir = plot_directory+"/HEM_fakes/"


path_WZ_CR  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_threePoint/UL2018/all/trilepFOnoT-minDLmass12-onZ1-btag0-met60/Results.root"
path_ttZ_CR = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v15_threePoint/UL2018/all/trilepFOnoT-minDLmass12-onZ1-njet3p-btag1p/Results.root"

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

histnames = ["l1_eta", "l1_phi"]

xtitles = {
    "Z1_pt": "Z boson candidate #it{p}_{T} [GeV]",
    "yield": "",
    "N_jets": "Number of jets",
    "l1_pt": "Leading lepton #it{p}_{T} [GeV]",
    "l2_pt": "Sub-leading lepton #it{p}_{T} [GeV]",
    "l3_pt": "Trailing lepton #it{p}_{T} [GeV]",
    "l1_eta": "Leading lepton #eta",
    "l1_phi": "Leading lepton #phi",
}

# signals = ["ttZ", "WZ", "ZZ"]
signals = ["ttZ_sm", "WZTo3LNu", "ZZ_powheg"]
backgrounds = ["tWZ", "ttX", "tZq", "triBoson", "ggToZZ", "nonprompt"]
processes_CR = ["nonprompt", "ttZ_sm", "WZTo3LNu", "ZZ_powheg", "tWZ", "ttX", "tZq", "triBoson", "ggToZZ"]

regions = {
    ("ttZ_CR", path_ttZ_CR, "CR_{t#bar{t}Z}"),
    ("WZ_CR", path_WZ_CR, "CR_{WZ}"),
}

for channel in ["all", "eee", "mumumu", "mumue", "muee"]:
    for (regionname, path, regiontext) in regions:
        path = path.replace("/all/", "/"+channel+"/")
        Nrebin = 3 if regionname == "WZ_CR" else 5
        for histname in histnames:
            for log in [False, True]:
                suffix = ""
                if log:
                    suffix+="_log"
                p = Plotter("UL2018__"+channel+"__"+regionname+"__"+histname+suffix)
                p.plot_dir = plotdir
                p.lumi = "60"
                p.xtitle = xtitles[histname]
                p.ytitle = "Events"
                p.subtext = "Preliminary"
                p.legshift = (-0.1, 0.1, 0.0, 0.0)
                p.yfactor = 2.
                if log:
                    p.log = True
                    if regionname == "WZ_CR":
                        p.setCustomYRange(0.001, 400)
                    elif regionname == "ttZ_CR":
                        p.setCustomYRange(0.001, 40)
                p.addText(0.22, 0.75, regiontext, font=43, size=16)
                processes = signals+backgrounds
                if regionname in ["ttZ_CR", "WZ_CR"]:
                    processes = processes_CR
                for process in processes:
                    altbinning = True if regionname in ["ZZ", "ttZ_CR", "WZ_CR"] else False
                    hist = getHist(path, histname+"__"+process, Nrebin)
                    p.addBackground(hist, processinfo[process][0], processinfo[process][1])
                if "_CR" in regionname:
                    h_data = getHist(path, histname+"__data", Nrebin)
                    p.addData(h_data)
                else:
                    h_data = getHist(path.replace("noData", "onlyData"), histname+"__data", Nrebin)
                    p.addData(h_data)
                p.draw()
