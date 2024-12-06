#!/usr/bin/env python
import ROOT
import os

import Analysis.Tools.syncer

from tWZ.Tools.triggerPrescale           import triggerPrescale
from tWZ.Tools.user                      import plot_directory
from MyRootTools.plotter.Plotter                 import Plotter

myprescales = {
    "UL2016preVFP": {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": 6632.6476944,
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 538.212887485,
        "HLT_Mu3_PFJet40": 6937.58625859,
        "HLT_Mu8": 4843.07206505,
        "HLT_Mu17": 74.0726475198,
        "HLT_Mu20": 159.917763426,
        "HLT_Mu27": 106.148938056,
    },
    "UL2016preVFP_noQCD": {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": 5642.46509969,
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 459.625498587,
        "HLT_Mu3_PFJet40": 6622.18340608,
        "HLT_Mu8": 4453.6591838,
        "HLT_Mu17": 72.0769703391,
        "HLT_Mu20": 156.955196484,
        "HLT_Mu27": 104.908948948,
    },
    "UL2016": {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": 8268.13525238,
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 2386.62098648,
        "HLT_Mu3_PFJet40": 8131.24543428,
        "HLT_Mu8": 24500.2167451,
        "HLT_Mu17": 597.120237457,
        "HLT_Mu20": 436.962795931,
        "HLT_Mu27": 139.872933174,
    },
    "UL2016_noQCD": {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": 6998.20314114,
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 2071.54228175,
        "HLT_Mu3_PFJet40": 7616.00464579,
        "HLT_Mu8": 21927.955456,
        "HLT_Mu17": 579.004932296,
        "HLT_Mu20": 426.256146412,
        "HLT_Mu27": 137.687756577,
    },
    "UL2017": {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": 11033.8612028,
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1163.73712005,
        "HLT_Mu3_PFJet40": 5442.70893137,
        "HLT_Mu8": 19611.8808228,
        "HLT_Mu17": 726.400200236,
        "HLT_Mu20": 68.4845636331,
        "HLT_Mu27": 210.244815418,
    },
    "UL2017_noQCD": {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": 8682.16405079,
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 943.116652767,
        "HLT_Mu3_PFJet40": 4910.27189405,
        "HLT_Mu8": 16259.9861854,
        "HLT_Mu17": 677.513432996,
        "HLT_Mu20": 65.0295663573,
        "HLT_Mu27": 203.909071782,
    },
    "UL2018": {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30": 6701.38176779,
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30": 1327.49862965,
        "HLT_Mu3_PFJet40": 8120.35771297,
        "HLT_Mu8": 9030.25055133,
        "HLT_Mu17": 1495.54956042,
        "HLT_Mu20": 906.638674162,
        "HLT_Mu27": 392.89380288,
    },
    "UL2018_noQCD": {
        "HLT_Ele8_CaloIdM_TrackIdM_PFJet30":5291.82990667,
        "HLT_Ele17_CaloIdM_TrackIdM_PFJet30":1094.4003856,
        "HLT_Mu3_PFJet40":7440.65654949,
        "HLT_Mu8":7575.38316412,
        "HLT_Mu17":1416.16468779,
        "HLT_Mu20":868.724968217,
        "HLT_Mu27":381.826796711,
    },
}


for year in ["UL2016preVFP", "UL2016", "UL2017", "UL2018"]:
    prescales_mine = triggerPrescale(year, "mine")
    prescales_bril = triggerPrescale(year, "bril")
    prescales_ghent = triggerPrescale(year, "ghent")


    triggers_muon = ["HLT_Mu3_PFJet40","HLT_Mu8","HLT_Mu17","HLT_Mu20","HLT_Mu27"]
    triggers_elec = ["HLT_Ele8_CaloIdM_TrackIdM_PFJet30","HLT_Ele17_CaloIdM_TrackIdM_PFJet30"]

    Ntriggers = len(triggers_muon)+len(triggers_elec)

    h_mine_old = ROOT.TH1F("mine_old", "", Ntriggers, -0.5, Ntriggers-0.5)
    h_bril = ROOT.TH1F("bril", "", Ntriggers, -0.5, Ntriggers-0.5)
    h_ghent = ROOT.TH1F("ghent", "", Ntriggers, -0.5, Ntriggers-0.5)
    h_mine = ROOT.TH1F("mine", "", Ntriggers, -0.5, Ntriggers-0.5)
    h_mine_noQCD = ROOT.TH1F("mine_noQCD", "", Ntriggers, -0.5, Ntriggers-0.5)

    for i, trigger in enumerate(triggers_elec+triggers_muon):
        f_mine_old = prescales_mine.prescales[trigger]
        f_bril = prescales_bril.prescales[trigger]
        f_ghent = prescales_ghent.prescales[trigger]
        f_mine = myprescales[year][trigger]
        f_mine_noQCD = myprescales[year+"_noQCD"][trigger]

        h_mine_old.SetBinContent(i+1, f_mine_old)
        h_bril.SetBinContent(i+1, f_bril)
        h_ghent.SetBinContent(i+1, f_ghent)
        h_mine.SetBinContent(i+1, f_mine)
        h_mine_noQCD.SetBinContent(i+1, f_mine_noQCD)

        h_mine_old.GetXaxis().SetBinLabel(i+1, trigger)
        h_bril.GetXaxis().SetBinLabel(i+1, trigger)
        h_ghent.GetXaxis().SetBinLabel(i+1, trigger)
        h_mine.GetXaxis().SetBinLabel(i+1, trigger)
        h_mine_noQCD.GetXaxis().SetBinLabel(i+1, trigger)


    p = Plotter(year)
    p.plot_dir = plot_directory+"/PrescaleComparison/"
    p.lumi = None
    p.xtitle = ""
    p.ytitle = "Prescale"
    p.log = True
    p.increaseMargin("bottom", 2)
    p.increaseMargin("right", 2)
    p.addBackground(h_bril, "BRIL", 15)
    p.addSignal(h_mine, "Fit", ROOT.kRed)
    p.addSignal(h_mine_noQCD, "Fit no QCD", ROOT.kGreen)
    # p.addSignal(h_mine_old, "Fit old", ROOT.kAzure+7)
    # p.addSignal(h_ghent, "Ghent", ROOT.kBlue)
    p.draw()
