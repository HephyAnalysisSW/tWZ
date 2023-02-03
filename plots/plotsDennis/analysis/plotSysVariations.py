#!/usr/bin/env python

import os
import ROOT
import Analysis.Tools.syncer
from tWZ.Tools.user                              import plot_directory
from tWZ.Tools.helpers                           import getObjFromFile
from tWZ.samples.color                           import color
from MyRootTools.plotter.Plotter                 import Plotter

ROOT.gROOT.SetBatch(ROOT.kTRUE)

################################################################################
# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--era',            action='store', type=str, default="ULRunII")
argParser.add_argument('--channel',        action='store', type=str, default="all")
argParser.add_argument('--selection',      action='store', type=str, default="trilepT-minDLmass12-onZ1-njet3p-btag1p")
argParser.add_argument('--hist',           action='store', type=str, default="Z1_pt")
args = argParser.parse_args()

path  = "/groups/hephy/cms/dennis.schwarz/www/tWZ/plots/analysisPlots/EFT_UL_v5/"
year = args.era
channel = args.channel
selection = args.selection
histname = args.hist

# processes = ["tWZ", "ttZ", "ttX", "tZq", "WZ",  "triBoson", "ZZ", "nonprompt"]
processes = ["ttZ", "WZ", "ZZ", "nonprompt"]

uncertainties = {
    "Trigger": ["UP", "DOWN"],
    "LepIDstat": ["UP", "DOWN"],
    "LepIDsys": ["UP", "DOWN"],
    "BTag_b": ["UP", "DOWN"],
    "BTag_l": ["UP", "DOWN"],
    "PU": ["UP", "DOWN"],
    "JES": ["UP", "DOWN"],
    "JER": ["UP", "DOWN"],
    "Scale": ["UPUP", "UPNONE", "NONEUP", "DOWNDOWN", "DOWNNONE", "NONEDOWN"],
}

signalcolors = {
    "UP":       ROOT.kAzure+7,
    "DOWN":     ROOT.kRed-2,
    "UPUP":     ROOT.kAzure+7, 
    "UPNONE":   ROOT.kBlue,
    "NONEUP":   ROOT.kBlue+4, 
    "DOWNDOWN": ROOT.kRed-2, 
    "DOWNNONE": ROOT.kRed-10, 
    "NONEDOWN": ROOT.kRed-5,
}

for unc in uncertainties.keys():
    variations = uncertainties[unc]
    filename_central = path+"/"+year+"/"+channel+"/"+selection+"/Results.root"
    for process in processes:
        p = Plotter(process+"__"+unc)
        p.plot_dir = plot_directory+"/SysVariations/"+selection+"/"+year+"/"+channel+"/"
        p.lumi = ""
        p.xtitle = "Z p_{T} [GeV]"
        p.drawRatio = True
        p.ratiorange = (0.2, 1.8)
        h_central = getObjFromFile(filename_central, histname+"__"+process)
        p.addBackground(h_central, process, 13)
        for var in variations:
            fname = filename_central.replace("EFT_UL_v5", "EFT_UL_v5_noData_"+unc+"_"+var)
            h_var = getObjFromFile(fname, histname+"__"+process)
            p.addSignal(h_var, unc+" "+var, signalcolors[var])
        p.draw()
