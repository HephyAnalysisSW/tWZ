#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
import array

ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

files = {
    "muon": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/LeptonPtScan_v2/ULRunII/muon/singlelepFO-vetoAddLepFO-vetoMET/Results.root",
    "elec": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/LeptonPtScan_v2/ULRunII/elec/singlelepFO-vetoAddLepFO-vetoMET/Results.root",
    "muon_conept": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/LeptonPtScan_v2/ULRunII/muon/singlelepFOconept-vetoAddLepFOconept-vetoMET/Results.root",
    "elec_conept": "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/LeptonPtScan_v2/ULRunII/elec/singlelepFOconept-vetoAddLepFOconept-vetoMET/Results.root",
}


boundaries_mva_fine = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
Nbins_fine = len(boundaries_mva_fine)
histname_fine = "L_cone_pt__BIN_mvaBINNR__QCD_MuEnriched"

boundaries_mva_WP = [0.0, 0.20, 0.41, 0.64, 0.81, 1.0]
Nbins_WP = len(boundaries_mva_WP)
histname_WR = "L_cone_pt__BIN_WP_mvaBINNR__QCD_MuEnriched"



for channel in ["muon", "elec", "muon_conept", "elec_conept"]:
    print channel 
    for mode in ["fine", "WP"]:
        if mode == "WP":
            boundaries_mva = boundaries_mva_WP
            Nbins = Nbins_WP
            histname = histname_WR
        else:
            boundaries_mva = boundaries_mva_fine
            Nbins = Nbins_fine            
            histname = histname_fine            
        h_scan = ROOT.TH1F("scan_"+channel, "scan", Nbins-1, array.array("f", boundaries_mva) )
        for i in range(Nbins):
            bin = i+1
            if bin >= Nbins:
                continue
            newhistname = histname.replace("BINNR", str(bin)) 
            if "elec" in channel:
                newhistname=newhistname.replace("MuEnriched", "EMEnriched")
            print newhistname
            hist = getObjFromFile(files[channel], newhistname)
            average = hist.GetMean() 
            h_scan.SetBinContent(bin, average)
        c = ROOT.TCanvas("c", "c", 600, 600)
        h_scan.SetTitle(" ")
        h_scan.GetXaxis().SetTitle("MVA score")
        h_scan.GetYaxis().SetTitle("average p_{t}^{Cone} [GeV]")
        h_scan.GetXaxis().SetNdivisions(505)
        h_scan.GetYaxis().SetNdivisions(505)
        h_scan.Draw("HIST")
        c.Print(plot_directory+"/FakeRate/PtConeVsMVA_"+channel+"_"+mode+".pdf")            
