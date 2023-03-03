#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile

ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

files = {
    "muon": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/LeptonPtScan_v1_reduce/UL2018/muon/singlelepFO-vetoAddLepFO-vetoMET/Results.root",
    "elec": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/LeptonPtScan_v1_reduce/UL2018/elec/singlelepFO-vetoAddLepFO-vetoMET/Results.root",
}

histname = "L_cone_pt__BIN_mvaBINNR__TTbar"

boundaries_mva = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
Nbins = len(boundaries_mva)



for channel in ["muon", "elec"]:
    h_scan = ROOT.TH1F("scan_"+channel, "scan", Nbins-1, boundaries_mva[0], boundaries_mva[-1])
    for i in range(Nbins):
        bin = i+1
        if bin >= Nbins:
            continue
        hist = getObjFromFile(files[channel], histname.replace("BINNR", str(bin)) )
        average = hist.GetMean() 
        h_scan.SetBinContent(bin, average)
    c = ROOT.TCanvas("c", "c", 600, 600)
    h_scan.SetTitle(" ")
    h_scan.GetXaxis().SetTitle("MVA score")
    h_scan.GetYaxis().SetTitle("average p_{t}^{Cone} [GeV]")
    h_scan.GetXaxis().SetNdivisions(505)
    h_scan.GetYaxis().SetNdivisions(505)
    h_scan.Draw("HIST")
    c.Print(plot_directory+"/FakeRate/PtConeVsMVA_"+channel+".pdf")            
