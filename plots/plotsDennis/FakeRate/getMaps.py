#!/usr/bin/env python
import os
import ROOT
from tWZ.Tools.user                      import plot_directory
import Analysis.Tools.syncer


import tWZ.Tools.logger as logger
logger    = logger.get_logger(   "INFO", logFile = None)

def getSumOfHistograms(file, histname, processList):
    if len(processList) == 0:
        print "You gave an empty list of process names, aborting..."
        return  
    hist = ROOT.TH2F()
    hist = file.Get(histname+"__"+processList[0])
    for i,process in enumerate(processList):
        if i==0: 
            continue
        else:
            tmp_hist = file.Get(histname+"__"+process)
            hist.Add(tmp_hist)
    return hist

def drawMap(map, plotname):
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c", "c", 600, 600)
    ROOT.gPad.SetRightMargin(0.19)
    ROOT.gPad.SetLeftMargin(0.19)
    ROOT.gPad.SetBottomMargin(0.12)
    map.SetTitle(" ")
    map.GetXaxis().SetTitle("Lepton p_{T}^{cone}")
    map.GetYaxis().SetTitle("Lepton |#eta|")
    map.Draw("COLZ")
    map.GetXaxis().SetRangeUser(0, 100)
    c.Print(plot_directory+"/FakeRate/"+plotname+".pdf")
    
ROOT.gROOT.SetBatch(ROOT.kTRUE)
paths = [
    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v4/",
    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v4_noLooseSel/",
    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v4_noLooseWP/",
]

    
years = ["UL2018"]
channels = ["elec", "muon"]
selection = "singlelepL-vetoAddLepL-vetoMET"
selection_noLooseWP = "singlelepVL-vetoAddLepVL-vetoMET"

QCDsamples = {
    "elec": ["QCD_EMEnriched", "QCD_bcToE"],
    "muon": ["QCD_MuEnriched"]
}

backgrounds = ["Wjets","WZ", "ZZ", "WW", "TTbar", "DY"]

histnameL = "lep_pt_eta_loose"
histnameT = "lep_pt_eta_tight"

logger.info("Script to create lepton fake rate maps")
for year in years:
    logger.info("Running year %s", year)
    outputfile = ROOT.TFile("LeptonFakerate_"+year+".root", "RECREATE")
    for path in paths:
        sel = selection
        suffix = ""
        if "_noLooseSel" in path:
            suffix = "__noLooseSel"
        if "_noLooseWP" in path:
            suffix = "__noLooseWP"
            sel = selection_noLooseWP
        for channel in channels:
            filepath =  os.path.join(path, year, channel, sel, "Results.root")
            logger.info("Reading histograms from %s", filepath)
            file = ROOT.TFile(filepath)
            backgroundsL =  getSumOfHistograms(file, histnameL, backgrounds)
            backgroundsT =  getSumOfHistograms(file, histnameT, backgrounds)
            dataL = getSumOfHistograms(file, histnameL, ["data"])
            dataT = getSumOfHistograms(file, histnameT, ["data"])
            dataL.Add(backgroundsL, -1.0)
            dataT.Add(backgroundsT, -1.0)
            QCDL =  getSumOfHistograms(file, histnameL, QCDsamples[channel])
            QCDT =  getSumOfHistograms(file, histnameT, QCDsamples[channel])
            
            mapData = dataT
            mapData.Divide(dataL)
            mapMC = QCDT.Clone()
            mapMC.Divide(QCDL)
            
            outputfile.cd()
            mapMC.Write("fakerate__MC__"+channel+suffix)
            mapData.Write("fakerate__DATA__"+channel+suffix)
            
            drawMap(QCDL, year+"__"+channel+"__QCD_loose"+suffix)
            drawMap(QCDT, year+"__"+channel+"__QCD_tight"+suffix)
            drawMap(backgroundsL, year+"__"+channel+"__Backgrounds_loose"+suffix)
            drawMap(backgroundsT, year+"__"+channel+"__Backgrounds_tight"+suffix)        
            drawMap(dataL, year+"__"+channel+"__Data_loose"+suffix)
            drawMap(mapData, year+"__"+channel+"__Map_Data"+suffix)
            drawMap(mapMC, year+"__"+channel+"__Map_MC"+suffix)
        
    outputfile.Close()