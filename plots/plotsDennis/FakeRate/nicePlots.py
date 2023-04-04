#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter
import Analysis.Tools.syncer
ROOT.gROOT.SetBatch(True)

year = "UL2018"
channel = "muon"
filename = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v10/"+year+"/"+channel+"/singlelepFO-vetoAddLepFO-vetoMET/Results.root"
print "Reading", filename

histnames = [
    "L_MTfix__BIN_pt1_eta1", "L_MTfix__BIN_pt2_eta1", "L_MTfix__BIN_pt3_eta1", 
    "T_MTfix__BIN_pt1_eta1", "T_MTfix__BIN_pt2_eta1", "T_MTfix__BIN_pt3_eta1"
    ]

processes = [
    ("QCD_MuEnriched", "QCD",  color.QCD),
    ("WZ", "WZ", color.WZ),
    ("ZZ", "ZZ", color.ZZ),
    ("WW", "WW", color.WW),
    ("TTbar", "t#bar{t}", color.TTJets),
    ("DY", "DY", color.DY),
    ("Wjets", "W+jets", color.WJets),
]

for histname in histnames:
    plotdir = plot_directory+"/FakeRate/NicePlots/"
    p = Plotter(plotdir+year+"__"+channel+"__"+histname)
    p.drawRatio = True
    p.ratiorange = (0.5, 1.5)
    p.xtitle = "m_{T}^{fix} [GeV]"
    h_data = getObjFromFile(filename, histname+"__data")
    # p.addData(h_data)
    for (process, legname, color) in processes:
        hist = getObjFromFile(filename, histname+"__"+process)
        p.addBackground(hist, legname, color)
    p.draw()
