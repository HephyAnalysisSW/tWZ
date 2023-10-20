#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter


ROOT.gROOT.SetBatch(ROOT.kTRUE)

version = "v11"
dataTag = "_noData"
year = "ULRunII"

paths = {
    "ZZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+year+"/all/qualepT-minDLmass12-onZ1-onZ2/",
    "WZ":     "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+year+"/all/trilepT-minDLmass12-onZ1-btag0-met60/",
    "ttZ":    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_"+version+"_reduceEFT_threePoint"+dataTag+"/"+year+"/all/trilepT-minDLmass12-onZ1-njet3p-btag1p/",
}

sys = {
    "muR":                        ("_Scale_UPNONE", "_Scale_DOWNNONE"),
    "muF":                        ("_Scale_NONEUP", "_Scale_NONEDOWN"),
}

histnames = {
    "Z1_pt": ("Z p_{T} [GeV]", 2, 400),
    # "l1_pt": ("Leading lepton p_{T} [GeV]", 2, 300),
    # "l2_pt": ("Sub-leading lepton p_{T} [GeV]", 2, 200),
    # "l3_pt": ("Trailing lepton p_{T} [GeV]", 2, 150),
    # "N_jets": ("Number of jets", 1, 10.5),
    # "yield": ("", 1, 4.0),
}

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


                (upname, downname) = sysnames[sys]
                sysdirUP = sysdirUP.replace('/Run', upname+'/Run').replace('/UL', upname+'/UL')
                sysdirDOWN = dirs[region]
                sysdirDOWN = sysdirDOWN.replace('/Run', downname+'/Run').replace('/UL', downname+'/UL')

for histname in histnames:
    for region in ["ttZ", "WZ", "ZZ"]:
        print "Plotting region", region, "and histogram", histname
        p = Plotter(region+"__"+histname)
        (xtitle, rebin, xmax) = histnames[histname]
        p.plot_dir = plot_directory+"/EFTtoSM/"
        p.lumi = "138"
        p.xtitle = xtitle
        p.rebin = rebin
        p.setCustomXRange(0,xmax)
        p.NcolumnsLegend = 2
        h_nominal = getObjFromFile(files[region], histname+"__"+region)
            p.addBackground(hist, legname, color)

        p.draw()
