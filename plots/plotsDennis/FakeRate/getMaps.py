#!/usr/bin/env python
import os
import ROOT
import array as arr
from math                                import sqrt
from tWZ.Tools.user                      import plot_directory
import Analysis.Tools.syncer

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--mergeBins',      action='store_true', default=False)
args = argParser.parse_args()

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

def mergeBins(map, channel):
    boundaries_pt = [0, 20, 30, 45, 65, 120]
    boundaries_pt_new = [0, 20, 30, 45, 120]
    boundaries_eta = [0, 1.2, 2.1, 2.4]
    if channel == "elec":
        boundaries_eta = [0, 0.8, 1.44, 2.4]
    newmap = createMap(boundaries_pt_new, boundaries_eta)
    for i in range(len(boundaries_pt_new)-1):
        for j in range(len(boundaries_eta)-1):
            ptbin = i+1
            etabin = j+1
            if ptbin == len(boundaries_pt_new)-1:
                content = map.GetBinContent(ptbin, etabin)+map.GetBinContent(ptbin+1, etabin)
            else:
                content = map.GetBinContent(ptbin, etabin)
            newmap.SetBinContent(ptbin, etabin, content)
    return newmap

def createMap(boundaries_pt, boundaries_eta):
    array_pt = arr.array('d',boundaries_pt)
    array_eta = arr.array('d',boundaries_eta)
    map = ROOT.TH2F("hist", "hist", len(array_pt)-1, array_pt, len(array_eta)-1, array_eta)
    return map

def getRatio(h1, h2):
    NbinsX = h1.GetXaxis().GetNbins()
    NbinsY = h1.GetYaxis().GetNbins()
    h_ratio = h1.Clone()
    h_error = h1.Clone()
    h_ratio.Reset()
    h_error.Reset()
    for i in range(NbinsX):
        for j in range(NbinsY):
            binx = i+1
            biny = j+1
            N1 = h1.GetBinContent(binx, biny)
            N2 = h2.GetBinContent(binx, biny)
            e1 = h1.GetBinError(binx, biny)
            e2 = h2.GetBinError(binx, biny)            
            if N1 == 0 or N2 == 0:
                ratio = 0
                error = 0
            else:
                ratio = N1/N2
                error = sqrt( pow((e1/N2),2) + pow((-N1*e2/(N2*N2)),2) )
            h_ratio.SetBinContent(binx, biny, ratio)
            h_error.SetBinContent(binx, biny, error)
    return h_ratio, h_error


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
    "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v5/",
    # "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v4_noLooseSel/",
    # "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/FakeRate/FakeRate_v4_noLooseWP/",
]

    
years = ["UL2018"]
channels = ["elec", "muon"]
selection = "singlelepFO-vetoAddLepFO-vetoMET"
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
    for path in paths:
        sel = selection
        suffix = ""
        if args.mergeBins:
            suffix += "__mergedBins"
        if "_noLooseSel" in path:
            suffix += "__noLooseSel"
        if "_noLooseWP" in path:
            suffix += "__noLooseWP"
            sel = selection_noLooseWP
        for channel in channels:
            outputfile = ROOT.TFile("LeptonFakerate__MC__"+year+"__"+channel+suffix+".root", "RECREATE")
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
            
            if args.mergeBins:
                backgroundsL = mergeBins(backgroundsL, channel)
                backgroundsT = mergeBins(backgroundsT, channel)
                dataL = mergeBins(dataL, channel)
                dataT = mergeBins(dataT, channel)
                QCDL = mergeBins(QCDL, channel)
                QCDT = mergeBins(QCDT, channel)
            
            mapData, errorData = getRatio(dataT, dataL)
            mapMC, errorMC = getRatio(QCDT, QCDL)
            
            outputfile.cd()
            mapMC.Write("Fakerate_MC")
            errorMC.Write("Fakerate_MC_stat")
            mapData.Write("Fakerate_DATA")
            errorData.Write("Fakerate_DATA_stat")
            
            drawMap(QCDL, year+"__"+channel+"__QCD_loose"+suffix)
            drawMap(QCDT, year+"__"+channel+"__QCD_tight"+suffix)
            drawMap(backgroundsL, year+"__"+channel+"__Backgrounds_loose"+suffix)
            drawMap(backgroundsT, year+"__"+channel+"__Backgrounds_tight"+suffix)        
            drawMap(dataL, year+"__"+channel+"__Data_loose"+suffix)
            drawMap(mapData, year+"__"+channel+"__Map_Data"+suffix)
            drawMap(mapMC, year+"__"+channel+"__Map_MC"+suffix)
            drawMap(errorData, year+"__"+channel+"__Map_Data_statUnc"+suffix)
            drawMap(errorMC, year+"__"+channel+"__Map_MC_statUnc"+suffix)
            outputfile.Close()
