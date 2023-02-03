#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter


def adjustHistogram(hist):
    hist.Rebin(2)
    hist.GetXaxis().SetRangeUser(0, 400)
    return hist

def makeEnvelope(variations, nominal):
    Nbins = variations[0].GetSize()-2
    h_up = nominal.Clone()
    h_down = nominal.Clone()
    for i in range(Nbins):
        bin = i+1
        up = 0.0
        down = 0.
        for var in variations:
            central = nominal.GetBinContent(bin)
            diff = var.GetBinContent(bin)-central
            if diff < 0.0 and diff < down:
                down = diff 
            if diff > 0.0 and diff > up:
                up = diff 
        h_up.SetBinContent(bin, central+up)
        h_down.SetBinContent(bin, central+down)
    return h_up, h_down

ROOT.gROOT.SetBatch(ROOT.kTRUE)


path  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v5/ULRunII/all/trilepFOnoT-minDLmass12/Results.root"

histname = "Z1_pt"

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

uncertainties = [
    "Trigger",
    "LepIDstat",
    "LepIDsys",
    "BTag_b",
    "BTag_l",
    "PU",
    "JER",
    "JES",
    "Scale",
]

normsys = {
    "ttX": 0.2,
    "Triboson": 0.2,
    "Nonprompt": 0.3,
    "ttZ": 0.11,
    "tWZ": 0.2,
    "tZq": 0.033,
    "ZZ": 0.1,
    "WZ": 0.1,
}


p = Plotter("SM_CR_SYS")
p.plot_dir = plot_directory+"/SMplots/"
p.lumi = "138"
p.xtitle = "Z p_{T} [GeV]"
p.drawRatio = True
p.ratiorange = (0.2, 1.8)
for (bkg, legname, color) in backgrounds:
    h_bkg = getObjFromFile(path, histname+"__"+bkg)
    h_bkg = adjustHistogram(h_bkg)
    p.addBackground(h_bkg, legname, color)
    for unc in uncertainties:
        if unc == "Scale":
            variations = []
            for var in ["UPUP", "UPNONE", "NONEUP", "DOWNDOWN", "DOWNNONE", "NONEDOWN"]:
                hist = getObjFromFile(path.replace("EFT_UL_v5", "EFT_UL_v5_noData_"+unc+"_"+var), histname+"__"+bkg)
                hist = adjustHistogram(hist)
                variations.append(hist)
            h_up, h_down = makeEnvelope(variations, h_bkg)
        else:
            h_up = getObjFromFile(path.replace("EFT_UL_v5", "EFT_UL_v5_noData_"+unc+"_UP"), histname+"__"+bkg)
            h_down = getObjFromFile(path.replace("EFT_UL_v5", "EFT_UL_v5_noData_"+unc+"_DOWN"), histname+"__"+bkg)
            h_up = adjustHistogram(h_up)
            h_down = adjustHistogram(h_down)
        p.addSystematic(h_up, h_down, unc, legname)
    p.addNormSystematic(legname, normsys[legname])
h_data = getObjFromFile(path, histname+"__data")
h_data = adjustHistogram(h_data)
p.addData(h_data)
p.draw()
